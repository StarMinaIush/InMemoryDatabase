import json
import os
import shutil

import requests
from node import run
from config import BOOKLIST_JSON_PATH, BOOKLIST_UPDATE_JSON_PATH, PROXY_DIRECTORY
from multiprocessing import Process
import time


def test_database_load():

    database_files = [f for f in os.listdir(PROXY_DIRECTORY)]
    for d in database_files:
        shutil.rmtree(os.path.join(PROXY_DIRECTORY, d), ignore_errors=True)
    URL = "http://127.0.0.2:5000"
    p = Process(target=run, args=("127.0.0.2", 5000,))
    p.start()
    time.sleep(2)

    with open(BOOKLIST_JSON_PATH) as file:
        test_content = json.loads(file.read())

    for i in range(len(test_content)):
        requests.put("/".join([URL, str(i)]), json.dumps(test_content[str(i)], ensure_ascii=False).encode('utf-8'))

    result_dict = dict()
    for i in range(len(test_content)):
        r = requests.get("/".join([URL, str(i)]))
        result_dict[str(i)] = r.content

    assert result_dict, test_content

    with open(BOOKLIST_UPDATE_JSON_PATH) as file:
        update_content = json.loads(file.read())

    for i in range(len(update_content)):
        requests.put("/".join([URL, str(i)]), json.dumps(test_content[str(i)]))

    result_dict = dict()
    for i in range(len(update_content)):
        r = requests.get("/".join([URL, str(i)]))
        result_dict[i] = r.content

    assert result_dict, update_content

    for i in range(len(test_content)):
        requests.delete("/".join([URL, str(i)]))

    result_counter = 1
    for i in range(len(update_content)):
        try:
            r = requests.get("/".join([URL, str(i)]))
            if r.status_code == 404:
                result_counter += 1
        except requests.HTTPError:
            continue

    assert result_counter, len(update_content)


if __name__ == "__main__":
    test_database_load()
