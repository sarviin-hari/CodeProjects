import math
from tqdm import tqdm
import time

from locations import City, Country

import city_country_csv_reader

from vehicles import CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley

from trip import Trip

import path_finding
from path_finding import find_shortest_path

from map_plotting import plot_trip

city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")  # calls the create_cities_countries_from_CSV function to create CIties and Countries from csv file


########################################## Vehicle selection #################################################################################

def vehicle_option():
    """
    This function acts as a validation for the input entered for vehicle option in the game.
    Checks if the type and range of input entered matches the requirement and runs on loop until its met.

    Return: Only a valid integer input.
    """

    # while loops again and again until a valid number is entered
    while True:
        # prints vehicle options and asks for input
        print("Please enter an integer for the vehicle option: \n1. Example Vehicle Fleet\n2. Custom Parameter Vehicle")
        vehc_opt = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            vehc_opt = int(vehc_opt)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # check if vehicle option is within the given range of 1 and 2
        if vehc_opt >= 1 and vehc_opt <= 2:
            break
        else:
            print('Valid number, please')

    return vehc_opt


def vehicle_choice_1():
    """
    This function acts as a validation for the input entered for vehicle choice for the first.
    Checks if the type and range of input entered matches the requirement and runs on loop until its met.

    Return: Only a valid integer input.
    """
    # while loops again and again until a valid number is entered
    while True:
        # prints vehicle options and asks for input
        print(
            "Please enter your vehicle choice: \n1. [CrappyCrepeCar(200), DiplomacyDonutDinghy(100, 500), TeleportingTarteTrolley(3, 2000)])\n2. [CrappyCrepeCar(150), DiplomacyDonutDinghy(75, 350), TeleportingTarteTrolley(5, 1000)]\n3. [CrappyCrepeCar(300), DiplomacyDonutDinghy(125, 450), TeleportingTarteTrolley(2, 6000)]")
        choice = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            choice = int(choice)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # check if vehicle option is within the given range of 1 and 3
        if choice >= 1 and choice <= 3:
            break
        else:
            print('Valid number, please')

    return choice


def vehicle_choice_2():
    """
    This function acts as a validation for the input entered for vehicle choice for the second.
    Checks if the type and range of input entered matches the requirement and runs on loop until its met.

    Return: Only a valid integer input.
    """
    # while loops again and again until a valid number is entered
    while True:
        # prints vehicle options and asks for input
        print("Please enter type of vehicle: \n1. CrappyCrepeCar\n2. DiplomacyDonutDinghy\n3. TeleportingTarteTrolley")
        choice = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            choice = int(choice)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # check if vehicle option is within the given range of 1 and 3
        if choice >= 1 and choice <= 3:
            break
        else:
            print('Valid number, please')

    return choice


def parameter_check(val_name):
    """
    This function acts as a validation for the input entered for parameter of a vehicle choice.
    Checks if the type and range of input entered matches the requirement and runs on loop until its met.

    Parameter: the value name that is the parameter for the vehicle

    Return: Only a valid integer input.
    """
    # while loops again and again until a valid number is entered
    while True:
        # asks for input for the parameters
        print("Please enter a value for " + val_name + ": ")
        choice = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            choice = int(choice)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # check if choice value is more than equals to 0
        if choice >= 0:
            break
        else:
            print('Valid number, please')

    return choice


def loop_check():
    """
    This function acts as a validation for the loop_check to check if to add vehicles or not in the vehicle_fleet.
    Checks if the type and range of input entered matches the requirement and runs on loop until its met.

    Return: Only a valid integer input.
    """
    # while loops again and again until a valid number is entered
    while True:
        # asks for input for 1 or 2 to add or not vehicles
        print("Please enter '1' to continue adding vehicles or '0' to stop adding vehicles")
        loop = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            loop = int(loop)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # check if choice value is more than equals to 0
        if loop >= 0 and loop <= 1:
            return loop
        else:
            print('Valid number, please')


