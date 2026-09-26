from datetime import datetime

from train_data import TrainData
from route import Route
from row import Row

class RowGenerator:
    def generate_row(self) -> Row:
        rw = Row()
        tr = TrainData()
        tr.place_number = 12
        tr.wagon_number = 3
        tr.train_number = "723A"

        rw.name = "Иванов Иван Иванович"
        rw.passport_number = "1234 123456"
        rw.route = Route("Санкт-Петербург", "Москва", 600)
        rw.departure_time = datetime(year=2026, month=1, day=22, hour=8, minute=30)
        rw.arrival_time = datetime(year=2026, month=1, day=22, hour=22, minute=30)
        rw.train_data = tr
        rw.cost = 2460
        rw.card_number = "1234 5678 1234 5678"
        
        return rw

    def __generate_name(self) -> str:
        raise NotImplementedError

    def __generate_card(self) -> str:
        raise NotImplementedError

    def __generate_passport(self) -> str:
        raise NotImplementedError
