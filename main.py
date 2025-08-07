import json
import random
import os

current_player = "Player1"
p1l = 2
p1r = 2
p2l = 2
p2r = 1

file_name = "q_learning_values_for_bot.json"
script_directory = os.path.dirname(os.path.abspath(__file__))
data_json = os.path.join(script_directory, file_name)

def prepare_JSON_files(file_name="q_learning_values_for_bot.json"):

    data = {}

    # --- The crucial part: Getting the script's actual directory ---
    # 1. os.path.abspath(__file__): Gets the absolute path of the current script file (e.g., C:\Users\T\Python projects\current_chopsticks_project\CWD test.py)
    # 2. os.path.dirname(...): Extracts the directory part from that path (e.g., C:\Users\T\Python projects\current_chopsticks_project\)
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path for the new JSON file
    full_file_path = os.path.join(script_directory, file_name)

    print(f"The script is located in: {script_directory}")
    print(f"Attempting to create file at: {full_file_path}")

    try:
        with open(full_file_path, "w") as f:
            json.dump(data, f, indent=4)
        print(f"File '{file_name}' created successfully at the specified path.")

    except IOError as e:
        print(f"Error creating file: {e}")

def confirm_no_over_5(p1l, p1r, p2l, p2r):
    if p1l >= 5:
        p1l -= 5
    if p1r >= 5:
        p1r -= 5
    if p2l >= 5:
        p2l -= 5
    if p2r >= 5:
        p2r -= 5
    return p1l, p1r, p2l, p2r

def all_legal_moves(p1l, p1r, p2l, p2r, data_json):
    def calculate_how_many_splitting_moves_are_legal(p1l, p1r, left_hand, right_hand, data_json):
        print("Entered the function")
        if left_hand != 0:
            right_hand_orginal = right_hand
            with open(data_json, "r") as f: #creating new key key value trios or key value pairs if needed
                data_py = json.load(f)
                print("opened file")
            for i in range(1,left_hand+1):
                right_hand += 1
                print(f"right hand is {right_hand}")
                if left_hand != right_hand:
                    print(f"{left_hand}{right_hand}")
                    try:
                        game_state = f"{p1l}{p1r}{left_hand}{right_hand_orginal}"
                        if game_state not in data_py:
                            data_py[game_state] = {}
                        move_choice = f"{left_hand}{right_hand_orginal}s{i}"
                        if move_choice not in data_py[game_state]:
                            data_py[game_state][move_choice] = {}
                            print("Adding new key-value")
                        with open(data_json, "w") as f: #writing it to the json file
                            json.dump(data_py, f, indent=4)
                            print("Successfuly uploaded data_py")
                    except json.JSONDecodeError as e:
                        print("Error decoding json:", e)
                    except KeyError as e:
                        print("Error: key not found during access:", e)
                    except Exception as e:
                        print(f"An error {e} occured")
            right_hand = right_hand_orginal
        if right_hand != 0:
            left_hand_original = left_hand
            with open(data_json, "r") as f: #creating new key key value trios or key value pairs if needed
                data_py = json.load(f)
                print("opened file")
            for i in range(1,right_hand+1):
                left_hand += 1
                if left_hand != right_hand:
                    try:
                        game_state = f"{p1l}{p1r}{left_hand_original}{right_hand}"
                        if game_state not in data_py:
                            data_py[game_state] = {}
                        move_choice = f"{left_hand_original}{right_hand}s{i}"
                        if move_choice not in data_py[game_state]:
                            data_py[game_state][move_choice] = {}
                            print("Adding new key-value")
                        with open(data_json, "w") as f: #writing it to the json file
                            json.dump(data_py, f, indent=4)
                            print("Successfuly uploaded data_py")
                    except json.JSONDecodeError as e:
                        print("Error decoding json:", e)
                    except KeyError as e:
                        print("Error: key not found during access:", e)
                    except Exception as e:
                        print(f"An error {e} occured")
            left_hand = left_hand_original
    def legal_attacking_moves(p1l, p1r, p2l, p2r, data_json):
        print("Entered attacking function")
        with open(data_json, "r") as f:
            data_py = json.load(f)
        game_state = f"{p1l}{p1r}{p2l}{p2r}"
        hand = [p1l,p1r,p2l,p2r]
        for i in range(0,2):
            print("entered the loop")
            print(hand[i])
            if hand[i] != 0:
                print(f"hand {hand[i]} is not 0")
                for j in range(0,2):
                    if hand[j+2] != 0:
                        print(f"hand {hand[i]} and hand {hand[j+2]} are not 0")
                        move_choice = f"{p2l}{p2r}a{hand[i]}w{hand[j+2]}"
                        try:
                            if game_state not in data_py:
                                data_py[game_state] = {}
                            if move_choice not in data_py[game_state]:
                                data_py[game_state][move_choice] = {}
                            with open(data_json, "w") as f:
                                json.dump(data_py, f, indent = 4)
                                print("Successfully added new attacking key value pair")
                        except json.JSONDecodeError as e:
                            print("Error decoding json:", e)
                        except KeyError as e:
                            print("Error: key not found during access:", e)
                        except Exception as e:
                            print(f"An error {e} occured")
    
    calculate_how_many_splitting_moves_are_legal(p1l, p1r, p2l, p2r, data_json)
    print(p1l, p1r, p2l, p2r, "current hands inbetween split and attack functions")
    legal_attacking_moves(p1l, p1r, p2l, p2r, data_json)


