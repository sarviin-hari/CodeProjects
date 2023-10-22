"""
Group name: Myvi Rangers
Authors: Sarviin a/l Hari, Tharani a/p Prathaban, Wong Jun Wei, Gareth Xin Yoong Lim
"""

import time
import random

def display_rules():
  print("""
  _____________________________________________________________________________
  Twenty One is a game of chance where players take turns rolling two dice every 
  round until they decide to stop rolling and lock in their score or end up 
  going bust with a total over 21. The objective is to be the closest to 21 
  when everyone is done rolling.

  Rules are as per follows:
    - Players begin with a score of 0.
    - Each player has one turn to either roll or stop rolling each round.
    - Players can only do a regular roll of two dice until they 
      reach a score of at least 14.
    - Players with a score >= 14 have the option to only roll one dice.
    - If a player scores more than 21 they go bust and are out of the game.
    - The winning player is the one with the score closest to 21 when everyone 
      has finished rolling.
    - If all players go bust, no one wins.
    - If more than one player has the winning score, no one wins.
  _____________________________________________________________________________
  """)
  input("Press enter to go back")
  return

def display_main_menu():
    print("------------Main Menu------------")
    print("Welcome to Twenty One!")
    print("1. Solo")
    print("2. Local Multiplayer")
    print("3. Rules")
    print("4. Exit")
    print("---------------------------------")

def int_input(prompt="", restricted_to=None):
  """
  Helper function that modifies the regular input method,
  and keeps asking for input until a valid one is entered. Input
  can also be restricted to a set of integers.

  Arguments:
    - prompt: String representing the message to display for input
    - restricted: List of integers for when the input must be restricted
                  to a certain set of numbers

  Returns the input in integer type.
  """
  while True:
    player_input = input(prompt)
    try:
      int_player_input = int(player_input)
    except ValueError:
      continue
    if restricted_to is None:
      break
    elif int_player_input in restricted_to:
      break

  return int_player_input

def cpu_player_choice(score):
  """
  This function simply returns a choice for the CPU player based
  on their score.

  Arguments:
    - score: Int

  Returns an int representing a choice from 1, 2 or 3.
  """
  time.sleep(2)
  if score < 14:
    return 1
  elif score < 17:
    return 3
  else:
    return 2

def display_game_options(player):
    """
    Prints the game options depending on if a player's score is
    >= 14.

    Arguments:
      - player: A player dictionary object
    """

    print("------------" + player['name'] + "'s turn------------")  # prints the specific player's name
    print(player['name'] + "'s score: " + str(player['score']))  # prints the player's name and score
    print("1. Roll")  # displays option 1 (Roll)
    print("2. Stay")  # displays option 2 (Stay)

    if player['score'] >= 14:  # displays option 3 (Roll One) if score is more than or equal to 14
        print("3. Roll One")

def display_round_stats(round, players): # accepts parameters round (the round that the game is in) and players (player dictionary of all players in the game)
    """
    Print the round statistics provided a list of players.

    Arguments:
      - round: Integer for round number
      - players: A list of player-dictionary objects
    """

    print("-----------Round " + str(round) + "-----------")  # print the round that the game is in

    for i in range (len(players)):  # prints the player name and score for each player in the dictionary
        print(players[i]['name'] + " is at " + str(players[i]['score']))

def roll_dice(num_of_dice=1): # accepts the number of dice rolls, default value is 1
    """
    Rolls dice based on num_of_dice passed as an argument.

    Arguments:
      - num_of_dice: Integer for amount of dice to roll

    Returns the following tuple: (rolls, display_string)
      - rolls: A list of each roll result as an int
      - display_string: A string combining the dice art for all rolls into one string
    """

    die_art = {
        1: ["┌─────────┐", "│         │", "│    ●    │", "│         │", "└─────────┘"],
        2: ["┌─────────┐", "│  ●      │", "│         │", "│      ●  │", "└─────────┘"],
        3: ["┌─────────┐", "│  ●      │", "│    ●    │", "│      ●  │", "└─────────┘"],
        4: ["┌─────────┐", "│  ●   ●  │", "│         │", "│  ●   ●  │", "└─────────┘"],
        5: ["┌─────────┐", "│  ●   ●  │", "│    ●    │", "│  ●   ●  │", "└─────────┘"],
        6: ["┌─────────┐", "│  ●   ●  │", "│  ●   ●  │", "│  ●   ●  │", "└─────────┘"]
    }

    roll_list = []  # stores the value of roll from dice of each round in a list
    die_face_list = [""] * 5  # stores the text-image of dice for of each round in a list of 5 index
    diagram = ""  # store the combined text-image as a string separated by \n (prints the next strings in a new line)

    for i in range(num_of_dice):  # loop i number of times to get the roll dice value and its corresponding text-image
        dice_number = random.randint(1, 6)
        roll_list.append(dice_number)  # for every loop it inserts the value of the rolled dice in the list

        for j in range(5):  # for every dice value, the corresponding text_line will be added to their corresponding indexes in the die_face_list
            die_face_list[j] += die_art[dice_number][j]

    for i in range (5):  # loops five times to convert the strings in the lists into a string where each of the indexes are separated by \n (makes the following strings in a new line when printed)
        diagram += die_face_list[i] + "\n"

    result_list = (roll_list, diagram)  # store results in a tuple that has the dice roll list and the corresponding text-image

    return result_list  # returns the result_list

