#creatures.py
import json
from card import Card

try:
    with open('./data.json', 'r', encoding='utf') as f:
        cards_data = json.load(f)

except Exception as e:
    print(f"Error loading data: {e}")
    with open('./data.json', 'r', encoding='utf-8-sig') as f:
        cards_data = json.load(f)

class Creature(Card):
    def __init__(self, name, landscape, cost, attack, defense, ability=None):
        super().__init__(name, landscape, ability, cost)     
        self.attack = attack
        self.defense = defense

    def facedown():
        pass

    def amaizing_avalanche():
        #Each creature has +1 ATK this turn for each facedown landscape in play 
        pass

    def display_stats(self):
        """Prints the creature's stats."""
        print(f"Name: {self.name}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        if self.ability:
            print(f"Ability: {self.ability}")

    def battle(self, other_creature):
        """A simple battle function."""
        print(f"{self.name} is battling {other_creature.name}!")
        if self.attack > other_creature.defense:
            print(f"{self.name} wins!")
        elif self.attack < other_creature.defense:
            print(f"{other_creature.name} wins!")
        else:
            print("It's a draw!")

creatures = cards_data.get('Creature', [])
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

creature_deck = {
    'Creatures' : creature_objects, 
    }



def ancient_scholar_ability():    
    #Return a random Rainbow card from your discard pile to your hand. 
    # If you control a Building in this Lane, gain 1 Action."
    pass

def cool_dog_ability():        #Your Creatures on adjacent Lanes may not be Attacked.
    pass

def archer_dan_ability():      #Destroy target Building in Archer Dan's Lane.
    pass

def big_foot_ability():        #Flip target face down Landscape you control face up."
    pass    

def corn_dog_ability():       #Corn Dog has +1 DEF for each Cornfield Landscape you control. If you control 3 or fewer Cornfield Landscapes, Corn Dog has +1 ATK.",
    pass

def corn_lord_ability(): #Corn Lod has +1 ATK for each other cornfield Ceature you control
    pass


ability_list = {}

for creature in creature_deck['Creatures']:
    temp = creature.name.split(' ')[3:]
    temp_join = ' '.join(temp)
    creature.name = temp_join
    ability_power = "#" + creature.ability
    ability_str = "def " + creature.name.lower().replace(" ", "_" ) + "_abililty()"

    ability_list[ability_str] = ability_power

print(ability_list)


'''
for creature in creature_deck['Creatures']:
    temp = creature.name.split(' ')[3:]
    temp_join = ' '.join(temp)
    creature.name = temp_join
    creature.ability = eval(creature.name.lower().replace(" ", "_") + "_ability()")
    print(creature.ability)
'''



