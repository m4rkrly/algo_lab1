from config import *
from random import choice, choices, randint

from data_holder import DataHolder
from card_generator import CardGenerator
from departure_generator import DepartureGenerator
from row import Row

class RowGenerator:
    _cur_row: Row
    _wagon_type: str
    _data_holder: DataHolder
    _card_gen: CardGenerator
    _dep_gen: DepartureGenerator

    passports: set = set()

    def __init__(self, dh: DataHolder):
        self._data_holder = dh

        self._card_gen = CardGenerator(self._data_holder)
        self._dep_gen = DepartureGenerator(self._data_holder)

    def __generate_name(self) -> str:
        NAMES = {
            "man":{
                "names":self._data_holder.NAMES_MAN,
                "surnames":self._data_holder.SURNAMES_MAN,
                "patronymics":self._data_holder.PATRONIMYCS_MAN
            },
            "woman":{
                "names":self._data_holder.NAMES_WOMAN,
                "surnames":self._data_holder.SURNAMES_WOMAN,
                "patronymics":self._data_holder.PATRONIMYCS_WOMAN
            }
        }

        cur_sex = choice(["man", "woman"])
        
        cur_name = choice(NAMES[cur_sex]["names"])
        cur_surname = choice(NAMES[cur_sex]["surnames"])
        cur_patronymic = choice(NAMES[cur_sex]["patronymics"])
       
        return f"{cur_surname} {cur_name} {cur_patronymic}"


    def __generate_passport(self) -> str:
        while True:
            region_numbers = self._data_holder.PASSPORT_REGIONS
            region_number = choice(region_numbers)
            
            passport_blank_year = choice([year for year in range(PASSPORT_YEAR_RANGE[0], PASSPORT_YEAR_RANGE[1]+1)])
            passport_blank_year = str(passport_blank_year)[2:]
            
            passport_blank_number = str(randint(1, 999_999))
            passport_blank_number = passport_blank_number.zfill(6)
            
            passport_number = f"{region_number}{passport_blank_year} {passport_blank_number}"
            
            if passport_number not in self.passports:
                self.passports.add(passport_number)
                return passport_number

    def __generate_wagon_and_place(self, train_subtype: str) -> str:
        wagon_types = self._data_holder.WAGONS[train_subtype]
        self._wagon_type = choices(
            list(wagon_types.keys()),
            weights = list(wagon_types.values()),
            k = 1
        )[0]

        if self._data_holder.WAGONS_NUMBERS.get(train_subtype) is not None:
            wagon_number = choice(self._data_holder.WAGONS_NUMBERS[train_subtype][self._wagon_type])
        else:
            wagon_number = randint(1, 20)
       
        max_seats = int()
        if self._wagon_type == "1Р" and train_subtype == "sapsan":
            max_seats = self._data_holder.WAGONS_SEATS[f"{train_subtype}_1Р"]
        else:
            max_seats = self._data_holder.WAGONS_SEATS[self._wagon_type]

        seat_number = randint(1, max_seats)
        return f"{wagon_number}-{seat_number}"


    def __generate_cost(self, distance: float, train_type: str, train_subtype: str, wagon_type: str) -> int:
        train_class = self._data_holder.TRAINS_COSTS[train_type]
        wagon_class = self._data_holder.WAGONS_COSTS[train_subtype][wagon_type]
        cost = int(distance * train_class * wagon_class)
        if cost < 60:
            # Приблизительная минимальная цена на проезд в РЖД
            cost = 60

        return cost

    def generate_row(self) -> Row:
        self._cur_row = Row()

        self._cur_row.name = self.__generate_name()
        self._cur_row.passport_number = self.__generate_passport()
        
        self._cur_row.dep_data = self._dep_gen.generate_departure()

        self._cur_row.wagon_and_place = self.__generate_wagon_and_place(
            self._cur_row.dep_data.train_subtype
        )

        self._cur_row.card_number = self._card_gen.generate_card(self._data_holder)
        self._cur_row.cost = self.__generate_cost(
            self._cur_row.dep_data.route.distance,
            self._cur_row.dep_data.train_type,
            self._cur_row.dep_data.train_subtype,
            self._wagon_type
        )
        
        return self._cur_row

