from route import Route
from route_time import RouteTime
from train_data import TrainData

from datetime import datetime

class Row:
    name: str
    passport_number: str
    route: Route
    route_time: RouteTime
    train_data: TrainData
    cost: int
    card_number: str

    def get_row_as_tuple(self) -> tuple:
        return (
                self.name,
                self.passport_number,
                self.route.city_from,
                self.route.city_to,
                self.route_time.departure_time,
                self.route_time.arrival_time,
                self.train_data.train_number,
                self.train_data.get_place_number(),
                self.cost,
                self.card_number
        )
    
