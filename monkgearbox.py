import pprint

from conn import download_content

from excel import write_data
from excel import select_excel

from constants import cells

from calculations import Stat
from calculations import get_owe
from calculations import get_data
from calculations import parse_item
from calculations import is_shield

if __name__ == '__main__':
    # initialize storage
    workbook = select_excel()

    # download content
    content = download_content()
    owe = get_owe(content)

    # grab each item
    for slot, item in get_data(content):
        attributes = parse_item(item, owe)

        # if offhand is shield, set accordingly
        if slot == 'offhand':
            if is_shield(item):
                slot = 'shield'

        if slot == 'pants':
            pprint.pprint(item)

        # for each item, grab each attribute
        for attribute, value in attributes.items():
            cellname = '{}-{}'.format(slot, attribute)
            try:
                cells[cellname] = Stat(cells[cellname].cell, value)
            except KeyError as e:
                # no cell is set up to take this value
                pass

    write_data(workbook, 'Gear', cells)
