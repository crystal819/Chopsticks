import random
import json
from main import Player, Game

#state = (p1l, p1r, p2l, p2r)


class Agent(Player):
    def __init__(self):
        super().__init__(name='Agent')

agent = Agent()


def load_q_values():
    with open('q_learning_values_for_bot.json', 'r') as file:
        q_values = json.loads(file.read())
    return q_values




def get_valid_moves(state):
    #for attack
    valid_moves = []
    if state[0] != 0:
        if state[2] != 0:
            valid_moves.append(('a', 0, 0)) #attack, self hand, opponent hand
        if state[3] != 0:
            valid_moves.append(('a', 0, 1))
    if state[1] != 0:
        if state[2] != 0:
            valid_moves.append(('a', 1, 0))
        if state[3] != 0:
            valid_moves.append(('a', 1, 1))
    
    #for splitting
    if state[0] != 0:
        for i in range(1, state[0]+1):
            temp = state[1] + i
            if temp != state[0]:
                valid_moves.append(('s', 0, i)) #split, splitting hand, amount
    elif state[1] != 0:
        for i in range(1, state[1]+1):
            temp = state[0] + i
            if temp != state[1]:
                valid_moves.append(('s', 0, i)) 

    return valid_moves #returns the valid moves in a list














q_values = load_q_values()


#------------------------------------------------------------
if __name__ == '__main__':
    Player1 = Player('Taras')
    Player2 = Agent('Bot1')
    game = Game(Player1, Player2)

