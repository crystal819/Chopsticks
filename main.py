import json
import random
import os

current_player = "Player1"
p1l = 0
p1r = 4
p2l = 0
p2r = 1

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

def calculate_how_many_splitting_moves_are_legal(p1l, p1r, left_hand, right_hand):
    print("Entered the function")
    file_name = "q_learning_values_for_bot.json"
    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_json = os.path.join(script_directory, file_name)
    if left_hand != 0:
        right_hand_orginal = right_hand
        with open(data_json, "r") as f: #creating new key key value trios or key value pairs if needed
            data_py = json.load(f)
            print("opened file")
        for i in range(1,left_hand+1):
            right_hand += 1
            if left_hand != right_hand:
                try:
                    game_state = f"{p1l}{p1r}{left_hand}{right_hand_orginal}"
                    if game_state not in data_py:
                        data_py[game_state] = {}
                    move_choice = f"{left_hand}{right_hand_orginal} {i}"
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
                    move_choice = f"{left_hand_original}{right_hand} {i}"
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

while (p1l+p1r != 0) and (p2l+p2r !=0):
    calculate_how_many_splitting_moves_are_legal(p1l, p1r, p2l, p2r)
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
    calculate_how_many_splitting_moves_are_legal(p1l, p1r, p2l, p2r)
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

q_vales = "q_learning_values_for_bot.json"
