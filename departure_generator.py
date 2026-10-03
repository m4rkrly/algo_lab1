from datetime import timedelta
from random import choice, choices, randint

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

        # (1) Подкинуть монетку и взять/не брать обратный рейс
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
            cur_departure.train_type,
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
        time_limit = self.__calculate_time_limit(cur_departure.train_type, cur_departure.road_time)
        self.dep_manager.add_occupied_time(cur_departure.train_number, time_limit)

        return cur_departure


    def __generate_route(self) -> Route:
        departure_city = choice(self.data_holder.CITIES)
        arrival_city = departure_city
        while departure_city == arrival_city:
            arrival_city = choice(self.data_holder.CITIES)
       
        arr_city_status = arrival_city["capital"] if arrival_city["capital"] != "" else "minor"
        dep_city_status = departure_city["capital"] if departure_city["capital"] != "" else "minor"

        delta = (
            float(departure_city["lat"]) - float(arrival_city["lat"]),
            float(departure_city["lng"]) - float(arrival_city["lng"])
        )
        
        distance = ((delta[0] * self.data_holder.DISTANCE_COEFFICITENT)**2 + (delta[0] * self.data_holder.DISTANCE_COEFFICITENT)**2)**(1/2)
        
        return Route(
            departure_city["ru_name"],
            dep_city_status, 
            arrival_city["ru_name"],
            arr_city_status,
            distance
        )


    def __generate_time(self, train_type: str, distance: float, time_limits: list[RoadTime]) -> RoadTime:
        # Время пути выражается в часах 
        time_in_way = timedelta(hours = distance / self.data_holder.TRAINS_SPEEDS[train_type])

        previous_time = self.data_holder.CURRENT_TIME
        free_times = []
        free_times_lengths = []
        for limit in time_limits:
            free_times.append((previous_time, limit.departure_time))
            previous_time = limit.arrival_time
            free_times_lengths.append(limit.departure_time - previous_time)

        time_window = tuple()
        for i in range(len(free_times)):
            diff = free_times_lengths[i] - time_in_way
            if diff > timedelta(days = 1):
                time_window = (free_times[i][0], diff)
        
        if time_window == tuple():
            time_window = (previous_time, timedelta(days = 1))

        seconds = time_window[1].total_seconds()
        dep_time = time_window[0] + timedelta(seconds=randint(3600, int(seconds)))
        arr_time = dep_time + time_in_way        

        return RoadTime(dep_time, arr_time)

    def __generate_train_type(self, route: Route) -> tuple[str, str]:
        distance = route.distance

        route_case = str()
        if route.arrival_city in ("Москва, Санкт-Петербург") and route.departure_city in ("Москва, Санкт-Петербург"):
            route_case = "moscow-spb"
        elif (route.dep_city_status == "admin") ^ (route.arr_city_status == "admin"):
            route_case = "admin-minor"
        else:
            route_case = "minor-minor"

        probabilities: dict[str, dict[str, float]] = self.data_holder.TRAINS_TYPES_PROBS[route_case]

        types_probs = dict()
        for str_limit, probs in probabilities.items():
            limit = str_limit.split("-")
            limit = list(map(int, limit))

            if limit[0] <= distance <= limit[1]:
                types_probs = probs
                break

        train_type = choices(list(types_probs.keys()), weights = list(types_probs.values()), k=1)[0]

        subtype_probs: dict[str, float] = self.data_holder.TRAINS_SUBTYPES_PROBS[route_case][train_type]
        train_subtype = choices(list(subtype_probs.keys()), weights= list(subtype_probs.values()), k=1)[0]
        
        return (train_type, train_subtype)
            

    def __generate_route_number(self, train_type: str) -> str:
        if train_type in ("regular", "hasty"):
            chosen_type = choices(list(self.data_holder.SEASONAL_PROB.keys()), weights = list(self.data_holder.SEASONAL_PROB.values()), k = 1)[0]
        else:
            chosen_type = "regular"

        train_number_limits: list[int] = self.data_holder.TRAINS_NUMBERS[train_type][chosen_type]

        chosen_number = randint(train_number_limits[0], train_number_limits[1])
        chosen_number = str(chosen_number).zfill(3)
        chosen_letter = choice(self.data_holder.TRAINS_LETTERS) 

        return f"{chosen_number}{chosen_letter}"

    def __calculate_time_limit(self, train_type: str, road_time: RoadTime) -> RoadTime:
        time_in_way = road_time.arrival_time - road_time.departure_time
        occupied_time = road_time.departure_time + 2*time_in_way + 2*self.data_holder.TRAINS_BREAKS[train_type]
        return RoadTime(road_time.departure_time, occupied_time)
        

    # def __build_back(self, dep: DepartureData) -> DepartureData:
    #     # Здесь сделать алгоритм создания обратного рейса
    #     raise NotImplementedError


