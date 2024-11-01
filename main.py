import random
import pandas as pd
import matplotlib.pyplot as plt
from model.model import Order, Manager, Carrier
from model.model import NUM_CARRIERS, MANAGER_PROCESSING_DAYS, SIMULATION_DAYS, PROPOSAL_DAYS, ORDER_INTERVAL, K_RANGE, L_RANGE

# Моделирование процесса
def simulate():
    manager = Manager()
    day = 0
    next_order_day = random.randint(ORDER_INTERVAL[0] - ORDER_INTERVAL[1], ORDER_INTERVAL[0] + ORDER_INTERVAL[1])

    for day in range(SIMULATION_DAYS):
        if day == next_order_day:
            manager.announce_order(day)
            next_order_day = day + random.randint(ORDER_INTERVAL[0] - ORDER_INTERVAL[1], ORDER_INTERVAL[0] + ORDER_INTERVAL[1])

        manager.assign_order(day)
        manager.complete_orders(day)

    return manager

# Запуск симуляции и анализ результатов
manager = simulate()

# Вывод распределения заказов по компаниям-перевозчикам
order_distribution_df = pd.DataFrame.from_dict(manager.order_distribution, orient='index', columns=['Completed Orders'])
order_distribution_df.index.name = 'Carrier ID'

# Подсчет времени простоя
total_idle_days = manager.order_idle_days

# Вывод результатов
print("Распределение заказов по перевозчикам:")
print(order_distribution_df)
print(f"\nОбщее количество дней простоя из-за занятости всех перевозчиков: {total_idle_days} дней")

# Визуализация
order_distribution_df.plot(kind='bar', legend=False)
plt.title("Распределение заказов по перевозчикам")
plt.xlabel("Carrier ID")
plt.ylabel("Completed Orders")
plt.show()
import random
import pandas as pd
import matplotlib.pyplot as plt

# Константы
NUM_CARRIERS = 6  # Количество агентов-перевозчиков
SIMULATION_DAYS = 365  # Количество дней моделирования (1 год)
ORDER_INTERVAL = (5, 3)  # Средний интервал между заказами и разброс (5±3 дней)
K_RANGE = (100, 500)  # Диапазон для числа товаров
L_RANGE = (1, 15)  # Диапазон для расстояния в заказе
PROPOSAL_DAYS = 3  # Время формирования предложений
MANAGER_PROCESSING_DAYS = 1  # Время обработки предложений менеджером



# Запуск симуляции и анализ результатов
manager = simulate()

# Вывод распределения заказов по компаниям-перевозчикам
order_distribution_df = pd.DataFrame.from_dict(manager.order_distribution, orient='index', columns=['Completed Orders'])
order_distribution_df.index.name = 'Carrier ID'

# Подсчет времени простоя
total_idle_days = manager.order_idle_days

# Вывод результатов
print("Распределение заказов по перевозчикам:")
print(order_distribution_df)
print(f"\nОбщее количество дней простоя из-за занятости всех перевозчиков: {total_idle_days} дней")

# Визуализация
order_distribution_df.plot(kind='bar', legend=False)
plt.title("Распределение заказов по перевозчикам")
plt.xlabel("Carrier ID")
plt.ylabel("Completed Orders")
plt.show()