vehicle_fleet = []  # empty vehicle list
boolean = False  # boolean is set to false
opt = vehicle_option()  # calls the vehicle option function to choose example vehicle or custom parameter vehicle
print()

# if option is 1, then call the vehicle_choice_1 function for the option value and choose the correct option and store in vehicle_fleet
if opt == 1:
    choice = vehicle_choice_1()
    if choice == 1:
        vehicle_fleet = [CrappyCrepeCar(200), DiplomacyDonutDinghy(100, 500), TeleportingTarteTrolley(3, 2000)]
    elif choice == 2:
        vehicle_fleet = [CrappyCrepeCar(150), DiplomacyDonutDinghy(75, 350), TeleportingTarteTrolley(5, 1000)]
    else:
        vehicle_fleet = [CrappyCrepeCar(300), DiplomacyDonutDinghy(125, 450), TeleportingTarteTrolley(2, 6000)]

else:

    # if custom parameter the while loop runs as long as boolean is false
    while not boolean:
        # choose the type of vehicle to choose
        choice = vehicle_choice_2()
        # gets the parameter for that vehicle, and create the vehicle
        if choice == 1:
            speed = parameter_check("speed")
            trip = CrappyCrepeCar(speed)
        elif choice == 2:
            count_speed = parameter_check("country speed")
            prim_speed = parameter_check("primary speed")
            trip = DiplomacyDonutDinghy(count_speed, prim_speed)
        else:
            speed = parameter_check("time")
            distance = parameter_check("distance")
            trip = TeleportingTarteTrolley(speed, distance)
        # stores the vehicle in vehicle_fleet
        vehicle_fleet.append(trip)
        # calls the loop_check() function to ask if to add more vehicles or not, if 0 then set boolean to true to stop the loop
        if int(loop_check()) == 0:
            boolean = True
print()


########################################## Trip selection & Progress Bar ######################################################################

def trip_option():
    """
    This function acts as a validation for the input entered for trip option.
    Checks if the type and range of input entered matches the requirement and runs on loop until its met.

    Return: Only a valid integer input.
    """
    # while loops again and again until a valid number is entered
    while True:
        # prints trip options and asks for input
        print(
            "Please enter an integer for the trip options: \n1. Example Trips\n2. Manually Add Cities\n3. Shortest Path Between Two Cities")
        trip_opt = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            trip_opt = int(trip_opt)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # check if trip option is within the given range of 1 and 3
        if trip_opt >= 1 and trip_opt <= 3:
            break
        else:
            print('Valid number, please')

    return trip_opt


def trip_choice_1():
    """
    This function acts as a validation for the input entered for trip_choice_1.
    Checks if the type and range of input entered matches the requirement and runs on loop until its met.

    Return: Only a valid integer input.
    """
    # while loops again and again until a valid number is entered
    while True:
        # prints trip options and asks for input
        print("Please enter the trip of your choice: ")
        choice = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            choice = int(choice)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # check if trip option is within the given range of 1 and length of trip (by calling the new_trip function)
        if choice <= len(new_trips()) and choice >= 1:
            break
        else:
            print('Valid number, please')

    return choice


def trip_choice_2():
    """
     This function acts as a validation for the input entered for trip_choice_2.
     Checks if the type and range of input entered matches the requirement and runs on loop until its met.

     Return: Only a valid integer input.
     """
    # while loops again and again until a valid number is entered
    while True:
        # prints trip options and asks for input
        print("Please enter city id of choice (ex: XXXXXXXXXX): ")
        choice = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            choice = int(choice)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # checks using for loop if the city_id is in the City.cities list. If it is then return the city object of the corresponding city
        for city in City.cities:
            if str(choice) == city:
                new_city = City.cities[city]
                return new_city
        # if not print invalid city and loops again
        print("Invalid City")


