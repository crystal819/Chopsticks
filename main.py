import time

#------------------------------------------------------------

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
        elif amount > splitter_hand.get_value():
            print("you cannot split this amount")
            return False
        elif amount == 0 or splitter_hand.get_value() == 0:
            print("You cannot split 0 or from a hand with 0")
            return False        
        else:
            splitter_hand.set_value(splitter_hand.get_value() - amount) 
            recipient_hand.set_value((recipient_hand.get_value() + amount)%5)
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
    temp = current_player
    current_player = not_current_player
    not_current_player = temp
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

def attack_function(current_player, not_current_player):
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

def split_function(current_player):
    choice = input('split "left" to right or "right" to left: ').lower()
    splitter_hand = get_hand(current_player, choice)
    amount = int(input("how much to split: "))
    if splitter_hand.get_value() > 0 and splitter_hand.get_value() >= amount:
        if current_player.split(amount, splitter_hand, get_opposite_hand(current_player, choice)):
            return None
        else:
            return 'back'
    
def update_state(state, Player1, Player2):
    if state[4] == 0:
        state = (Player1.left.get_value(), Player1.right.get_value(), Player2.left.get_value(), Player2.right.get_value(), 1)
    elif state[4] == 1:
        state = (Player1.left.get_value(), Player1.right.get_value(), Player2.left.get_value(), Player2.right.get_value(), 0)
    return state

#-----------------------------------------------------------

class Game:
    def __init__(self, Player1, Player2, q_values=None):
        self.Player1 = Player1
        self.Player2 = Player2
        self.q_values = q_values
        self.scores = [0,0]

    def play_CLI(self):
        Player1 = self.Player1
        Player2 = self.Player2
        q_values = self.q_values
        current_player = Player1
        not_current_player = Player2
        Player1.left.set_value(1)
        Player1.right.set_value(1)
        Player2.left.set_value(1)
        Player2.right.set_value(1)
        
        state = (Player1.left.get_value(), Player1.right.get_value(), Player2.left.get_value(), Player2.right.get_value(), 0) #0 means which players move it is
        while state[0] + state[1] > 0 and state[2] + state[3] > 0:
            #print(f"scores: {Player1.name} {Player1.left.get_value()} {Player1.right.get_value()}\n{Player2.name} {Player2.left.get_value()} {Player2.right.get_value()}")
            if type(current_player).__name__ == 'Player':
                choice = input(current_player.name + " attack or split: ").lower()
                while choice not in ['attack', 'split']:
                    choice = input("You must attack or split, try again: ").lower()
                if choice == 'attack':
                    result = attack_function(current_player, not_current_player)
                    if result == None:
                        current_player, not_current_player = switch_players(current_player, not_current_player)
                    else:
                        print("Returning back")
                        time.sleep(1)

                elif choice == 'split':
                    result = split_function(current_player)
                    if result == None:
                        current_player, not_current_player = switch_players(current_player, not_current_player)
                    else:
                        print("Returning back")
                        time.sleep(1)
            elif type(current_player).__name__ == 'Agent':
                current_player.make_move(state, q_values, not_current_player, Player1, Player2)
                current_player, not_current_player = switch_players(current_player, not_current_player)
            state = update_state(state, Player1, Player2)
        if Player1.right.get_value() + Player1.left.get_value() == 0:
            self.scores[1] += 1
            #print(Player2.name, 'Wins!!!!')
        else:
            self.scores[0] += 1
            #print(Player1.name, 'Wins!!!!')
        
#------------------------------------------------------------
if __name__ == '__main__':
    Player1 = Player('Taras')
    Player2 = Player('Yarema')
    game = Game(Player1, Player2)
    game.play_CLI()