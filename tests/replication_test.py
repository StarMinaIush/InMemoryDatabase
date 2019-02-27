import json
import time
from multiprocessing import Process

import requests

from config import BOOKLIST_JSON_PATH
from node import run


def test_replication():
    # запускаем две слейв-ноды
    slave1 = Process(target=run, args=("127.0.0.2", 5000,))
    slave1.start()
    time.sleep(4)
    slave2 = Process(target=run, args=("127.0.0.3", 5000,))
    slave2.start()
    time.sleep(4)
    # запускаем мастер
    master = Process(target=run, args=("127.0.0.1", 5000, ["127.0.0.2", "127.0.0.3"]))
    master.start()
    time.sleep(4)
    # запускаем репликацию
    with open(BOOKLIST_JSON_PATH) as file:
        test_content = json.loads(file.read())

    for i in range(len(test_content)):
        requests.put("/".join(["http://127.0.0.1:5000", str(i)]), json.dumps(test_content[str(i)]))

    result_dict_slave1 = dict()
    for i in range(len(test_content)):
        r = requests.get("/".join(["http://127.0.0.2:5000", str(i)]))
        result_dict_slave1[str(i)] = r.text

    result_dict_slave2 = dict()
    for i in range(len(test_content)):
        r = requests.get("/".join(["http://127.0.0.3:5000", str(i)]))
        result_dict_slave2[str(i)] = r.text

    assert result_dict_slave1, test_content
    assert result_dict_slave2, test_content
