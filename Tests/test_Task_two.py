#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Task_two import (
    RandomMatrix,
    IllegalRowValue,
    IllegalColValue,
    IllegalStartValue,
    IllegalEndValue,
)

# Тест генерации матрицы с корректными данными
def test_generate_matrix_valid():
    matrix = RandomMatrix(3, 2, 1, 10)
    result = matrix.generate_matrix()
    assert len(result) == 2, "Количество строк должно быть равно 2"
    assert all(len(row) == 3 for row in result), "Количество столбцов в каждой строке должно быть равно 3"
    assert all(1 <= value <= 10 for row in result for value in row), "Все значения должны быть в пределах [1, 10]"

# Тест некорректного значения строки
def test_illegal_row_value():
    with pytest.raises(IllegalRowValue) as excinfo:
        matrix = RandomMatrix(3, 0, 1, 10)
        matrix.generate_matrix()
    assert "Illegal count of Row" in str(excinfo.value), "Ожидалось исключение IllegalRowValue"

# Тест некорректного значения столбца
def test_illegal_col_value():
    with pytest.raises(IllegalColValue) as excinfo:
        matrix = RandomMatrix(0, 3, 1, 10)
        matrix.generate_matrix()
    assert "Illegal count of Col" in str(excinfo.value), "Ожидалось исключение IllegalColValue"

# Тест некорректного стартового значения
def test_illegal_start_value():
    with pytest.raises(ValueError) as excinfo:
        matrix = RandomMatrix(3, 3, 10, 1)
        matrix.generate_matrix()
    assert "empty range for randrange" in str(excinfo.value), "Ожидалось исключение ValueError для диапазона"

# Тест матрицы без генерации
def test_show_matrix_without_generation():
    matrix = RandomMatrix(3, 3, 1, 10)
    assert matrix.matrix == [], "Матрица должна быть пустой до вызова generate_matrix"

# Тест проверки генерации матрицы с отрицательными пределами
def test_negative_values_in_matrix():
    matrix = RandomMatrix(3, 3, -10, -1)
    result = matrix.generate_matrix()
    assert all(-10 <= value <= -1 for row in result for value in row), "Все значения должны быть в пределах [-10, -1]"

# Тест на отображение матрицы
def test_show_matrix(capsys):
    matrix = RandomMatrix(2, 2, 1, 5)
    matrix.generate_matrix()
    matrix.show_matrix()
    captured = capsys.readouterr()
    output_lines = captured.out.strip().split("\n")
    assert len(output_lines) == 2, "Должно быть 2 строки в выводе"
    assert all(len(line.split()) == 2 for line in output_lines), "Каждая строка должна содержать 2 значения"