def new_trips() -> list[Trip]:
    """
    Creates examples of trips.
    """

    australia = Country.countries["Australia"]
    melbourne = australia.get_city("Melbourne")
    sydney = australia.get_city("Sydney")
    canberra = australia.get_city("Canberra")
    japan = Country.countries["Japan"]
    tokyo = japan.get_city("Tokyo")

    canada = Country.countries['Canada']
    montreal = canada.get_city("Montreal")

    brazil = Country.countries['Brazil']
    goiania = brazil.get_city("Goiania")

    united_states = Country.countries['United States']
    new_york = united_states.get_city("New York")

    russia = Country.countries['Russia']
    kazan = russia.get_city("Kazan")

    india = Country.countries['India']
    mumbai = india.get_city("Mumbai")
    allahabad = india.get_city("Allahabad")

    singapore = Country.countries['Singapore']
    singapore_city = singapore.get_city("Singapore")

    china = Country.countries['China']
    jieyang = china.get_city("Jieyang")

    trips = []

    for cities in [(sydney, goiania), (mumbai, kazan), (jieyang, allahabad, singapore_city), (melbourne, canberra, tokyo), (sydney, new_york), (melbourne, canberra), (melbourne, montreal)]:
        trip = Trip(cities[0])
        for city in cities[1:]:
            trip.add_next_city(city)

        trips.append(trip)

    return trips


def num_of_cities():
    """
    This function acts as a validation for the input entered for num_of_cities of choice.
    Checks if the type and range of input entered matches the requirement and runs on loop until its met.

    Return: Only a valid integer input.
    """
    # while loops again and again until a valid number is entered
    while True:
        # prints trip options and asks for input
        print("Please enter the number of cities to add: ")
        num = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            num = int(num)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # check if num_of_cities is more than 2
        if num >= 2:
            break
        else:
            print('Invalid number. Please enter a valid number (>=2)')
    return num


def shortest_path_trip(max_num):
    """
    This function acts as a validation for the input entered for parameter of a shortest_path_trip choice.
    Checks if the type and range of input entered matches the requirement and runs on loop until its met.

    Parameter: the value name that is the parameter for the vehicle

    Return: Only a valid integer input.
    """
    # while loops again and again until a valid number is entered
    while True:
        # prints trip options and asks for input
        print("Please enter which shortest path you would like to choose: ")
        num = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            num = int(num)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # check if num is within the given range of 1 and teh max_num
        if num <= max_num and num >= 1:
            break
        else:
            print('Valid number, please')
    return num


def progress_bar(best_trip, best_vehicle, cities, time_list, best_trip_time):
    # calls the plot_trip function with trip as its parameter and plots the map
    print()
    print("Please wait a few moments for the program to compute the map\n")
    plot_trip(best_trip)
    # prints the journey path, time, best vehicle
    print("~~> Journey Path: " + str(best_trip) + f"\n~~> Journey Time: {best_trip_time} \n~~> Journey Vehicle: {best_vehicle}\n")
    # prints progress bar
    print("<<<<<<<<<<<<<<<< Progress Bar >>>>>>>>>>>>>>>>> ")
    # for loop runs for every pairs of cities
    for k in range(1, len(cities)):
        # loops through the progress bar for 0.1 seconds per hour from 0% to 100%
        for _ in tqdm(range(0, time_list[k - 1]), desc="Travelling from " + str(cities[k - 1]) + " to " + str(cities[k])):
            time.sleep(0.1)


def trip_vehicle(num_of_vehc):
    """
     This function acts as a validation for the input entered for trip_choice_2.
     Checks if the type and range of input entered matches the requirement and runs on loop until its met.

     Return: Only a valid integer input.
     """
    # while loops again and again until a valid number is entered
    while True:
        # prints trip options and asks for input
        print("Please enter the vehicle of your choice: ")
        choice = input("--> ")
        # try to cast input to an integer, if not possible then loop again
        try:
            choice = int(choice)
        except ValueError:
            print('Please enter a numeric value!')
            continue
        # check if trip option is within the given range of 1 and 3
        if choice >= 1 and choice <= num_of_vehc:
            break
        else:
            print('Valid number, please')

    return choice


trip_list = []  # creates an initial trip_list
opt = trip_option()  # calls the trip option function to choose example trip or manually add city or shortest path

