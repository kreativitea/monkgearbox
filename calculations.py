import json

from bs4 import BeautifulSoup
from collections import Counter
from collections import namedtuple
from collections import defaultdict


elements = tuple('poison cold fire physical arcane lightning'.split())
Stat = namedtuple('Stat', 'cell, value')


def get_owe(content):
    ''' Unfortunately, its impossible to determine the OWE resist on the fly. '''
    c = Counter()
    print 'grabbing One With Everything information...'
    for _, attributes in get_data(content, logoutput=False):
        for attribute, value in attributes.get('attrs', {}).items():
            if attribute.startswith(elements) and attribute.endswith('resist'):
                c[attribute] += int(value)

    resist, value = c.most_common(1)[0]
    print "determined {} to be the One With Everything resist at {}".format(resist.upper(), value)
    return resist


def get_data(content, logoutput=True):
    ''' Downloads and yields the data for each piece of equipment on a d3up page.
    content is from requests.content (a string). '''
    if logoutput:
        print 'parsing data...'
    soup = BeautifulSoup(content, 'lxml')
    equipment = soup.find('table', class_='equipment-table')
    equipped  = equipment.findAll('span', class_='equipped')
    if logoutput:
        print 'getting information for each piece of equipment...'
    for i in equipped:
        if logoutput:
            print 'reading data for data-slot: {}'.format(i['data-slot'])
        yield i['data-slot'], json.loads(i.a.attrs['data-json'])


def parse_item(slot, itemdict, owe):
    attributes = itemdict.get('attrs', {})
    attributes.update(itemdict.get('stats', {}))
    item = Item(slot, attributes, owe)
    return item.data


class Item(object):
    ''' The manipulations of an item suitable for populating the monk gearbox table. '''
    def __init__(self, slot, itemdict, owe=None):
        self._elements  = elements
        self._owe = owe
        self.data = defaultdict(int)

        # go through each case here
        for attribute, value in itemdict.items():

            # merge all sources of elemental damage together
            if self.is_elemental_damage(attribute):
                self.data['plus-elemental-damage'] = value

            # move elemental min-max damage into distinct categories
            elif self.is_elemental_weapon(attribute):
                self.data['elemental-max-damage'] = value.get('max', 0)
                self.data['elemental-min-damage'] = value.get('min', 0)

            # move jewelry min-max damage into distinct categories
            elif self.is_minmax_damage(attribute):
                self.data['min-damage'] = value.get('min', 0)
                self.data['max-damage'] = value.get('max', 0)

            # OWE monks only care about their owe resist
            elif self.is_elemental_resist(attribute):
                if self.is_owe_resist(attribute):
                    self.data['elemental-resist'] = value
                else:
                    self.data['elemental-resist'] = 0

            # move weapon damage into distinct categories
            elif self.is_damage(attribute):
                self.data['weapon-max-damage'] = value.get('max', 0)
                self.data['weapon-min-damage'] = value.get('min', 0)

            # otherwise, use the given {attribute: value}
            else:
                self.data[str(attribute)] = value

    def is_owe_resist(self, attribute):
        ''' Returns True if attribute is the specified owe resist.'''
        return attribute == self._owe

    def is_elemental_resist(self, attribute):
        ''' Returns True if an attribute is an elemental resistance. '''
        return attribute.startswith(self._elements) and attribute.endswith('resist')

    def is_elemental_damage(self, attribute):
        ''' Returns True if an attribute is elemental damage. '''
        return attribute.startswith('plus') and attribute.endswith('damage')

    def is_elemental_weapon(self, attribute):
        ''' Returns True if an attribute is the damage component of an elemental weapon. '''
        return attribute.startswith(self._elements) and attribute.endswith('damage')

    def is_minmax_damage(self, attribute):
        ''' Returns True if an attribute is the min-max damage component of a piece of jewelry. '''
        return attribute == 'minmax-damage'

    def is_damage(self, attribute):
        ''' Returns True if an attribute is the damage component of a weapon. '''
        return attribute == 'damage'