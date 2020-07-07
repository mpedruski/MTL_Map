import random
import logging

from MTL_data import *

logging.basicConfig(level=logging.CRITICAL,format='%(asctime)s - %(levelname)s - %(message)s')

### Input sanitization functions

def yes_no_input(initial_message):
    '''
    -> str
    Prints out an initial message that requires a Y or N answer, and
    verifies that the user's input is one of those two options, returning
    the answer'''
    answer = input(initial_message).upper()
    print("")
    while answer not in {"Y","N"}:
        print("Oops, looks like you made a typo.")
        answer = input(initial_message).upper()
        print("")
    return answer

def choice_sanitization(option_set):
    '''{set} -> int
    Accepts a set of options, and returns an integer within the range 0,
    len(set) - 1. Prompts the user to try again if they make illegal input.
    '''
    valid_choices = [str(i) for i in range(len(option_set))]
    choice = input()
    while choice not in valid_choices:
        print('''Oops, looks like you made an error. Choose one of the numbers
        available to you.''')
        choice = input()
    return int(choice)

### Initiation of program and tours

def initiate_program():
    '''Greets user and initiates one of the two walking tours following the
    user's choice.'''

    print("Welcome to Michael's walking tour of Montréal")
    print("Please choose the kind of tour you would like to be on:")
    print("1) A spatial walking tour")
    print("2) An emotional walking tour")
    print("3) A temporal walking tour")

    print("\n Please enter your choice as an integer:\n")

    choice = input()
    while choice not in ("1", "2", "3"):
        print("Oops, try again")
        choice = input()
    choice = int(choice)

    return choice

### Common functions
def give_user_options(options):
    '''Prints options for movement for user and returns length of options list
    for input verification'''
    print("Where do you want to go now?")
    for i in options:
        print(i)
    return len(options)

### Spatial walking tour functions

def initiate_walking_tour(locations):
    '''Given the list of locations on the walking tour, offer the user the choice
    of the neighbourhood to start in, and then start the tour at the first
    location in that neighbourhood (in terms of location in the array).
    Returns the index of this first tour location.'''
    ### List of unique neighbourhoods for user to choose from
    quartiers = list({i.quartier for i in locations})
    print("What neighbourhood would you like to start in? Your options are: \n")
    for i in range(len(quartiers)):
        print("{}) {}".format(i, quartiers[i]))
    ### Input sanitization
    valid_choices = [str(i) for i in range(len(quartiers))]
    choice = input()
    while choice not in valid_choices:
        print('''Oops, looks like you made an error. Choose one of the numbers
        available to you.''')
        choice = input()
    ### Return index of first location in locations to satistfy neighbourhood
    choice = quartiers[int(choice)]
    for i in range(len(locations)):
        if locations[i].quartier == choice:
            return i

def dist_matrix(locations, metric):
    '''Returns a matrix of distances between locations depending on the metric
    chosen. Currently returns values for distance in latitude and distance
    in longitude'''
    arr = []
    for i in locations:
        sub_arr = []
        for j in locations:
            if metric == "lat":
                sub_arr.append(i.lat - j.lat)
            elif metric == "long":
                sub_arr.append(i.long - j.long)
            else:
                print("Error - unrecognized mode")
        arr.append(sub_arr)
    return arr

def euclidean_dist(lat_matrix,long_matrix):
    ''' Returns a matrix of euclidean distances between locations given a matrix
    of their distances in latitude and their distances in longitude'''
    arr = []
    for i in range(len(locations)):
        sub_arr = []
        for j in range(len(locations)):
            sub_arr.append((lat_matrix[i][j]**2 + long_matrix[i][j]**2)**0.5)
        arr.append(sub_arr)
    return arr