# if the option is 1
if opt == 1:
    print("Available trips are as below: ")
    i = 1
    # call the new_trips function to print all the trips available
    for trip in new_trips():
        print("    " + str(i) + ") " + str(trip))
        i += 1

    choice = trip_choice_1()  # call the trip_choice_1 function to get the trip of choice
    trip = new_trips()[choice - 1]  # set trips to the trip of choice
    trip_list.append(trip)  # store the trip in trip_list

    print("\nVehicle choice are as below: ")
    i = 1
    for vehc in vehicle_fleet:
        print("    " + str(i) + ") " + str(vehc))
        i += 1
    print("    " + str(i) + ") " + "Fastest Vehicle")

    index = trip_vehicle(len(vehicle_fleet) + 1)  # gets the vehicle of user's choice

    if index == len(vehicle_fleet) + 1:
        best_trip = trip  # best_trip is stored as trip
        best_vehc_time = trip.find_fastest_vehicle(vehicle_fleet)  # get the best vehicle time by finding the fastest vehicle of vehicle flee
        best_vehicle = best_vehc_time[0]  # get the best vehicle and best trip time from best_vehc_time which has  a return value of (Vehicle, Total Time)
        best_trip_time = best_vehc_time[1]
        cities = trip.city_list  # store the cities of the trip in cities


        if best_trip_time == math.inf or best_trip == None:
            print("The travel is not possible... Re-run the program to try again")  # if no trip available then print error message
        else:
            index = vehicle_fleet.index(best_vehicle)  # get the index based on the vehicle of choice
            time_list = best_trip.every_time_list[index]  # get the corresponding time based on the vehicle
            progress_bar(best_trip, best_vehicle, cities, time_list, best_trip_time)  # call progress bar function to output the progress bar

    else:
        best_trip = trip                                        # best_trip is stored as trip
        best_vehicle = vehicle_fleet[index-1]                   # get the best vehicle based on the index from vehicle fleet
        best_trip_time = trip.total_travel_time(best_vehicle)   # compute the best travel time by calling the total_travel_time function from the trip class
        cities = trip.city_list                                 # get the cities list from the trip class instance variable
        time_list = trip.every_time_list[0]                     # gets the time_list between two cities

        if best_trip_time == math.inf:
            print("The travel is not possible... Re-run the program to try again")
        else:
            progress_bar(best_trip, best_vehicle, cities, time_list, best_trip_time)  # call progress bar function to output the progress bar


elif opt == 2:
    loop_num = num_of_cities()      # call num_of_cities() function to get the number of cities
    choice = trip_choice_2()        # call the trip choice to add the first city id
    trip = Trip(choice)             # create a trip from Trip class

    # for every other cities in the trip, add the city to the trip and store the trip in trip_list
    for i in range(1, loop_num):
        choice = trip_choice_2()
        trip.add_next_city(choice)
    trip_list.append(trip)

    print("\nVehicle choice are as below: ")
    i = 1
    for vehc in vehicle_fleet:
        print("    " + str(i) + ") " + str(vehc))
        i += 1
    print("    " + str(i) + ") " + "Fastest Vehicle")

    index = trip_vehicle(len(vehicle_fleet) + 1)  # gets the vehicle of user's choice

    if index == len(vehicle_fleet) + 1:
        best_trip = trip  # best_trip is stored as trip
        best_vehc_time = trip.find_fastest_vehicle(vehicle_fleet)  # get the best vehicle time by finding the fastest vehicle of vehicle flee
        best_vehicle = best_vehc_time[0]  # get the best vehicle and best trip time from best_vehc_time which has  a return value of (Vehicle, Total Time)
        best_trip_time = best_vehc_time[1]
        cities = trip.city_list  # store the cities of the trip in cities


        if best_trip_time == math.inf or best_trip == None:
            print("The travel is not possible... Re-run the program to try again")  # if no trip available then print error message
        else:
            index = vehicle_fleet.index(best_vehicle)  # get the index based on the vehicle of choice
            time_list = best_trip.every_time_list[index]  # get the corresponding time based on the vehicle
            progress_bar(best_trip, best_vehicle, cities, time_list, best_trip_time)  # call progress bar function to output the progress bar

    else:
        best_trip = trip                                        # best_trip is stored as trip
        best_vehicle = vehicle_fleet[index-1]                   # get the best vehicle based on the index from vehicle fleet
        best_trip_time = trip.total_travel_time(best_vehicle)   # compute the best travel time by calling the total_travel_time function from the trip class
        cities = trip.city_list                                 # get the cities list from the trip class instance variable
        time_list = trip.every_time_list[0]                     # gets the time_list between two cities

        if best_trip_time == math.inf:
            print("The travel is not possible... Re-run the program to try again")
        else:
            progress_bar(best_trip, best_vehicle, cities, time_list, best_trip_time)  # call progress bar function to output the progress bar



