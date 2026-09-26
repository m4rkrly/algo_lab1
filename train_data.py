class TrainData:
    train_type: str
    train_subtype: str
    wagon_type: str
    train_number: str
    wagon_number: int
    place_number: int

    def get_place_number(self) -> str:
        return f"{self.wagon_number}-{self.place_number}"
