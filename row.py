from departure_data import DepartureData

class Row:
    name: str
    passport_number: str
    dep_data: DepartureData
    wagon_and_place: str
    cost: int
    card_number: str

    def get_row_as_tuple(self) -> tuple:
        return (
                self.name,
                self.passport_number,
                self.dep_data.route.departure_city,
                self.dep_data.route.arrival_city,
                self.dep_data.road_time.departure_time,
                self.dep_data.road_time.arrival_time,
                self.dep_data.train_number,
                self.wagon_and_place,
                self.cost,
                self.card_number
        )
    