while (p1l+p1r != 0) and (p2l+p2r !=0):
    all_legal_moves(p1l, p1r, p2l, p2r, data_json)
    p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
    print(" "*50,p1l,":",p1r,"|", p2l,":",p2r)
    if current_player == "Player1":
        print("Player 1:")
        choice_1 = int(input("Do you want to attack (1) or split (2)?"))
        if choice_1 == 1: #attacking
            choice_2 = int(input("Do you want to attack with: \nl-> l (1) \nl->r (2) \nr-> l (3) \nr-> r (4)\n"))
            while p2l == 0:
                if choice_2 == 1 or choice_2 == 3:
                    print("You cannot attack this hand as they have 0 fingers held up, try again")
                    choice_2 = int(input("Do you want to attack with: \nl-> l (1) \nl->r (2) \nr-> l (3) \nr-> r (4)\n"))
                else: 
                    break
            while p2r == 0:
                if choice_2 == 2 or choice_2 == 4:
                    print("You cannot attack this hand as they have 0 fingers held up, try again")
                    choice_2 = int(input("Do you want to attack with: \nl-> l (1) \nl->r (2) \nr-> l (3) \nr-> r (4)\n"))
                else: 
                    break
            while p1l == 0:
                if choice_2 == 1 or choice_2 == 2:
                    print("You cannot attack with this hand as you have 0 fingers held up, try again")
                    choice_2 = int(input("Do you want to attack with: \nl-> l (1) \nl->r (2) \nr-> l (3) \nr-> r (4)\n"))
                else: 
                    break
            while p1r == 0:
                if choice_2 == 3 or choice_2 == 4:
                    print("You cannot attack with this hand as you have 0 fingers held up, try again")
                    choice_2 = int(input("Do you want to attack with: \nl-> l (1) \nl->r (2) \nr-> l (3) \nr-> r (4)\n"))
                else: 
                    break
            if choice_2 == 1:
                p2l += p1l
                if p2l >= 5:
                    p2l -= 5
            elif choice_2 == 2:
                p2r += p1l
                if p2r >= 5:
                    p2r -= 5
            elif choice_2 == 3:
                p2l += p1r
                if p2l >= 5:
                    p2l -= 5
            elif choice_2 == 4:
                p2r += p1r
                if p2r >= 5:
                    p2r -= 5
        elif choice_1 == 2: #splitting
            choice_2_1 = "Not Valid"
            while choice_2_1 != "Valid": #confirming splitting hand doesnt have 0 fingers
                choice_2 = int(input("Do you want to split: \nl->r (1) \nr->l (2)"))
                if choice_2 == 1:
                    if p1l > 0:
                        choice_2_1 = "Valid"
                    else:
                        print("You cannot split from this hand as it has 0 fingers up, try again")
                elif choice_2 == 2:
                    if p1r > 0:
                        choice_2_1 = "Valid"
                    else:
                        print("You cannot split from this hand as it has 0 fingers up, try again")


            if choice_2 == 1:
                add = int(input("How much do you want to split to your right hand?"))
                while add > p1l:
                    print("You cannot perform this split as your hand doesnt have enough fingers up currently, try again")
                    add = int(input("How much do you want to split to your right hand?"))
                p1r = p1r + add
                while p1r == p1l: #preventing switching same hands over
                    print("You cannot switch the fingers around, try again")
                    p1r = p1r - add
                    add = int(input("How much do you want to split to your right hand?"))
                    while add > p1l:
                        print("You cannot perform this split as your hand doesnt have enough fingers up currently, try again")
                        add = int(input("How much do you want to split to your right hand?"))
                    p1r += add
                    if p1r >= 5:
                        over5 = True
                        p1r -= 5
                p1l -= add


            if choice_2 == 2:
                add = int(input("How much do you want to split to your left hand?"))
                while add > p1r:
                    print("You cannot perform this split as your hand doesnt have enough fingers up currently, try again")
                    add = int(input("How much do you want to split to your right hand?"))
                p1l = p1l + add
                while p1l == p1r: #preventing switching same hands over
                    print("You cannot switch the fingers around, try again")
                    p1l = p1l - add
                    add = int(input("How much do you want to split to your right hand?"))
                    while add > p1r:
                        print("You cannot perform this split as your hand doesnt have enough fingers up currently, try again")
                        add = int(input("How much do you want to split to your right hand?"))
                    p1l += add
                    if p1l >= 5:
                        over5 = True
                        p1l -= 5
                p1r -= add
        current_player = "Player2"
    all_legal_moves(p1l, p1r, p2l, p2r, data_json)
    p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
    print(" "*50,p1l,":",p1r,"|", p2l,":",p2r)
    if (p1l+p1r == 0) or (p2l+p2r ==0):
        break
    if current_player == "Player2":
        print("Player 2:")
        choice_1 = int(input("Do you want to attack (1) or split (2)?"))
        if choice_1 == 1: #attacking
            choice_2 = int(input("Do you want to attack with: \nl-> l (1) \nl->r (2) \nr-> l (3) \nr-> r (4)\n"))
            while p1l == 0:
                if choice_2 == 1 or choice_2 == 3:
                    print("You cannot attack this hand as they have 0 fingers held up, try again")
                    choice_2 = int(input("Do you want to attack with: \nl-> l (1) \nl->r (2) \nr-> l (3) \nr-> r (4)\n"))
                else: 
                    break
            while p1r == 0:
                if choice_2 == 2 or choice_2 == 4:
                    print("You cannot attack this hand as they have 0 fingers held up, try again")
                    choice_2 = int(input("Do you want to attack with: \nl-> l (1) \nl->r (2) \nr-> l (3) \nr-> r (4)\n"))
                else: 
                    break
            while p2l == 0:
                if choice_2 == 1 or choice_2 == 2:
                    print("You cannot attack with this hand as you have 0 fingers held up, try again")
                    choice_2 = int(input("Do you want to attack with: \nl-> l (1) \nl->r (2) \nr-> l (3) \nr-> r (4)\n"))
                else: 
                    break
            while p2r == 0:
                if choice_2 == 3 or choice_2 == 4:
                    print("You cannot attack with this hand as you have 0 fingers held up, try again")
                    choice_2 = int(input("Do you want to attack with: \nl-> l (1) \nl->r (2) \nr-> l (3) \nr-> r (4)\n"))
                else: 
                    break
            if choice_2 == 1:
                p1l += p2l
                if p1l >= 5:
                    p1l -= 5
            elif choice_2 == 2:
                p1r += p2l
                if p1r >= 5:
                    p1r -= 5
            elif choice_2 == 3:
                p1l += p2r
                if p1l >= 5:
                    p1l -= 5
            elif choice_2 == 4:
                p1r += p2r
                if p1r >= 5:
                    p1r -= 5
        elif choice_1 == 2: #splitting
            choice_2_1 = "Not Valid"
            while choice_2_1 != "Valid": #confirming splitting hand doesnt have 0 fingers
                choice_2 = int(input("Do you want to split: \nl->r (1) \nr->l (2)"))
                if choice_2 == 1:
                    if p2l > 0:
                        choice_2_1 = "Valid"
                    else:
                        print("You cannot split from this hand as it has 0 fingers up, try again")
                elif choice_2 == 2:
                    if p2r > 0:
                        choice_2_1 = "Valid"
                    else:
                        print("You cannot split from this hand as it has 0 fingers up, try again")
                    

            if choice_2 == 1:
                add = int(input("How much do you want to split to your right hand?"))
                while add > p2l:
                    print("You cannot perform this split as your hand doesnt have enough fingers up currently, try again")
                    add = int(input("How much do you want to split to your right hand?"))
                p2r = p2r + add
                while p2r == p2l: #preventing switching same hands over
                    print("You cannot switch the fingers around, try again")
                    p2r = p2r - add
                    add = int(input("How much do you want to split to your right hand?"))
                    while add > p2l:
                        print("You cannot perform this split as your hand doesnt have enough fingers up currently, try again")
                        add = int(input("How much do you want to split to your right hand?"))
                    p2r += add
                    if p2r >= 5:
                        over5 = True
                        p2r -= 5
                p2l -= add
                    

            if choice_2 == 2:
                add = int(input("How much do you want to split to your left hand?"))
                while add > p2r:
                    print("You cannot perform this split as your hand doesnt have enough fingers up currently, try again")
                    add = int(input("How much do you want to split to your right hand?"))
                p2l = p2l + add
                while p2l == p2r: #preventing switching same hands over
                    print("You cannot switch the fingers around, try again")
                    p2l = p2l - add
                    add = int(input("How much do you want to split to your right hand?"))
                    while add > p2r:
                        print("You cannot perform this split as your hand doesnt have enough fingers up currently, try again")
                        add = int(input("How much do you want to split to your right hand?"))
                    p2l += add
                    if p2l >= 5:
                        over5 = True
                        p2l -= 5
                p2r -= add
        current_player = "Player1"

