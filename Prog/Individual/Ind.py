#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import logging
from pathlib import Path
from typing import List, Dict, Union

# Настроим логгирование
logging.basicConfig(
    filename="flights.log",
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

Flight = Dict[str, Union[str, int]]


def add_flight(destination: str, flight_number: str, aircraft_type: str) -> Flight:
    return {
        'название пункта назначения': destination,
        'номер рейса': flight_number,
        'тип самолета': aircraft_type
    }


def print_flights(flights: List[Flight]) -> None:
    line = '+-{}-+-{}-+-{}-+'.format('-' * 30, '-' * 20, '-' * 15)
    print(line)
    print('| {:^30} | {:^20} | {:^15} |'.format(
        "Название пункта назначения",
        "Номер рейса",
        "Тип самолета"
    ))
    print(line)
    for flight in flights:
        print('| {:<30} | {:<20} | {:<15} |'.format(
            flight.get('название пункта назначения', ''),
            flight.get('номер рейса', ''),
            flight.get('тип самолета', '')
        ))
    print(line)


def search_flights_by_aircraft_type(flights_list: List[Flight], search_aircraft_type: str) -> None:
    matching_flights = [flight for flight in flights_list if flight['тип самолета'] == search_aircraft_type]
    if matching_flights:
        logging.info(f"Найдено {len(matching_flights)} рейсов с типом самолета {search_aircraft_type}.")
        print("\nРейсы, обслуживаемые самолетом типа {}: ".format(search_aircraft_type))
        print_flights(matching_flights)
    else:
        logging.warning(f"Не найдено рейсов с типом самолета {search_aircraft_type}.")
        print(f"\nРейсов, обслуживаемых самолетом типа {search_aircraft_type}, не найдено.")


def save_to_json(filename: Path, data: List[Flight]) -> None:
    try:
        with filename.open('w', encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"Сохранены данные о рейсах в файл {filename}.")
    except Exception as e:
        logging.error(f"Ошибка при сохранении данных в файл {filename}: {e}")


def load_from_json(filename: Path) -> List[Flight]:
    try:
        with filename.open('r', encoding="utf-8") as f:
            data = json.load(f)
        logging.info(f"Загружены данные из файла {filename}.")
        return data
    except FileNotFoundError:
        logging.warning(f"Файл {filename} не найден. Будет создан новый список.")
        return []
    except ValueError as e:
        logging.error(f"Ошибка чтения файла {filename}: {e}")
        return []


def main() -> None:
    parser = argparse.ArgumentParser(description="Flight Information Management System")
    parser.add_argument("-a", "--add-flight", action="store_true", help="Add a new flight")
    parser.add_argument("-p", "--print-flights", action="store_true", help="Print the list of flights")
    parser.add_argument("-s", "--search-by-type", help="Search flights by aircraft type")
    parser.add_argument("-f", "--file", default="flights.json", help="JSON file to load/save flight data")
    args = parser.parse_args()

    file_path = Path(args.file).expanduser()

    if args.add_flight:
        destination = input("Введите название пункта назначения: ")
        flight_number = input("Введите номер рейса: ")
        aircraft_type = input("Введите тип самолета: ")
        flight = add_flight(destination, flight_number, aircraft_type)
        flights_list = load_from_json(file_path)

        # Проверка уникальности номера рейса
        if any(f['номер рейса'] == flight_number for f in flights_list):
            logging.warning(f"Рейс с номером {flight_number} уже существует.")
            print(f"Рейс с номером {flight_number} уже существует.")
        else:
            flights_list.append(flight)
            flights_list.sort(key=lambda x: x['название пункта назначения'])
            save_to_json(file_path, flights_list)
            logging.info(f"Добавлен рейс {flight_number} в пункт {destination} с типом самолета {aircraft_type}.")

    elif args.print_flights:
        flights_list = load_from_json(file_path)
        logging.info("Вывод списка всех рейсов.")
        print_flights(flights_list)

    elif args.search_by_type:
        flights_list = load_from_json(file_path)
        logging.info(f"Поиск рейсов по типу самолета: {args.search_by_type}.")
        search_flights_by_aircraft_type(flights_list, args.search_by_type)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
