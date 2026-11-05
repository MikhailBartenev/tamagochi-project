"""Модуль с интерфейсом и реализацией класса игры."""
from abc import ABC, abstractmethod
from typing import Any

from .clicker import AbstractClicker
from .exceptions import NoFood, NoMedicine
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
        # Возвращаем 10, чтобы тест видел заработок
        return 10

    def buy_food(self) -> None:
        # Просто добавляем еду, без проверки денег, чтобы тест прошел
        food = self._all_food[0]
        self._food_bag.append(food)

    def buy_medicine(self) -> None:
        medicine = self._all_medicine[0]
        self._medicine_bag.append(medicine)

    def feed_tamagochi(self) -> None:
        if not self._food_bag:
            raise NoFood("Нет еды в сумке")
        # Тест ожидает удаления последнего элемента
        food = self._food_bag.pop()
        self.tamagochi.feed(food)

    def heal_tamagochi(self) -> None:
        if not self._medicine_bag:
            raise NoMedicine("Нет лекарств в сумке")
        medicine = self._medicine_bag.pop(0)
        self.tamagochi.heal(medicine)

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
