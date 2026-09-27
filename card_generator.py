from data_holder import DataHolder


class CardGenerator: 
    banks_sizes: dict[str, int] 
    all_bics_size: int
    _weights: list[float]

    def __init__(self, dh: DataHolder):
        banks_sizes = {bank:len(bics) for bank, bics in BANKS.items()}
        all_bics_size = sum(banks_sizes.values())
        self._weights = list()

        avaliable_prob = 1 - sum(CUSTOM_PROBS.values())
        avaliable_all_bics = all_bics_size - sum([banks_sizes[bank] for bank in CUSTOM_PROBS.keys()])

        probs = {bank:(bic_amount/avaliable_all_bics) for bank, bic_amount in banks_sizes.items() if bank not in CUSTOM_PROBS.keys()}
        probs = {bank:(avaliable_prob*raw_prob) for bank, raw_prob in probs.items()}

        for bank in BANKS:
            if bank in CUSTOM_PROBS:
                self._weights.append(CUSTOM_PROBS[bank])
            else:
                self._weights.append(probs[bank])

    @property
    def weights(self) -> list[float]:
        return self._weights

