import pprint

from conn import download_content
from calculations import get_owe
from calculations import get_data
from calculations import parse_item

if __name__ == '__main__':
    content = download_content()
    owe = get_owe(content)
    for slot, item in get_data(content):
        attributes = parse_item(item, owe)
        print pprint.pformat(dict(attributes))