def execute_turn(player, player_input):
    """
    Executes one turn of the round for a given player.

    Arguments:
      - player: A player dictionary object

    Returns an updated player dictionary object.
    """

    if player_input == 1:  # if the player input is 1, it prints rolling both, calls roll_dice(2) function, print the text-image, sum the result and print the player name and score
        print("Rolling both...")
        result = roll_dice(2)
        print(result[1])
        player['score'] += sum(result[0])
        print(player['name'] + " is now on " + str(player['score']))
    elif player_input == 2:  # if player input is 2, it prints player stayed with the score and 'stayed' in dictionary is set to True
        print(player['name'] + " has stayed with a score of " + str(player['score']))
        player['stayed'] = True
    elif player_input == 3:  # if the player input is 3, it prints rolling one, calls roll_dice(1) function, print the text-image, sum the result and print the player name and score
        print("Rolling one...")
        result = roll_dice(1)
        print(result[1])  # print the text-image of dice
        player['score'] += sum(result[0])  # sum the roll dice value
        print(player['name'] + " is now on " + str(player['score']))  # print player name and score

    if player['score'] > 21:  # if player score more than 21, at_14 and bust is set to True
        player['at_14'] = True
        player['bust'] = True
        print(player['name'] + " goes bust!")
    elif player['score'] >= 14:  # elif player score is more than or equal to 14, only at_14 is set to True
        player['at_14'] = True

    return player  # returns the updated player dictionary

def end_of_game(players):
    """
    Takes the list of all players and determines if the game has finished,
    returning false if not else printing the result before returning true.

    Arguments:
      - players: A list of player-dictionary objects

    Returns True if round has ended or False if not. If true results are
    printed before return.
    """

    bust_list = []  # set a bust list to store the boolean value of bust from each player dictionary
    score_list = []  # stores the tuple of each player name and score for those who have not gone busted and stayed

    for i in range(len(players)):  # store bust value of all players from the dictionary into the bust list
        bust_list.append(players[i]['bust'])
    if False not in bust_list:  # if all data values in bust list is True, print everyone goes bust and return True (Game ends)
        print("Everyone's gone bust! No one wins :(")
        return True

    for player_set in players:  # loop through each player dictionary
        if player_set['stayed'] == False and player_set['bust'] == False:  # if stayed and bust is False return False (Game still continues)
            return False
        elif player_set['stayed'] != player_set['bust'] and player_set['score'] <= 21:  # if stayed and bust is both not True or False and score is less than or equal to 21, store tuple of player name and score in score list
            score_list.append((player_set['name'], player_set['score']))

    top_score_list = score_list[0]  # retrieves first player name and score
    high_score = score_list[0][1]  # retrieves first player score

    for i in range (1, len(score_list)):  # loop starts from index 1 to the total length of score list
        if score_list[i][1] > high_score:  # if the score in score list higher than the original highscore, high_score and top_score_list is updated to the current value
            high_score = score_list[i][1]
            top_score_list = score_list[i]

    counter = 0  # counter is used to find the number of players with max score
    for player_score in score_list:  # for loop to identify the number of times the high score is repeated from the score list
        if player_score[1] == high_score:
            counter += 1

    if counter > 1:  # if the high score is repeated more than once (many same highscore values) the game is a draw is printed and return True (Game ends)
        print("The game is a draw! No one wins :(")
        return True

    print(top_score_list[0] + " is the winner!")  # prints the player as the winner as he is the only one with highscore and return True (Game ends)
    return True

