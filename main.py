import json

with open('carddweeb_cards_by_type.json', 'r', encoding='utf-8') as f:
    cards_data = json.load(f)


creatues = cards_data.get('Creature', [])
spells = cards_data.get('Spell', [])
heroes = cards_data.get('Hero', [])
buildings = cards_data.get('Building', [])

class Menu():
    pass


class Card():
    def __init__(self, name, landscape, ability, cost):
        self.name = name 
        self.landscape = landscape
        self.ability = ability
        self.cost = cost


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

class Creature(Card):
    def __init__(self, attack, defense):
        self.attack = attack
        self.defense = defense
    

    def facedown():
        pass




    def amaizing_avalanche():
        #Each creature has +1 ATK this turn for each facedown landscape in play 
        pass

class Hero(Card):
    pass

class Spell(Card):
    pass



class Game():
    pass

class Map():
    pass

class Player():
    def __init__(self, health, action):
        self.health = health
        self.action = action
    

    def draw():
        pass
    #2 Action (play Creature or buildings) Turns or pull

    #creatues

    #Buildings

    #spells


    

#40 cards

#health 25


def main():
    
    print(deck)

if __name__ == "__main__":
    main()