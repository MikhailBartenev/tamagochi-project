"""Модуль с интерфейсом и реализацией кликера."""
import random
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера."""
    @abstractmethod
    def __init__(self) -> None: pass
    @abstractmethod
    def click(self) -> None: pass
    @property
    @abstractmethod
    def income_per_click(self) -> int: pass


class SimpleRandomClicker(AbstractClicker):
    """Реализация кликера со случайным заработком."""
    def __init__(self) -> None:
        self._coins = 0

    def click(self) -> None:
        self._coins += random.randint(5, 15)

    @property
    def income_per_click(self) -> int:
        return self._coins
