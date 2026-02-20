from flask import Flask, render_template, jsonify, request, session
from agent import Agent
from main import Player, Game

app = Flask(__name__)
app.secret_key = 'HelloWorld!'

Player1 = None
Player2 = None


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')



@app.route('/play-against-bot', methods=['GET', 'POST'])
def play_against_bot():

    global Player1 
    Player1 = Player(request.form['username'])
    global Player2
    Player2 = Agent('bot')

    return render_template('play-against-bot.html',
                           name = request.form['username'],
                           game_data = {
                               'player1l': Player2.left.get_value(),
                               'player1r': Player2.right.get_value(),
                               'player2l': Player1.left.get_value(),
                               'player2r': Player1.right.get_value()
                           })



@app.route('/play-against-player', methods=['GET', 'POST'])
def play_against_player():
    return render_template('play-against-player.html')



@app.route('/perform-move', methods=['POST'])
def perform_move():

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
            if data['opponentSide'] == 'left':
                if recipient_hand.get_value() == 0:
                    img_url = '/static/img/left_0'
                elif recipient_hand.get_value() == 1:
                    img_url = '/static/img/left_1'
                elif recipient_hand.get_value() == 2:
                    img_url = '/static/img/left_2'
                elif recipient_hand.get_value() == 3:
                    img_url = '/static/img/left_3'
                elif recipient_hand.get_value() == 4:
                    img_url = '/static/img/left_4'
            elif data['opponentSide'] == 'right':
                if recipient_hand.get_value() == 0:
                    img_url = '/static/img/right_0'
                elif recipient_hand.get_value() == 1:
                    img_url = '/static/img/right_1'
                elif recipient_hand.get_value() == 2:
                    img_url = '/static/img/right_2'
                elif recipient_hand.get_value() == 3:
                    img_url = '/static/img/right_3'
                elif recipient_hand.get_value() == 4:
                    img_url = '/static/img/right_4'
            output = jsonify({
                'isSuccessful': True,
                'playerHand': attacker_hand.get_value(),
                'opponentHand': recipient_hand.get_value(),
                'opponentImgUrl': img_url
            })

    elif data['move'] == 'split':
        pass
    elif data['move'] == 'deterimneAmount':
        pass


    return output



if __name__ == '__main__':
    app.run(debug=True)