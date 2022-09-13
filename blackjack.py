import os
import random

class PlayingCard:
    """Instantiates a card complete with it's rank and suit.
    The rank and suit attributes of the card will be used for displaying 
    the graphics later.
    """
    # list of possible card ranks
    rank_list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    # list of possible card suits
    suit_list = ["♠", "♥", "♦", "♣"]
    
    def __init__(self, rank: str="", suit: str="", value: int=0):
        """Initialize class variables.
        Args:
            rank: the rank of a card
            suit: the suit of a card
            value: 
            
        Returns:
        """
        self.rank = rank  # rank of the card for displaying graphics
        self.suit = suit  # suit of the card for displaying graphics
        self.value = value  # numerical value of the card for calculations
        
    def __repr__(self):
        """Display information about the card."""
        # ensure card has a proper rank
        if self.rank not in self.rank_list:
            return "Invalid rank!"
        # ensure card has a proper suit
        elif self.suit not in ["♠", "♥", "♦", "♣"]:
            return "Invalid suit!"
        # display information about the card
        else:
            return "{} of {}".format(self.rank, self.suit)

class Deck:
    """Instantiates a Deck object complete with at least 52 standard cards in 
    a deck of cards.
    - shuffle_deck() method to randomize position of cards for dealing.
    - deal_card() method to remove a card from the deck.
    """
    # list of possible card ranks
    rank_list = ["2", "3", "4", "5", "6", "7", "8", "9", "10", 
                 "J", "Q", "K", "A"]
    # list of possible card suits
    suit_list = ["♠", "♥", "♦", "♣"]
    # dictionary of card ranks their numerical values
    value = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, 
             "J":10, "Q":10, "K":10, "A":11}
    
    def __init__(self):
        """Initialize class variables."""
        # start with no cards
        self.cards = []
        # specify number of decks to use
        self.num_decks = 5
        
        # populate the deck
        while self.num_decks > 0:
            for x in self.suit_list:
                for y in self.rank_list:
                    val = self.value[y]
                    self.cards.append(PlayingCard(y, x, val))
            self.num_decks -= 1

    def shuffle_deck(self):
        """Randomly shuffle the cards in a deck."""
        random.shuffle(self.cards)
    
    def deal_card(self):
        """This method will deal cards until there are no cards left.
        
        Raises:
            AttributeError: If there are no cards in the deck left to deal.
        """
        # try to deal a card from the deck
        try:
            if self.cards:        
                return self.cards.pop(0)
        # raise error if there are no cards left
        except AttributeError:
            print("There are no cards left to deal!")
    
        
class Hand():
    """Instantiates a blackjack hand complete with drawing cards, evaluating
    aces, and updating the score of the current hand.
    """
    def __init__(self):
        """Initialize class variables."""
        # a list to store cards
        self.cards = []
        # store score of hand
        self.score = 0
        
    def evaluate_aces(self, ace):
        """Determines the value of the ace.
        
        Args:
            ace: a PlayingCard object with an Ace rank
        """
        # overwrites the value of the ace PlayingCard object
        if (self.score + 11) > 21:
            ace.value = 1
            
    def update_score(self):
        """Update the score of the current hand"""
        # clear the score of the hand
        self.score = 0
        # calculate the score of the hand
        for card in self.cards:
            self.score += card.value
            
    def draw_card(self, deck):
        """This method draws one card from the deck.
        
        Args: Deck instance
        """
        # deal a card from the deck to the hand
        if deck.cards:
            card = deck.deal_card()
            # evaluate the aces 
            if card.rank == "A":
                self.evaluate_aces(card)
            # add card to the hand
            self.cards.append(card)
            # update the score of the hand
            self.update_score()
        # alert if there are no cards left in the deck
        else:
            print("There are no more cards to draw!")

    def clear_cards_score(self):
        """Clear hand."""
        # clear cards in the hand
        self.cards = []
        # clear the score of the current hand
        self.score = 0

