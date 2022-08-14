from itertools import product
import random
import time

print("If you are using this file you are likely running it through my Replit. For the blackjack rules, see the "
      "'README.md' file in my GitHub or Replit repository.")
time.sleep(3.25)


def Ace(repeated=False):  # For when an ace is drawn.
    if repeated:  # For invalid values.
        print("Please enter either 1 or 11. ")
    val = input("You drew an ace! What would you like it to be worth (1 or 11)? \n")
    return int(val) if val == "1" or val == "11" else Ace(repeated=True)  # Recursion for invalid values.


text_values = ["Two of", "Three of", "Four of", "Five of", "Six of", "Seven of", "Eight of", "Nine of", "Ten of",
               "King of", "Queen of", "Jack of", "Ace of"]
suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
card_values = dict(zip(text_values, [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 42069]))  # Dict to identify card values


class Card:
    def __init__(self, dealer_card=False, dealer_score=0, hidden=False):
        self.text_value = random.choice(text_values)
        self.value = card_values[self.text_value]  # Dictionary used for card values
        self.suit = random.choice(suits)
        if self.value == 42069 and dealer_card == False:  # Last value in the dictionary signifies an ace
            self.value = Ace()
        elif self.value == 42069 and dealer_card == True and hidden == False:
            print("The dealer draws an ace. ")
            time.sleep(1)
            self.value = 1 if dealer_score > 10 else 11
            print(f"The dealer decides that the ace's value will be {self.value}.")
        elif self.value == 42069 and dealer_card == True and hidden == True:
            self.value = 1 if dealer_score > 10 else 11

    def __repr__(self):
        return f"{self.text_value} {self.suit}"


class Split_Hand:
    def __init__(self, card1, card2, bet):
        self.card1 = card1
        self.card2 = card2
        self.bet = bet
        self.score = card1.value + card2.value


def Hit_Stand(player_score, repeat=False):
    if repeat:
        print("Please enter either hit or stand.")
    user_input = input("Would you like to 'hit' or 'stand'? ").lower()
    if user_input == "hit":
        new_card = Card()
        player_score += new_card.value
        print(f"The dealer gave you the {repr(new_card)}. ")
        if player_score > 21:
            return "Busted"
        Hit_Stand(player_score)
    elif user_input == "stand":
        print(f"Your score will stay at {player_score}.")
        return player_score
    else:
        Hit_Stand(player_score, repeat=True)


def play_again_func(balance):
    if balance < 1:
        print("You have no money! Get out of my casino!")
        exit()
    play_again = input("Play again? ").lower()
    if play_again == "yes":
        Blackjack(balance)
    elif play_again == "no":
        print(f"Thanks for playing! Your final balance is {balance}.")
        exit()
    else:
        print("Please say either 'yes' or 'no'. ")
        play_again_func(balance)


def bet_func(balance, repeat=False):
    if repeat:
        print("Please enter a number and make sure it is within your balance.")
    bet_val = input("How much would you like to bet? ")
    return int(bet_val) if any(char.isdigit() for char in bet_val) and int(bet_val) <= balance else bet_func(balance,
                                                                                                             repeat=True)


def double_down(balance, bet, repeat=False):
    if bet * 2 > balance:
        return bet, 0
    if repeat:
        print("Please enter either 'yes' or 'no'.")
    input_ = input("Would you like to double down? ").lower()
    if input_ == "no":
        return bet, 0
    if input_ != "yes":
        double_down(balance, bet, repeat=True)
    else:
        return bet * 2, 1


def split_double_down(hand1, hand2, bet, balance, repeat=False):
    if repeat:
        print("Make sure to enter a valid input. ")
    double = input("Would you like to double down on hand 1 or 2 (enter either '1', '2', 'both', or 'no'): ").lower()
    if double == "1" or double == "2":
        print(f"The bet on hand {double} was doubled to {bet}, and the total bet is now {bet * 1.5}.")
        hands = [hand1, hand2]
        hands[int(double) - 1].bet *= 2
        return hand1, hand2, bet, balance, double, True
    if double == "both":
        print(f"The bet on both hands were doubled to {bet}, and the total bet is now {bet * 2}.")
        hand1.bet, hand2.bet = hand1.bet * 2, hand2.bet * 2
        return hand1, hand2, bet, balance, double, True
    if double == "no":
        return hand1, hand2, bet, balance, double, True
    else:
        split_double_down(hand1, hand2, bet, balance, repeat=True)


def split(card1, card2, bet, balance, repeat=False):
    if card1.text_value != card2.text_value or bet * 2 > balance:
        hand1 = Split_Hand(card1, card2, bet)
        return hand1, False, bet, balance, False, False
    if repeat:
        print("Please enter either 'yes' or 'no'. ")

    user_input = input("You have 2 of the same card. Would you like to split your hand? ").lower()
    if user_input == "yes":
        bet *= 2
        print("The dealer splits your hand and deals 2 new cards.")
        card5, card6 = Card(), Card()
        time.sleep(3)
        print(f"The dealer deals the {repr(card5)} and the {repr(card6)}. ")
        time.sleep(3)
        print(f"Your 2 new hands are the {repr(card1)}/{repr(card5)} and the {repr(card2)}/{repr(card6)}.")
        print(f"Your two scores are now {card1.value + card5.value} and {card2.value + card6.value}.")
        hand1, hand2 = Split_Hand(card1, card5, bet / 2), Split_Hand(card2, card6, bet / 2)
        return split_double_down(hand1, hand2, bet, balance)
    elif user_input == "no":
        hand1 = Split_Hand(card1, card2, bet)
        return hand1, False, bet, balance, False, False
    else:
        split(card1, card2, bet, balance, repeat=True)


