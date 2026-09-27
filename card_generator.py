from random import choice, choices, randint

from data_holder import DataHolder


class CardGenerator: 
    _weights: list[float]

    def __init__(self, dh: DataHolder):
        banks_sizes = {bank:len(bics) for bank, bics in dh.BICS.items()}
        all_bics_size = sum(banks_sizes.values())
        self._weights = list()

        avaliable_prob = 1 - sum(dh.CUSTOM_PROBS.values())
        avaliable_all_bics = all_bics_size - sum([banks_sizes[bank] for bank in dh.CUSTOM_PROBS.keys()])

        probs = {bank:(bic_amount/avaliable_all_bics) for bank, bic_amount in banks_sizes.items() if bank not in dh.CUSTOM_PROBS.keys()}
        probs = {bank:(avaliable_prob*raw_prob) for bank, raw_prob in probs.items()}

        for bank in dh.BANKS:
            if bank in dh.CUSTOM_PROBS:
                self._weights.append(dh.CUSTOM_PROBS[bank])
            else:
                self._weights.append(probs[bank])


    def generate_card(self, dh: DataHolder) -> str:
        chosen_bank = choices(dh.BANKS, weights = self._weights, k=1)[0]
        chosen_bic = choice(dh.BICS[chosen_bank])

        card_user_number = str(randint(1, 999_999_999))
        card_user_number = card_user_number.zfill(9)
        
        control_digit = randint(0, 9)

        raw_card_number = f"{chosen_bic}{card_user_number}{control_digit}"

        counter = 0
        card_number = str()
        for digit in raw_card_number:
            card_number += digit
            counter += 1
            if counter == 4:
                card_number += ' '
                counter = 0

        return card_number