class Strategy:
    """Instantiates a strategy recommender to recommend the next move to the
    player based on the current situation in the game."""
    
    def __init__(self, dealer_card: str, player_ranks: list, player_values: list):
        """Initiating Strategy class with attributes
        
        Args:
            dealer_card: rank of face up card in dealer's hand
            player_ranks: list of ranks of the cards in player's hand
            player_values: list of values of the in the player's hand
        """
        self.dealer_card = dealer_card
        self.player_ranks = player_ranks
        self.player_values = player_values
        
    def basic_strategy(self) -> str:
        """Recommend a player action based on the Basic Strategy of Blackjack.
        
        Returns:
            Player action based on Basic Strategy
        """
        self.split_flag = 0
        self.soft_flag = 0
        self.action = ""
        
        # strategy for if the initial 2 player cards is a pair
        if len(self.player_ranks) == 2 and self.player_ranks[0] == self.player_ranks[1]:
            self.split_flag = 1
            if self.player_ranks[0] in ["A","8"]:
                self.action = "Split"
            elif self.player_ranks[0] == "9" and self.dealer_card in ["2","3","4","5","6","8","9"]:
                self.action = "Split"
            elif self.player_ranks[0] == "9" and self.dealer_card == "7":
                self.action = "Stand"
            elif self.player_ranks[0] == "7" and self.dealer_card in ["2","3","4","5","6","7"]:
                self.action = "Split" 
            elif self.player_ranks[0] == "6" and self.dealer_card in ["2","3","4","5","6"]:
                self.action = "Split"
            elif self.player_ranks[0] == "5" and self.dealer_card in ["2","3","4","5","6","7","8","9"]:
                self.action = "Split"
            elif self.player_ranks[0] == "4" and self.dealer_card in ["5", "6"]:
                self.action = "Split"
            elif self.player_ranks[0] == "3" and self.dealer_card in ["2","3","4","5","6","7"]:
                self.action = "Split"
            elif self.player_ranks[0] == "2" and self.dealer_card in ["2","3","4","5","6","7"]:
                self.action = "Split"
            else:
                self.action = "Hit"
            
        # strategy for soft totals, when one of initial player cards is an ace
        if "A" in self.player_ranks[0:2] and self.split_flag == 0:
            self.soft_flag = 1
            if sum(self.player_values) == 20:
                self.action = "Stand"
            elif sum(self.player_values) == 19:
                if self.dealer_card == "6":
                    self.action = "Double Down"
                else:
                    self.action = "Stand"
            elif sum(self.player_values) == 18:
                if self.dealer_card in ["2","3","4","5","6"]:
                    self.action = "Double Down"
                elif self.dealer_card in ["9","10","J","Q","K", "A"]:
                    self.action = "Hit"
                else:
                    self.action = "Stand"
            elif sum(self.player_values) == 17:
                if self.dealer_card in ["3","4","5","6"]:
                    self.action = "Double Down"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) == 16:
                if self.dealer_card in ["4","5","6"]:
                    self.action = "Double Down"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) == 15:
                if self.dealer_card in ["4","5","6"]:
                    self.action = "Double Down"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) == 14:
                if self.dealer_card in ["5","6"]:
                    self.action = "Double Down"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) == 13:
                if self.dealer_card in ["5","6"]:
                    self.action = "Double Down"
                else:
                    self.action = "Hit"
        
        # strategy for hard totals, when the inital 2 player cards are not aces and is not a pair
        if self.split_flag == 0 and self.soft_flag == 0:
            if sum(self.player_values) >= 17:
                self.action = "Stand"
            elif sum(self.player_values) == 16:
                if self.dealer_card in ["2","3","4","5","6"]:
                    self.action = "Stand"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) == 15:
                if self.dealer_card in ["2","3","4","5","6"]:
                    self.action = "Stand"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) == 14:
                if self.dealer_card in ["2","3","4","5","6"]:
                    self.action = "Stand"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) == 13:
                if self.dealer_card in ["2","3","4","5","6"]:
                    self.action = "Stand"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) == 12:
                if self.dealer_card in ["4","5","6"]:
                    self.action = "Stand"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) == 11:
                self.action = "Double Down"
            elif sum(self.player_values) == 10:
                if self.dealer_card in ["2","3","4","5","6","8","9"]:
                    self.action = "Double Down"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) == 9:
                if self.dealer_card in ["3","4","5","6"]:
                    self.action = "Double Down"
                else:
                    self.action = "Hit"
            elif sum(self.player_values) <= 8:
                self.action = "Hit"
                
        return self.action

