import random
import time
import math

STD_DECK = ['2', '2', '2', '2', '3', '3', '3', '3',
        '4', '4', '4', '4', '5', '5', '5', '5',
        '6', '6', '6', '6', '7', '7', '7', '7',
        '8', '8', '8', '8', '9', '9', '9', '9',
        '10', '10', '10', '10', 'J', 'J', 'J', 'J',
        'Q', 'Q', 'Q', 'Q', 'K', 'K', 'K', 'K',
        'A', 'A', 'A', 'A']

VALUE = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
         '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

class Player:
    def __init__(self, name, deposit):
        self.name = name
        self.balance = deposit
        self.bet = 0
        self.hand = []
        self.holecard = ""
        self.standing = False

    def hit(self, deck):
        if deck:
            self.hand.append(deck.pop(random.randint(0, len(deck)-1)))

    def place_bet(self, amount):
        self.bet = amount

    def get_holecard(self, deck):
        if deck:
            self.holecard = deck.pop(random.randint(0, len(deck)-1))
            self.hand.append("?")

    def reveal_holecard(self):
        if self.holecard:
            self.hand[1] = self.holecard
            self.holecard = ""

    def has_blackjack(self):
        return self.get_score() == 21

    def has_busted(self):
        return self.get_score() > 21

    def get_score(self):
        total = 0
        aces = 0
        for card in self.hand:
            if card == "?": continue
            val = VALUE[card]
            total += val
            if card == 'A': aces += 1
        while total > 21 and aces:
            total -= 10
            aces -= 1
        return total

    def to_dict(self):
        return {
            "name": self.name,
            "balance": self.balance,
            "bet": self.bet,
            "hand": self.hand,
            "score": self.get_score(),
            "blackjack": self.has_blackjack(),
            "busted": self.has_busted(),
            "standing": self.standing
        }

class GameManager:
    def __init__(self):
        random.seed(int(time.time()))
        self.deck = []
        self.dealer = Player("Dealer", 0)
        self.players = []
        self.current_player = 0
        self.state = "waiting"

    def start(self, players):
        self.deck = STD_DECK.copy()
        random.shuffle(self.deck)
        self.players = [Player(p["name"], p["deposit"]) for p in players]
        self.dealer = Player("Dealer", 0)
        self.state = "playing"

        # Deal first card to each
        for p in self.players: p.hit(self.deck)
        self.dealer.hit(self.deck)
        for p in self.players: p.hit(self.deck)
        self.dealer.get_holecard(self.deck)

    def place_bet(self, name, amount):
        for p in self.players:
            if p.name == name:
                if 0 < amount <= p.balance:
                    p.place_bet(amount)

    def handle_action(self, name, action):
        player = next((p for p in self.players if p.name == name), None)
        if not player or player.standing:
            return
        
        if action == "hit":
            player.hit(self.deck)
            if player.has_busted():
                player.standing = True
        elif action == "stand":
            player.standing = True
        elif action == "double":
            if player.balance >= player.bet * 2:
                player.place_bet(player.bet * 2)
                player.hit(self.deck)
                player.standing = True
        
        if all(p.standing or p.has_busted() for p in self.players):
            self.dealer_turn()

    def dealer_turn(self):
        self.dealer.reveal_holecard()
        while self.dealer.get_score() < 17:
            self.dealer.hit(self.deck)
        self.resolve_bets()
        self.state = "finished"

    def resolve_bets(self):
        dealer_score = self.dealer.get_score()
        for p in self.players:
            if p.has_busted():
                p.balance -= p.bet
            elif p.has_blackjack() and not self.dealer.has_blackjack():
                p.balance += math.floor(p.bet * 1.5)
            elif self.dealer.has_busted() or p.get_score() > dealer_score:
                p.balance += p.bet
            elif p.get_score() < dealer_score:
                p.balance -= p.bet
            # else: push, no change
            p.bet = 0

    def get_state(self):
        return {
            "state": self.state,
            "dealer": self.dealer.to_dict(),
            "players": [p.to_dict() for p in self.players]
        }