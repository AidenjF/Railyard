""" File: railyard.py
    Author: Aiden Foster
    Class: CSC 120
    Purpose: To simulate an online railroad
             game with the purpose of leaving
             the board empty in the end.
"""

def main():
    """ The main function that runs the other important
        functions.
    """
    yard = get_file()
    if yard == False:
        return
    loco_and_print(yard)
    move(yard)

def get_file():
    """ This function reads an imput and returns
        the yard list or false if the file does
        not exist.
    """
    # grab the file and sererate it into a list
    try:
        file = input('Please give the yard file:\n')
        yard_file = open(file, 'r')
        lines = yard_file.readlines()
        yard = []
        for line in lines:
            line = line.strip('\n')
            yard.append(list(line))
        return yard
    except FileNotFoundError:
        print('\nERROR: Could not open the yard file\n')
        return False

def loco_and_print(yard):
    """ This function print out the yard visual
        and the loco and destination count.
        yard: the list of the tracks in a 2d list
    """
    print_yard(yard)
    desinations, loco = numbers(yard)
    print(f'Locomotive count:  {loco}')
    print(f'Destination count: {desinations}')

def commands(yard):
    """ This function asks the user for what move they
        would like to do and returns those values.
        yard: the list of the tracks in a 2d list
    """
    # ask for the commands and split them up into variables
    command = input('\nWhat is your next command? \n')
    command = command.split()
    if command[0] == 'move':
        try:
            # make sure they can all be integers
            try:
                from_t = int(command[2])
            except ValueError:
                print((f"\nERROR: Could not convert the 'from-track' value to "
                       f"an integer: '{command[2]}'\n"))
                loco_and_print(yard)
                move(yard)
            try:
                to_t = int(command[3])
            except ValueError:
                print((f"\nERROR: Could not convert the 'to-track' value to "
                       f"an integer: '{command[3]}'\n"))
                loco_and_print(yard)
                move(yard)
            try:
                number = int(command[1])
            except ValueError:
                print((f"\nERROR: Could not convert the 'count' value to "
                       f"an integer: '{command[1]}'\n"))
                loco_and_print(yard)
                move(yard)
        except IndexError:
            not_an_int(yard)
        # check all of the numbers to see if they make sense
        if number < 0:
            print('\nERROR: Cannot move a negative number of cars.')
            loco_and_print(yard)
            move(yard)
        if from_t <= 0 or to_t <= 0 or to_t > len(yard) or from_t > len(yard):
            print('\nERROR: The to-track or from-track number is invalid.')
            loco_and_print(yard)
            move(yard)
        if from_t == to_t:
            print("\nERROR: The 'to' track is the same as the 'from' track.")
            loco_and_print(yard)
            move(yard)
        if len(command) > 4:
            not_an_int(yard)
        # if all checks out return the values
        return from_t, to_t, number
    elif command[0] == 'quit':
        if len(command) > 1:
            not_an_int(yard)
        else:
            print('\nQuitting!\n')
            exit()
    else:
        not_an_int(yard)

