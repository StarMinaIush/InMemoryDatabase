import json
from config import BOOKLIST_PATH, BOOKLIST_JSON_PATH


def write_booklist_dict():
    booklist_dict = dict()
    book_counter = 0
    with open(BOOKLIST_PATH) as file:
        content = file.readlines()

    for i in content:
        booklist_dict[book_counter] = i
        book_counter += 1

    with open(BOOKLIST_JSON_PATH, 'w') as jsonfile:
        json.dump(booklist_dict, jsonfile)


if __name__ == "__main__":
    write_booklist_dict()
