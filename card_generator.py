from os import WTERMSIG, system
from random import choice, choices, randint

from data_holder import DataHolder


class CardGenerator: 
    _bank_weights: list[float]
    _systems_weights: list[float]
    _card_counter: dict[str, int] = {}

    def __init__(self, dh: DataHolder):
        self._bank_weights = self.__set_banks_probabilities(dh)
        self._systems_weights = self.__set_systems_probabilities(dh)

    
    def __set_systems_probabilities(
        self,
        dh: DataHolder,
    ) -> list[float]:
        weights = list()
        avaliable_prob = 1 - sum(dh.CUSTOM_SYSTEMS_PROBS.values())
        avaliable_systems = len(dh.SYSTEMS) - len(dh.CUSTOM_SYSTEMS_PROBS)

        for system in dh.SYSTEMS:
            if system in dh.CUSTOM_SYSTEMS_PROBS:
                weights.append(dh.CUSTOM_SYSTEMS_PROBS[system])
            else:
                weights.append(avaliable_prob*(1/avaliable_systems))
        return weights


    def __set_banks_probabilities(
        self,
        dh: DataHolder,
    ) -> list[float]:
        banks_bins_amount = dict()
        for bank, systems_and_bins in dh.BINS.items():
            s = sum([len(bins) for bins in systems_and_bins.values()])
            banks_bins_amount[bank] = s

        overall_bins_amount = sum(banks_bins_amount.values())

        weights = list()
        avaliable_prob = 1 - sum(dh.CUSTOM_BANKS_PROBS.values())
        avaliable_all_bics = overall_bins_amount - sum([banks_bins_amount[bank] for bank in dh.CUSTOM_BANKS_PROBS.keys()])

        probs = {bank:(bic_amount/avaliable_all_bics) for bank, bic_amount in banks_bins_amount.items() if bank not in dh.CUSTOM_BANKS_PROBS.keys()}
        probs = {bank:(avaliable_prob*raw_prob) for bank, raw_prob in probs.items()}

        for bank in dh.BANKS:
            if bank in dh.CUSTOM_BANKS_PROBS:
                weights.append(dh.CUSTOM_BANKS_PROBS[bank])
            else:
                weights.append(probs[bank])
        return weights


    def _adapt_systems_probabilities(self, dh: DataHolder, bank: str, systems_weights: list[float]) -> list[float]:
        system_probs = dict(zip(dh.SYSTEMS, systems_weights))
        avaliable_systems = list(dh.BINS[bank].keys())

        probs = {sys:prob if sys in avaliable_systems else 0 for sys, prob in system_probs.items()}
        avaliable_prob = sum(probs.values())
        probs = {sys:(prob/avaliable_prob) for sys, prob in probs.items()}
        
        new_weights = list()
        for system in dh.SYSTEMS:
            new_weights.append(probs[system])
        return new_weights
            



    def generate_card(self, dh: DataHolder) -> str:
        while True:
            chosen_bank = choices(dh.BANKS, weights = self._bank_weights, k = 1)[0]
            cur_system_weights = self._adapt_systems_probabilities(dh, chosen_bank, self._systems_weights)
            chosen_system = choices(dh.SYSTEMS, weights = cur_system_weights, k = 1)[0]
            chosen_bin = choice(dh.BINS[chosen_bank][chosen_system])

            card_user_number = str(randint(1, 999_999_999))
            card_user_number = card_user_number.zfill(9)
            
            control_digit = randint(0, 9)

            raw_card_number = f"{chosen_bin}{card_user_number}{control_digit}"

            counter = 0
            card_number = str()
            for digit in raw_card_number:
                card_number += digit
                counter += 1
                if counter == 4:
                    card_number += ' '
                    counter = 0
    
            counter = self._card_counter.get(card_number, 0)
            if counter <= 5:
                if counter == 0:
                    self._card_counter[card_number] = 0
                self._card_counter[card_number] += 1 
                return card_number

