import time
import os
import math
import random

MAX_PLAYERS = 5
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
    # Create a player with a name and initial deposit
    def __init__(self, name:str, deposit: int):
        self.name = name
        self.balance = deposit
        self.bet = 0
        self.hand = []
        self.holecard = ""
    
    # Hit the player with a random card from the deck
    def hit(self, deck):
        if len(deck) == 0:
            print("Deck is empty, cannot hit.")
            return None
        ind = random.randint(0, len(deck)-1)
        self.hand.append(deck[ind])
        del deck[ind]
    
    # Place a bet for the player
    def placeBet(self, amount):
        self.bet = amount

    # Dealer's holecard helper functions
    def getHoleCard(self, deck):
        if len(deck) == 0:
            print("Deck is empty, cannot hit.")
            return None
        ind = random.randint(0, len(deck)-1)
        self.holecard = deck[ind]
        del deck[ind]
        self.hand.append("X")    
    def revealHoleCard(self):
        if self.holecard == "":
            print("No hole card to reveal.")
            return None
        self.hand[1] = self.holecard
        self.holecard = ""

    # Check if the player has blackjack or busted
    def hasBlackjack(self):
        return sum(VALUE[card] for card in self.hand) == 21
    def hasBusted(self):
        return sum(VALUE[card] for card in self.hand) > 21
    
    # Print the player's hand and bet
    def printHand(self):
        print(f"{self.name} (${self.bet}): | ", end='')
        for card in self.hand:
            print(card, end=' ')
        print("|")



# Clears the terminal display
def clearDisplay():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

# Prints the current hands of the dealer and players
def printHands(dealer, players):
    print("Dealer: | ", end='')
    for card in dealer.hand:
        print(card, end=' ')
    print("|\n")

    for p in players:
        p.printHand()

# Display options for next round
def endOfRound(dealer, players):
    if not players:
        print("No players left. Exiting game.")
        return
    for p in players:
        p.hand = []
        p.placeBet(0)
        print(f"{p.name} | Balance: ${p.balance}")
    choice = input("================================\nPlay again (Y/n): ")[0]
    if choice == "Y":
        clearDisplay()
        startRound(players)
    elif choice == 'n':
        print("Thanks for playing!")
    else:
        print("You're bad at following directions aren't you?")
        endOfRound(dealer, players)


# GAME PLAN:
# 1. Place bets
# 2. Deal player and dealer hands
# 3. If dealer has blackjack, handle it, end game
#    If dealer does not have blackjack, call playerActions()
def startRound(players):
    # 1) Place bets
    for p in players:
        print(f"================================\n{p.name} | Balance: {p.balance}")
        while True:
            bet = int(input("Enter bet amount: "))
            if bet > p.balance or bet < 1:
                print("!-- Enter valid bet amount --!")
            else:
                p.placeBet(bet)
                break
    
    # 2) Deal hands + holecard
    deck = STD_DECK.copy()
    dealer = Player("Dealer", 0)
    dealer.hit(deck)
    for p in players:
        p.hit(deck)    
    dealer.getHoleCard(deck)
    for p in players:
        p.hit(deck)

    # 3) Handle dealer blackjack
    if VALUE[dealer.hand[0]] + VALUE[dealer.holecard] == 21:
        dealer.revealHoleCard()
        dealerBJ(dealer, players)
    else:
        playerActions(dealer, players, deck)


# The dealer has blackjack
# Check if players have blackjack or not
# If they do, it's a push, if not, they lose their bet
# End and start next round
def dealerBJ(dealer, players):
    clearDisplay()
    print("_________________________\n\ Dealer has BLACKJACK! /\n -----------------------")
    broke = []
    for p in players:
        p.printHand()
        if p.hasBlackjack():
            print(f" --> Push  | Balance: ${p.balance}")
        else:
            p.balance -= p.bet
            print(f" --> Lost ${p.bet} | New Balance: ${p.balance}")
        p.placeBet(0)
    
    for p in players:
        if p.balance <= 0:
            print(f"!-- {p.name} is out of money --!")
            broke.append(p)
    for p in broke:
        players.remove(p)
    endOfRound(dealer, players)


