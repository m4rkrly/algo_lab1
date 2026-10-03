from datetime import datetime
from config import *
from random import choice, randint

from data_holder import DataHolder
from departure_data import DepartureData
from card_generator import CardGenerator
from departure_generator import DepartureGenerator
from road_time import RoadTime
from route import Route
from row import Row

class RowGenerator:
    cur_row: Row
    data_holder: DataHolder
    card_gen: CardGenerator
    dep_gen: DepartureGenerator

    passports: set = set()

    def __init__(self, dh: DataHolder):
        self.data_holder = dh

        self.card_gen = CardGenerator(self.data_holder)
        self.dep_gen = DepartureGenerator(self.data_holder)

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
        while True:
            region_numbers = self.data_holder.PASSPORT_REGIONS
            region_number = choice(region_numbers)
            
            passport_blank_year = choice([year for year in range(PASSPORT_YEAR_RANGE[0], PASSPORT_YEAR_RANGE[1]+1)])
            passport_blank_year = str(passport_blank_year)[2:]
            
            passport_blank_number = str(randint(1, 999_999))
            passport_blank_number = passport_blank_number.zfill(6)
            
            passport_number = f"{region_number}{passport_blank_year} {passport_blank_number}"
            
            if passport_number not in self.passports:
                self.passports.add(passport_number)
                return passport_number

    def __generate_cost(self, distance: float) -> int:
        cost = int(distance * 1000)
        return cost

    def generate_row(self) -> Row:
        self.cur_row = Row()

        self.cur_row.wagon_and_place = "3-12"

        self.cur_row.name = self.__generate_name()
        self.cur_row.passport_number = self.__generate_passport()
        
        self.cur_row.dep_data = self.dep_gen.generate_departure()

        self.cur_row.card_number = self.card_gen.generate_card(self.data_holder)
        self.cur_row.cost = self.__generate_cost(self.cur_row.dep_data.route.distance)
        
        return self.cur_row

