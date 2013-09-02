from conn import download_content
from calculations import get_owe
from calculations import get_data
from calculations import parse_item

if __name__ == '__main__':
    content = download_content()
    owe = get_owe(content)
    for slot, attributes in get_data(content):
        parse = parse_item(slot, attributes, owe)
        print slot, parse
