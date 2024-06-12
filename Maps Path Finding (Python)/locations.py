from __future__ import annotations

import math
from enum import Enum
from typing import Any
from geopy import distance


class CapitalType(Enum):
    """
    The different types of capitals (e.g. "primary").
    """
    primary = "primary"
    admin = "admin"
    minor = "minor"
    unspecified = ""

    def __str__(self) -> str:
        return self.value


class Country():
    """
    Represents a country.
    """

    countries = dict()  # a dict that associates country names to instances.

    def __init__(self, name: str, iso3: str) -> None:
        """
        Creates an instance with a country name and a country ISO code with 3 characters.
        """
        self.country_name = name    # stores country name
        self.ISO_code = iso3        # stores country ISO code

        self.city = dict()          # dictionary to store city of the specific countries

        Country.countries.update({self.country_name:self})  # stores the country name (key) and country object (value) in countries dictionary

    def _add_city(self, city: City):
        """
        Adds a city to the country.
        """

        self.city.update({str(city.name): city})    # stores the city name (key) and city object (value) of specific cities of a country in self.city dictionary


    def get_cities(self, capital_types: list[CapitalType] = None) -> list[City]:
        """
        Returns a list of cities of this country.

        The argument capital_types can be given to specify a subset of the capital types that must be returned.
        Cities that do not correspond to these capital types are not returned.
        If no argument is given, all cities are returned.
        """

        city_capital_type = []

        # if capital type is None return all cities of a country
        if capital_types is None:
            return list(self.city.values())

        # stores cities that has the same capital as in the capital_types list
        for cities in list(self.city.values()):
            if cities.capital_type in capital_types:
                city_capital_type.append(cities)

        # returns the corresponding cities that has the capital_types as the list
        return city_capital_type

    def get_city(self, city_name: str) -> Any | None:
        """
        Returns a city of the given name in this country.
        Returns None if there is no city by this name.
        If there are multiple cities of the same name, returns an arbitrary one.
        """

        # if given city_name is in the self.city dictionary, return the city object
        if city_name in list(self.city.keys()):
            return self.city[city_name]

        # if no such city, return None
        else:
            return None

    def __str__(self) -> str:
        """
        Returns the name of the country.
        """
        return self.country_name

class City():
    """
    Represents a city.
    """

    cities = dict() # a dict that associates city IDs to instances.

    def __init__(self, name: str, latitude: str, longitude: str, country: str, capital_type: str, city_id: str) -> None:
        """
        Initialises a city with the given data.
        """
        self.name = name                                # stores city name
        self.latitude = latitude                        # stores city latitude
        self.longitude = longitude                      # stores city longitude
        self.country = country                          # stores country name of the city
        self.capital_type = CapitalType(capital_type)   # stores the enum capital type of the city
        self.city_id = city_id                          # stores city_id

        City.cities.update({self.city_id:self}) # stores the ccity id (key) and city object (value) in cities dictionary

        Country._add_city(Country.countries[self.country], self)    # calls _add_city method from the Country class to add city to it's respective country when initialized

    def distance(self, other_city: City) -> int:
        """
        Returns the distance in kilometers between two cities using the great circle method,
        rounded up to an integer.
        """

        city1 = (self.latitude, self.longitude)             # stores latitude and longitude of city
        city2 = (other_city.latitude, other_city.longitude) # stores latitude and longitude of city

        return math.ceil(distance.great_circle(city1, city2).km)    # gets the great circle distance(from geopy) between both cities in km

    def __str__(self) -> str:
        """
        Returns the name of the city and the country ISO3 code in parentheses.
        For example, "Melbourne (AUS)".
        """
        return self.name + " (" + Country.countries[self.country].ISO_code + ")"    # return city name and country ISO code

def create_example_countries_and_cities() -> None:
    """
    Creates a few Countries and Cities for testing purposes.
    """
    australia = Country("Australia", "AUS")
    melbourne = City("Melbourne", "-37.8136", "144.9631", "Australia", "admin", "1036533631")
    canberra = City("Canberra", "-35.2931", "149.1269", "Australia", "primary", "1036142029")
    sydney = City("Sydney", "-33.865", "151.2094", "Australia", "admin", "1036074917")

    japan = Country("Japan", "JPN")
    tokyo = City("Tokyo", "35.6839", "139.7744", "Japan", "primary", "1392685764")

def test_example_countries_and_cities() -> None:
    """
    Assuming the correct cities and countries have been created, runs a small test.
    """
    australia = Country.countries['Australia']
    canberra = australia.get_city("Canberra")
    melbourne = australia.get_city("Melbourne")
    sydney = australia.get_city("Sydney")

    japan = Country.countries['Japan']
    tokyo = japan.get_city("Tokyo")

    print("The distance between {} and {} is {}km".format(melbourne, sydney, melbourne.distance(sydney)))

    for city in australia.get_cities([CapitalType.admin, CapitalType.primary]):
        print("{} is a {} capital of {}".format(city, city.capital_type, city.country))


if __name__ == "__main__":
    create_example_countries_and_cities()
    test_example_countries_and_cities()
