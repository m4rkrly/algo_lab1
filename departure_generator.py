from random import choice

from data_holder import DataHolder
from departure_data import DepartureData
from departure_manager import DepartureManager
from road_time import RoadTime
from route import Route

class DepartureGenerator:
    data_holder: DataHolder
    dep_manager: DepartureManager


    def __init__(self, dh: DataHolder):
        self.data_holder = dh
        self.dep_manager = DepartureManager()


    def generate_departure(self) -> DepartureData:
        cur_departure = DepartureData()

        # # (1) Подкинуть монетку и взять/не брать обратный рейс
        # random_back = self.dep_manager.get_random_back()
        # if random_back != None: return random_back

        # (2) Сгенерировать маршрут
        cur_departure.route = self.__generate_route()

        # (3) Сгенерировать тип и подтип поезда
        cur_departure.train_type, cur_departure.train_subtype = self.__generate_train_type(
            cur_departure.route
        )
        
        # (4) Сгенерировать номер рейса
        cur_departure.train_number = self.__generate_route_number(
            cur_departure.train_type
        )

        # (5) Узнать ограничения по времени из DepartureManager, если они есть
        time_limits = self.dep_manager.get_occupied_time(cur_departure.train_number)

        # (6) Сгенерировать время отправления и прибытия
        cur_departure.road_time = self.__generate_time(
            cur_departure.train_subtype,
            cur_departure.route.distance,
            time_limits
        )

        # # (7) Сгенерировать обратный маршрут
        # back_departure = self.__build_back(cur_departure)
        #
        # # (8) Проверить обратный маршрут на пересеченеи
        # intersection = self.dep_manager.find_intersection(
        #     back_departure.train_number,
        #     back_departure.road_time
        # )
        # if intersection is None:
        #     self.dep_manager.add_to_backs(back_departure)
        #
        #     # (8.1) Не забыть учесть то, что обратный маршрут тоже что-то да занимает
        #     self.dep_manager.add_time_to_occupied(
        #         back_departure.train_number,
        #         RoadTime(back_departure.road_time.departure_time, back_departure.road_time.arrival_time)
        #     )

        # (9) Добавить ограничения по времени в архив
        time_limit = self.__calculate_time_limit(cur_departure.train_subtype, cur_departure.road_time)
        self.dep_manager.add_occupied_time(cur_departure.train_number, time_limit)

        return cur_departure


    def __generate_route(self) -> Route:
        departure_city = choice(self.data_holder.CITIES)
        arrival_city = departure_city
        while departure_city == arrival_city:
            arrival_city = choice(self.data_holder.CITIES)
        
        delta = (
            float(departure_city["lat"]) - float(arrival_city["lat"]),
            float(departure_city["lng"]) - float(arrival_city["lng"])
        )
        
        distance = (delta[0]**2 + delta[1]**2)**(1/2)
        
        return Route(departure_city["ru_name"], arrival_city["ru_name"], distance)


    def __generate_time(self, train_subtype: str, distance: float, time_limits: list[RoadTime]) -> RoadTime:
        # Здесь сделать тот алгортм, который я записал, со свободными интервалами
        raise NotImplementedError

    def __generate_train_type(self, route: Route) -> tuple[str, str]:
        # Здесь сделать выбор типа и подтипа поезда 
        raise NotImplementedError

    def __generate_route_number(self, train_type: str) -> str:
        # Здесь сделать выбор случайного номера и буквы по типу поезда
        raise NotImplementedError

    # def __build_back(self, dep: DepartureData) -> DepartureData:
    #     # Здесь сделать алгоритм создания обратного рейса
    #     raise NotImplementedError

    def __calculate_time_limit(self, train_type: str, road_time: RoadTime) -> RoadTime:
        # Здесь высчитывать полное время занятости рейса
        raise NotImplementedError
