"""Модуль с интерфейсом и реализацией класса игры."""
from abc import ABC, abstractmethod
from dataclasses import replace
from typing import Any

from .clicker import AbstractClicker
from .exceptions import (
    ActionCancelled,
    EmptyBag,
    NotEnoughMoney,
    TamagochiIsGone,
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
    @property
    @abstractmethod
    def tamagochi(self) -> AbstractTamagochi:
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
    """Игра: кошелёк, сумки с едой и лекарствами и ход времени."""
    def __init__(self, tamagochi: AbstractTamagochi, clicker: AbstractClicker,
                 all_food: list[Food], all_medicine: list[Medicine]) -> None:
        if not all_food or not all_medicine:
            raise ValueError('В магазине должны быть и еда, и лекарства')
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._coins = START_COINS
        self._food_bag: list[Food] = []
        self._medicine_bag: list[Medicine] = []

    @property
    def tamagochi(self) -> AbstractTamagochi:
        return self._tamagochi

    def work(self) -> int:
        self._check_game_over()
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._next_turn()
        return income

    def buy_food(self) -> None:
        self._check_game_over()
        food = self._choose('Какую еду купить?', self._all_food)
        self._pay(food.price)
        self._food_bag.append(food)
        self._next_turn()

    def buy_medicine(self) -> None:
        self._check_game_over()
        medicine = self._choose('Какое лекарство купить?', self._all_medicine)
        self._pay(medicine.price)
        self._medicine_bag.append(replace(medicine, uses=0))
        self._next_turn()

    def feed_tamagochi(self) -> None:
        self._check_game_over()
        if not self._food_bag:
            raise EmptyBag('Сумка с едой пуста, сначала купите еду')
        food = self._choose('Чем покормить питомца?', self._food_bag)
        self._food_bag.remove(food)
        self._tamagochi.feed(food)
        self._next_turn()

    def heal_tamagochi(self) -> None:
        self._check_game_over()
        if not self._medicine_bag:
            raise EmptyBag('Сумка с лекарствами пуста, сначала купите лекарство')
        medicine = self._choose('Каким лекарством лечить?', self._medicine_bag)
        self._tamagochi.heal(medicine)
        if medicine.is_empty():
            self._remove_by_identity(self._medicine_bag, medicine)
        self._next_turn()

    def rest_tamagochi(self) -> None:
        self._check_game_over()
        self._tamagochi.rest()
        self._next_turn()

    def play_with_tamagochi(self) -> None:
        self._check_game_over()
        self._tamagochi.play()
        self._next_turn()

    def get_status(self) -> dict[str, Any]:
        return {**self._tamagochi.status, 'coins': self._coins}

    @property
    def food(self) -> list[Food]:
        return self._food_bag

    @property
    def medicine(self) -> list[Medicine]:
        return self._medicine_bag

    @staticmethod
    def _choose(title: str, items: list[Any]) -> Any:
        print(title)
        for number, item in enumerate(items, start=1):
            print(f'{number}. {item}')
        try:
            answer = input('Введите номер (0 — отмена): ')
        except EOFError:
            raise ActionCancelled('Выбор отменён') from None
        if answer.strip().isdigit() and 1 <= int(answer) <= len(items):
            return items[int(answer) - 1]
        raise ActionCancelled('Выбор отменён')

    def _pay(self, price: int) -> None:
        if price > self._coins:
            raise NotEnoughMoney(f'Не хватает монет: нужно {price}, у вас {self._coins}')
        self._coins -= price

    @staticmethod
    def _remove_by_identity(items: list[Any], target: Any) -> None:
        for index, item in enumerate(items):
            if item is target:
                del items[index]
                return

    def _next_turn(self) -> None:
        self._tamagochi.update()
        self._check_game_over()

    def _check_game_over(self) -> None:
        if not self._tamagochi.is_alive():
            raise TamagochiIsGone('Здоровье питомца упало ниже нуля. Игра окончена!')