def move(yard):
    """ This function is the function that controls all of the 
        moving pieces. Esentially the second main function.
        yard: the list of the tracks in a 2d list
    """
    # commands function
    from_t, to_t, number = commands(yard)
    if 'T' in yard[from_t - 1] and 'T' not in yard[to_t - 1]:
        moving = (yard[from_t - 1][(-2-number):-1])
        # see if there are any letters on the track
        if '-' in moving:
            print((f'\nERROR: Cannot move {number} cars from track {from_t} '
                  f'because it doesn\'t have that many cars.'))
            loco_and_print(yard)
            move(yard)
        there_already = []
        for letters in yard[to_t - 1]:
            if letters.isalpha():
                there_already.append(letters)
        # if the track is empty run this
        if there_already == []:
            i = len(moving)
            while i >= len(moving):
                for k in range(len(moving)):
                    yard[to_t - 1].pop(-i)
                    yard[to_t - 1].insert(-i, moving[k])
                    i -= 1
        # if there is already cars to the moving spot
        else:
            if (len(there_already) + len(moving)) <= (len(yard[to_t - 1]) - 2):
                count = 0
                i = 0
                # make sure you do not index past the length 
                # of the line or what is there already
                while i <= len(yard[to_t - 1]) and count < len(there_already):
                    if yard[to_t - 1][i].isalpha():
                        yard[to_t - 1][i], yard[to_t - 1][i - len(moving)] = \
                        yard[to_t - 1][i - len(moving)], yard[to_t - 1][i]
                        i += 1
                        count += 1
                    else:
                        i += 1
                length = len(moving) - 1
                count = 0
                while length >= 0 and count < len(moving):
                    yard[to_t - 1][-length-2] = moving[count]
                    length -= 1
                    count += 1
            else:
                print((f'\nERROR: Cannot move {number} cars to track {to_t} '
                      f'because it doesn\'t have enough space.'))
                loco_and_print(yard)
                move(yard)
        # get rid of the cars we are moving from the original track
        i = len(moving)
        while i >= 0:
            if i == 0:
                yard[from_t - 1].pop(-1)
                yard[from_t - 1].insert(-1, '-')
                i -= 1
            else:
                yard[from_t - 1].pop(-i)
                yard[from_t - 1].insert(-i, '-')
                i -= 1
        # see how many cars are left from the rack we moved from
        left = 0
        for letters in yard[from_t - 1]:
            if letters.isalpha():
                left += 1
        # move the left over cars from the track we moved from
        count = 0
        i = -1
        while i <= from_t and count < left:
            if yard[from_t - 1][i].isalpha():
                yard[from_t - 1][i], yard[from_t - 1][i + len(moving)] = \
                yard[from_t - 1][i + len(moving)], yard[from_t - 1][i]
                i -= 1
                count += 1
            else:
                i -= 1
        # print the new state of the yard tracks after the 
        # move has been proccessed 
        print((f'\nThe locomotive on track {from_t} moved {number} cars to '
               f'track {to_t}.\n'))
        print_yard(yard)
        ready_to_leave(yard)
        desinations, loco = numbers(yard)
        print(f'Locomotive count:  {loco}')
        print(f'Destination count: {desinations}')

        move(yard)
    else:
        # run this if a locomotive is not present or already is present
        if 'T' not in yard[from_t - 1]:
            print((f'\nERROR: Cannot move from track {from_t} because it '
                  f'doesn\'t have a locomotive.'))
            loco_and_print(yard)
            move(yard)
        if 'T' in yard[to_t - 1]:
            print((f'\nERROR: Cannot move to track {to_t} because it already '
                   f'has a locomotive.'))
            loco_and_print(yard)
            move(yard)

def ready_to_leave(yard):
    """ This function goes through all of the 
        tracks to see if one is ready to leave.
        yard: the list of the tracks in a 2d list
    """
    # got through each of the tracks and see if they are
    # ready to leave
    for i in range(len(yard)):
        letters = []
        car = ''
        count = 1
        for k in yard[i]:
            if k.isalpha():
                if k not in letters:
                    letters.append(k)
                if car != '' and k != 'T':
                    count += 1
                else:
                    if k != 'T':
                        car = k
        # if there is only two letters on the track and one of 
        # them is the locomotive then we know it is ready to leave
        if len(letters) == 2 and 'T' in letters:
            old = len(yard[i])
            yard.pop(i)
            yard.insert(i,['-'] * old)
            print((f'*** ALERT***  The train on track {i + 1}, which had '
                   f'{count} cars, departs for destination {car}.\n'))
            # print the new yard after the train departed
            loco_t_f = loco_check(yard)
            if not loco_t_f:
                print('The last locomotive has departed!\n')
                loco_and_print(yard)
                quit()
            print_yard(yard)

def loco_check(yard):
    """ This checks if there is a locomotive on the tracks.
        yard: the list of the tracks in a 2d list
    """
    check = False
    for rails in yard:
        if 'T' in rails:
            check = True
    return check    

def print_yard(yard):
    """ This function prints the 2d list in order 
        for the user to view.
        yard: the list of the tracks in a 2d list
    """
    count = 1
    for line in yard:
        new = ''.join(line)
        new = new.strip('\n')
        print(f'{count}: {new}')
        count += 1   
    
def numbers(yard):
    """ This functions returns how many locations and 
        desstinations the board has.
        yard: the list of the tracks in a 2d list
    """
    cars = []
    loco = 0
    for i in yard:
        for k in i:
            if k != '-' and k != 'T' and k != '\n' and k not in cars:
                cars.append(k)
            if k == 'T':
                loco += 1
    destinations = len(cars)
    return destinations, loco

def not_an_int(yard):
    """ This function runs the error code when a number can't
        be converted to an integer.
        yard: the list of the tracks in a 2d list
    """
    print((f'\nERROR: The only valid command formats are (where each X '
          'represents an integer):'))
    print('move X X X')
    print('quit\n')
    loco_and_print(yard)
    move(yard)

if __name__ == "__main__":
    main()