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
    global Player1
    global Player2
    global q_values


    data = request.get_json()
    print(data['move'])
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
                Player2.make_move((Player1.left.get_value(), Player1.right.get_value(), Player2.left.get_value(), Player2.right.get_value(), 1), q_values, Player1) #assuming that the bot is always 2nd to play
                if Player1.left.get_value() + Player1.right.get_value() == 0:
                    game_state = 'player lost bot'
                elif Player2.left.get_value() + Player2.right.get_value() == 0:
                    game_state = 'player won bot'

            output = jsonify({
                'isSuccessful': True,
                'playerHand': attacker_hand.get_value(),
                'opponentHand': recipient_hand.get_value(),
                'opponentImgUrl': img_url,
                'errorMsg': 'Something went wrong',
                'handsAfter': [Player1.left.get_value(), Player1.right.get_value(), Player2.left.get_value(), Player2.right.get_value()],
                'gameState': game_state,
                'handsAfterUrl': [f"/static/img/left_{Player1.left.get_value()}.png", f"/static/img/right_{Player1.right.get_value()}.png", f"/static/img/left_{Player2.left.get_value()}.png", f"/static/img/right_{Player2.right.get_value()}.png"]
            })

    elif data['move'] == 'split':
        pass
    elif data['move'] == 'deterimneAmount':
        pass


    return output

def get_url(p1l, p1r, p2l, p2r):
    return 

if __name__ == '__main__':
    app.run(debug=True)