from flask import Flask, render_template, jsonify, request
from agent import Agent
from main import Player, Game

app = Flask(__name__)



@app.route('/play-against-bot', methods=['GET', 'POST'])
def index():
    return render_template('play-against-bot.html')



@app.route('/perform-move', methods=['POST'])
def perform_move():

    data = request.get_json()
    if data['move'] == 'attack':
        pass
    return 'x'



if __name__ == '__main__':
    app.run(debug=True)