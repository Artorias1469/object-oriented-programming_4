#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
from unittest.mock import patch
from typing import Union
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Task_one import Meaning

# Фикстура для создания экземпляров Meaning
@pytest.fixture
def create_meaning():
    def _create_meaning(mock_input: Union[str, list[str]]):
        with patch("builtins.input", side_effect=mock_input if isinstance(mock_input, list) else [mock_input]):
            return Meaning()
    return _create_meaning

# Тест сложения чисел
def test_add_numbers(create_meaning):
    x = create_meaning("5.5")
    y = create_meaning("4.5")
    result = x + y
    assert result == 10.0, f"Ожидалось 10.0, но получено {result}"

# Тест сложения строк
def test_add_strings(create_meaning):
    x = create_meaning("hello")
    y = create_meaning("world")
    result = x + y
    assert result == "helloworld", f"Ожидалось 'helloworld', но получено {result}"

# Тест смешанных значений (число + строка)
def test_add_mixed(create_meaning):
    x = create_meaning("42")
    y = create_meaning("test")
    result = x + y
    assert result == "42test", f"Ожидалось '42test', но получено {result}"

# Тест проверки числа через метод is_number
def test_is_number(create_meaning):
    x = create_meaning("3.14")
    assert x.is_number(x.mean), "Ожидалось, что значение '3.14' будет числом"

    y = create_meaning("abc")
    assert not y.is_number(y.mean), "Ожидалось, что значение 'abc' не будет числом"