else:
    travel_time_list = []
    city1 = trip_choice_2()  # gets the first city of choice
    city2 = trip_choice_2()  # gets the second city of choice

    print("\nPlease wait a few moments for the program to compute the shortest path\n")

    # for every vehicle in the vehicle list, compute the shortest path trip, store the trip in trip_list and get prints the shortest path, path, vehc type and time
    i = 1
    for vehc in vehicle_fleet:
        trip = find_shortest_path(vehc, city1, city2)
        trip_list.append(trip)
        print("Shortest Path " + str(i))
        print("~~> Path: " + str(trip))
        if path_finding.valid_time_list[i - 1] == math.inf:
            travel_time_list.append(math.inf)
        else:
            travel_time_list.append(sum(path_finding.valid_time_list[i - 1]))
        i += 1
    print("")

    number = shortest_path_trip(len(vehicle_fleet))  # calls the shortest_path_trip function to get the user choice short path

    best_trip = trip_list[number - 1]

    print("\nVehicle choice are as below: ")
    i = 1
    for vehc in vehicle_fleet:
        print("    " + str(i) + ") " + str(vehc))
        i += 1
    print("    " + str(i) + ") " + "Fastest Vehicle")

    index = trip_vehicle(len(vehicle_fleet) + 1)  # gets the vehicle of user's choice

    if index == len(vehicle_fleet) + 1:
        best_trip = trip_list[number - 1]  # best_trip is stored as trip
        if best_trip == None:
            print("The travel is not possible... Re-run the program to try again")  # if no trip available then print error message

        else:
            best_vehc_time = best_trip.find_fastest_vehicle(vehicle_fleet)  # get the best vehicle time by finding the fastest vehicle of vehicle flee
            best_vehicle = best_vehc_time[0]  # get the best vehicle and best trip time from best_vehc_time which has  a return value of (Vehicle, Total Time)
            best_trip_time = best_vehc_time[1]
            cities = best_trip.city_list  # store the cities of the trip in cities

            if best_trip_time == math.inf:
                print("The travel is not possible... Re-run the program to try again")  # if no trip available then print error message
            else:
                index = vehicle_fleet.index(best_vehicle)  # get the index based on the vehicle of choice
                time_list = best_trip.every_time_list[index]  # get the corresponding time based on the vehicle
                progress_bar(best_trip, best_vehicle, cities, time_list, best_trip_time)  # call progress bar function to output the progress bar

    else:
        best_trip = trip_list[number - 1]                                        # best_trip is stored as trip
        if best_trip == None:
            print("The travel is not possible... Re-run the program to try again")  # if no trip available then print error message
        else:
            best_vehicle = vehicle_fleet[index-1]                   # get the best vehicle based on the index from vehicle fleet
            best_trip_time = best_trip.total_travel_time(best_vehicle)   # compute the best travel time by calling the total_travel_time function from the trip class
            cities = best_trip.city_list                                 # get the cities list from the trip class instance variable
            time_list = best_trip.every_time_list[0]                     # gets the time_list between two cities

            if best_trip_time == math.inf:
                print("The travel is not possible... Re-run the program to try again")
            else:
                progress_bar(best_trip, best_vehicle, cities, time_list, best_trip_time)  # call progress bar function to output the progress bar

