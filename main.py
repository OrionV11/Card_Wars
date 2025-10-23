import json
import random
import copy
from creatures import Creature
from card import Card
import pygame

try:
    with open('./data.json', 'r', encoding='utf') as f:
        cards_data = json.load(f)

except Exception as e:
    print(f"Error loading data: {e}")
    with open('./data.json', 'r', encoding='utf-8-sig') as f:
        cards_data = json.load(f)


class Map():
    pass


class Hero(Card):
    def __init__(self, name, ability):
        super().__init__(name, None, ability, None)
        self.name = name
        self.ability = ability

class Spell(Card):
    def __init__(self, name, landscape, ability, cost):
        super().__init__(name, landscape, ability, cost)

class Building(Card):
    def __init__(self, name, landscape, ability, cost):
        super().__init__(name, landscape, ability, cost)

class Landscape():
    def __init__(self, name):
        self.name = name

    def pull_landscape():
        for i in range(4):

            pass

creatures = cards_data.get('Creature', [])
spells = cards_data.get('Spell', [])
heroes = cards_data.get('Hero', [])
buildings = cards_data.get('Building', [])
landscape = cards_data.get('Landscape', [])

class Menu():
    pass

creature_objects = []
for creature_data in creatures:
    creature = Creature(
        name=creature_data['name'],
        landscape=creature_data['landscape'],
        ability=creature_data['ability'],
        cost=creature_data['cost'],
        attack=creature_data['attack'],
        defense=creature_data['defense']
        )
    creature_objects.append(creature)


    spells_objects = []
    for spell_data in spells:
        spell = Spell(
            name=spell_data['name'],
            landscape=spell_data['landscape'],
            ability=spell_data['ability'],
            cost=spell_data['cost']
            )
        spells_objects.append(spell)

    heroes_objects = []
    for hero_data in heroes:
        hero = Hero(
            name=hero_data['name'],
            ability=hero_data['ability']
            )
        heroes_objects.append(hero)

    buildings_objects = []
    for building_data in buildings:
        building = Building(
            name=building_data['name'],
            landscape=building_data['landscape'],
            ability=building_data['ability'],
            cost=building_data['cost']
            )
        buildings_objects.append(building)
    landscape_objects = []
    for landscape_data in landscape:
        landscape_card = Landscape(
            name=landscape_data['name'],
            )
        landscape_objects.append(landscape_card)

card_deck = {
    'Creatures' : creature_objects, 
    'Spells': spells_objects,
    'Heros': heroes_objects,
    'Buildings': buildings_objects,
    }

landscape_deck = {
    'Landscapes': landscape_objects
    }

building_deck = {
    'Buildings': buildings_objects,
    }

creatures_deck = {
    'Creatures' : creature_objects
    }

master_deck = copy.deepcopy(card_deck)
landscape_playing_deck = copy.deepcopy(landscape_deck)
building_playing_deck = copy.deepcopy(building_deck)
creatures_playing_deck = copy.deepcopy(creatures_deck)

drawn_cards = []

def draw_random_card(deck):
    non_empty_types = [key for key, value in deck.items() if value]

    if not non_empty_types:
        return None, None  # No cards left to draw

    random_card_type = random.choice(non_empty_types)
    chosen_card_list = deck[random_card_type]
    random_card = random.choice(chosen_card_list)
    chosen_card_list.remove(random_card)

    return random_card_type, random_card


