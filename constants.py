from itertools import product

from calculations import Stat


def main_cells():
    ''' Creates the bulk of the cells dictionary for use in the monkgearbox. '''
    attributes = ('armor strength elemental-resist resist-all vitality'
                         ' dexterity intelligence critical-hit critical-hit-damage'
                         ' attack-speed plus-life').split()
    slots = ('chest boots shoulders bracers belt pants '
                    'helm gloves ring1 ring2 amulet').split()
    columns = 'EFGHIJKLMNO'
    rows = [str(i) for i in range(4, 50, 5)] + ['73']  # amulet is row 73
     
    return cellsdict(attributes, slots, columns, rows)


def elemental_damage_cells():
    ''' manually add in gear that can have elemental damage on it '''
    elemental_pieces = {'boots-plus-elemental-damage': Stat('P9', 0),
                        'belt-plus-elemental-damage': Stat('P24', 0)}
    return elemental_pieces


def jewelry_extra_cells():
    ''' Creates the min-max value cells for jewelry. '''
    attributes = 'min max life-on-hit plus-elemental-damage'.split()
    slots = 'ring1 ring2 amulet'.split()
    columns = 'PQRS'
    rows = '44 49 73'.split()
     
    return cellsdict(attributes, slots, columns, rows)


def weapon_main_cells():
    ''' Creates the main values of the weapon cells. '''
    attributes = ('strength vitality dexterity intelligence critical-hit-damage'
                  ' life-steal life-on-hit elemental-damage').split()
    slots = 'mainhand offhand'.split()
    columns = 'EFGHIJKL'
    rows = '54 63'.split()
    
    return cellsdict(attributes, slots, columns, rows)


def cellsdict(attributes, slots, columns, rows):
    ''' Takes a list of attributes, the slots they go into, and their 
    respective cells and drops them into a dictionary suitable for
    consumption by the excel writer. '''
    return {'{}-{}'.format(prefix, suffix): Stat('{}{}'.format(col, row), 0)
            for (suffix, col), (prefix, row)
            in product(zip(attributes, columns),
                       zip(slots, rows))}

def make_cells():
    cells = main_cells()
    cells.update(elemental_damage_cells())
    cells.update(jewelry_extra_cells())
    cells.update(weapon_main_cells())
    return cells

cells = make_cells()