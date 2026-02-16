import json
import random
import time


class Player:
    def __init__(self, name):
        self.right = Hand()
        self.left = Hand()
        self.name = name

    def attack(self, attacker_hand, recipient_hand):
        if attacker_hand.get_value() > 0 and recipient_hand.get_value() > 0:
            recipient_hand.set_value((recipient_hand.get_value() + attacker_hand.get_value()) % 5)
            return True
        return False
    
    def split(self, amount, splitter_hand, recipient_hand):
        temp_splitter = splitter_hand.get_value() - amount
        temp_recipient = (recipient_hand.get_value() + amount) % 5

        if temp_splitter == recipient_hand.get_value() and temp_recipient == splitter_hand.get_value():
            print("You cannot switch around the hands")
            return False
        else:
            splitter_hand.set_value(splitter_hand.get_value() - amount) 
            return True

class Hand:
    def __init__(self):
        self.value = 1
        self.prev_value = 0

    def get_value(self):
        return self.value
    
    def set_value(self, amount):
        self.value = amount
    
    def get_prev_value(self):
        return self.prev_value
    
    def set_prev_value(self, amount):
        self.prev_value = amount

#-------------------------------------------------------------


def switch_players(current_player, not_current_player):
    if current_player == Player1:
        current_player = Player2
        not_current_player = Player1
        return current_player, not_current_player
    else:
        current_player = Player1
        not_current_player = Player2
        return current_player, not_current_player

def get_hand(player, hand):
    if hand == 'left':
        return player.left
    elif hand == 'right':
        return player.right

def get_opposite_hand(player, hand):
    if hand == 'left':
        return player.right
    elif hand == 'right':
        return player.left

#-----------------------------------------------------------

def attack_function():
    attacker_hand_str = input('left or right to attack with or back to go back: ').lower()
    while attacker_hand_str not in ['left', 'right', 'back']:
        attacker_hand_str = input("try again, enter left or right to attack with or back: ")
    if attacker_hand_str == 'back':
        return 'back'
    if current_player.right.get_value() == 0:
        while attacker_hand_str not in ['left', 'back']:
            attacker_hand_str = input("You must choose to attack with left or back to go back: ")
        if attacker_hand_str == 'back':
            return 'back'
    elif current_player.left.get_value() == 0:
        while attacker_hand_str not in ['right', 'back']:
            attacker_hand_str = input("You must choose to attack with right or back to go back: ")
        if attacker_hand_str == 'back':
            return 'back'
    attacking_hand = get_hand(current_player, attacker_hand_str)

    recipient_hand_str = input("left or right hand to attack: ").lower()
    while recipient_hand_str not in ['left', 'right', 'back']:
        recipient_hand_str = input("try again, enter left or right to attack or back: ")
    if recipient_hand_str == 'back':
        return 'back'
    if not_current_player.right.get_value() == 0:
        while recipient_hand_str not in ['left', 'back']:
            recipient_hand_str = input("You must choose to attack their left or right or go back to go back: ")
        if recipient_hand_str == 'back':
            return 'back'
    elif not_current_player.left.get_value() == 0:
        while recipient_hand_str not in ['right', 'back']:
            recipient_hand_str = input("You must choose to attack their right or back to go back: ")
        if recipient_hand_str == 'back':
            return 'back'
    recipient_hand = get_hand(not_current_player, recipient_hand_str)
    current_player.attack(attacking_hand, recipient_hand)
    return None

def split_function():
    choice = input('split "left" to right or "right" to left: ').lower()
    splitter_hand = get_hand(current_player, choice)
    amount = int(input("how much to split: "))
    if splitter_hand.get_value() > 0 and splitter_hand.get_value() >= amount:
        if current_player.split(amount, splitter_hand, get_opposite_hand(current_player, choice)):
            return None
        else:
            return 'back'
    
#-----------------------------------------------------------

Player1 = Player('Taras')
Player2 = Player('Yarema')

current_player = Player1
not_current_player = Player2

#-----------------------------------------------------------

while Player1.right.get_value() + Player1.left.get_value() > 0 and Player2.right.get_value() + Player2.left.get_value() > 0:
    print(f"scores: {Player1.name} {Player1.left.get_value()} {Player1.right.get_value()}\n{Player2.name} {Player2.left.get_value()} {Player2.right.get_value()}")
    
    choice = input(current_player.name + " attack or split: ").lower()
    while choice not in ['attack', 'split']:
        choice = input("You must attack or split, try again: ").lower()
    if choice == 'attack':
        result = attack_function()
        if result == None:
            current_player, not_current_player = switch_players(current_player, not_current_player)
        else:
            print("Returning back")
            time.sleep(1)

    elif choice == 'split':
        result = split_function()
        if result == None:
            current_player, not_current_player = switch_players(current_player, not_current_player)
        else:
            print("Returning back")
            time.sleep(1)

if Player1.right.get_value() + Player1.left.get_value() == 0:
    print(Player2.name, 'Wins!!!!')
else:
    print(Player1.name, 'Wins!!!!')
    
