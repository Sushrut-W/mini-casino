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
    def __init__(self, name:str, deposit: int):
        self.name = name
        self.balance = deposit
        self.bet = 0
        self.hand = []
        self.action = 'z'


def clearDisplay():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def printHands(dealer, players):
    print("Dealer: | ", end='')
    for card in dealer:
        print(card, end=' ')
    print("|\n")

    for p in players:
        print(f"{p.name} (${p.bet}): | ", end='')
        for card in p.hand:
            print(card, end=' ')
        print("|")


def hasBlackjack(hand):
    if sum(VALUE[card] for card in hand) == 21:
        return True
    return False


def playerActions(dealer, players, deck, hole_card):
    clearDisplay()
    printHands(dealer, players)
    left_standing = len(players)
    for p in players:
        print("================================")
        if hasBlackjack(p.hand):
            print(f"{p.name} has BLACKJACK!")
            continue
        while True:
            action = input(f"{p.name}, choose your action (h: hit, s: stand, d: double down): ")[0].lower()
            # player hits
            if action == 'h':
                ind = random.randint(0, len(deck)-1)
                p.hand.append(deck[ind])
                del deck[ind]
                print(f"{p.name} hits and draws {p.hand[-1]}")
                if hasBlackjack(p.hand):
                    print(f"{p.name} has BLACKJACK!")
                    break
                elif sum(VALUE[card] for card in p.hand) > 21:
                    print(f"{p.name} busts! You lose ${p.bet}")
                    p.balance -= p.bet
                    p.bet = 0
                    left_standing -= 1
                    break
                #
                # NEED TO BE ABLE TO HIT REPEATEDLY
                #

            # player stands
            elif action == 's':
                print(f"{p.name} stands with {sum(VALUE[card] for card in p.hand)}")
                break
            #player doubles down
            elif action == 'd':
                if p.balance < p.bet*2:
                    print("!-- Not enough balance to double down --!")
                else:
                    p.bet *= 2
                    ind = random.randint(0, len(deck)-1)
                    p.hand.append(deck[ind])
                    del deck[ind]
                    break
            else:
                print("!-- Invalid action. Please choose again --!")
    print("================================\nAll players have acted. Dealer's hole card is .")
    dealer[1] = hole_card
    printHands(dealer, players)
    dealerActions(dealer, players, deck)
    
    
    
    # call dealerActions() after all players have acted
    # dealerActions() takes care of returning bets for
        # push
        # player blackjack
        # dealer busts
    # inside dealerActions(), call nextRound() after dealer's turn is over


def startGame(players):
    # place bets
    for p in players:
        print(f"================================\n{p.name} | Balance: {p.balance}")
        while True:
            bet = int(input("Enter bet amount: "))
            if bet > p.balance or bet < 1:
                print("!-- Enter valid bet amount --!")
            else:
                p.bet = bet
                break
    
    # first card
    deck = STD_DECK.copy()
    ind = random.randint(0, len(deck)-1)
    dealer = [deck[ind], "X"]
    del deck[ind]
    for p in players:
        ind = random.randint(0, len(deck)-1)
        p.hand.append(deck[ind])
        del deck[ind]
    # second card
    hole_ind = random.randint(0, len(deck)-1)
    hole_card = deck[hole_ind]
    del deck[hole_ind]
    for p in players:
        ind = random.randint(0, len(deck)-1)
        p.hand.append(deck[ind])
        del deck[ind]
    
    # handle dealer blackjack
    if hasBlackjack([dealer[0], hole_card]):
        dealer[1] = hole_card
        dealerBJ(dealer, players)
        return
    playerActions(dealer, players, deck, hole_card)

# TO DO:
# Implement player actions (hit, stand, double down, split)
# Implement dealer actions (hit until 17 or higher)

def nextRound(dealer, players):
    if not players:
        print("No players left. Exiting game.")
        return
    for p in players:
        p.hand = []
        p.bet = 0
    print("================================\nPress ENTER to continue to next round (q to quit): ", end='')
    choice = input()
    if len(choice) == 0:
        clearDisplay()
        startGame(players)
    elif choice[0] == 'q':
        print("Thanks for playing! Better luck next time.")
    else:
        print("You're bad at following directions aren't you?")
        nextRound(dealer, players)



def dealerBJ(dealer, players):
    clearDisplay()
    print("_________________________\n\ Dealer has BLACKJACK! /\n -----------------------")
    broke = []
    for p in players:
        print(f"{p.name}: | ", end='')
        for card in p.hand:
            print(card, end=' ')
        print("|", end='')
        if hasBlackjack(p.hand):
            print(f" --> Push  | Balance: ${p.balance}")
        else:
            p.balance -= p.bet
            print(f" --> Lost ${p.bet} | New Balance: ${p.balance}")
        p.bet = 0
    
    for p in players:
        if p.balance <= 0:
            print(f"!-- {p.name} is out of money --!")
            broke.append(p)
    for p in broke:
        players.remove(p)
    nextRound(dealer, players)


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
            startGame(players)
            break
        elif choice[0] == 'q':
            print("Would've hit it big on the next hand...\nBetter luck next time.")
            break
        else:
            print("You're bad at following directions aren't you?")




main()