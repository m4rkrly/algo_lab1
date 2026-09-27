class Route:
    departure_city: str
    arrival_city: str
    distance: float

    def __init__(self, city_from: str, city_to: str, distance: float):
        self.departure_city = city_from
        self.arrival_city = city_to
        self.distance = distance


