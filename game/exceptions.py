"""Модуль с исключениями."""

class TamagochiIsGone(Exception):
    """Ошибка при смерти тамагочи."""

class NotEnoughMoney(Exception):
    """Ошибка, когда не хватает монет для покупки."""

class NoFood(Exception):
    """Ошибка, когда в сумке нет еды."""

class NoMedicine(Exception):
    """Ошибка, когда в сумке нет лекарств."""