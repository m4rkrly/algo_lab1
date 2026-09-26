class TrainData:
    train_type: str
    train_subtype: str
    wagon_type: str
    train_number: str
    wagon_number: int
    place_number: int
    place_cost_mod: float

    def get_place_number(self) -> str:
        return f"{self.wagon_number}-{self.place_number}"
