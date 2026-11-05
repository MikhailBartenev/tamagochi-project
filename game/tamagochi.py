"""Модуль с интерфейсом и реализациями класса тамагочи."""
from abc import ABC, abstractmethod

from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""
    @abstractmethod
    def feed(self, food: Food) -> None: raise NotImplementedError
    @abstractmethod
    def play(self) -> None: raise NotImplementedError
    @abstractmethod
    def rest(self) -> None: raise NotImplementedError
    @abstractmethod
    def heal(self, medicine: Medicine) -> None: raise NotImplementedError
    @property
    @abstractmethod
    def status(self) -> dict[str, int]: raise NotImplementedError
    @abstractmethod
    def is_alive(self) -> bool: raise NotImplementedError
    @abstractmethod
    def is_sick(self) -> bool: raise NotImplementedError
    @abstractmethod
    def update(self) -> None: raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Простая реализация тамагочи."""
    
    def __init__(self) -> None:
        self._hunger = 50
        self._hp = 100
        self._energy = 50
        self._sick = False

    def feed(self, food: Food) -> None:
        self._hunger = max(0, self._hunger - food.satiety)
        self._energy += 5

    def play(self) -> None:
        self._energy -= 15
        self._hunger += 10
        self._hp += 5

    def rest(self) -> None:
        if self._sick:
            self._energy += 10
        else:
            self._energy += 20
        self._hunger += 10

    def heal(self, medicine: Medicine) -> None:
        if not self._sick:
            return
        self._hp += medicine.heal_hp
        medicine.uses += 1
        if medicine.is_empty() or self._hp > 0:
            self._sick = False

    @property
    def status(self) -> dict[str, int]:
        return {'hunger': self._hunger, 'hp': self._hp, 'energy': self._energy}

    def is_alive(self) -> bool:
        return self._hp > 0

    def is_sick(self) -> bool:
        return self._sick

    def update(self) -> None:
        if not self.is_alive():
            raise TamagochiIsGone("Питомец умер :(")
        self._hunger += 5
        self._energy -= 5
        if self._energy <= 0:
            self._energy = 0
            self._sick = True
            self._hp -= 10
