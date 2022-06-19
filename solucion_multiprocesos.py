from datetime import datetime, timedelta
from multiprocessing import Process
import os
import random
import time
import uuid


class OrdersManager:
    __orders = []
    __orders_processed = 0
    __last_printed_log = datetime.now()

    def __init__(self) -> None:
        self.__generate_fake_orders(quantity=1_000)

    def __generate_fake_orders(self, quantity):
        self.__log(f"Generating fake orders")
        self.__orders = [(uuid.uuid4(), x) for x in range(quantity)]
        self.__log(f"{len(self.__orders)} generated...")
        
    def start_process(self):
        processes = []
        core = self.cores()
        for n in range(core):
            process = Process(target=self.process_orders, args=(n,))
            processes.append(process)
        for process in processes:
            process.start()
        for process in processes:
            process.join()
        
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
        print("Tamaño de orden:",len(self.__orders))

    def start_end(self, n):
        start = n * (len(self.__orders) // 5)
        end = start + (len(self.__orders) // 5)
        if n == 5:
            end = len(self.__orders) + 1
        return start, end
    
    def cores(self):
        cores = os.cpu_count()
        if cores <= 2:
            core = 1
            return core
        else:
            core = cores -2
            return core

#
#
# ---
if __name__=="__main__":
    orders_manager = OrdersManager()

    start_time = time.time()

    orders_manager.start_process()

    delay = time.time() - start_time

    print(f"{datetime.now()} > Tiempo de ejecucion: {delay} segundos...")
