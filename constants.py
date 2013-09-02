from calculations import Stat

rows = ('armor strength elemental-resist resist-all vitality'
        ' dexterity intelligence critical-hit critical-hit-damage'
        ' attack-speed plus-life elemental-damage'.split())

columns = 'chest boots shoulders bracers belt pants helm gloves ring1 ring2'.split()

cells = {'chest-armor': Stat('E4', 0)}