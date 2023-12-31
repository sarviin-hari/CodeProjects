import math
from abc import ABC, abstractmethod

from locations import CapitalType, City, Country
from locations import create_example_countries_and_cities

class Vehicle(ABC):
    """
    A Vehicle defined by a mode of transportation, which results in a specific duration.
    """

    @abstractmethod
    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        """
        pass


class CrappyCrepeCar(Vehicle):
    """
    A type of vehicle that:
        - Can go from any city to any other at a given speed.
    """

    def __init__(self, speed: int) -> None:
        """
        Creates a CrappyCrepeCar with a given speed in km/h.
        """
        self.speed = speed  # instance variable that stores speed

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        """

        distance = departure.distance(arrival)  # gets the distance between 2 cities
        time = distance / self.speed            # formulate the time taken for the said distance

        return math.ceil(time)                  # returns the time

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "CrappyCrepeCar (100 km/h)"
        """

        return "CrappyCrepeCar ({} km/h)".format(self.speed)    # return Car name and speed


class DiplomacyDonutDinghy(Vehicle):
    """
    A type of vehicle that:
        - Can travel between any two cities in the same country.
        - Can travel between two cities in different countries only if they are both "primary" capitals.
        - Has different speed for the two cases.
    """

    def __init__(self, in_country_speed: int, between_primary_speed: int) -> None:
        """
        Creates a DiplomacyDonutDinghy with two given speeds in km/h:
            - one speed for two cities in the same country.
            - one speed between two primary cities.
        """
        self.count_speed = in_country_speed     # instance variable that stores country speed
        self.prim_speed = between_primary_speed # instance variable that stores primary speed

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """

        # if departure country and arrival country is the same, find the distance and compute the time with country speed
        if departure.country == arrival.country:
            distance = departure.distance(arrival)
            time = distance / self.count_speed
            return math.ceil(time)

        # if departure country and arrival country is primary capital type, find the distance and compute the time with country speed
        elif departure.capital_type == CapitalType.primary and arrival.capital_type == CapitalType.primary:
            distance = departure.distance(arrival)
            time = distance / self.prim_speed
            return math.ceil(time)

        # all other invalid cases return math.inf
        else:
            return math.inf

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "DiplomacyDonutDinghy (100 km/h | 200 km/h)"
        """
        return "DiplomacyDonutDinghy ({} km/h | {} km/h)".format(self.count_speed, self.prim_speed) # returns Car name and country and primary speed

class TeleportingTarteTrolley(Vehicle):
    """
    A type of vehicle that:
        - Can travel between any two cities if the distance is less than a given maximum distance.
        - Travels in fixed time between two cities within the maximum distance.
    """

    def __init__(self, travel_time:int, max_distance: int) -> None:
        """
        Creates a TarteTruck with a distance limit in km.
        """
        self.time = travel_time         # stores travel time of car
        self.distance = max_distance    # stores maximum distance that car can travel

    def compute_travel_time(self, departure: City, arrival: City) -> float:
        """
        Returns the travel duration of a direct trip from one city
        to another, in hours, rounded up to an integer.
        Returns math.inf if the travel is not possible.
        """
        # gets the distance between departure and arrival cities
        distance = departure.distance(arrival)

        # if computes distance is less than max distance, return the fixed time
        if distance < self.distance:
            return self.time

        # all other cases return math.inf
        else:
            return math.inf

    def __str__(self) -> str:
        """
        Returns the class name and the parameters of the vehicle in parentheses.
        For example "TeleportingTarteTrolley (5 h | 1000 km)"
        """
        return "TeleportingTarteTrolley ({} h | {} km)".format(self.time, self.distance)    # returns Car name and fixed time and max distance


def create_example_vehicles() -> list[Vehicle]:
    """
    Creates 3 examples of vehicles.
    """
    return [CrappyCrepeCar(200), DiplomacyDonutDinghy(100, 500), TeleportingTarteTrolley(3, 2000)]


if __name__ == "__main__":
    create_example_countries_and_cities()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    canberra = australia.get_city("Canberra")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    vehicles = create_example_vehicles()

    for vehicle in vehicles:
        for from_city, to_city in [(melbourne, canberra), (tokyo, canberra), (tokyo, melbourne)]:
        # for from_city, to_city in [(paris, bordeaux)]:
            print("Travelling from {} to {} will take {} hours with {}".format(from_city, to_city, vehicle.compute_travel_time(from_city, to_city), vehicle))
