from flask import Flask, render_template, jsonify, request, session
from agent import Agent, load_q_values
from main import Player, Game

app = Flask(__name__)
app.secret_key = 'HelloWorld!'




@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route('/play-against-bot', methods=['GET', 'POST'])
def play_against_bot():

    global Player1 
    Player1 = Player(request.form['username'])
    global Player2
    Player2 = Agent('bot')
    global q_values
    q_values = load_q_values()
    
    #Player2.make_move((1,1,1,1,0), q_values, Player1, Player1, Player2)
    return render_template('play-against-bot.html',
                           name = request.form['username'],
                           game_data = {
                               'player1l': Player1.left.get_value(),
                               'player1r': Player1.right.get_value(),
                               'player2l': Player2.left.get_value(),
                               'player2r': Player2.right.get_value()
                           })



@app.route('/play-against-player', methods=['GET', 'POST'])
def play_against_player():
    global Player1 
    Player1 = Player(request.form['username'])
    global Player2
    Player2 = Player('Player2')
    global q_values
    q_values = load_q_values()

    return render_template('play-against-player.html',
                           name = request.form['username'],
                           game_data = {
                               'player1l': Player2.left.get_value(),
                               'player1r': Player2.right.get_value(),
                               'player2l': Player1.left.get_value(),
                               'player2r': Player1.right.get_value()
                           })



@app.route('/perform-move-bot', methods=['POST'])
def perform_move_bot():
    global Player1
    global Player2
    global q_values

    data = request.get_json()

    if data['move'] == 'attack':
        if data['playerSide'] == 'left':
            attacker_hand = Player1.left
        else:
            attacker_hand = Player1.right
        if data['opponentSide'] == 'left':
            recipient_hand = Player2.left
        else:
            recipient_hand = Player2.right
        result = Player1.attack(attacker_hand, recipient_hand)
        if result == True:
            img_url = f"/static/img/{data['opponentSide']}_{recipient_hand.get_value()}.png"
            game_state_after = None

            if Player1.left.get_value() + Player1.right.get_value() == 0:
                game_state_before = 'player lost'
            elif Player2.left.get_value() + Player2.right.get_value() == 0:
                game_state_before = 'player won'
            else:
                game_state_before = 'continuing'
                Player2.make_move((Player1.left.get_value(), Player1.right.get_value(), Player2.left.get_value(), Player2.right.get_value(), 1), q_values, Player1, Player1, Player2) #assuming that the bot is always 2nd to play
                if Player1.left.get_value() + Player1.right.get_value() == 0:
                    game_state_after = 'player lost bot'
                elif Player2.left.get_value() + Player2.right.get_value() == 0:
                    game_state_after = 'player won bot'
                else:
                    game_state_after = 'continuing'

            output = jsonify({
                'isSuccessful': True,
                'playerHand': attacker_hand.get_value(),
                'opponentHand': recipient_hand.get_value(),
                'opponentImgUrl': img_url,
                'handsAfter': [Player1.left.get_value(), Player1.right.get_value(), Player2.left.get_value(), Player2.right.get_value()],
                'gameStateBefore': game_state_before,
                'gameStateAfter': game_state_after,
                'handsAfterUrl': [f"/static/img/left_{Player1.left.get_value()}.png", f"/static/img/right_{Player1.right.get_value()}.png", f"/static/img/left_{Player2.left.get_value()}.png", f"/static/img/right_{Player2.right.get_value()}.png"]
            })
        else:
            output = jsonify({
                'isSuccessful': False,
                'errorMsg': 'something went wrong'
            })

    elif data['move'] == 'split':
        if data['splitterHandSide'] == 'left':
            splitter_hand = Player1.left
            recipient_hand = Player1.right
            recipient_hand_side = 'right'
        elif data['splitterHandSide'] == 'right':
            splitter_hand = Player1.right
            recipient_hand = Player1.left
            recipient_hand_side = 'left'
        
        result = Player1.split(data['amount'], splitter_hand, recipient_hand)
        if result == True:
            splitter_hand_url = f"/static/img/{data['splitterHandSide']}_{splitter_hand.get_value()}.png"
            recipient_hand_url = f"/static/img/{recipient_hand_side}_{recipient_hand.get_value()}.png"
            game_state_after = None
            if Player1.left.get_value() + Player1.right.get_value() == 0:
                game_state_before = 'player lost'
            elif Player2.left.get_value() + Player2.right.get_value() == 0:
                game_state_before = 'player won'
            else:
                game_state_before = 'continuing'
                Player2.make_move((Player1.left.get_value(), Player1.right.get_value(), Player2.left.get_value(), Player2.right.get_value(), 1), q_values, Player1, Player1, Player2) #assuming that the bot is always 2nd to play
                if Player1.left.get_value() + Player1.right.get_value() == 0:
                    game_state_after = 'player lost bot'
                elif Player2.left.get_value() + Player2.right.get_value() == 0:
                    game_state_after = 'player won bot'
                else:
                    game_state_after = 'continuing'

            output = jsonify({
                'isSuccessful': True,
                'splitterHand': splitter_hand.get_value(),
                'recipientHand': recipient_hand.get_value(),
                'splitterHandUrl': splitter_hand_url,
                'recipientHandUrl': recipient_hand_url,
                'handsAfter': [Player1.left.get_value(), Player1.right.get_value(), Player2.left.get_value(), Player2.right.get_value()],
                'gameStateBefore': game_state_before,
                'gameStateAfter': game_state_after,
                'handsAfterUrl': [f"/static/img/left_{Player1.left.get_value()}.png", f"/static/img/right_{Player1.right.get_value()}.png", f"/static/img/left_{Player2.left.get_value()}.png", f"/static/img/right_{Player2.right.get_value()}.png"]
            })
        else:
            output = jsonify({
                'isSuccessful': False,
                'errorMsg': 'something went wrong'
            })

    elif data['move'] == 'determineAmount':
        if data['splitterHandSide'] == 'left':
            splitter_hand = Player1.left
            recipient_hand = Player1.right
        elif data['splitterHandSide'] == 'right':
            splitter_hand = Player1.right
            recipient_hand = Player1.left
        if data['splitterHand'] == splitter_hand.get_value():
            if data['recipientHand'] == recipient_hand.get_value():
                temp = Agent('temp')
                valid_moves = temp.get_valid_moves((splitter_hand.get_value(), recipient_hand.get_value(), Player2.left.get_value(), Player2.right.get_value(), 0))
                valid_splits = []
                for i in range(len(valid_moves)):
                    if valid_moves[i][0] == 's':
                        valid_splits.append(valid_moves[i][2])
                output = jsonify({
                    'isSuccessful': True,
                    'buttons': valid_splits

                })
            else:
                output = jsonify({
                    'isSuccessful': False,
                    'errorMsg': 'something went wrong'
                })
        else:
            output = jsonify({
                'isSuccessful': False,
                'errorMsg': 'something went wrong'
            })


    return output



