from datetime import datetime
from config import *
import json
from random import choice, randint

from data_holder import DataHolder
from card_generator import CardGenerator
from route_time import RouteTime
from train_data import TrainData
from route import Route
from row import Row

class RowGenerator:
    cur_row: Row
    data_holder: DataHolder
    card_gen: CardGenerator

    def __init__(self, dh: DataHolder):
        self.data_holder = dh

        self.card_gen = CardGenerator(self.data_holder)

    def __generate_name(self) -> str:
        NAMES = {
            "man":{
                "names":self.data_holder.NAMES_MAN,
                "surnames":self.data_holder.SURNAMES_MAN,
                "patronymics":self.data_holder.PATRONIMYCS_MAN
            },
            "woman":{
                "names":self.data_holder.NAMES_WOMAN,
                "surnames":self.data_holder.SURNAMES_WOMAN,
                "patronymics":self.data_holder.PATRONIMYCS_WOMAN
            }
        }

        cur_sex = choice(["man", "woman"])
        
        cur_name = choice(NAMES[cur_sex]["names"])
        cur_surname = choice(NAMES[cur_sex]["surnames"])
        cur_patronymic = choice(NAMES[cur_sex]["patronymics"])
       
        return f"{cur_surname} {cur_name} {cur_patronymic}"


    def __generate_passport(self) -> str:
        region_numbers = self.data_holder.PASSPORT_REGIONS
        region_number = choice(region_numbers)
        
        passport_blank_year = choice([year for year in range(PASSPORT_YEAR_RANGE[0], PASSPORT_YEAR_RANGE[1]+1)])
        passport_blank_year = str(passport_blank_year)[2:]
        
        passport_blank_number = str(randint(1, 999_999))
        passport_blank_number = passport_blank_number.zfill(6)
        
        passport_number = f"{region_number}{passport_blank_year} {passport_blank_number}"
        return passport_number


    def __generate_route(self) -> Route:
        departure_city = choice(self.data_holder.CITIES)
        arrival_city = departure_city
        while departure_city == arrival_city:
            arrival_city = choice(self.data_holder.CITIES)
        
        delta = (
            float(departure_city["lat"]) - float(arrival_city["lat"]),
            float(departure_city["lng"]) - float(arrival_city["lng"])
        )
        
        distance = (delta[0]**2 + delta[1]**2)**(1/2)
        
        return Route(departure_city["ru_name"], arrival_city["ru_name"], distance)

    def __generate_time(self) -> RouteTime:
        raise NotImplementedError

    def __generate_train_data(self) -> TrainData:
        raise NotImplementedError

    def __generate_cost(self) -> int:
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
        self.cur_row.card_number = self.card_gen.generate_card(self.data_holder)
        self.cur_row.route = self.__generate_route()

        self.cur_row.route_time = rt
        self.cur_row.train_data = tr
        self.cur_row.cost = 2460
        
        return self.cur_row




