from config import PROXY_IP, PROXY_PORT, BOOKLIST_JSON_PATH
import requests
import json
from multiprocessing import Process
from proxy import run_server
from node import run
import time


def test_sharding():
    p = Process(target=run_server)
    p.start()
    time.sleep(2)
    n1 = Process(target=run, args=("127.0.0.2", 5000,))
    n1.start()
    time.sleep(4)
    n2 = Process(target=run, args=("127.0.0.3", 5000,))
    n2.start()
    time.sleep(4)

    with open(BOOKLIST_JSON_PATH) as file:
        test_content = json.loads(file.read())

    for i in range(len(test_content)):
        requests.put("/".join([f"http://{PROXY_IP}:{PROXY_PORT}", "api", str(i)]), json.dumps(test_content[str(i)]))

    result_dict = dict()
    for i in range(len(test_content)):
        r = requests.get("/".join([f"http://{PROXY_IP}:{PROXY_PORT}", "api", str(i)]))
        result_dict[str(i)] = r.text

    assert result_dict, test_content

    p.terminate()
    n1.terminate()
    n2.terminate()

    p = Process(target=run_server)
    p.start()
    time.sleep(2)
    n1 = Process(target=run, args=("127.0.0.2", 5000,))
    n1.start()
    time.sleep(4)
    n2 = Process(target=run, args=("127.0.0.3", 5000,))
    n2.start()
    time.sleep(4)
    n3 = Process(target=run, args=("127.0.0.4", 5000,))
    n3.start()
    time.sleep(4)


if __name__ == "__main__":
    test_sharding()
