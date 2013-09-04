import json

from bs4 import BeautifulSoup
from collections import Counter
from collections import namedtuple
from collections import defaultdict


elements = tuple('poison cold fire physical arcane lightning'.split())
Stat = namedtuple('Stat', 'cell, value')


def get_owe(content):
    ''' Unfortunately, its impossible to determine OWE resist on the fly. '''
    c = Counter()
    print 'grabbing One With Everything information...'
    for _, attributes in get_data(content, logoutput=False):
        for attribute, value in attributes.get('attrs', {}).items():
            if attribute.startswith(elements) and attribute.endswith('resist'):
                c[attribute] += int(value)

    resist, value = c.most_common(1)[0]
    print('determined {} to be the One With Everything resist at {}'
          ''.format(resist.upper(), value))
    return resist


def get_data(content, logoutput=True):
    ''' Downloads and yields the data for each piece of equipment on
    a d3up page. `content` is requests.content (a string). '''
    if logoutput:
        print 'parsing data...'
    soup = BeautifulSoup(content, 'lxml')
    equipment = soup.find('table', class_='equipment-table')
    equipped = equipment.findAll('span', class_='equipped')
    if logoutput:
        print 'getting information for each piece of equipment...'
    for i in equipped:
        if logoutput:
            print 'reading data for data-slot: {}'.format(i['data-slot'])
        yield i['data-slot'], json.loads(i.a.attrs['data-json'])

#TODO: Figure out whether or not a shield is parsed properly
def parse_item(itemdict, owe):
    ''' Returns the attributes from a single item. '''
    attributes = itemdict.get('attrs', {})
    attributes.update(itemdict.get('stats', {}))
    item = Item(attributes, owe)
    return item.data


class Item(object):
    ''' The manipulations of an item suitable for populating the
    monk gearbox table. '''
    def __init__(self, itemdict, owe=None):
        self._elements = elements
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

            # some values must be expressed as percentages
            elif self.is_percentage_value(attribute):
                self.data[str(attribute)] = "{0:.2f}".format(value)

            # otherwise, use the given {attribute: value}
            else:
                self.data[str(attribute)] = value

    def is_percentage_value(self, attrib):
        ''' Returns True if attribute is a percenage based value.'''
        percentage_values = ('critical-hit-damage')
        return attrib in percentage_values

    def is_owe_resist(self, attrib):
        ''' Returns True if attribute is the specified owe resist.'''
        return attrib == self._owe

    def is_elemental_resist(self, attrib):
        ''' Returns True if an attribute is an elemental resistance. '''
        return attrib.startswith(self._elements)and attrib.endswith('resist')

    def is_elemental_damage(self, attrib):
        ''' Returns True if an attribute is elemental damage. '''
        return attrib.startswith('plus') and attrib.endswith('damage')

    def is_elemental_weapon(self, attrib):
        ''' Returns True if an attribute is the damage component
        of an elemental weapon. '''
        return attrib.startswith(self._elements) and attrib.endswith('damage')

    def is_minmax_damage(self, attrib):
        ''' Returns True if an attribute is the min-max damage
        component of a piece of jewelry. '''
        return attrib == 'minmax-damage'

    def is_damage(self, attrib):
        ''' Returns True if an attribute is the damage component
        of a weapon. '''
        return attrib == 'damage'
