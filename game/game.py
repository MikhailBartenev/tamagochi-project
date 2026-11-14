"""Модуль с интерфейсом и реализацией класса игры."""
from abc import ABC, abstractmethod
from dataclasses import replace
from typing import Any

from .clicker import AbstractClicker
from .exceptions import (
    EmptyBag,
    NotEnoughMoney,
)
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi

START_COINS = 0


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
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = all_food
        self._all_medicine = all_medicine
        self._coins = START_COINS
        self._food_bag: list[Food] = []
        self._medicine_bag: list[Medicine] = []

    @property
    def tamagochi(self) -> AbstractTamagochi:
        return self._tamagochi

    def work(self) -> int:
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._tamagochi.update()
        return income

    def buy_food(self) -> None:
        food = self._all_food[0]
        if self._coins < food.price:
            raise NotEnoughMoney("Не хватает монет на еду")
        self._coins -= food.price
        self._food_bag.append(food)
        self._tamagochi.update()

    def buy_medicine(self) -> None:
        medicine = self._all_medicine[0]
        if self._coins < medicine.price:
            raise NotEnoughMoney("Не хватает монет на лекарство")
        self._coins -= medicine.price
        self._medicine_bag.append(replace(medicine, uses=0))
        self._tamagochi.update()

    def feed_tamagochi(self) -> None:
        if not self._food_bag:
            raise EmptyBag("Сумка с едой пуста")
        # Берем последний элемент и удаляем его через remove
        food = self._food_bag[-1]
        self._food_bag.remove(food)
        self._tamagochi.feed(food)
        self._tamagochi.update()

    def heal_tamagochi(self) -> None:
        if not self._medicine_bag:
            raise EmptyBag("Сумка с лекарствами пуста")
        medicine = self._medicine_bag[0]
        self._tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine_bag.pop(0)
        self._tamagochi.update()

    def rest_tamagochi(self) -> None:
        self._tamagochi.rest()
        self._tamagochi.update()

    def play_with_tamagochi(self) -> None:
        self._tamagochi.play()
        self._tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        status = self._tamagochi.status
        status['coins'] = self._coins
        return status

    @property
    def food(self) -> list[Food]:
        return self._food_bag

    @property
    def medicine(self) -> list[Medicine]:
        return self._medicine_bag
