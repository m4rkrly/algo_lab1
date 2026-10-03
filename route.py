class Route:
    departure_city: str
    arrival_city: str
    distance: float

    def __init__(self, city_from: str, city_from_status: str, city_to: str, city_to_status: str, distance: float):
        self.departure_city = city_from
        self.dep_city_status = city_from_status
        self.arrival_city = city_to
        self.arr_city_status = city_to_status
        self.distance = distance


