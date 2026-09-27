from json import load
from config import *

class DataHolder:
    def __init__(self):
        # Имена, фамилии, отчества
        with open(NAMES_PATH + NAMES_FILES["man"]["names"], encoding = 'utf-8') as file:
            self.NAMES_MAN = load(file)

        with open(NAMES_PATH + NAMES_FILES["woman"]["names"], encoding = 'utf-8') as file:
            self.NAMES_WOMAN = load(file)


        with open(NAMES_PATH + NAMES_FILES["man"]["surnames"], encoding = 'utf-8') as file:
            self.SURNAMES_MAN = load(file)

        with open(NAMES_PATH + NAMES_FILES["woman"]["surnames"], encoding = 'utf-8') as file:
            self.SURNAMES_WOMAN = load(file)


        with open(NAMES_PATH + NAMES_FILES["man"]["patronymics"], encoding = 'utf-8') as file:
            self.PATRONIMYCS_MAN = load(file)

        with open(NAMES_PATH + NAMES_FILES["woman"]["patronymics"], encoding = 'utf-8') as file:
            self.PATRONIMYCS_WOMAN = load(file)

        
        # Паспортные регионы
        with open(PASSPORT_FILE, encoding = "utf-8") as file:
            self.PASSPORT_REGIONS = load(file)


        # Банки        
        with open(CARD_BANKS_FILE, encoding = "utf-8") as file:
            self.BANKS = load(file)

        with open(CARD_BICS_FILE, encoding = "utf-8") as file: 
            self.BICS = load(file)

        self.CUSTOM_PROBS = {}
        
        # Города
        with open(CITIES_FILE, encoding = "utf-8") as file:
            self.CITIES = load(file)

    


