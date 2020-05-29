import random
import logging
from MTL_data import *

logging.basicConfig(level=logging.CRITICAL,format='%(asctime)s - %(levelname)s - %(message)s')

def initiate_program():
    '''Greets user and initiates one of the two walking tours following the
    user's choice.'''

    print("Welcome to Michael's walking tour of Montréal")
    print("Please choose the kind of tour you would like to be on:")
    print("1) A spatial walking tour")
    print("2) An emotional walking tour")

    print("\n Please enter your choice as an integer:\n")

    choice = input()
    while choice not in ("1", "2"):
        print("Oops, try again")
        choice = input()
    choice = int(choice)
    while choice != 1:
        print('''\n Sorry, the emotional walking tour isn't online yet. Try
        the spatial walking tour. It's great. We promise. \n''')
        choice = 1
    return choice

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

    print("")
    print("Keep going? (Y/N)")
    keep_going = input()
    while keep_going not in ("Y", "N", "y", "n"):
        print("Oops, seems like you made a typo. Choose Y or N.")
        keep_going = input().upper()
    if keep_going == "Y":
        keep_going = True
        show_the_options()
        choice = input()
        while choice not in ("1", "2", "3", "4", "5", "6"):
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

def show_the_options():
    '''Simply prints options for movement for user'''

    print("Where do you want to go now?")
    print("1) I want to go north.")
    print("2) I want to go east.")
    print("3) I want to go south.")
    print("4) I want to go west.")
    print("5) Take me to whatever is closest.")
    print("6) I don't care, take me anywhere.")

def go_anywhere(current_location):
    ''' Returns a random index for a location that is not the current_location'''
    next_location = current_location
    while next_location == current_location:
        next_location = random.choice(range(len(locations)))
    logging.debug("Next destination - random: {}".format(next_location))
    return next_location

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

def spatial_walking_tour(index, locations):
    ''' Function that implements all spatial walking tour functionality'''
    logging.debug("Working")
    ### Distances between locations in latitude, longitude, euclidean
    lat_matrix = dist_matrix(locations, "lat")
    long_matrix = dist_matrix(locations, "long")
    euc_matrix = euclidean_dist(lat_matrix, long_matrix)
    ### At beginning of tour kee_going = True, after that print location output
    ### reassess whether to continue, and index of next location
    ### repeat until tour terminated by user
    keep_going = True
    while keep_going == True:
        locations[index].output()
        index, keep_going = next_step(index, lat_matrix, long_matrix, euc_matrix)

if __name__ == "__main__":

    tour = initiate_program()
    index = initiate_walking_tour(locations)
    if tour == 1:
        spatial_walking_tour(index, locations)
