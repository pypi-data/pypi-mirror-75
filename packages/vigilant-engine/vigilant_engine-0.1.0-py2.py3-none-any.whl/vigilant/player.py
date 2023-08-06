
from termcolor import cprint
import random


class Player:
    def __init__(self, name):
        self.name = name
        self.properties = {}
        self.money = 1500
        self.color = random.choice(['red', 'cyan', 'blue', 'green', 'yellow'])

        self.location = 0
        self.doubles_count = 0

    def buy_property(self, property):
        property.ownedby = self
        self.properties[property.id] = property
        self.log(f'{self.name} bought {property}')

    def subtract_money(self, amount):
        self.money -= amount

    def add_money(self, amount):
        self.money += amount

    def log(self, msg):
        return cprint(msg, self.color, attrs=['bold'])

    def __repr__(self):
        return f'{self.name} has ${self.money} and {len(self.properties)} properties'