# Player actions: Hit, Stand, Double Down (split in next iteration of game)
def playerActions(dealer, players, deck):
    clearDisplay()
    printHands(dealer, players)
    
    for p in players:
        print("================================")
        action = 0
        while True:
            if p.hasBlackjack():
                print(f"{p.name} has BLACKJACK!")
                break
            elif p.hasBusted():
                print(f"{p.name} has BUSTED!")
                break
            
            message = f"{p.name}, choose action (h: hit, s: stand, d: double down): " if action == 0 else f"{p.name}, choose action (h: hit, s: stand): "
            choice = input(message).lower()[0]
            if choice == 'h':
                p.hit(deck)
                clearDisplay()
                printHands(dealer, players)
                action += 1
            elif choice == 's':
                break
            elif choice == 'd':
                if p.balance >= p.bet * 2:
                    p.placeBet(p.bet * 2)
                    p.hit(deck)
                    clearDisplay()
                    printHands(dealer, players)
                    break
                else:
                    print("!-- Not enough balance to double down --!")
            else:
                print("!-- Invalid choice --!")
    dealerActions(dealer, players, deck)


def dealerActions(dealer, players, deck):
    clearDisplay()
    print("____________________________\n\      Dealer's turn!      /\n --------------------------")
    dealer.revealHoleCard()
    printHands(dealer, players)
    while sum(VALUE[card] for card in dealer.hand) < 17:
        time.sleep(1)
        clearDisplay()
        print("____________________________\n\      Dealer's turn!      /\n --------------------------")
        dealer.hit(deck)
        printHands(dealer, players)
    
    # Dealer has dealt all cards, check scores
    dealerScore = sum(VALUE[card] for card in dealer.hand)
    if dealerScore > 21:
        print("\n======================\n  Dealer has BUSTED!\n======================")
        for p in players:
            if p.hasBusted():
                print(f"== {p.name} has BUSTED! You lose ${p.bet}. ==")
                p.balance -= p.bet
                p.placeBet(0)
            elif p.hasBlackjack():
                print(f"== {p.name} has BLACKJACK! You win ${math.floor(p.bet * 1.5)}! ==")
                p.balance += math.floor(p.bet * 1.5)
                p.placeBet(0)
            else:
                print(f"== {p.name} wins ${p.bet}! ==")
                p.balance += p.bet
                p.placeBet(0)
    elif dealerScore == 21:
        print("\n========================\n\  Dealer has BLACKJACK!\n========================")
        for p in players:
            if p.hasBlackjack():
                print(f"== {p.name} has BLACKJACK! It's a push. ==")
            else:
                print(f"== {p.name} loses ${p.bet}. ==")
                p.balance -= p.bet
                p.placeBet(0)
    else:
        print(f"\n======================\n  Dealer's score: {dealerScore}\n======================")
        for p in players:
            if p.hasBusted():
                print(f"== {p.name} has BUSTED! You lose ${p.bet}. ==")
                p.balance -= p.bet
                p.placeBet(0)
            elif p.hasBlackjack():
                print(f"== {p.name} has BLACKJACK! You win ${math.floor(p.bet * 1.5)}! ==")
                p.balance += math.floor(p.bet * 1.5)
                p.placeBet(0)
            elif sum(VALUE[card] for card in p.hand) > dealerScore:
                print(f"== {p.name} wins ${p.bet}! ==")
                p.balance += p.bet
                p.placeBet(0)
            elif sum(VALUE[card] for card in p.hand) < dealerScore:
                print(f"== {p.name} loses ${p.bet}. ==")
                p.balance -= p.bet
                p.placeBet(0)
            else:
                print(f"== {p.name} ties with the dealer. It's a push. ==")
    print()
    endOfRound(dealer, players)
        




def main():
    clearDisplay()
    # Initializing players
    while True:
        num_players = input("Enter number of players: ")
        if num_players.isdigit() and int(num_players) > 0:
            if int(num_players) <= MAX_PLAYERS:
                num_players = int(num_players)
                break
            else:
                print("!-- Too many players. Limit 5 player per table --!\n")
        else:
            print("!-- Enter a valid number of players --!\n")
    
    players = []
    for i in range(num_players):
        name = input(f"Enter player {i+1} name: ")
        deposit = int(input("Enter initial deposit amount: "))
        p = Player(name, deposit)
        players.append(p)
    clearDisplay()

    while True:
        print("=============================================\nAdded players:\n|", end="")
        for p in players:
            print(f" {p.name}, ${p.balance} |", end='')
        choice = input("\nPress ENTER to play blackjack (q to quit): ")
        if len(choice) == 0:
            clearDisplay()
            startRound(players)
            break
        elif choice[0] == 'q':
            print("Would've hit it big on the next hand...\nBetter luck next time.\n")
            break
        else:
            print("You're bad at following directions aren't you?")


main()