class Player():
    def __init__(self, name, deck=master_deck):
        self.name = name
        self.action = 2
        self.health = 25
        self.pick_hand = []
        self.deck = deck
        self.idle_hand = []
        self.hand = []
        self.get_landscape_hand = []

    def out_of_action(self):
        if self.action <= 0:
            print(f"{self.name} is out of actions for this turn.")
            return True
        return False

    def reset_actions(self):
        self.action = 2
        print(f"{self.name}'s actions have been reset to {self.action} for the new turn.")

    def lose_health(self, amount):
        self.health -= amount
        print(f"{self.name} loses {amount} health. Remaining health: {self.health}")
        if self.health <= 0:
            print(f"{self.name} has been defeated!")


    def starting_landscape_cards(self, deck, num_cards=4):
        print(f"\n{self.name} Drawing {num_cards} starting landscape cards...")
        for _ in range(num_cards):
            landscape_list = deck['Landscapes']
            card = random.choice(landscape_list)
            landscape_list.remove(card)
            temp = card.name.split(' ')[3:]
            temp_join = ' '.join(temp)
            card.name = temp_join
            if card:
                self.get_landscape_hand.append(card)
            else:
                print("No more landscape cards to draw.")
                break

    def starting_cards(self, deck, num_cards=5):
        print(f"\n{self.name} Drawing {num_cards} starting cards...")
        for _ in range(num_cards):
            card_type, card = draw_random_card(deck)
            if card:
                self.hand.append(card)
            else:
                print("No more cards to draw.")
                break

    def cards_in_hand(self):
        print(f"\n{self.name}'s cards in hand:")

        if not self.hand:
            print("No cards in hand.")
            return
        for card in self.hand:
            temp = card.name.split(' ')[3:]
            temp_join = ' '.join(temp)
            card.name = temp_join
            print(f" - {card.name} ({type(card).__name__})")


    def play_card(self, card_index):
        if 0 <= card_index < len(self.hand):
            card = self.hand[card_index]
            if self.action > 0:
                self.action -= 1
                played_card = self.hand.pop(card_index)
                temp = played_card.name.split(' ')[3:]
                temp_join = ' '.join(temp)
                played_card.name = temp_join
                print(f"{self.name} played {played_card.name}. Remaining actions: {self.action}")
                return played_card
            else:
                print(f"{self.name} has no actions left to play a card.")
        else:
            print("Invalid card index.")
        return None

    def pull_card(self, deck):
        card_type, card = draw_random_card(deck)
        temp = card.name.split(' ')[3:]
        temp_join = ' '.join(temp)
        card.name = temp_join
        if card:
            self.action -= 1
            self.hand.append(card)
            print(f"{self.name} pulled a card: {card.name} ({card_type})")
        else:
            print("No more cards to draw.")

    def get_landscape(self, deck, num_card):
        print(f"\n{self.name} Drawing {num_card} landscape cards...")
        for _ in range(num_card):
            landscape_list = deck['Landscapes']
            card = random.choice(landscape_list)
            landscape_list.remove(card)
            temp = card.name.split(' ')[3:]
            temp_join = ' '.join(temp)
            card.name = temp_join
            if card:
                self.get_landscape_hand.append(card)
                print(f"{self.name} pulled a landscape card: {card.name})")
            else:
                print("No more landscape cards to draw.")



class Game:
    def __init__(self):
        self.game_state = "MENU"
        self.main_menu = Menu(...)
        # ... other game components

    def run(self):
        while True:
            if self.game_state == "MENU":
                self.main_menu.handle_input()
                #self.main_menu.draw()
            elif self.game_state == "PLAYING":
                self.update_game_state()
                self.draw_game_world()
            


class Menu:
    def __init__(self, options):
        self.options = options

    def handle_input(self):
        # Handle key presses to navigate and select options
        user_input = input("Select an option (Play/Quit): ").strip()
        selected_option = user_input
       
        confirmation = input().strip().upper()
        if confirmation != 'Y':
            return  # Return to menu without changing state
        
        if selected_option == "Play":
            # Tell the Game class to change its state
            # This can be done by returning a value or calling a method
            return "start_game"
        elif selected_option == "Quit":
            return "quit"

    def draw(self):
        # Logic for drawing text and buttons on the screen
        pass


def starting_structure_cards(player, deck, num_cards=6, ):
        print(f"\n{player.name} Drawing {num_cards} starting building cards...")
        for _ in range(num_cards):
            card_type, card = draw_random_card(deck)
            if card:
                player.pick_hand.append(card)
            else:
                print("No more cards to draw.")
                break

        print(f"\n{player.name}, you drew the following building cards:")
        for i, card in enumerate(player.pick_hand, start=1):
            print(f"{i}. {card.name}")
            
        while len(player.idle_hand) < 4:
            try:
                choice = int(input(f"Choose a card to keep (1-{len(player.pick_hand)}): ")) - 1
                if 1 <= choice < len(player.pick_hand):
                    input = player.pick_hand[choice]
                    selected_card = player.pick_hand.pop(choice - 1)
                    player.idle_hand.append(selected_card)
                    print(f"Added '{selected_card.name}' to your idle hand.")
                else:
                    print("Invalid number. Please choose a valid card index.")
            except ValueError:
                print("Please enter a valid number.")

        print(f"\n{player.name} kept the following building cards:")
        for card in player.idle_hand:
            print(f"- {card.name}")


for creature in creatures_playing_deck['Creatures']:
    temp = creature.name.split(' ')[3:]
    temp_join = ' '.join(temp)
    creature.name = temp_join
    creature.ability = eval(creature.name.lower().replace(" ", "_") + "_ability()")
    print(creature.ability)

def main():

    Finn = Player("Finn")
    Jake = Player("Jake")


    #Finn.starting_landscape_cards(landscape_playing_deck, 4)
    #Finn.get_landscape(landscape_playing_deck, 4)



    #Finn.starting_cards(playing_deck, 5)
    #Jake.starting_cards(playing_deck, 5)


    #print(Finn.cards_in_hand())
    #print(Finn.pull_card(playing_deck))
    #print(Finn.get_landscape(landscape_playing_deck, 4))




'''
    print("Remaining cards in playing deck:")
    for card_type, card_list in playing_deck.items():
        print(f"Card Type: {card_type}, Card List: {card_list}")
    print("Original Deck")
    for card_type, card_list in card_deck.items():
        print(f"Card Type: {card_type}, Card List: {card_list}")
'''
    #*temp card_deck 0
    #*rand card_deck 0 

#print(creature_objects[0].name)
#print(len(card_deck.get('Spells')))

if __name__ == "__main__":
    main()
