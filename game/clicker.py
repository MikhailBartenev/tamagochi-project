"""Модуль с интерфейсом и реализацией кликера."""
import random
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    @abstractmethod
    def __init__(self) -> None: raise NotImplementedError
    @abstractmethod
    def click(self) -> None: raise NotImplementedError
    @property
    @abstractmethod
    def income_per_click(self) -> int: raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    def __init__(self) -> None:
        self._coins = 0

    def click(self) -> None:
        self._coins += random.randint(5, 15)

    @property
    def income_per_click(self) -> int:
        return self._coins