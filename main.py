import json
import random
import copy

try:
    with open('Card_Wars/data.json', 'r', encoding='utf') as f:
        cards_data = json.load(f)

except Exception as e:
    print(f"Error loading data: {e}")
    with open('Card_Wars/data.json', 'r', encoding='utf-8-sig') as f:
        cards_data = json.load(f)


class Map():
    pass

class Card():
    def __init__(self, name, landscape, ability, cost):
        self.name = name 
        self.landscape = landscape
        self.ability = ability
        self.cost = cost
    


class Creature(Card):
    def __init__(self, name, landscape, ability, cost, attack, defense):
        super().__init__(name, landscape, ability, cost)     
        self.attack = attack
        self.defense = defense
    
    def facedown():
        pass

    def amaizing_avalanche():
        #Each creature has +1 ATK this turn for each facedown landscape in play 
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
    pass

creatures = cards_data.get('Creature', [])
spells = cards_data.get('Spell', [])
heroes = cards_data.get('Hero', [])
buildings = cards_data.get('Building', [])



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
    
card_deck = {
    'Creatures' : creature_objects, 
    'Spells': spells_objects,
    'Heros': heroes_objects,
    'Buildings': buildings_objects
    }

playing_deck = copy.deepcopy(card_deck)
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
    def __init__(self, name, deck=playing_deck):
        self.name = name
        self.action = 2
        self.health = 25
        self.hand = []    

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
    
    def pull_card(self, deck):
        card_type, card = draw_random_card(deck)
        temp = card.name.split(' ')[3:]
        temp_join = ' '.join(temp)
        card.name = temp_join
        if card:
            self.hand.append(card)
            print(f"{self.name} pulled a card: {card.name} ({card_type})")
        else:
            print("No more cards to draw.")


    #2 Action (play Creature or buildings) Turns or pull

    #creatues

    #Buildings

    #spells


#40 cards

#health 25

class Game:
    def __init__(self):
        self.game_state = "MENU"
        self.main_menu = Menu(...)
        # ... other game components

    def run(self):
        while True:
            if self.game_state == "MENU":
                self.main_menu.handle_input()
                self.main_menu.draw()
            elif self.game_state == "PLAYING":
                self.update_game_state()
                self.draw_game_world()

class Menu:
    def __init__(self, options):
        self.options = options
    
    def handle_input(self):
        # Handle key presses to navigate and select options
        selected_option = self.get_user_input()
        if selected_option == "Play":
            # Tell the Game class to change its state
            # This can be done by returning a value or calling a method
            return "start_game"
        elif selected_option == "Quit":
            return "quit"
    
    def draw(self):
        # Logic for drawing text and buttons on the screen
        pass

def main():
    
    Finn = Player("Finn")
    Jake = Player("Jake")

    Finn.starting_cards(playing_deck, 5)
    Jake.starting_cards(playing_deck, 5)
 
    print(Finn.cards_in_hand())
    print(Finn.pull_card(playing_deck))


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