import math

import city_country_csv_reader
from locations import City, Country
from trip import Trip
from vehicles import Vehicle, create_example_vehicles
import networkx

valid_time_list = [] # stores the time taken between cities (list in a list) for each vehicle passed (required for Task 7)

def find_shortest_path(vehicle: Vehicle, from_city: City, to_city: City) -> Trip:
    """
    Returns a shortest path between two cities for a given vehicle,
    or None if there is no path.
    """

    # calls the Graph function in networkx and stores in G
    G = networkx.Graph()

    # add all cities found as the nodes (names of the cities)
    for city in City.cities.values():
        G.add_node(city)

    for city_index_1 in range(len(City.cities)):
        # loops through every pair of cities possible to check if a path exists
        for city_index_2 in range(city_index_1, len(City.cities)):
            if city_index_1 != city_index_2:

                # gets two cities
                city1_val = list(City.cities.values())[city_index_1]   # corresponds to the index of first loop
                city2_val = list(City.cities.values())[city_index_2]   # corresponds to the index of second loop

                # compute the valid time for given vehicle by calling compute_travel_time method
                valid_time = vehicle.compute_travel_time(city1_val, city2_val)

                # as long as valid_time is not math.inf, add edges between corresponding cities and it's valid_time as the weight
                if valid_time != math.inf:
                    G.add_edge(city1_val, city2_val, weight=valid_time)

    # if the given source and target city has a path, find the shortest path and corresponding path_trip
    if networkx.has_path(G, source=from_city, target=to_city):

        # finds the shortest path between both cities and it's weight (time)
        short_path_list = networkx.shortest_path(G, source=from_city, target=to_city, weight='weight')

        # gets the first city (departure) and creates aa Trip
        dept = short_path_list[0]
        path_trip = Trip(dept)

        time_list = []  # time_list to store corresponding time between 2 cities

        # loops through every cities, get the next city name, add the next city to the trip, store the time taken between 2 cities in time_list
        for city_index_1 in range(1, len(short_path_list)):
            path_trip.add_next_city(short_path_list[city_index_1])
            time_list.append(networkx.shortest_path_length(G, source=short_path_list[city_index_1-1], target=short_path_list[city_index_1], weight='weight'))

        # stores the time_list in variable outside the method called valid_time_list
        valid_time_list.append(time_list)

        # returns the corresponding trip
        return path_trip

    else:
        # if no trip possible, stores math.inf in valid_time_list and returns None
        valid_time_list.append(math.inf)
        return None

if __name__ == "__main__":
    city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")

    vehicles = create_example_vehicles()

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")
    india = Country.countries["India"]
    bangalore = india.get_city("Bangalore")
    china = Country.countries["China"]
    guiyang = china.get_city("Guiyang")

    print(australia, melbourne)
    print(india, bangalore)

    for vehicle in vehicles:
        print("The shortest path for {} from {} to {} is {}".format(vehicle, bangalore, guiyang,
                                                                    find_shortest_path(vehicle, bangalore, guiyang)))

    # vehicle = create_example_vehicles()[1]
    # print("The shortest path for {} from {} to {} is {}".format(vehicle, melbourne, tokyo, find_shortest_path(vehicle, melbourne, tokyo)))