class Counter:
    """Instantiate a card counter object based on Blackjack card counting
    strategy.
    """
    def __init__(self, current_count: int, dealer_cards: list, player_hands: list, 
                 decks_remaining: int, betting_unit: int):
        """Initiating class with attributes.
        
        Args:
            current_count: the current count of the round
            dealer_cards: current cards in the dealer's hand
            player_hands: current cards in the player's hand
            decks_remaining: number of decks remaining
            betting_unit: the amount to bet
        """
        self.current_count = current_count
        self.dealer_cards = dealer_cards
        self.player_hands = player_hands 
        self.decks_remaining = decks_remaining
        self.betting_unit = betting_unit
        
        self.running_count = 0
    
    def count_strategy(self):
        """Calculate the current count.
        
        Returns: 
            The true count of cards.
        """
        # adjust the count based on the cards in the dealer's hand
        for card in self.dealer_cards:
            if card.rank in ["2","3","4","5","6"]:
                self.running_count += 1
            elif card.rank in ["10", "J", "Q", "K","A"]:
                self.running_count -= 1
        
        # adjust the count based on the cards in the player's hand
        for hand in self.player_hands:
            for card in hand.cards:
                if card.rank in ["2","3","4","5","6"]:
                    self.running_count += 1
                elif card.rank in ["10", "J", "Q", "K","A"]:
                    self.running_count -= 1
        
        # true count is running count integer divided by the decks remaining
        true_count = self.running_count//self.decks_remaining
        
        return self.current_count + true_count 

    def bet_strategy(self) -> int:
        """Recommends the amount to be based on the current count.
        
        Returns:
            Amount to bet next round.
        """
        # calculate the amount to bet
        amount_to_bet = (self.current_count - 1) * self.betting_unit
        
        return amount_to_bet
    
# GAME LOGIC STARTS

