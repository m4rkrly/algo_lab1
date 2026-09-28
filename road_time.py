from datetime import datetime


class RoadTime:
    departure_time: datetime
    arrival_time: datetime

    def __init__(
        self,
        departure_time: datetime = datetime(0, 0, 0),
        arrival_time: datetime = datetime(0, 0, 0)
    ):
        self.departure_time = departure_time
        self.arrival_time = arrival_time
