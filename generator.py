from datetime import datetime

from route_time import RouteTime
from train_data import TrainData
from route import Route
from row import Row

class RowGenerator:
    cur_row: Row

    def generate_row(self) -> Row:
        self.cur_row = Row()
        tr = TrainData()
        tr.place_number = 12
        tr.wagon_number = 3
        tr.train_number = "723A"
        rt = RouteTime()
        rt.departure_time = datetime(year=2026, month=1, day=22, hour=8, minute=30)
        rt.arrival_time = datetime(year=2026, month=1, day=22, hour=22, minute=30)

        self.cur_row.name = "Иванов Иван Иванович"
        self.cur_row.passport_number = "1234 123456"
        self.cur_row.route = Route("Санкт-Петербург", "Москва", 600)
        self.cur_row.route_time = rt
        self.cur_row.train_data = tr
        self.cur_row.cost = 2460
        self.cur_row.card_number = "1234 5678 1234 5678"
        
        return self.cur_row

    def __generate_name(self) -> str:
        raise NotImplementedError

    def __generate_passport(self) -> str:
        raise NotImplementedError

    def __generate_route(self) -> Route:
        raise NotImplementedError

    def __generate_time(self) -> RouteTime:
        raise NotImplementedError

    def __generate_train_data(self) -> TrainData:
        raise NotImplementedError

    def __generate_cost(self) -> int:
        raise NotImplementedError

    def __generate_card(self) -> str:
        raise NotImplementedError