if p1l+p1r == 0:
    print("Game over! Player 2 wins!")
else:
    print("Game over! Player 1 wins!")


def bot(p1l, p1r, p2l, p2r, epsilon=90):
    random_int = random.randint(1,100)
    with open(data_json, "r") as f:
        data_py = json.load(f)
    game_state = f"{p1l}{p1r}{p2l}{p2r}"
    game_state_dictionary = data_py[game_state]
    keys_for_game_state = game_state_dictionary.keys()
    list_of_keys_for_moves = list(keys_for_game_state)
    print("printing data_py[game_state] and [0]", data_py[game_state][list_of_keys_for_moves[0]])
    if random_int <= epsilon: #exploration
        total_legal_moves = len(game_state_dictionary)
        bot_choice = random.randint(0,total_legal_moves-1)
        bot_move = list_of_keys_for_moves[bot_choice]
        p2l_original = p2l
        p2r_original = p2r
        if bot_move[2] == "a": #if the random move selected is attacking
            print("The random move chosen is attacking")
            if p1l == int(bot_move[3]):
                p1l += int(bot_move[5])
                p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
            elif p1r == int(bot_move[3]):
                p1r += int(bot_move[5])
                p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
        elif bot_move[2] == "s": #if the random move chosen is splitting
            print("The chosen random move is splitting")
            if int(bot_move[0]) == 0:
                p2l += int(bot_move[3])
                p2r -= int(bot_move[3])
                p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
                if p2l_original == p2r:
                    p2l = p2l_original - int(bot_move[3])
                    p2r = p2r_original + int(bot_move[3])
                    p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
            else:
                p2l -= int(bot_move[3])
                p2r += int(bot_move[3])
                p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
                if p2l_original == p2r:
                    p2l = p2l_original - int(bot_move[3])
                    p2r = p2r_original + int(bot_move[3])
                    p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
    elif random_int > epsilon: #exploitation
        print("exploitation")
        best_move = ""
        best_move_score = -999999
        for i in range(0,len(list_of_keys_for_moves)):
            current_testing_move = data_py[game_state][list_of_keys_for_moves[i]]
            if current_testing_move > best_move_score:
                best_move_score = current_testing_move
                best_move = list_of_keys_for_moves[i]
        bot_move = best_move
        p2l_original = p2l
        p2r_original = p2r
        if bot_move[2] == "a": #if the move selected is attacking
            print("The move chosen is attacking")
            if p1l == int(bot_move[3]):
                p1l += int(bot_move[5])
                p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
            elif p1r == int(bot_move[3]):
                p1r += int(bot_move[5])
                p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
        elif bot_move[2] == "s": #if the move chosen is splitting
            print("The move chosen is splitting")
            if int(bot_move[0]) == 0:
                p2l += int(bot_move[3])
                p2r -= int(bot_move[3])
                p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
                if p2l_original == p2r:
                    p2l = p2l_original - int(bot_move[3])
                    p2r = p2r_original + int(bot_move[3])
                    p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
            else:
                p2l -= int(bot_move[3])
                p2r += int(bot_move[3])
                p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
                if p2l_original == p2r:
                    p2l = p2l_original + int(bot_move[3])
                    p2r = p2r_original - int(bot_move[3])
                    p1l, p1r, p2l, p2r = confirm_no_over_5(p1l, p1r, p2l, p2r)
    print("Reached end of the function")
    return p1l, p1r, p2l, p2r


