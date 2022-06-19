from datetime import datetime, timedelta
from threading import Thread
import time
import uuid
import random


class OrdersManager:
    __orders = []
    __orders_processed = 0
    __last_printed_log = datetime.now()

    def __init__(self) -> None:
        self.__generate_fake_orders(quantity=1_000)
    
    def start_thread(self):
        hilos = []
        for n in range(5):
            hilo = Thread(target=self.process_orders, args=(n,))
            hilos.append(hilo)
        for hilo in hilos:
            hilo.start()
        for hilo in hilos:
            hilo.join()

    def __generate_fake_orders(self, quantity):
        self.__log(f"Generating fake orders")
        self.__orders = [(uuid.uuid4(), x) for x in range(quantity)]
        self.__log(f"{len(self.__orders)} generated...")

    def __log(self, message):
        print(f"{datetime.now()} > {message}")

    def __fake_save_on_db(self, order):
        id, number = order

        self.__log(
            message=f"Order [{id}] {number} was successfully prosecuted."
        )

        time.sleep(random.uniform(0, 1))

    def process_orders(self, n):
        start, end = self.start_end(n)
        for orden in range(start, end):
            order=self.__orders[orden]
            self.__fake_save_on_db(order=order)
            self.__orders_processed += 1

            if datetime.now() > self.__last_printed_log:
                self.__last_printed_log = datetime.now() + timedelta(seconds=5)
                self.__log(
                    message=f"Total orders executed: {self.__orders_processed}/{len(self.__orders)}"
                )

    def start_end(self, n):
        start = n * (len(self.__orders) // 5)
        end = start + (len(self.__orders) // 5)
        if n == 5:
            end = len(self.__orders) + 1
        return start, end
        
#
#
# ---
orders_manager = OrdersManager()

start_time = time.time()

orders_manager.start_thread()

delay = time.time() - start_time

print(f"{datetime.now()} > Tiempo de ejecucion: {delay} segundos...")
