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
        pass
    return 'x'



if __name__ == '__main__':
    app.run(debug=True)