@app.route('/perform-move-player', methods=['POST'])
def perform_move_player():
    global Player1
    global Player2

    data = request.get_json()

    if data['currentPlayer'] == 'player1':
        if data['move'] == 'attack':
            if data['playerSide'] == 'left':
                attacker_hand = Player1.left
            else:
                attacker_hand = Player1.right
            if data['opponentSide'] == 'left':
                recipient_hand = Player2.left
            else:
                recipient_hand = Player2.right
            result = Player1.attack(attacker_hand, recipient_hand)
            if result == True:
                img_url = f"/static/img/{data['opponentSide']}_{recipient_hand.get_value()}.png"

                if Player1.left.get_value() + Player1.right.get_value() == 0:
                    game_state = 'player lost'
                elif Player2.left.get_value() + Player2.right.get_value() == 0:
                    game_state = 'player won'
                else:
                    game_state = 'continuing'

                output = jsonify({
                    'isSuccessful': True,
                    'playerHand': attacker_hand.get_value(),
                    'opponentHand': recipient_hand.get_value(),
                    'opponentImgUrl': img_url,
                    'gameState': game_state,
                })
            else:
                output = jsonify({
                    'isSuccessful': False,
                    'errorMsg': 'something went wrong'
                })

        elif data['move'] == 'split':
            if data['splitterHandSide'] == 'left':
                splitter_hand = Player1.left
                recipient_hand = Player1.right
                recipient_hand_side = 'right'
            elif data['splitterHandSide'] == 'right':
                splitter_hand = Player1.right
                recipient_hand = Player1.left
                recipient_hand_side = 'left'
            
            result = Player1.split(data['amount'], splitter_hand, recipient_hand)
            if result == True:
                splitter_hand_url = f"/static/img/{data['splitterHandSide']}_{splitter_hand.get_value()}.png"
                recipient_hand_url = f"/static/img/{recipient_hand_side}_{recipient_hand.get_value()}.png"
                if Player1.left.get_value() + Player1.right.get_value() == 0:
                    game_state = 'player lost'
                elif Player2.left.get_value() + Player2.right.get_value() == 0:
                    game_state = 'player won'
                else:
                    game_state = 'continuing'
                    
                output = jsonify({
                    'isSuccessful': True,
                    'splitterHand': splitter_hand.get_value(),
                    'recipientHand': recipient_hand.get_value(),
                    'splitterHandUrl': splitter_hand_url,
                    'recipientHandUrl': recipient_hand_url,
                    'gameState': game_state,
                })
                
            else:
                output = jsonify({
                    'isSuccessful': False,
                    'errorMsg': 'something went wrong'
                })

        elif data['move'] == 'determineAmount':
            if data['splitterHandSide'] == 'left':
                splitter_hand = Player1.left
                recipient_hand = Player1.right
            elif data['splitterHandSide'] == 'right':
                splitter_hand = Player1.right
                recipient_hand = Player1.left
            if data['splitterHand'] == splitter_hand.get_value():
                if data['recipientHand'] == recipient_hand.get_value():
                    temp = Agent('temp')
                    valid_moves = temp.get_valid_moves((splitter_hand.get_value(), recipient_hand.get_value(), Player2.left.get_value(), Player2.right.get_value(), 0))
                    valid_splits = []
                    for i in range(len(valid_moves)):
                        if valid_moves[i][0] == 's':
                            valid_splits.append(valid_moves[i][2])
                    output = jsonify({
                        'isSuccessful': True,
                        'buttons': valid_splits

                    })
                else:
                    output = jsonify({
                        'isSuccessful': False,
                        'errorMsg': 'something went wrong'
                    })
            else:
                output = jsonify({
                    'isSuccessful': False,
                    'errorMsg': 'something went wrong'
                })

    else:
        if data['move'] == 'attack':
            if data['playerSide'] == 'left':
                attacker_hand = Player2.left
            else:
                attacker_hand = Player2.right
            if data['opponentSide'] == 'left':
                recipient_hand = Player1.left
            else:
                recipient_hand = Player1.right
            result = Player2.attack(attacker_hand, recipient_hand)
            if result == True:
                img_url = f"/static/img/{data['opponentSide']}_{recipient_hand.get_value()}.png"

                if Player2.left.get_value() + Player2.right.get_value() == 0:
                    game_state = 'player lost'
                elif Player1.left.get_value() + Player1.right.get_value() == 0:
                    game_state = 'player won'
                else:
                    game_state = 'continuing'

                output = jsonify({
                    'isSuccessful': True,
                    'playerHand': attacker_hand.get_value(),
                    'opponentHand': recipient_hand.get_value(),
                    'opponentImgUrl': img_url,
                    'gameState': game_state,
                })
            else:
                output = jsonify({
                    'isSuccessful': False,
                    'errorMsg': 'something went wrong'
                })

        elif data['move'] == 'split':
            print("hello")
            if data['splitterHandSide'] == 'left':
                splitter_hand = Player2.left
                recipient_hand = Player2.right
                recipient_hand_side = 'right'
            elif data['splitterHandSide'] == 'right':
                splitter_hand = Player2.right
                recipient_hand = Player2.left
                recipient_hand_side = 'left'
            
            result = Player2.split(data['amount'], splitter_hand, recipient_hand)
            if result == True:
                splitter_hand_url = f"/static/img/{data['splitterHandSide']}_{splitter_hand.get_value()}.png"
                recipient_hand_url = f"/static/img/{recipient_hand_side}_{recipient_hand.get_value()}.png"
                if Player2.left.get_value() + Player2.right.get_value() == 0:
                    game_state = 'player lost'
                elif Player1.left.get_value() + Player1.right.get_value() == 0:
                    game_state = 'player won'
                else:
                    game_state = 'continuing'
                    
                output = jsonify({
                    'isSuccessful': True,
                    'splitterHand': splitter_hand.get_value(),
                    'recipientHand': recipient_hand.get_value(),
                    'splitterHandUrl': splitter_hand_url,
                    'recipientHandUrl': recipient_hand_url,
                    'gameState': game_state,
                })
                
            else:
                output = jsonify({
                    'isSuccessful': False,
                    'errorMsg': 'something went wrong'
                })

        elif data['move'] == 'determineAmount':
            if data['splitterHandSide'] == 'left':
                splitter_hand = Player2.left
                recipient_hand = Player2.right
            elif data['splitterHandSide'] == 'right':
                splitter_hand = Player2.right
                recipient_hand = Player2.left
            if data['splitterHand'] == splitter_hand.get_value():
                if data['recipientHand'] == recipient_hand.get_value():
                    temp = Agent('temp')
                    valid_moves = temp.get_valid_moves((splitter_hand.get_value(), recipient_hand.get_value(), Player1.left.get_value(), Player1.right.get_value(), 0))
                    valid_splits = []
                    for i in range(len(valid_moves)):
                        if valid_moves[i][0] == 's':
                            valid_splits.append(valid_moves[i][2])
                    output = jsonify({
                        'isSuccessful': True,
                        'buttons': valid_splits

                    })
                else:
                    output = jsonify({
                        'isSuccessful': False,
                        'errorMsg': 'something went wrong'
                    })
            else:
                output = jsonify({
                    'isSuccessful': False,
                    'errorMsg': 'something went wrong'
                })

    print(Player1.left.get_value(), Player1.right.get_value(), Player2.left.get_value(), Player2.right.get_value())
    return output




if __name__ == '__main__':
    app.run(debug=True)