def min_dist(distances, index, mode):
    '''Returns the index of the location that is closest to the current location
    (index) (but is not the current location) either in terms of
    absolute distance, positive distance, or negative distanceGiven an array of
    distances (by whatever metric) '''
    min_dist = 100 ## an arbitrarily large number to compare against
    if mode == "absolute":
        ### Which location is closest, point final?
        for i in range(len(distances)):
            if abs(distances[i]) < min_dist and i != index:
                min_dist = abs(distances[i]) ### There's always a closest location
                next_location = i
    elif mode == "positive":
        ### Which location is closest moving in a positive direction?
        logging.debug("Distances: {}".format(distances))
        for i in range(len(distances)):
            if distances[i] < min_dist and i != index and distances[i] > 0:
                min_dist = distances[i]
                next_location = i
        ### Need to see if min_dist was updated, could be at the end of the map
        if min_dist == 100:
            print("Sorry, looks like you can't go that way")
            next_location = index
    elif mode == "negative":
        ### Which location is closest moving in a negative direction?
        logging.debug("Distances: {}".format(distances))
        for i in range(len(distances)):
            if abs(distances[i]) < min_dist and i != index and distances[i] < 0:
                min_dist = abs(distances[i])
                next_location = i
        ### Need to see if min_dist was updated, could be at the end of the map
        if min_dist == 100:
            print("Sorry, looks like you can't go that way")
            next_location = index
    logging.debug("Next destination - min_dist returns: {}".format(next_location))
    return next_location

def next_step(index, lat_matrix, long_matrix, euc_matrix):
    '''Returns an index for the next tour location (next_location) and a boolean
    indicating if tour should continue (keep_going). Takes as arguments current
    location (index), and matrices of distance according to latitude, longitude,
    and euclidean distance.'''
    options = ["1) I want to go north.", "2) I want to go east.", "3) I want to go south.",
        "4) I want to go west.", "5) Take me to whatever is closest.","6) I don't care, take me anywhere."]

    print("")
    keep_going = yes_no_input("Keep going? (Y/N) \n")
    if keep_going == "Y":
        keep_going = True
        val = give_user_options(options)
        choice = input()
        while choice not in ([str(i) for i in range(val+1)]):
            print("Oops, seems like you made a typo. Choose a number from 1 to 6:")
            choice = input()
        if int(choice) == 1:
            next_location = min_dist(lat_matrix[index], index, "negative")
        elif int(choice) == 2:
            next_location = min_dist(long_matrix[index], index, "negative")
        elif int(choice) == 3:
            next_location = min_dist(lat_matrix[index], index, "positive")
        elif int(choice) == 4:
            next_location = min_dist(long_matrix[index], index, "positive")
        elif int(choice) == 5:
            next_location = min_dist(euc_matrix[index], index, "absolute")
        elif int(choice) == 6:
            next_location = go_anywhere(index)
    else:
        next_location = 0
        keep_going = False
        print("See you next time!")
    logging.debug("Next location: {}".format(next_location))
    return next_location, keep_going

def go_anywhere(current_location):
    ''' Returns a random index for a location that is not the current_location'''
    next_location = current_location
    while next_location == current_location:
        next_location = random.choice(range(len(locations)))
    logging.debug("Next destination - random: {}".format(next_location))
    return next_location

def spatial_walking_tour(index, locations, lat_matrix, long_matrix, euc_matrix):
    '''Prints output of spatial tour and calls next_step to determine if user
    wants to keep going and if so, what the next location is'''
    logging.debug("Working")
    ### At beginning of tour keep_going = True, after that print location output
    ### reassess whether to continue, and index of next location
    ### repeat until tour terminated by user
    keep_going = True
    while keep_going == True:
        locations[index].output()
        index, keep_going = next_step(index, lat_matrix, long_matrix, euc_matrix)

def emotional_walking_tour():
    print('''\n Sorry, the emotional walking tour isn't online yet. Try
    the spatial walking or the temporal walking tour. They're great. We promise.''')
    return control_flow()

### Temporal walking tour functions

def initiate_temporal_tour(locations):
    years = sorted(list({i.year for i in locations}))
    print("What year would you like to start the tour in? Your options are: \n")
    for i in range(len(years)):
        print("{}) {}".format(i, years[i]))
    choice = choice_sanitization(years)
    ### Return index of first location in locations to satistfy choice
    chosen_year = years[choice]
    for i in range(len(locations)):
        if locations[i].year == chosen_year:
            return i

def temporal_organization(locations):
    '''Returns a list of timepoints (summed number of months since timepoint 0)
     for each location'''
    # '''Returns a dictionary in which each location index is the key, and the
    # timepoint (summed number of months since timepoint 0) is the value.'''
    # timepoints = {i: (locations[i].year - 2002)*12 + locations[i].month for i in range(len(locations))}
    timepoints = [(i.year - 2002)*12 + i.month for i in locations]
    return timepoints

