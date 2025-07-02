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


class Player:
    def __init__(self, name:str, deposit: int):
        self.name = name
        self.balance = deposit
        self.bet = 0
        self.hand = []


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
    if len(hand) == 2 and 'A' in hand and any(card in hand for card in ['10', 'J', 'Q', 'K']):
        return True
    return False



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
    dealer[0] = 'A'
    hole_card = 'J'    
    if hasBlackjack([dealer[0], hole_card]):
        dealer[1] = hole_card
        dealerBJ(dealer, players)
        return
    clearDisplay()
    printHands(dealer, players)

# TO DO: Implement player actions (hit, stand, double down, split)

def nextRound(dealer, players):
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