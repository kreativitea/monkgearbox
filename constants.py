from itertools import product

from calculations import Stat


def main_cells():
    ''' Creates most of the cells dictionary for use in the monkgearbox. '''
    attributes = ('armor strength elemental-resist resist-all vitality'
                  ' dexterity intelligence critical-hit'
                  ' critical-hit-damage attack-speed'
                  ' plus-life').split()
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
    attributes = ('min-damage max-damage life-hit'
                  ' plus-elemental-damage').split()
    slots = 'ring1 ring2 amulet'.split()
    columns = 'PQRS'
    rows = '44 49 73'.split()

    return cellsdict(attributes, slots, columns, rows)


def pants_life_on_hit():
    ''' Creates LoH cell for pants. '''
    attributes = ['life-hit']
    slots = ['pants']
    columns = 'P'
    rows = ['29']

    return cellsdict(attributes, slots, columns, rows)


def weapon_main_cells():
    ''' Creates the main values of the weapon cells. '''
    attributes = ('strength vitality dexterity intelligence'
                  ' critical-hit-damage life-steal life-hit'
                  ' plus-elemental-damage plus-lightning-damage-skills').split()
    slots = 'mainhand offhand'.split()
    columns = 'EFGHIJKLM'
    rows = '54 63'.split()

    return cellsdict(attributes, slots, columns, rows)


def monk_skill_cells():
    ''' Creates the attributes for monk skills '''
    attributes = 'mk-sweeping-wind mk-fists-of-thunder'.split()
    slots = ['helm']
    columns = 'PQ'
    rows = ['34']
    return cellsdict(attributes, slots, columns, rows)


def mh_attrib_cells():
    ''' Creates the attribute values of the mh weapon cells. '''
    attributes = ('speed attack-speed plus-aps plus-damage'
                  ' weapon-min-damage weapon-max-damage'
                  ' elemental-min-damage elemental-max-damage').split()
    slots = ['mainhand']
    columns = 'C'
    rows = range(53, 61)
    return cellsdict(attributes, slots, columns, rows, transpose=True)


def oh_attrib_cells():
    ''' Creates the attribute values of the oh weapon cells. '''
    attributes = ('speed attack-speed plus-aps plus-damage'
                  ' weapon-min-damage weapon-max-damage'
                  ' elemental-min-damage elemental-max-damage').split()
    slots = ['offhand']
    columns = 'C'
    rows = range(62, 70)
    return cellsdict(attributes, slots, columns, rows, transpose=True)


def shield_attrib_cells():
    ''' Creates the attribute values of the shield cells. '''
    attributes = ('armor strength elemental-resist resist-all vitality'
                  ' dexterity intelligence critical-hit plus-life'
                  ' block-chance block-amount-max block-amount-min').split()
    slots = ['shield']
    columns = 'EFGHIJKLMNOP'
    rows = [79]

    return cellsdict(attributes, slots, columns, rows)


def cellsdict(attributes, slots, columns, rows, transpose=False):
    ''' Takes a list of attributes, the slots they go into, and their
    respective cells and drops them into a dictionary suitable for
    consumption by the excel writer. '''
    if transpose:
        columns, rows = rows, columns
        return {'{}-{}'.format(prefix, suffix): Stat('{}{}'.format(row, col), 0)
            for (suffix, col), (prefix, row)
            in product(zip(attributes, columns),
                        zip(slots, rows))}

    else:
        return {'{}-{}'.format(prefix, suffix): Stat('{}{}'.format(col, row), 0)
                for (suffix, col), (prefix, row)
                in product(zip(attributes, columns),
                           zip(slots, rows))}


def make_cells():
    cells = main_cells()
    cells.update(elemental_damage_cells())
    cells.update(jewelry_extra_cells())
    cells.update(weapon_main_cells())
    cells.update(oh_attrib_cells())
    cells.update(mh_attrib_cells())
    cells.update(shield_attrib_cells())
    cells.update(monk_skill_cells())
    cells.update(pants_life_on_hit())
    return cells


cells = make_cells()