def solo_game():
    """
    This function defines a game loop for a solo game of Twenty One against
    AI.
    """

    player = {'name': 'Player 1', 'score': 0, 'stayed': False, 'at_14': False, 'bust': False}  # player's dictionary
    cpu_player = {'name': 'CPU Player', 'score': 0, 'stayed': False, 'at_14': False, 'bust': False}  # CPU palyer's dictionary
    player_list = [player, cpu_player]  # player dictionary and CPU dictionary are stored in a list

    round_number = 0  # sets round number to 0
    boolean = False  # boolean is set to False

    while boolean == False:  # loop continues until the boolean value is not equal to False
        display_round_stats(round_number, player_list)  # displays the round number and score of the players

        if player['stayed'] == False and player['bust'] == False:  # if function runs if player stayed and bust is False
            display_game_options(player)  # displays the game options for player
            if player['score'] < 14:  # prompts user to enter an option of either 1 or 2 only
                player_input = int_input(prompt="Please enter an option: ", restricted_to=[1,2])
            else:   # prompts user to enter an option of either 1 or 2 or 3 only
                player_input = int_input(prompt="Please enter an option: ", restricted_to=[1,2,3])
            player = execute_turn(player, player_input)

        if cpu_player['stayed'] == False and cpu_player['bust'] == False:
            display_game_options(cpu_player)  # displays the game options for cpu_player
            player_input = cpu_player_choice(cpu_player['score'])  # player input is randomly chosen intelligently based on the function cpu_player_choice()
            cpu_player = execute_turn(cpu_player, player_input)  # executes cpu_player's turn based on the option chosen, prints text-image of dice and score (option 1 or 3) but prints the player has stayed (option 2)

        player_list = [player, cpu_player]  # player dictionary and CPU dictionary are updated
        boolean = end_of_game(player_list)  # returns True or False if the game is over or not respectively and stores the value in boolean

        round_number += 1  # round_number is increased by 1 each time the loop is executed

def multiplayer_game(num_of_players):
    """
    This function defines a game loop for a local multiplayer game of Twenty One,
    where each iteration of the while loop is a round within the game.
    """
    multiplayer_list = []  # list to append the dictionary for each player based on the num_of_players

    for i in range (num_of_players):  # loop to create individual player dictionary for each player, set the name of player as (player + number) and store it in the multiplayer_list
        dictionary = {'name': 'Player', 'score': 0, 'stayed': False, 'at_14': False, 'bust': False}
        dictionary['name'] = "Player " + str(i+1)
        multiplayer_list.append(dictionary)

    round_counter = 0  # round_counter set to 0 and increased by 1 for each while loop to indicate the round number
    boolean = False  # original boolean value is set to False

    while boolean == False:  # while loop continues as long as the boolean value is False
        display_round_stats(round_counter, multiplayer_list)  # displays the round number and score of the players
        for i in range(len(multiplayer_list)):  # loops for each player in the dictionary for the respective round
            if multiplayer_list[i]['stayed'] == False and multiplayer_list[i]['bust'] == False:  # if both stayed and bust is false (not possible to have both as true), if function runs
                display_game_options(multiplayer_list[i])  # displays the game options for players
                if multiplayer_list[i]['score'] < 14:
                    player_input = int_input(prompt="Please enter an option: ", restricted_to=[1, 2])
                else:
                    player_input = int_input(prompt="Please enter an option: ", restricted_to=[1, 2, 3])
                execute_turn(multiplayer_list[i], player_input)  # executes the player's turn based on the option chosen, prints text-image of dice and score (option 1 and 3) but prints the player has stayed (option 2)

        boolean = end_of_game(multiplayer_list)  # returns True or False if the game is over or not respectively and stores the value in boolean
        round_counter += 1  # increase round_counter by 1 for each loop

def main():
    """
    Defines the main loop that allows the player to start a game, view rules or quit.
    """

    display_main_menu()  # displays the main menu
    player_input = int_input(prompt="Choose your option: ", restricted_to=[1,2,3,4])  # prompts user to enter an option

    while player_input != 4:  # the loops run until option 4 is entered
        if player_input == 1:  # if option 1 selected, solo game function runs and after the game ends returns to the main menu
            solo_game()
            print("")

        elif player_input == 2:  # if option 2 selected, it prompts user to enter an option, multiplayer_game function runs and after the game ends returns to the main menu
            num_of_players = int_input(prompt="Please enter number of players: ", restricted_to=None)  # prompts user to enter number of players
            while num_of_players == 1:  # while number of players is equal to 1, it loops again and again to prompt user to enter an option until a number != 1 is entered
                num_of_players = int_input(prompt="Please enter number of players: ", restricted_to=None)
            multiplayer_game(num_of_players)
            print("")

        elif player_input == 3:  # if option 3 selected, it displays the rules and returns to the main menu once enter is clicked
            display_rules()
            print("")

        display_main_menu()  # displays the main menu
        player_input = int_input(prompt="Choose your option: ", restricted_to=[1, 2, 3, 4])  # prompts user to enter an option

    print("\nYou exited the game.")  # print and exits the game when option 4 is entered

main()  # call the main function to run the game