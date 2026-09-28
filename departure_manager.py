from departure_data import DepartureData
from road_time import RoadTime

class DepartureManager:
    occupied_time: dict[str, list[RoadTime]]
    # backs_pool: list[DepartureData]

    def get_occupied_time(self, departure_number: str) -> list[RoadTime]:
        return self.occupied_time.get(departure_number, [])

    def add_occupied_time(self, departure_number: str, road_time: RoadTime) -> None:
        raise NotImplementedError

    # def find_intersection(self, departure_number: str, road_time: RoadTime) -> DepartureData | None:
    #     raise NotImplementedError
 
    # def get_random_back(self) -> DepartureData:
    #     raise NotImplementedError
    #
    # def add_to_backs(self, departure: DepartureData) -> None:
    #     raise NotImplementedError
    #


