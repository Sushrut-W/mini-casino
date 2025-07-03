from flask import Flask, request, jsonify
from blackjack import GameManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

game = GameManager()

@app.route('/start', methods=['POST'])
def start_game():
    data = request.get_json()
    players = data.get('players', [])
    if not players or len(players) < 1:
        return jsonify({"error": "At least one player is required"}), 400
    
    game.start(players)
    return jsonify(game.get_state())

@app.route("/bet", methods=['POST'])
def place_bet():
    data = request.get_json()
    name = data.get('name')
    amount = data.get('amount')
    game.place_bet(name, amount)
    return jsonify(game.get_state())

@app.route("/action", methods=['POST'])
def take_action():
    data = request.get_json()
    name = data.get('name')
    action = data.get('action')
    game.handle_action(name, action)
    return jsonify(game.get_state())

@app.route("/state", methods=['GET'])
def get_game_state():
    return jsonify(game.get_state())

if __name__ == '__main__':
    app.run(debug=True)