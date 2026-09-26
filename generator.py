from datetime import datetime
from config import *
import json
from random import choice, randint

from route_time import RouteTime
from train_data import TrainData
from route import Route
from row import Row

class RowGenerator:
    cur_row: Row

    def __generate_name(self) -> str:
        cur_sex = choice(["man", "woman"])
        cur_name = str()
        cur_surname = str()
        cur_patronymic = str()

        with open(NAMES_PATH + NAMES_FILES[cur_sex]["names"], encoding = 'utf-8') as file:
            names = json.load(file)
            cur_name = choice(names)

        with open(NAMES_PATH + NAMES_FILES[cur_sex]["surnames"], encoding = 'utf-8') as file:
            surnames = json.load(file)
            cur_surname = choice(surnames)

        with open(NAMES_PATH + NAMES_FILES[cur_sex]["patronymics"], encoding = 'utf-8') as file:
            patronymics = json.load(file)
            cur_patronymic = choice(patronymics)
        
        return f"{cur_surname} {cur_name} {cur_patronymic}"


    def __generate_passport(self) -> str:
        with open(PASSPORT_FILE, encoding = 'utf-8') as file:
            region_numbers = json.load(file)
            region_number = choice(region_numbers)
           
            passport_blank_year = choice([year for year in range(PASSPORT_YEAR_RANGE[0], PASSPORT_YEAR_RANGE[1]+1)])
            passport_blank_year = str(passport_blank_year)[2:]
            
            passport_blank_number = randint(100_000, 999_999)
            
            passport_number = f"{region_number}{passport_blank_year} {passport_blank_number}"
            return passport_number


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

    def generate_row(self) -> Row:
        self.cur_row = Row()
        tr = TrainData()
        tr.place_number = 12
        tr.wagon_number = 3
        tr.train_number = "723A"
        rt = RouteTime()
        rt.departure_time = datetime(year=2026, month=1, day=22, hour=8, minute=30)
        rt.arrival_time = datetime(year=2026, month=1, day=22, hour=22, minute=30)


        self.cur_row.name = self.__generate_name()
        self.cur_row.passport_number = self.__generate_passport()

        self.cur_row.route = Route("Санкт-Петербург", "Москва", 600)
        self.cur_row.route_time = rt
        self.cur_row.train_data = tr
        self.cur_row.cost = 2460
        self.cur_row.card_number = "1234 5678 1234 5678"
        
        return self.cur_row




