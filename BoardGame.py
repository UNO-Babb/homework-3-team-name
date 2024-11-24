from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Game Constants
player_colors = ["red", "yellow", "green", "blue"]
card_values = {str(i): i for i in range(2, 11)}
card_values.update({"7": 1, "Ace": 2, "King": 3, "Queen": 4, "Jack": 5})
player_cards = {color: [] for color in player_colors}
player_positions = {color: 0 for color in player_colors}
round_wins = {color: 0 for color in player_colors}
discarded_cards = {color: [] for color in player_colors}

# Standard deck of cards
deck = [f"{value} of {suit}" for value in card_values for suit in ["Hearts", "Diamonds", "Clubs", "Spades"]]

# Initialize game state
def deal_cards():
    global deck
    random.shuffle(deck)
    for player in player_colors:
        player_cards[player] = [deck.pop() for _ in range(7)]

def discard_cards(player, cards_to_discard):
    discarded_cards[player].extend(cards_to_discard)
    for card in cards_to_discard:
        player_cards[player].remove(card)

def play_round():
    # Each player plays a card (card values are compared, suits don't matter)
    played_cards = {}
    for player in player_colors:
        # We assume that player chooses a card here (just for simplicity, pick the first card)
        played_cards[player] = player_cards[player][0]  # This can be changed to allow player to choose
        player_cards[player].remove(player_cards[player][0])
    
    # Determine who wins the round
    round_winner = max(played_cards, key=lambda p: card_values[played_cards[p].split()[0]])
    round_wins[round_winner] += 1

def game_step():
    if all(position >= 10 for position in player_positions.values()):
        return "Game Over", None  # One player has reached the end

    return "Game Ongoing", None

@app.route('/')
def index():
    # Initialize the game state
    deal_cards()
    return render_template('index.html', player_colors=player_colors)

@app.route('/play_turn', methods=['POST'])
def play_turn():
    data = request.get_json()
    player = data['player']
    discarded_cards_for_player = data['discarded_cards']
    
    # Discard cards
    discard_cards(player, discarded_cards_for_player)
    
    # Simulate a round of the game
    play_round()
    
    # Check if anyone has won the game
    game_status, winner = game_step()
    
    return jsonify({"game_status": game_status, "round_wins": round_wins})

if __name__ == '__main__':
    app.run(debug=True)