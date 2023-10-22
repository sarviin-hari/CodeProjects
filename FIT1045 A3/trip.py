import math

from vehicles import Vehicle, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley
from vehicles import create_example_vehicles
from locations import City, Country
from locations import create_example_countries_and_cities


class Trip():
    """
    Represents a sequence of cities.
    """

    def __init__(self, departure: City) -> None:
        """
        Initialises a Trip with a departure city.
        """
        self.city_list = []                 # stores the cities involved in the trip
        self.every_time_list = []           # stores the time taken between cities (list in a list) for each vehicle passed (required for Task 7)

        self.dept_city = departure          # stores departure city
        self.city_list.append(departure)    # stores departure city in city list

    def add_next_city(self, city: City) -> None:
        """
        Adds the next city to this trip.
        """
        self.city_list.append(city)         # stores other cities of the trip in self.city_list

    def total_travel_time(self, vehicle: Vehicle) -> float:
        """
        Returns a travel duration for the entire trip for a given vehicle.
        Returns math.inf if any leg (i.e. part) of the trip is not possible.
        """

        time_list = []  # stores the time for vehicle to move between 2 cities

        for i in range(len(self.city_list)-1):

            # gets departure and arrival cities
            departure = self.city_list[i]
            arrival = self.city_list[i+1]

            # calls compute_travel_time method of the specific vehicle to get the time and stores in time_list
            time = vehicle.compute_travel_time(departure, arrival)
            time_list.append(time)

            # if time is math.inf, return math.inf
            if time == math.inf:
                self.every_time_list.append(time_list)
                return math.inf

        # stores time_list in self.time_list
        self.every_time_list.append(time_list)

        return sum(time_list)   # retruns total time taken

    def find_fastest_vehicle(self, vehicles: list[Vehicle]) -> (Vehicle, float):
        """
        Returns the Vehicle for which this trip is fastest, and the duration of the trip.
        If there is a tie, return the first vehicle in the list.
        If the trip is not possible for any of the vehicle, return (None, math.inf).
        """
        time_val = dict()   # stores the vehicle as the key and minimum time as the value

        # for every vehicle compute the total travel time and stores in the dictionary to the corresponding key
        for vehc in vehicles:
            time_val.update({vehc: self.total_travel_time(vehc)})

        # calculate the number of math.inf in teh values list that stores the time for each vehicle
        num_of_inf = list(time_val.values()).count(math.inf)

        # if all vehicles have time math.inf, return (None, math.inf)
        if num_of_inf == len(vehicles):
            return (None, math.inf)

        # else, find the minimum time from the list and returns the corresponding vehicle adn time for the one with the smallest time
        else:
            min_time = min(list(time_val.values()))

            for key, value in time_val.items():
                if value == min_time:
                    return (key, value)

    def __str__(self) -> str:
        """
        Returns a representation of the trip as a sequence of cities:
        City1 -> City2 -> City3 -> ... -> CityX
        """

        # stores first city name in str_city
        str_city = str(self.city_list[0])

        # for loop to add the next city name's in str_city
        for i in range(len(self.city_list)-1):
            str_city += " -> " + str(self.city_list[i+1])

        return str_city # returns str_city

def create_example_trips() -> list[Trip]:
    """
    Creates examples of trips.
    """

    #first we create the cities and countries
    create_example_countries_and_cities()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    sydney = australia.get_city("Sydney")
    canberra = australia.get_city("Canberra")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    #then we create trips
    trips = []

    for cities in [(melbourne, sydney), (canberra, tokyo), (melbourne, canberra, tokyo), (canberra, melbourne, tokyo)]:
        trip = Trip(cities[0])
        for city in cities[1:]:
            trip.add_next_city(city)

        trips.append(trip)

    return trips


if __name__ == "__main__":
    vehicles = create_example_vehicles()
    trips = create_example_trips()

    print("")
    print(trips)
    print("")


    for trip in trips:
        vehicle, duration = trip.find_fastest_vehicle(vehicles)
        print("The trip {} will take {} hours with {}".format(trip, duration, vehicle))
