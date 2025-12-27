import random
import asyncio # will be used to simulate thinking behavior and makes the programm easier to follow 

# variable declaration field
starting_money = 100 
suits = ["♦","♣","♥","♠"]
types_of_cards = [2,3,4,5,6,7,8,9,10,"Jack","Queen","King", "Ace"]
value_of_cards = {2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, "Jack":11, "Queen":12, "King":13, "Ace":14} # will be used to compare cards


# classes declaration field 
class Player():
    def __init__(self,name):
        self.name = name 
        self.points = 100

class Bot(Player):
    # Bot is inhariting the name and points property from player

    bot_random_choice_list = ["h", "l"] # for the cases where the odds are even

    def __init__(self, name):
        super().__init__(name)
        self.bet_decision = ""
        self.betting_amount = 0
        self.bot_decision_to_quit = ""


    async def bot_betting(self) -> str:

     # the bot will compare the odds and choose the more likely win situation
        self.decision_container_for_h = 0
        self.decision_container_for_l = 0
        current_card = value_of_cards[Playing_card.deck[0].value]

        for key in value_of_cards.keys():
            if current_card > value_of_cards[key]:
                self.decision_container_for_l += 1
            elif current_card < value_of_cards[key]:
                self.decision_container_for_h += 1

        if self.decision_container_for_h > self.decision_container_for_l:
            self.bet_decision = "h"
            await asyncio.sleep(random.randint(1, 5))  # Wait between 1 and 5 seconds
            print("I think the next card will be will be higher")
        elif self.decision_container_for_h < self.decision_container_for_l:
            self.bet_decision = "l"
            await asyncio.sleep(random.randint(1, 5))
            print("I think the next card will be lower")
        else:
            self.bet_decision = random.choice(self.bot_random_choice_list)
            await asyncio.sleep(random.randint(1, 5))
            print(f"I am not sure maybe {self.bet_decision}")
        return self.bet_decision
    
    async def bot_choosing_amount(self) -> int:

    # depending on how sure the bot is, he will choose higher or smaller amount

        if float(self.decision_container_for_h / len(value_of_cards))* 100 > 75.0 or \
            float(self.decision_container_for_l / len(value_of_cards))* 100 > 75.0 :
            self.betting_amount = 250
            await asyncio.sleep(random.randint(1, 3))
            print(f"I will bet ${self.betting_amount}")

        elif float(self.decision_container_for_h / len(value_of_cards))* 100 < 25.0 or \
            float(self.decision_container_for_l / len(value_of_cards))* 100 < 25.0:
            self.betting_amount = 5
            await asyncio.sleep(random.randint(1, 3))
            print(f"I will bet ${self.betting_amount}")
        else:
            self.betting_amount = random.randint(25,75)
            await asyncio.sleep(random.randint(1, 3))
            print(f"I will bet ${self.betting_amount}")
        return self.betting_amount
    
    async def bot_considering_to_quit(self) -> str:

    # giving the bot some logic which he will follow and decide when to stop playing

        if self.points < 50:
            self.bot_decision_to_quit = "y"
            await asyncio.sleep(2)
            print("Today is not my lucky day. I would rather quit")
        elif self.points > 450:
            self.bot_decision_to_quit = "y"
            await asyncio.sleep(2)
            print("I had enough for today. I quit!")
        else:
            self.bot_decision_to_quit = "n"
            await asyncio.sleep(2)
            print("I would like to keep playing")
        return self.bot_decision_to_quit

class Playing_card():
    deck = [] 
    def __init__(self,value,suit,index):
        self.value = value
        self.suit = suit
        self.index = index     

class Game():
    def __init__(self):
        self.status = True
        self.cards_played = 0

    def exit(self,escape:str):   
        if escape == "y":
            self.status = False
            print("Thanks for playing")
            print("*******************************************")
        
    # allows the bot to end the game

    @staticmethod
    def shuffel_cards():
        random.shuffle(Playing_card.deck)

    # shuffles the cards
    
    def load_deck(self):
        index = 0
        for suit in suits:
            for card in types_of_cards:
                Playing_card.deck.append(Playing_card(card,suit,index))
                index += 1 

    # creates a card with a value and suit as well as an index
    # the cards are emidiatly added to the deck
    # cards are currently in order / unshuffled

    @staticmethod
    def display_top_card():
        print(f"\nCurrent card is: {Playing_card.deck[0].value} of {Playing_card.deck[0].suit}")
        
    # displays the very first card so the player can take a proper guess
                    
    def evaluate_bet(self,bot:object):

        '''
    This function
    1. takes the money in order to place a bet
    2. evaluates the bet to see if the bot was right or wrong
    3. depening on the outcome the bot will gain more, lose or get his money back
    4. after the evaluation the first card comes at the bottom and the second card is the next card on which the bot can bet
    5.after each round the bot is offered the opportunity to leave the game with what he currently has
    6. so the cycly doesn't repeat endlessly when there are only 10 cards not shown in the deck, the whole deck gets shuffled
        '''

        bot.points -= bot.betting_amount
        if value_of_cards[Playing_card.deck[0].value] < value_of_cards[Playing_card.deck[1].value] and bot.bet_decision == "h":
            print("You were wright!!!")
            print(f"You gained ${2 * bot.betting_amount}")
            bot.points += bot.betting_amount * 2
            print(f"{bot.name}'s money: ${bot.points}")
            print("*******************************************")
        elif value_of_cards[Playing_card.deck[0].value] > value_of_cards[Playing_card.deck[1].value] and bot.bet_decision == "l":
            print("You were right!!!")
            print(f"You gained {2 * bot.betting_amount}")
            bot.points += bot.betting_amount * 2
            print(f"{bot.name}'s money: ${bot.points}")
            print("*******************************************")
        elif value_of_cards[Playing_card.deck[0].value] == value_of_cards[Playing_card.deck[1].value]:
            print("Both cards are equal, you can bet again. \n Your bet has been restored")
            print("*******************************************")
            bot.points += bot.betting_amount
        else: 
            print(f"Wrong you lose the bet\n {bot.name}'s money: ${bot.points}")
            print("*******************************************")

        top_card = Playing_card.deck.pop(0)
        Playing_card.deck.append(top_card)

        self.cards_played += 1
        if self.cards_played > 42:
            print("Less than 10 cards left.\n The deck will be shuffled")
            self.shuffel_cards()


async def main():
    print("*******************************************")
    print("Welcome to our card game")
    game = Game()
    p1 = Bot("Bot")
    print(f"Player:  {p1.name}")
    print(f"money: ${p1.points}")
    game.load_deck()
    game.shuffel_cards()
    while game.status != False:
        game.display_top_card()
        await p1.bot_betting()
        await p1.bot_choosing_amount()
        game.evaluate_bet(p1)
        await p1.bot_considering_to_quit()
        game.exit(p1.bot_decision_to_quit)
        if p1.points <= 0:
            game.status = False
            print("You are out of money")
            print("Game over")
            print("*******************************************")

if __name__ == "__main__":
    asyncio.run(main()) 
    # asyncio.run is required because of our await functions