class Game:
    """Instantiates the core Blackjack game object."""
    
    def __init__(self):
        """Initialize class with attributes."""
        self.player_action = 0
        self.game_round = 1
        self.action = ""
        
        self.deck = Deck()
        self.dealer = Hand()
        self.player_hands = [Hand()]

        self.split_flag = 0
        self.split_store = []
        
        self.funds = 1000
        self.bet = 0
        self.count = 0
        self.betting_unit = 100
        
    def insert_bet(self, bet_amount=0):
        """Executes the bet the user specified.
        
        Args:
            bet_amount: the amount to bet
        """
        # check to see if player has funds
        self.funds > 0
        # 
        self.bet += bet_amount
        self.funds -= bet_amount
    
    def blackjack(self):
        """add 1.5 * bet to funds"""
        self.funds += self.bet + self.bet * 1.5
        
    def win_hand(self):
        self.funds += self.bet + self.bet
    
    def player_dealer_draw(self):
        self.funds += self.bet
        
    def clear(self):
        """Clears the playing board"""
        os.system('clear')
    
    def card_template(self, rank="", suit="", hidden=1):
        if hidden == 1:
            template = ['┌───┐',
                        '│░░░│',
                        '│░░░│',
                        '└───┘']
        elif rank == "10":
            template = ['┌───┐',
                        f'│ {rank}│',
                        f'│ {suit} │',
                        '└───┘']
        else:
            template = ['┌───┐',
                        f'│ {rank} │',
                        f'│ {suit} │',
                        '└───┘']
        return template
    
    def template_print(self, template_list):
        for i in range(4):
            count = 0
            for template in template_list:
                if count < len(template_list)-1:
                    print(template[i], end=" ")
                    count += 1
                else:
                    print(template[i])
    
    def add_template_list(self, cards, dealer=1):
        template_list = []
        
        if dealer == 1:
            for card in cards:
                if cards.index(card) == 0:
                    template_list.append(self.card_template(card.rank, card.suit, 1))
                else:
                    template_list.append(self.card_template(card.rank, card.suit, 0))
        else:
            for card in cards:
                template_list.append(self.card_template(card.rank, card.suit, 0))
                
        return template_list
        
    def board(self, strategy):
        """prints out board
        hand is a Hand instance from self.player_hands list"""
        
        print("Dealer's cards:")
        
        if self.player_action == 0:
            self.template_print(self.add_template_list(self.dealer.cards, 1))
            print("Dealer's score:", self.dealer.score - self.dealer.cards[0].value)
        else:
            self.template_print(self.add_template_list(self.dealer.cards, 0))
            print("Dealer's score:", self.dealer.score)
            
        print("\nPlayer's cards:")
        self.template_print(self.add_template_list(self.player_hands[0].cards, 0))
        print("Player's score:", self.player_hands[0].score)
        
        if self.split_flag == 1:
            print("\nSplit cards:")
            self.template_print(self.add_template_list(self.player_hands[1].cards, 0))
            print("\nSplit score", self.player_hands[1].score)

        print("\n-----------------------------------------------")
        print(f"Player's funds: {self.funds}     Player's bet: {self.bet}")
        print(f"\nStrategy: You should {strategy}!")

    def p_action(self, action_dict):
        """prints the actions available according to action_dict dictionary"""
        print("\nPlease enter one of the following: ")  
        for action in action_dict.keys():
            print(f"\t'{action}' to {action_dict[action]}")   
        selected_action = input("Enter your action: ")
        return selected_action
    
    def clear_player_hands(self):
        self.player_hands = []

    def core_player_logic(self, bet_amount):
        # each hand is played to completion
        for hand in self.player_hands:
              
            # drawing card logic
            if self.split_flag == 0:
                # draw 2 cards if not playing a split
                hand.draw_card(self.deck)
                hand.draw_card(self.deck)
            elif self.split_flag == 1:
                # each split hand takes appropriate split card
                if self.player_hands.index(hand) == 0:
                    hand.cards.append(self.split_store[0])
                elif self.player_hands.index(hand) == 1:
                    hand.cards.append(self.split_store[1])
                # draw one card in addition to the split card
                hand.draw_card(self.deck)
                
            while self.action != "q":
                # keeps asking the player for actions until player chooses
                # stand or double down
                # prevents overusing break

                self.clear()
                
                strategy = Strategy(self.dealer.cards[1], [x.rank for x in hand.cards], [x.value for x in hand.cards])
                self.board(strategy.basic_strategy())
                
                # for testing
                #print([x.rank for x in hand.cards])
                #print([x.value for x in hand.cards])
                
                if hand.score == 21:
                    print("Blackjack! You've won!")
                    self.blackjack()
                    break
                
                # hand can choose 'double' and 'split' if circumstances are met
                
                if hand.score <= 11 and (hand.cards[0].rank == hand.cards[1].rank) and len(hand.cards) == 2:
                    action_dict = {'h':'Hit', 's':'Stand', 'd':'Double Down', 'x': 'Split'}
                elif hand.score <= 11:
                    action_dict = {'h':'Hit', 's':'Stand', 'd':'Double Down'}
                elif hand.cards[0].rank == hand.cards[1].rank and len(hand.cards) == 2:
                    action_dict = {'h':'Hit', 's':'Stand', 'x':'Split'}
                else:
                    action_dict = {'h':'Hit', 's':'Stand'}

                self.action = self.p_action(action_dict)
                if self.action not in action_dict.keys():
                    if self.action == "q":
                        return
                    else:
                        print("Please enter a valid action!")
                    continue
                
                # logic for the action the player chooses
                if self.action == 'h':
                    hand.draw_card(self.deck)
                elif self.action == 's':
                    #self.player_action = 1
                    break
                elif self.action == 'd':
                    self.insert_bet(bet_amount)
                    hand.draw_card(self.deck)
                    #self.player_action = 1
                    break
                elif self.action == 'x':
                    self.funds -= self.bet
                    self.player_hands.append(Hand())
                    self.split_flag = 1
                    self.split_store.append(hand.cards[0])
                    self.split_store.append(hand.cards[1])
                    self.clear()
                    hand.clear_cards_score()
                    return  # exit out of function
                else:
                    print("Please enter a valid action!")
                
                if hand.score == 21:
                    self.clear()
                    self.board(strategy.basic_strategy())
                    print("\nBlackjack! You've won!")
                    self.blackjack()
                    break
                elif hand.score > 21:
                    self.clear()
                    self.board(strategy.basic_strategy())
                    print("\nBust! You've lost!")
                    break
                
                self.clear()
        
        self.player_action = 1
        
        for hand in self.player_hands:
                    
            if self.player_action == 1 and hand.score < 21:
                self.clear()
                while self.dealer.score < 17:
                    self.dealer.draw_card(self.deck)
                
                self.board(strategy.basic_strategy())

                if hand.score != 21:
                    if hand.score > 21:
                        self.clear()
                        self.board(strategy.basic_strategy())
                        print("\nBust! You've lost!")
                    elif self.dealer.score > 21:
                        self.win_hand()
                        print("\nDealer bust! You've won!")
                    elif hand.score > self.dealer.score:
                        self.win_hand()
                        print("\nYou've beat the dealer! You've won!")
                    elif hand.score == self.dealer.score:
                        self.player_dealer_draw()
                        print("\nIt's a draw!")
                    else:
                        print("\nDealer wins!")
                else:
                    print("Blackjack! You won!")
            
            #if self.split_flag == 1:
            #    input("\nPlaying the split hand now. Press any key to continue...")
            #elif self.split_flag == 0:
            #    action = input("\nEnter 'n' for the next round or enter 'q' to quit game: ")
            #    if action == "q":
            #        self.action = "q"
            #        return
            
            action = input("\nEnter 'n' for the next round or enter 'q' to quit game: ")
            if action == "q":
                self.action = "q"
                return
            
        self.player_action = 0
        self.clear()
            
    def new_game(self):
        
        # main loop
        # keeps running the game until some user action is detected
        while self.action != "q":
    
            # entering the bet
            while True:
                self.clear()
                print(f"Player funds: {self.funds}")
                print(f"The true count is: {self.count}")
                
                counter = Counter(self.count, self.dealer.cards, self.player_hands, 1, self.betting_unit)
                
                if self.count > 1:
                    print(f"Strategy: You should bet: {counter.bet_strategy()}")
                else:
                    print("Strategy: You should bet the minimum: 50")
                
                try:
                    bet_amount = abs(int(input("\nHow much would you like to bet?: ")))
                    
                except:
                    action = input("Please enter a valid numerical amount! \
                        \nPress the 'enter' key to continue or 'q' to quit... ")
                    if action == "q":
                        break
                    continue
                
                self.clear()
                if bet_amount > self.funds:
                    print("You cannot bet more than your funds!")
                else:
                    break
            
            
            self.insert_bet(bet_amount)
            
            self.deck.shuffle_deck()
            self.dealer.draw_card(self.deck)
            self.dealer.draw_card(self.deck)
            
            self.player_hands = [Hand()]
            
            self.core_player_logic(bet_amount)
            
            if self.split_flag == 1:
                self.core_player_logic(bet_amount)
            
            # for testing: number of decks should be higher
            counter = Counter(self.count, self.dealer.cards, self.player_hands, 1, self.betting_unit)
            self.count = counter.count_strategy()
            
            self.split_flag = 0
            self.split_store = []
            self.dealer.clear_cards_score() 
            self.clear_player_hands()
            self.bet = 0
        
        print("Thanks for playing the game!")
        return

