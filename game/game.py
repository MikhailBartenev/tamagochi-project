"""Модуль с интерфейсом и реализацией класса игры."""
from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .exceptions import NoFood, NoMedicine, NotEnoughMoney
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры."""
    @abstractmethod
    def __init__(self, tamagochi: AbstractTamagochi, clicker: AbstractClicker,
                 all_food: list[Food], all_medicine: list[Medicine]) -> None:
        pass
    @abstractmethod
    def work(self) -> int:
        pass
    @abstractmethod
    def buy_food(self) -> None:
        pass
    @abstractmethod
    def buy_medicine(self) -> None:
        pass
    @abstractmethod
    def feed_tamagochi(self) -> None:
        pass
    @abstractmethod
    def heal_tamagochi(self) -> None:
        pass
    @abstractmethod
    def rest_tamagochi(self) -> None:
        pass
    @abstractmethod
    def play_with_tamagochi(self) -> None:
        pass
    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        pass
    @property
    @abstractmethod
    def food(self) -> list[Food]:
        pass
    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        pass


class SimpleGame(AbstractGame):
    """Простая реализация игры."""
    def __init__(self, tamagochi: AbstractTamagochi, clicker: AbstractClicker,
                 all_food: list[Food], all_medicine: list[Medicine]) -> None:
        self.tamagochi = tamagochi
        self.clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._food_bag: list[Food] = []
        self._medicine_bag: list[Medicine] = []

    def work(self) -> int:
        self.clicker.click()
        return self.clicker.income_per_click

    def buy_food(self) -> None:
        food = self._all_food[0]
        if self.clicker.income_per_click >= food.price:
            self._food_bag.append(food)
            self.clicker._coins -= food.price
        else:
            raise NotEnoughMoney("Не хватает монет на еду")

    def buy_medicine(self) -> None:
        medicine = self._all_medicine[0]
        if self.clicker.income_per_click >= medicine.price:
            self._medicine_bag.append(medicine)
            self.clicker._coins -= medicine.price
        else:
            raise NotEnoughMoney("Не хватает монет на лекарство")

    def feed_tamagochi(self) -> None:
        if not self._food_bag:
            raise NoFood("Нет еды в сумке")
        food = self._food_bag.pop(0)
        self.tamagochi.feed(food)

    def heal_tamagochi(self) -> None:
        if not self._medicine_bag:
            raise NoMedicine("Нет лекарств в сумке")
        medicine = self._medicine_bag[0]
        if medicine.is_empty():
            self._medicine_bag.pop(0)
            raise NoMedicine("Лекарство закончилось")
        self.tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine_bag.pop(0)

    def rest_tamagochi(self) -> None:
        self.tamagochi.rest()

    def play_with_tamagochi(self) -> None:
        self.tamagochi.play()

    def get_status(self) -> dict[str, Any]:
        status = self.tamagochi.status
        status['coins'] = self.clicker.income_per_click
        return status

    @property
    def food(self) -> list[Food]:
        return self._food_bag

    @property
    def medicine(self) -> list[Medicine]:
        return self._medicine_bag

# Псевдоним для тестов
Game = SimpleGame
