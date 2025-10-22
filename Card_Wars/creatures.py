#creatures.py
from card import Card

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
