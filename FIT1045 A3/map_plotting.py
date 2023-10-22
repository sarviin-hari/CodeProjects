import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np


import city_country_csv_reader
from locations import create_example_countries_and_cities
from trip import Trip, create_example_trips


def axis_check(m, ax, long_min, lat_min, long_max, lat_max):
    """
    sets the longitude and latitudes to the map format
    sets the x_limit and y_limit of the map diagram
    """

    # converts minimum and maximum of latitude and longitude to map of m
    xmin, ymin = m(long_min, lat_min)
    xmax, ymax = m(long_max, lat_max)

    # sets the longitude and latitude limit of the map diagram
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])


def plot_trip(trip: Trip, projection = 'robin', line_width=3, colour='b') -> None:
    """
    Plots a trip on a map and writes it to a file.
    Ensures a size of at least 50 degrees in each direction.
    Ensures the cities are not on the edge of the map by padding by 5 degrees.
    The name of the file is map_city1_city2_city3_..._cityX.png.
    """

    lat_list = []
    long_list = []
    diff_long_list = []
    tip = "map_" + trip.city_list[0].name

    padding_val = 5 # set the padding value to 5

    # gets the list fo latitudes and longitudes of all cities
    for city in trip.city_list:
        lat_list.append(float(city.latitude))
        long_list.append(float(city.longitude))

    # gets the difference in longitude when travelling from a city to another and gets the maximum longitude difference
    for i in range(1, len(long_list)):
        diff = long_list[i] - long_list[i-1]
        if diff < 0:
            diff = diff*-1
        diff_long_list.append(diff)
    long_diff = max(diff_long_list)
    # print(diff_long_list)
    # print(long_diff)

    # gets the positive and negative longitudes in separate lists
    n__positive_diff_long_list = []
    n__negative_diff_long_list = []
    for i in long_list:
        if i > 0:
            n__positive_diff_long_list.append(i)
        else:
            n__negative_diff_long_list.append(i)

    # gets the minimum and maximum longitudes
    long_min = min(long_list)
    long_max = max(long_list)

    # if the maximum longitude difference is > 180 (shorter route possible that is < 180), find the shorter route's middle longitude
    if long_diff > 180:
        new_diff = min(n__positive_diff_long_list) - min(n__negative_diff_long_list)

        new_diff = 360 - new_diff
        mid_lon = long_min - new_diff / 2

    # if the maximum longitude difference is <= 180, find the middle longitude
    else:
        mid_lon = long_min + (long_max - long_min) / 2

    # sets fig to a figure/image to plot and sets ax to the axes to plot
    fig = plt.figure(figsize=(10, 9))
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    # m is set to Basemap of projection (eck4), lon_0 as the middle longitude and resolution as 'i'
    m = Basemap(projection=projection, lon_0=mid_lon, resolution='i')

    # draw the coastlines for the world map
    m.drawcoastlines()

    # plots the city name and marks with a 'o' symbol
    x, y = m(float(trip.city_list[0].longitude), float(trip.city_list[0].latitude))
    # plt.text(x, y, trip.city_list[0].name, fontsize=9, fontweight='semibold', bbox=dict(facecolor='w', alpha=0.3))
    plt.plot(x, y, 'bo', markersize=7, markerfacecolor='w')
    m.set_axes_limits()

    # plots the great circle for every pair of cities in city list
    for i in range(len(trip.city_list) - 1):

        # plots the city name and marks with a 'o' symbol
        x, y = m(float(trip.city_list[i + 1].longitude), float(trip.city_list[i + 1].latitude))
        # plt.text(x, y, trip.city_list[i + 1].name, fontsize=9, fontweight='semibold',bbox=dict(facecolor='w', alpha=0.3))
        plt.plot(x, y, 'bo', markersize=7, markerfacecolor='w')

        # plots the greatcircle distance on the map
        m.drawgreatcircle(float(trip.city_list[i].longitude), float(trip.city_list[i].latitude),
                          float(trip.city_list[i + 1].longitude), float(trip.city_list[i + 1].latitude),
                          linewidth=line_width, color=colour)

        # stores the name of all the cities in a string
        tip += "_" + trip.city_list[i + 1].name

    tip += ".png"

