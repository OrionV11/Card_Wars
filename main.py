from carddweeb_cards_by_type import carddweeb_cards_by_type

deck = carddweeb_cards_by_type


class Menu():
    pass


class Card():
    def __init__(self, name, landscape, ability, cost):
        self.name = name 
        self.description = description
        self.landscape = landscape
        self.ability = ability
        self.cost = cost



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