class Engine:
    
    print("Welcome to Blackjack!")
    print("Please enter the following:\n\
        \t'n' to start a new game\n\
        \t'r' to see the game rules\n\
        \tAny other key to quit")
    
    action = input("Please enter your choice: ")

    if action == "n":
        start = Game()
        start.new_game()
    elif action == "r":
        print("Rules of Tony's Blackjack:\
            \n- The goal of blackjack is to beat the dealer's hand without going over 21.\
            \n- Face cards are worth 10. Aces are worth 1 or 11, whichever makes a better hand.\
            \n- Each player starts with two cards, one of the dealer's cards is hidden until the end.\
            \n- To 'Hit' is to ask for another card. To 'Stand' is to hold your total and end your turn.\
            \n- If you go over 21 you bust, and the dealer wins regardless of the dealer's hand.\
            \n- If you are dealt 21 from the start (Ace & 10), you got a blackjack.\
            \n- Blackjack usually means you win 1.5 the amount of your bet.\
            \n- Dealer will hit until his/her cards total 17 or higher.\
            \n- Doubling is like a hit, only the bet is doubled and you only get one more card.\
            \n- Split can be done when you have two of the same card - the pair is split into two hands.\
            \n- Splitting also doubles the bet, because each new hand is worth the original bet.\
            \n- You can only double/split on the first move, or first move of a hand created by a split.")
    else:
        print("Looking forward to seeing you again!")