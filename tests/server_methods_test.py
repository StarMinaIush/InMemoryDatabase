import json
import os
import requests
from app import run
from config import BOOKLIST_JSON_PATH, BOOKLIST_UPDATE_JSON_PATH, URL, DATABASE_DIRECTORY
from multiprocessing import Process


def test_database_load():
    filelist = [f for f in os.listdir(DATABASE_DIRECTORY)]
    for f in filelist:
        os.remove(os.path.join(DATABASE_DIRECTORY, f))
    headers = {"Content-Type": "application/json"}

    p = Process(target=run)
    p.start()

    with open(BOOKLIST_JSON_PATH) as file:
        test_content = json.loads(file.read())

    for i in range(len(test_content)):
        requests.put("/".join([URL, str(i)]), json.dumps(test_content[str(i)]), headers=headers)

    result_dict = dict()
    for i in range(len(test_content)):
        r = requests.get("/".join([URL, str(i)]), headers=headers)
        result_dict[str(i)] = r.content

    assert result_dict, test_content

    with open(BOOKLIST_UPDATE_JSON_PATH) as file:
        update_content = json.loads(file.read())

    for i in range(len(update_content)):
        requests.put("/".join([URL, str(i)]), json.dumps(test_content[str(i)]), headers=headers)

    result_dict = dict()
    for i in range(len(update_content)):
        r = requests.get("/".join([URL, str(i)]), headers=headers)
        result_dict[i] = r.content

    assert result_dict, update_content

    for i in range(len(test_content)):
        requests.delete("/".join([URL, str(i)]), headers=headers)

    result_counter = 1
    for i in range(len(update_content)):
        r = requests.get("/".join([URL, str(i)]), headers=headers)
        if r.status_code == 500:
            result_counter += 1

    assert result_counter, len(update_content)
    print("test passed!")


if __name__ == "__main__":
    test_database_load()
