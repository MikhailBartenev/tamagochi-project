"""Точка входа в игру."""
import os
from game.tamagochi import SimpleTamagochi
from game.clicker import SimpleRandomClicker
from game.game import SimpleGame
from game.models import Food, Medicine


def main():
    all_food = [
        Food(name='Бургер', satiety=20, price=40),
        Food(name='Салат', satiety=10, price=20),
        Food(name='Яблоко', satiety=10, price=15)
    ]
    all_medicine = [
        Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2)
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker()
    game = SimpleGame(tamagochi, clicker, all_food=all_food, all_medicine=all_medicine)

    print("Добро пожаловать в тамагочи-кликер!")
    output = ''

    while True:
        print(output)
        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")
        status = game.get_status()
        print(f"\nСтатус: голод {status['hunger']}, здоровье {status['hp']}, энергия {status['energy']}, монет {status['coins']}\n")
        
        if game.tamagochi.is_sick():
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")
            
        print("1. Пойти на работу")
        print("2. Купить еду")
        print("3. Купить лекарство")
        print("4. Покормить")
        print("5. Вылечить")
        print("6. Играть")
        print("7. Отдых")
        print("0. Выход")

        match input("Выберите действие: "):
            case "1":
                income = game.work()
                output = f'Вы заработали {income} монет'
                try:
                    game.tamagochi.update()
                except Exception as e:
                    print(e)
                    break
            case "2":
                try:
                    game.buy_food()
                except Exception as e:
                    output = str(e)
            case "3":
                try:
                    game.buy_medicine()
                except Exception as e:
                    output = str(e)
            case "4":
                try:
                    game.feed_tamagochi()
                except Exception as e:
                    output = str(e)
            case "5":
                try:
                    game.heal_tamagochi()
                except Exception as e:
                    output = str(e)
            case "6":
                game.play_with_tamagochi()
                output = 'Вы поиграли с питомцем'
                try:
                    game.tamagochi.update()
                except Exception as e:
                    print(e)
                    break
            case "7":
                game.rest_tamagochi()
                output = 'Питомец отдохнул'
                try:
                    game.tamagochi.update()
                except Exception as e:
                    print(e)
                    break
            case "0":
                break
            case _:
                output = "Неверная команда"

        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()