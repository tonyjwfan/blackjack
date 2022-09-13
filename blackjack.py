import random

class PlayingCard:
    """Instantiates a card complete with it's rank and suit.
    The rank and suit attributes of the card will be used for displaying 
    the graphics later.
    """
    rank_list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suit_list = ["♠", "♥", "♦", "♣"]
    
    def __init__(self, rank="", suit="", value=0):
        self.rank = rank  # we need the rank to display graphics
        self.suit = suit  # we need the suit to display graphics
        self.value = value
        
    def __repr__(self):
        if self.rank not in self.rank_list:
            return "Invalid rank!"
        elif self.suit not in ["♠", "♥", "♦", "♣"]:
            return "Invalid suit!"
        else:
            return "{} of {}".format(self.rank, self.suit)

class Deck:
    """Instantiates a Deck object complete with at least 52 standard cards in 
    a deck of cards.
    - shuffle_deck() method to randomize position of cards for dealing.
    - deal_card() method to remove a card from the deck.
    """
    rank_list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", 
                 "J", "Q", "K", "A"]
    suit_list = ["♠", "♥", "♦", "♣"]
    value = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, 
             "J":10, "Q":10, "K":10, "A":11}
    
    def __init__(self):
        self.cards = []

        for x in self.suit_list:
            for y in self.rank_list:
                val = self.value[y]
                self.cards.append(PlayingCard(y, x, val))

    def shuffle_deck(self):
        """This method will randomly shuffle the cards in a deck."""
        random.shuffle(self.cards)
    
    def deal_card(self):
        """This method will deal cards until there are no cards left
        input: self.cards
        output: last card in the deck of cards"""
        try:
            if self.cards:        
                return self.cards.pop(0)
            
        except AttributeError:
            print("There are no cards left to deal!")
    
class Role():
    
    def __init__(self):
        self.hand = []
        self.score = 0
        
    def draw_card(self, deck):
        """This method draws one card from the deck.
        inputs: Deck instance
        """
        if deck.cards:
            self.hand.append(deck.deal_card())
            
            if self.hand[-1].rank == "A" and (self.score + 11) > 21:
                self.score += 1
            else:
                self.score += self.hand[-1].value
        else:
            print("There are no more cards to draw!")

    def clear_hand_score(self):
        self.hand = []
        self.score = 0
        
class Player(Role):
    
    def __init__(self):
        super().__init__()
        self.bet = 0
        self.funds = 100
        
    def stand():
        pass
    
    def split():
        pass
    
    def insert_bet(self, bet=0):
        self.bet = bet
        self.funds -= bet
        
    def blackjack(self):
        self.funds += self.bet + self.bet * 1.5
        
    def win_hand(self):
        self.funds += self.bet + self.bet
    
    def draw_hand(self):
        self.funds += self.bet

    
class Dealer(Role):
    
    def __init__(self):
        super().__init__()

class Board():
    pass



# GAME LOGIC STARTS

def board():
    
    print("\nDealer's cards:", dealer.hand)
    print("\nDealer's score:", dealer.score)
    print("\nPlayer's cards:", hand.cards)
    print("\nPlayer's score:", hand.score)
    print("------------------------------------")
    print(f"Player's funds: {player.funds}     Player's bet: {player.bet}")

import os
def clear():
    os.system('clear')

player_action = 0
game_round = 1

deck = Deck()
player = Player()
dealer = Dealer()
deck.shuffle_deck()

def p_action(action_dict):
    """
    action_dict is a dictionary
    """
    print("Please enter one of the following: ")
    
    for action in action_list:
        print(f"\t'{action.key}' to {action}")
        
    selected_action = input("Enter now: ")
    
    return selected_action

while game_round <= 3:
    print(f"Starting round {game_round}.")

    for i in range(2):
        player.draw_card(deck)
        dealer.draw_card(deck)

    while True:
        print(f"Player funds: {player.funds}")
        bet_amount = int(input("\nHow much would you like to bet?: "))

        if bet_amount > player.funds:
            print("You cannot bet more than your funds!")
        else:
            break
    
    player.insert_bet(bet_amount)
    
    board()
    
    while True:
        
        if hand.score == 21:
            print("Blackjack! You've won!")
            player.blackjack()
            break
        
        action = input("\nPlease enter\
            \n'h' to hit\
            \n's' to stand\
            \nEnter your action: ").lower()
        
        if action == 'h':
            player.draw_card(deck)
            clear()
        elif action == 's':
            player_action = 1
            clear()
            break
        else:
            print("Please enter a valid action!")
        
        board()
        
        if hand.score == 21:
            print("\nBlackjack! You've won!")
            player.blackjack()
        elif hand.score > 21:
            print("\nBust! You've lost!")
        else:
            continue
        break
        
    if player_action:
        
        while dealer.score < 17:
            dealer.draw_card(deck)
            board()

        if dealer.score > 21:
            player.win_hand()
            print("\nDealer bust! You've won!")
        elif hand.score > dealer.score:
            player.win_hand()
            print("\nYou've beat the dealer! You've won!")
        elif hand.score == dealer.score:
            player.draw_hand()
            print("\nIt's a draw!")
        else:
            print("\nDealer wins!")
    
    if game_round < 3:
        print(len(deck.cards))
        input("\nMoving on to the next round. Press any key to continue...")
    elif game_round == 3:
        input("\nThank you for playing!")
        
    player.clear_hand_score()
    dealer.clear_hand_score()
    game_round += 1
    clear()
