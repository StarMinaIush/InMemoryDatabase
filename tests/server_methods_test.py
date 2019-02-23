import json
import shutil
import pytest
import requests
import api.app as server
from config import BOOKLIST_JSON_PATH, BOOKLIST_UPDATE_JSON_PATH, URL


@pytest.fixture()
def database_load_test():
    shutil.rmtree('data')
    server.run()
    headers = {"Content-Type": "application/json"}

    with open(BOOKLIST_JSON_PATH) as file:
        test_content = json.loads(file.read())

    for i in range(len(test_content)):
        requests.put("/".join([URL, str(i)]), json.dumps(test_content[i]), headers=headers)

    result_dict = dict()
    for i in range(len(test_content)):
        r = requests.get("/".join([URL, str(i)]), headers=headers)
        result_dict[i] = r.content

    assert result_dict, test_content

    with open(BOOKLIST_UPDATE_JSON_PATH) as file:
        update_content = json.loads(file.read())

    for i in range(len(update_content)):
        requests.put("/".join([URL, str(i)]), json.dumps(test_content[i]), headers=headers)

    result_dict = dict()
    for i in range(len(update_content)):
        r = requests.get("/".join([URL, str(i)]), headers=headers)
        result_dict[i] = r.content

    assert result_dict, update_content

    for i in range(len(test_content)):
        requests.delete("/".join([URL, str(i)]), headers = headers)

    result_counter = 0
    for i in range(len(update_content)):
        r = requests.get("/".join([URL, str(i)]), headers=headers)
        if r.status_code == 404:
            result_counter+=1

    assert result_counter, len(update_content)