def Split_Winner_Hand_Comparison(hand_name, hand, dealer_score, balance):
    time.sleep(3)
    if hand.score > dealer_score:
        balance += hand.bet
        print(f"Your {hand_name}'s score of {hand.score} beat the dealer's score of {dealer_score}! You won {hand.bet} "
              f"and your new balance is {balance}!")
        return balance
    if hand.score == dealer_score:
        print(f"The dealers hand's score of {dealer_score} is equal to your {hand_name}'s score of {hand.score}. No"
              f" money was won or lost, your balance remaines as {balance}.")
        return balance
    else:
        balance -= hand.bet
        print(f"The dealer's hand's score of {dealer_score} is greater than your {hand_name}'s score of {hand.score}."
              f"You lost {hand.bet} and your new balance is {balance}.")


def Split_Winner_Declaration(hand1, hand2, dealer_score, bet_amount, balance):
    time.sleep(2)
    print(f"The dealer's score is {dealer_score}.")
    if dealer_score > 21:
        balance += bet_amount
        print(f"You win! The dealer busts! You won {bet_amount} and your new balance is {balance}!")
        return balance
    balance = Split_Winner_Hand_Comparison("first hand", hand1, dealer_score, balance)
    balance = Split_Winner_Hand_Comparison("second hand", hand2, dealer_score, balance)
    return balance


def Dealer_Draw(card4, dealer_score, repeat=False):
    if not repeat:
        print(f"The dealer reveals his second card to be the {repr(card4)}. ")
    if dealer_score >= 17:
        print("The dealer doesn't draw further as his score is greater than 17. ")
        return dealer_score
    new_card = Card(dealer_card=True, dealer_score=dealer_score)
    dealer_score += new_card.value
    time.sleep(1.5)
    print(f"The dealer draws the {repr(new_card)}.")
    time.sleep(1.5)
    return Dealer_Draw(None, dealer_score, repeat=True)


def Winner_Declaration(balance, bet_amount, dealer_score, player_score):
    if dealer_score > 21:
        print("The dealer has busted! You win!")
        balance += bet_amount
        time.sleep(2)
        print(f"You won ${bet_amount} and your new balance is ${balance}!")

    elif dealer_score == player_score:
        print(f"You and the dealer tied at {dealer_score}, and no money was won or lost. Your balance remains "
              f"${balance}.")
        time.sleep(2)

    elif dealer_score > player_score:
        print(f"The dealer's score of {dealer_score} is greater than your score of {player_score}.")
        balance -= bet_amount
        time.sleep(2)
        print(f"You lost ${bet_amount}! Your new balance is ${balance}.")

    elif dealer_score < player_score:
        print(f"Your score of {player_score} is greater than the dealer's score of {dealer_score}! You win!")
        time.sleep(2)
        balance += bet_amount
        print(f"You won ${bet_amount} and your new balance is ${balance}!")

    return balance


def Blackjack(balance):
    # Set the amount that you are betting.
    print(f"Your balance is {balance}.")
    bet_amount = bet_func(balance)
    print(f"You bet ${bet_amount}.")
    time.sleep(1.5)

    # Dealer deals initial 4 cards and scores are taken.
    card1, card2, card3, card4 = Card(), Card(), Card(True), Card(True, hidden=True)  # 1/2 for player, 3/4 for dealer.
    print(f"The dealer draws his cards.")
    time.sleep(2.5)
    print(f"The dealer has drawn the {repr(card3)}. Their second card is placed face down.")
    time.sleep(4)
    print(f"The dealer gives you the {repr(card1)} and the {repr(card2)}.")
    player_score, dealer_score = card1.value + card2.value, card3.value + card4.value
    print(f"Your score is {player_score}.")

    # Asks if the player is ellegible to double down/split and asks if they want to
    hand1, hand2, bet, balance, double, split_check = split(card1, card2, bet_amount, balance)
    if not split_check:
        card1, card2 = hand1.card1, hand1.card2
        bet_amount, bet_change = double_down(balance, bet_amount)
    if not split_check and bet_change:
        print(f"The bet has risen to {bet_amount}. ")

    # Checks for Blackjack.
    if player_score == 21:
        time.sleep(1)
        print("Blackjack! You got 21 with your starting hand and win 1.5x your bet. ")
        play_again_func(balance + (bet_amount * 1.5))
    if not split_check:
        hit_stand_results = Hit_Stand(player_score)

    # Checks for a bust after hit sequence.
    if not split_check:
        if hit_stand_results == "Busted":
            balance -= bet_amount
            print("Your score is over 21! You lost!")
            play_again_func(balance)

    # Dealer reveals his card, draws, and declares a winner. Offers to play again (unless player has no money).
    dealer_score = Dealer_Draw(card4, dealer_score)
    time.sleep(2)
    if not split_check:
        balance = Winner_Declaration(balance, bet_amount, dealer_score, hit_stand_results)
    else:
        Split_Winner_Declaration(hand1, hand2, dealer_score, hand1.bet + hand2.bet, balance)
    play_again_func(balance)


Blackjack(500)