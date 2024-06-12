import csv

from locations import City, Country, test_example_countries_and_cities

def create_cities_countries_from_CSV(path_to_csv: str) -> None:
    """
    Reads a CSV file given its path and creates instances of City and Country for each line.
    """

    country_list = []

    with open(path_to_csv, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)

        for line in csv_reader:
            if line[header.index('country')] not in country_list:
                Country(line[header.index('country')], line[header.index('iso3')])
                country_list.append(line[4])

            City(line[header.index('city_ascii')], line[header.index('lat')], line[header.index('lng')], line[header.index('country')], line[header.index('capital')], line[header.index('id')])


if __name__ == "__main__":
    create_cities_countries_from_CSV("worldcities_truncated.csv")

    for country in Country.countries:
        print(country)

    for city in City.cities:
        print(city)

    test_example_countries_and_cities()

