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
    soup = BeautifulSoup(content)
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

    # stats object could be empty
    try:
        attributes.update(itemdict.get('stats', {}))
    except TypeError:
        pass
        
    item = Item(attributes, owe)
    return item.data


def is_shield(itemdict):
    return itemdict.get('type', '') == 'shield'


class Item(object):
    ''' The manipulations of an item suitable for populating the
    monk gearbox table. 
    
    This is really sloppy, I know. '''
    def __init__(self, itemdict, owe=None):
        self._elements = elements
        self._owe = owe
        self.data = defaultdict(int)

        # go through each case here
        for attribute, value in itemdict.items():

            if attribute == 'plus-damage':
                self.data['plus-damage'] = value / 100.0

            elif attribute == 'plus-lightning-damage-skills':
                self.data['plus-lightning-damage-skills'] = value / 100.0

            # merge all sources of elemental damage together
            elif self.is_elemental_damage(attribute):
                self.data['plus-elemental-damage'] = value / 100.0

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
                self.data[str(attribute)] = value / 100.0

            elif self.is_block_amount(attribute):
                self.data['block-amount-max'] = value.get('max', 0)
                self.data['block-amount-min'] = value.get('min', 0)
            
            elif self.is_skill(attribute):
                self.data[attribute] = value / 100.0

            # otherwise, use the given {attribute: value}
            else:
                self.data[str(attribute)] = value
    
    def is_skill(self, attrib):
        return attrib.startswith('mk-')

    def is_percentage_value(self, attrib):
        ''' Returns True if attribute is a percenage based value.'''
        percentage_values = ('critical-hit-damage', 'critical-hit',
                             'attack-speed', 'life-steal', 'plus-life',
                             'plus-damage plus-lightning-damage-skills',
                             'block-chance')
        return attrib in percentage_values

    def is_owe_resist(self, attrib):
        ''' Returns True if attribute is the specified owe resist.'''
        return attrib == self._owe

    def is_elemental_resist(self, attrib):
        ''' Returns True if an attribute is an elemental resistance. '''
        return attrib.startswith(self._elements)and attrib.endswith('resist')

    def is_elemental_damage(self, attrib, component=''):
        ''' Returns True if an attribute is elemental damage. '''
        if attrib.startswith('plus') and attrib.endswith('damage'):
            component = attrib.replace('plus', '').replace('damage', '')

        return len(component) > 1

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

    def is_block_amount(self, attrib):
        ''' Returns True if an attribute is block amount. '''
        return attrib == 'block-amount'