################################################## LATITUDE AXIS CHECK #################################################

    # gets the minimum latitude + padding value and maximum latitude + padding value and latitude difference
    lat_min = min(lat_list) - padding_val
    lat_max = max(lat_list) + padding_val
    lat_diff = max(lat_list) - min(lat_list)

    # if latitude difference is < 75
    if lat_diff < 80:

        # if longitude difference is between 150 and 210, change both latitude by 55
        if 150 <= long_diff <= 210:
            lat_min -= 55
            lat_max += 55

        elif lat_diff > 70:
            boundary = (115 - lat_diff) /2
            lat_min -= boundary
            lat_max += boundary

        # for all the other latitude difference make sure the boundary of each map is 75 degrees by adding half of the difference between 75 and lat_diff to lat_min and lat_max
        else:
            boundary = (75 - lat_diff) /2
            lat_min -= boundary
            lat_max += boundary
            # print(boundary, lat_min, lat_max)

        # if lat_max and lat_min exceeds the limit, reduce their limits to 85 or -85
        if lat_max >= 90:
            lat_max = 85
        if lat_min <= -90:
            lat_min = -85

################################################## LONGITUDE AXIS CHECK #################################################
    # sets the minimum and maximum longitude values
    long_min = min(long_list)
    long_max = max(long_list)

    # if the difference in longitude is  >180
    if long_diff >= 180:
        # find the difference between the smallest longitude in positive and negative side of the map
        long_min = min(n__negative_diff_long_list)
        long_max = min(n__positive_diff_long_list)
        new_diff = min(n__positive_diff_long_list) - min(n__negative_diff_long_list)

        # if the difference is >=180 as well, find the corresponding great circle difference(<180) and add boundaries (by setting the minimum boundary distance by 240) to the left and right
        if new_diff >= 180:
            new_diff = 360 - new_diff
            boundary = (240 - new_diff)
            long_min += boundary
            long_max -= boundary
            # sets the minimum and maximum latitude and adds the padding value
            long_min = long_min - padding_val
            long_max = long_max + padding_val
            # sets the axis of the map
            axis_check(m, ax, long_max, lat_min, long_min, lat_max)
        else:
            # converts the latitude and longitude to map diagram
            xmin, ymin = m(long_min, lat_min)
            xmax, ymax = m(long_max, lat_max)
            # sets the longitude and latitude limit of the map diagram
            ax.set_ylim([ymin, ymax])

    else:
        # if the longitude difference is less than 50, set the maximum boundary to 90 and add the boundaries to set the axis
        if long_diff < 50:
            boundary = (90 - long_diff) / 2
            long_min -= boundary
            long_max += boundary
        # if the longitude difference is less than 100, set the maximum boundary to 150 and add the boundaries to set the axis
        elif long_diff < 100:
            boundary = (150 - long_diff) / 2
            long_min -= boundary
            long_max += boundary
        # if the longitude difference is less than 150, set the maximum boundary to 260 and add the boundaries to set the axis
        elif long_diff < 150:
            boundary = (260 - long_diff) / 2
            long_min -= boundary
            long_max += boundary
        # if the longitude difference is more than 150 and less than 180, set the maximum boundary to 310 and add the boundaries to set the axis
        else:
            boundary = (310 - long_diff) /2
            long_min -= boundary
            long_max += boundary

        # sets the minimum and maximum longitude and adds the padding value
        long_min = long_min - padding_val
        long_max = long_max + padding_val

        # sets the axis of the map
        axis_check(m, ax, long_min, lat_min, long_max, lat_max)

############################################## MAP MODIFICATION & PLOTTING ##############################################
    # adds the latitude adn longitude lines in the map
    parallels = np.arange(-90, 90, 30.)
    m.drawparallels(parallels)
    meridians = np.arange(-180, 180, 30.)
    m.drawmeridians(meridians)

    # sets the title of the map diagram as tip
    ax.set_title(tip)

    # adds colour to lands and lakes on the map
    m.fillcontinents(color='coral', lake_color='aqua')
    m.drawmapboundary(fill_color='aqua')

    # save the figure of the map diagram with the name tip
    plt.savefig(tip)

    # plot and show the diagram
    plt.show()


if __name__ == "__main__":
    city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")

    create_example_countries_and_cities()

    trips = create_example_trips()

    for i in trips:
        print(i)
        plot_trip(i)
