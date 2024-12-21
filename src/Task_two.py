#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from typing import List


class IllegalRowValue(Exception):
    def __init__(self, row: int, message: str = "Illegal count of Row") -> None:
        self.row = row
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.row} -> {self.message}"


class IllegalColValue(Exception):  # Наследование от Exception
    def __init__(self, col: int, message: str = "Illegal count of Col") -> None:
        self.col = col
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.col} -> {self.message}"


class IllegalStartValue(Exception):  # Наследование от Exception
    def __init__(self, start: int, message: str = "Illegal start value") -> None:
        self.start = start
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.start} -> {self.message}"


class IllegalEndValue(Exception):  # Наследование от Exception
    def __init__(self, end: int, message: str = "Illegal end value") -> None:
        self.end = end
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.end} -> {self.message}"


class RandomMatrix:
    def __init__(self, col: int, row: int, start: int, end: int) -> None:
        self.col = col
        self.row = row
        self.start = start
        self.end = end
        self.matrix: List[List[int]] = []

    def generate_matrix(self) -> List[List[int]]:
        if self.row <= 0:
            raise IllegalRowValue(self.row)

        if self.col <= 0:
            raise IllegalColValue(self.col)

        result: List[List[int]] = []

        for _ in range(self.row):
            row_values = [random.randint(self.start, self.end) for _ in range(self.col)]
            result.append(row_values)

        self.matrix = result
        return result

    def show_matrix(self) -> None:
        for row in self.matrix:
            print(row)


def main() -> None:
    matrix = RandomMatrix(5, 4, 1, 5)
    matrix.generate_matrix()
    matrix.show_matrix()


if __name__ == "__main__":
    main()