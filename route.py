class Route:
    city_from: str
    city_to: str
    distance: str

    def __init__(self, city_from, city_to, distance):
        self.city_from = city_from
        self.city_to = city_to
        self.distance = distance