def time_travel(index, timepoints, mode):
    ### calculation of timediff could be refactored into a matrix calculated
    ### just once at the beginning of temporal mode
    timediff = [i - timepoints[index] for i in timepoints]
    if mode == "forward":
        next_step = move_forward(timediff, index)
    else:
        next_step = move_backward(timediff, index)
    return next_step

def move_forward(timediff, index):
    if max(timediff) < 1:
        print("Sorry, you can't go forward in time")
        ind = index
    else:
        min_diff = 100 ## an arbitrarily large number
        for i in range(len(timediff)):
            if timediff[i] > 0 and timediff[i] < min_diff:
                ind, min_diff = i, timediff[i]
    return ind

def move_backward(timediff, index):
    if min(timediff) > -1:
        print("Sorry, you can't go back in time")
        ind = index
    else:
        min_diff = 100 ## an arbitrarily large number
        for i in range(len(timediff)):
            if timediff[i] < 0 and timediff[i] < min_diff:
                ind, min_diff = i, abs(timediff[i])
    return ind

def random_season_selector(locations, mode):
    '''Return a random location from the sublist of locations of a given season'''

    if mode == "winter":
        options = {12, 1, 2}
    elif mode == "spring":
        options = {3,4,5}
    elif mode == "summer":
        options = {6,7,8}
    else:
        options = {9, 10, 11}

    season_locations = [i for i in range(len(locations)) if locations[i].month in options]
    ind = season_locations[random.randrange(0,len(season_locations))]

    return ind







def temporal_walking_tour(index, locations, timepoints):

    ### At beginning of tour keep_going = True, after that print location output
    ### reassess whether to continue, and index of next location
    ### repeat until tour terminated by user
    keep_going = True
    while keep_going == True:
        locations[index].output()
        index, keep_going = temporal_progress(index, timepoints, locations)

def temporal_progress(index, timepoints, locations):
    options = ["1) I want to go forward in time.", "2) I want to go back in time.",
        "3) I want to visit winter.", "4) I want to visit spring.",
        "5) I want to visit summer.", "6) I want to visit autumn.",
        "7) I don't care, take me anywhere."]
    print("")
    keep_going = yes_no_input("Keep going? (Y/N) \n")
    if keep_going == "Y":
        keep_going = True
        val = give_user_options(options)
        choice = input()
        while choice not in ([str(i) for i in range(val+1)]):
            print("Oops, seems like you made a typo. Choose a number from 1 to 6:")
            choice = input()
        if choice == "1":
            next_location = time_travel(index, timepoints, "forward")
        elif choice == "2":
            next_location = time_travel(index, timepoints, "backwards")
        elif choice == "3":
            next_location = random_season_selector(locations, "winter")
            # Choose any location that has a month 12, 1, or 2
        elif choice == "4":
            next_location = random_season_selector(locations, "spring")
            # Choose any location that has month == 3, 4, 5
        elif choice == "5":
            # Choose any location that has month == 6, 7, 8
            next_location = random_season_selector(locations, "summer")
        elif choice == "6":
            # Choose any location that has month == 9, 10, 11
            next_location = random_season_selector(locations, "fall")
        else:
            next_location = go_anywhere(index)
    else:
        next_location = 0
        keep_going = False
        print("See you next time!")
    logging.debug("Next location: {}".format(next_location))
    return next_location, keep_going

### General functions

def control_flow():
    tour = initiate_program()
    if tour == 1:
        index = initiate_walking_tour(locations)
        ### Distances between locations in latitude, longitude, euclidean
        lat_matrix, long_matrix = dist_matrix(locations, "lat"), dist_matrix(locations, "long")
        euc_matrix = euclidean_dist(lat_matrix, long_matrix)
        spatial_walking_tour(index, locations, lat_matrix, long_matrix, euc_matrix)
    elif tour == 2:
        emotional_walking_tour()
    else:
        index = initiate_temporal_tour(locations)
        timepoints = temporal_organization(locations)
        temporal_walking_tour(index, locations, timepoints)


if __name__ == "__main__":
    control_flow()
