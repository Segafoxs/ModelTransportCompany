import random

NUM_CARRIERS = 6  # Количество агентов-перевозчиков
SIMULATION_DAYS = 365  # Количество дней моделирования (1 год)
ORDER_INTERVAL = (5, 3)  # Средний интервал между заказами и разброс (5±3 дней)
K_RANGE = (100, 500)  # Диапазон для числа товаров
L_RANGE = (1, 15)  # Диапазон для расстояния в заказе
PROPOSAL_DAYS = 3  # Время формирования предложений
MANAGER_PROCESSING_DAYS = 1  # Время обработки предложений менеджером

class Order:
    def __init__(self, day, k, l):
        self.day = day
        self.k = k
        self.l = l
        self.completed = False

    def cost(self):
        return self.k * self.l + random.uniform(-0.2, 0.2) * self.k * self.l

class Carrier:
    def __init__(self, carrier_id):
        self.carrier_id = carrier_id
        self.is_contractor = False
        self.current_order = None
        self.orders_completed = 0

    def create_proposal(self, order):
        return order.cost() if not self.is_contractor else float('inf')

    def assign_order(self, order):
        self.is_contractor = True
        self.current_order = order

    def complete_order(self, day):
        if self.current_order and day >= self.current_order.day + self.current_order.l:
            self.is_contractor = False
            self.current_order.completed = True
            self.orders_completed += 1
            self.current_order = None

class Manager:
    def __init__(self):
        self.orders = []
        self.waiting_orders = []
        self.carriers = [Carrier(i) for i in range(NUM_CARRIERS)]
        self.order_distribution = {i: 0 for i in range(NUM_CARRIERS)}
        self.order_idle_days = 0

    def announce_order(self, day):
        k = random.randint(*K_RANGE)
        l = random.randint(*L_RANGE)
        order = Order(day, k, l)
        self.waiting_orders.append(order)

    def gather_proposals(self, order):
        proposals = {carrier.carrier_id: carrier.create_proposal(order) for carrier in self.carriers}
        return {k: v for k, v in proposals.items() if v != float('inf')}

    def assign_order(self, day):
        orders_to_remove = []
        for order in self.waiting_orders:
            if day >= order.day + PROPOSAL_DAYS:
                proposals = self.gather_proposals(order)
                if proposals:
                    best_carrier_id = min(proposals, key=proposals.get)
                    self.carriers[best_carrier_id].assign_order(order)
                    self.order_distribution[best_carrier_id] += 1
                else:
                    self.order_idle_days += 1
                orders_to_remove.append(order)
        for order in orders_to_remove:
            self.waiting_orders.remove(order)

    def complete_orders(self, day):
        for carrier in self.carriers:
            carrier.complete_order(day)
