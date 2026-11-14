"""Модуль с интерфейсом и реализацией кликера."""
from abc import ABC, abstractmethod
from random import randint


class AbstractClicker(ABC):
    """Интерфейс для кликера."""
    @abstractmethod
    def __init__(self) -> None:
        pass
    @abstractmethod
    def click(self) -> None:
        pass
    @property
    @abstractmethod
    def income_per_click(self) -> int:
        pass


class SimpleRandomClicker(AbstractClicker):
    """Кликер, который за каждый клик даёт случайное число монет."""
    def __init__(self, min_income: int, max_income: int) -> None:
        if not 0 <= min_income <= max_income:
            raise ValueError('Доход за клик должен быть неотрицательным')
        self._min_income = min_income
        self._max_income = max_income
        self._income_per_click = 0

    def click(self) -> None:
        self._income_per_click = randint(self._min_income, self._max_income)

    @property
    def income_per_click(self) -> int:
        return self._income_per_click
