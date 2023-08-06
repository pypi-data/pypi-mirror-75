import json
from collections import defaultdict
import pathlib

MOO = pathlib.Path(__file__).parent.absolute() / 'property_list.json'


class Property:
    def __init__(self, id, name, price, rent, multiplied_rent, group):
        self.id = id
        self.name = name
        self.price = price
        self.rent = rent
        self.multiplied_rent = multiplied_rent
        self.group = group

        self.ownedby = None
        self.buildings = 0
        self.mortgaged = False

    def __repr__(self):
        return f'[{self.name}]'


class MonopolyBoard:
    """Stores the properties on the board

    The main structure of the board is a dictionary + tilelist. The dictionary maps Names
    ("id" in the JSON) to actual properties. The _tiles simply stores the order that the
    tiles are in.

    As well, we want to easily query the items by group (for example, to see if a player
    has all the properties in a group). Hence, _groups.
    """

    def __init__(self, fname=MOO):
        self._properties = {}
        self._tiles = []
        self._groups = defaultdict(list)

        self._init_properties(fname=fname)

    def to_valid_location(self, n):
        return n % len(self._tiles)

    def get_property_at(self, index):
        name = self._tiles[self.to_valid_location(index)]
        return self._properties.get(name)

    def get_location(self, name):
        """Returns the index of a particular Name, like "stjamesplace" """
        return self._tiles.index(name)

    def get_property(self, name):
        return self._properties.get(name, None)

    def _add_property(self, property):
        if property.name in self._properties:
            print(f'{property.name} already added!')
            return
        self._properties[property.id] = property
        self._groups[property.group].append(property.id)

    def _init_properties(self, fname=MOO):
        print('Reading properties from', fname)
        with open(fname, 'r') as f:
            data = json.load(f)

        print(data.keys())

        print('Making Community Chest...')

        for i, d in enumerate(data['communitychest']):
            print(i, d.keys())

        print('Making Chance cards...')

        for i, d in enumerate(data['chance']):
            print(i, d.keys())

        print('Making Properties...')
        for i, d in enumerate(data['properties']):
            id = d['id']
            p = Property(
                id=d['id'],
                name=d['name'],
                price=d.get('price', 0),
                rent=d.get('rent', 0),
                multiplied_rent=d.get('multipliedrent', []),
                group=d['group']
            )
            self._add_property(p)
            print(i, self._properties[d['id']].name,
                  self._properties[d['id']].price)

        print('Putting everything in order...')
        for i, d in enumerate(data['tiles']):
            print(i, d['id'])

        self._tiles = [d['id'] for d in data['tiles']]
