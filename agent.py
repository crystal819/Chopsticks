import random
import json
from main import Player, Game, update_state
import time

#<state> format = (p1l, p1r, p2l, p2r, x) where x is either 0 or 1 where 0 represents the current player as player 1 so the bot understands from the q-value states whether it is the first two hands or last two hands

class Agent(Player):
    def __init__(self, name):
        super().__init__(name=name)

    def make_move(self, state, q_values, opponent, Player1, Player2):
        epsilon = 0.1 #exploration rate the higher the more random, the lower the more skill
        highest_action = self.max_Q(state, q_values)[1]

        
        if random.randint(0, 100) / 100 > epsilon: #exploitation
            action = highest_action
        else: #exploration
            action = random.choice(self.get_valid_moves(state))
        if action[0] == 'a': #chosen to attack
            if action[1] == 0:
                attacking_hand = self.left
            else:
                attacking_hand = self.right
            if action[2] == 0:
                recieving_hand = opponent.left
            else:
                recieving_hand = opponent.right
            self.attack(attacking_hand, recieving_hand)

        else: #chosen to split
            if action[1] == 0:
                splitting_hand = self.left
                recieving_hand = self.right
            else:
                splitting_hand = self.right
                recieving_hand = self.left

            self.split(action[2], splitting_hand, recieving_hand)
        
        if self.left.get_value() + self.right.get_value() == 0:
            reward = -1
        elif opponent.left.get_value() + opponent.right.get_value() == 0:
            reward = 1
        else:
            reward = 0

        self.updateQsa(state, action, q_values, reward, Player1, Player2)

    def max_Q(self, state, q_values): #returns a list with the q_value and its action with the highest q_value in this state
        highest = -1000000
        highest_action = None
        legal_moves = self.get_valid_moves(state)

        if str(state) not in q_values: #adds state if not present
            q_values[str(state)] = {}
        for action in legal_moves:
            if str(action) not in q_values[str(state)]: #adds action if not present
                q_values[str(state)][str(action)] = 0
            if q_values[str(state)][str(action)] > highest:
                highest = q_values[str(state)][str(action)]
                highest_action = action
        return [highest, highest_action]

    def min_Q(self, state, q_values): #returns a list with the q_value and its action with the highest q_value in this state
        lowest = 10000
        lowest_action = None
        legal_moves = self.get_valid_moves(state)

        if str(state) not in q_values: #adds state if not present
            q_values[str(state)] = {}
        for action in legal_moves:
            if str(action) not in q_values[str(state)]: #adds action if not present
                q_values[str(state)][str(action)] = 0
            if q_values[str(state)][str(action)] < lowest:
                lowest = q_values[str(state)][str(action)]
                lowest_action = action
        return [lowest, lowest_action]

    def get_valid_moves(self, state):
        #for attack
        valid_moves = []
        if state[4] == 0:
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
                        valid_moves.append(('s', 1, i)) 
        else:
            if state[2] != 0:
                if state[0] != 0:
                    valid_moves.append(('a', 0, 0)) #attack, self hand, opponent hand
                if state[1] != 0:
                    valid_moves.append(('a', 0, 1))
            if state[3] != 0:
                if state[0] != 0:
                    valid_moves.append(('a', 1, 0))
                if state[1] != 0:
                    valid_moves.append(('a', 1, 1))
            
            #for splitting
            if state[2] != 0:
                for i in range(1, state[2]+1):
                    temp = state[3] + i
                    if temp != state[2]:
                        valid_moves.append(('s', 0, i)) #split, splitting hand, amount
            elif state[3] != 0:
                for i in range(1, state[3]+1):
                    temp = state[2] + i
                    if temp != state[3]:
                        valid_moves.append(('s', 1, i)) 

        return valid_moves #returns the valid moves in a list

    def updateQsa(self, state, action, q_values, reward, Player1, Player2): #updates Q(s,a) based on the state and the action taken in it
        alpha = 0.3 #learning rate
        gamma = 0.9 #discount factor - how much future rewards matter compared to immediate rewards

        future_state = update_state(state, Player1, Player2)
        #print(state, action, q_values[str(state)][str(action)])
        q_values[str(state)][str(action)] = round(q_values[str(state)][str(action)] + alpha*(reward - gamma*self.max_Q(future_state, q_values)[0] - q_values[str(state)][str(action)]), 8) #switched the + to a - and max_Q() to min_Q() since the agent would want to update the q_value based on the opponents worst move
        #print(q_values[str(state)][str(action)])q_values[str(state)][str(action)] + alpha*(reward - gamma*self.max_Q(state, q_values)[0] - q_values[str(state)][str(action)])

def load_q_values():
    with open('q_learning_values_for_bot.json', 'r') as file:
        q_values = json.loads(file.read())
    return q_values

def save_q_values(q_values):
    try:
        with open('q_learning_values_for_bot.json', 'w', encoding='utf-8') as file:
            json.dump(q_values, file, indent=4, ensure_ascii=False)
    except (TypeError, ValueError) as e:
        print(f"Error: Data provided is not JSON serializable. Details: {e}")
    except OSError as e:
        print(f"File error: {e}")


#------------------------------------------------------------
if __name__ == '__main__':
    start_time = time.perf_counter()
    Player1 = Agent('Bot1')
    Player2 = Agent('Bot2')
    q_values = load_q_values()
    game = Game(Player1, Player2, q_values)
    n_games = 1000000
    for i in range(n_games):
        if i % (n_games//20) == 0:
            if i == n_games // 20:
                print(f'{str(i)[:1]}% completed')
            else:
                print(f'{str(i)[:2]}% completed')
        game.play_CLI()
    print(f'100% completed')
    save_q_values(q_values)
    end_time = time.perf_counter()
    print(end_time - start_time)
    print(game.scores)


