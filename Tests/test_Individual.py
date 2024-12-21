#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import json
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Individual.Ind import (
    add_flight,
    print_flights,
    search_flights_by_aircraft_type,
    save_to_json,
    load_from_json,
)

# Фикстура для временного файла
@pytest.fixture
def temp_file(tmp_path):
    return tmp_path / "flights_test.json"

# Тест добавления рейса
def test_add_flight():
    flight = add_flight("Москва", "SU123", "Boeing 737")
    assert flight == {
        'название пункта назначения': "Москва",
        'номер рейса': "SU123",
        'тип самолета': "Boeing 737"
    }, "Добавленный рейс должен соответствовать указанным данным"

# Тест сохранения и загрузки рейсов
def test_save_and_load_flights(temp_file):
    flights = [
        add_flight("Москва", "SU123", "Boeing 737"),
        add_flight("Сочи", "SU456", "Airbus A320"),
    ]
    save_to_json(temp_file, flights)
    loaded_flights = load_from_json(temp_file)

    assert flights == loaded_flights, "Загруженные данные должны совпадать с сохраненными"

# Тест поиска рейсов по типу самолета
def test_search_flights_by_aircraft_type(capsys):
    flights = [
        add_flight("Москва", "SU123", "Boeing 737"),
        add_flight("Сочи", "SU456", "Airbus A320"),
    ]
    search_flights_by_aircraft_type(flights, "Boeing 737")
    captured = capsys.readouterr()

    assert "Москва" in captured.out, "Поиск должен найти рейс в Москву"
    assert "SU123" in captured.out, "Поиск должен включать номер рейса SU123"
    assert "Boeing 737" in captured.out, "Поиск должен указать тип самолета Boeing 737"

# Тест поиска по несуществующему типу самолета
def test_search_flights_no_match(capsys):
    flights = [
        add_flight("Москва", "SU123", "Boeing 737"),
        add_flight("Сочи", "SU456", "Airbus A320"),
    ]
    search_flights_by_aircraft_type(flights, "Boeing 747")
    captured = capsys.readouterr()

    assert "не найдено" in captured.out, "Поиск должен сообщить об отсутствии рейсов"

# Тест вывода рейсов
def test_print_flights(capsys):
    flights = [
        add_flight("Москва", "SU123", "Boeing 737"),
        add_flight("Сочи", "SU456", "Airbus A320"),
    ]
    print_flights(flights)
    captured = capsys.readouterr()

    assert "Москва" in captured.out, "Вывод должен содержать пункт назначения Москва"
    assert "Сочи" in captured.out, "Вывод должен содержать пункт назначения Сочи"
    assert "SU123" in captured.out, "Вывод должен содержать номер рейса SU123"
    assert "SU456" in captured.out, "Вывод должен содержать номер рейса SU456"

# Тест загрузки из несуществующего файла
def test_load_from_nonexistent_file(temp_file):
    flights = load_from_json(temp_file)
    assert flights == [], "Для несуществующего файла должен возвращаться пустой список"
