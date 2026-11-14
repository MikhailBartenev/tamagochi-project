"""Модуль с интерфейсом и реализациями класса тамагочи."""
import random
from abc import ABC, abstractmethod

from .exceptions import MedicineIsEmpty
from .models import Food, Medicine

MIN_STAT = 0
MAX_STAT = 100
SICK_CHANCE = 0.1
WEAK_THRESHOLD = 70
WEAK_SICK_CHANCE_FACTOR = 2.5
HUNGER_PER_TICK = 2
FATIGUE_PER_TICK = 2
SICK_FATIGUE_PER_TICK = 4
ENERGY_PER_TICK = 2
SICK_HP_LOSS = 4
STARVING_HP_LOSS = 10
EXHAUSTED_HP_LOSS = 5
NO_ENERGY_HP_LOSS = 5
FEED_ENERGY_COST = 5
PLAY_ENERGY_COST = 20
PLAY_FATIGUE = 10
PLAY_HUNGER = 5
PLAY_HP_BONUS = 10
REST_FATIGUE_RECOVERY = 40
REST_ENERGY_RECOVERY = 40
SICK_REST_DIVIDER = 2


def clamp_stat(value: int) -> int:
    return max(MIN_STAT, min(MAX_STAT, value))


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""
    @abstractmethod
    def feed(self, food: Food) -> None: pass
    @abstractmethod
    def play(self) -> None: pass
    @abstractmethod
    def rest(self) -> None: pass
    @abstractmethod
    def heal(self, medicine: Medicine) -> None: pass
    @property
    @abstractmethod
    def status(self) -> dict[str, int]: pass
    @abstractmethod
    def is_alive(self) -> bool: pass
    @abstractmethod
    def is_sick(self) -> bool: pass
    @abstractmethod
    def update(self) -> None: pass


class SimpleTamagochi(AbstractTamagochi):
    def __init__(self, name: str = 'Мурзик', sick_chance: float = SICK_CHANCE) -> None:
        if not 0 <= sick_chance <= 1:
            raise ValueError('Вероятность болезни должна быть от 0 до 1')
        self._name = name
        self._sick_chance = sick_chance
        self._hunger = MIN_STAT
        self._fatigue = MIN_STAT
        self._energy = MAX_STAT
        self._hp = MAX_STAT
        self._sick = False

    @property
    def name(self) -> str:
        return self._name

    def feed(self, food: Food) -> None:
        self._hunger = clamp_stat(self._hunger - food.satiety)
        self._energy = clamp_stat(self._energy - FEED_ENERGY_COST)

    def play(self) -> None:
        self._energy = clamp_stat(self._energy - PLAY_ENERGY_COST)
        self._fatigue = clamp_stat(self._fatigue + PLAY_FATIGUE)
        self._hunger = clamp_stat(self._hunger + PLAY_HUNGER)
        if not self._sick:
            self._change_hp(PLAY_HP_BONUS)

    def rest(self) -> None:
        divider = SICK_REST_DIVIDER if self._sick else 1
        self._fatigue = clamp_stat(self._fatigue - REST_FATIGUE_RECOVERY // divider)
        self._energy = clamp_stat(self._energy + REST_ENERGY_RECOVERY // divider)

    def heal(self, medicine: Medicine) -> None:
        if medicine.is_empty():
            raise MedicineIsEmpty(f'Лекарство {medicine.name} закончилось')
        medicine.uses += 1
        self._change_hp(medicine.heal_hp)
        self._sick = False

    @property
    def status(self) -> dict[str, int]:
        return {
            'hunger': self._hunger,
            'fatigue': self._fatigue,
            'hp': self._hp,
            'energy': self._energy,
        }

    def is_alive(self) -> bool:
        return self._hp >= MIN_STAT

    def is_sick(self) -> bool:
        return self._sick

    def update(self) -> None:
        fatigue_gain = FATIGUE_PER_TICK
        if self._sick:
            fatigue_gain += SICK_FATIGUE_PER_TICK
        self._hunger = clamp_stat(self._hunger + HUNGER_PER_TICK)
        self._fatigue = clamp_stat(self._fatigue + fatigue_gain)
        self._energy = clamp_stat(self._energy - ENERGY_PER_TICK)
        self._change_hp(-self._calculate_hp_loss())
        if not self._sick and random.random() < self._current_sick_chance():
            self._sick = True

    def _calculate_hp_loss(self) -> int:
        hp_loss = 0
        if self._sick:
            hp_loss += SICK_HP_LOSS
        if self._hunger >= MAX_STAT:
            hp_loss += STARVING_HP_LOSS
        if self._fatigue >= MAX_STAT:
            hp_loss += EXHAUSTED_HP_LOSS
        if self._energy <= MIN_STAT:
            hp_loss += NO_ENERGY_HP_LOSS
        return hp_loss

    def _current_sick_chance(self) -> float:
        if self._hunger > WEAK_THRESHOLD or self._fatigue > WEAK_THRESHOLD:
            return min(1.0, self._sick_chance * WEAK_SICK_CHANCE_FACTOR)
        return self._sick_chance

    def _change_hp(self, delta: int) -> None:
        self._hp = min(MAX_STAT, self._hp + delta)
