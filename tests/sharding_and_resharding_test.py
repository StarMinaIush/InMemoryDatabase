from config import PROXY_IP, PROXY_PORT, BOOKLIST_JSON_PATH
import requests
import json
from multiprocessing import Process
from proxy import run_server
from node import run


def test_sharding():
    # запускаем прокси
    p = Process(target=run_server)
    p.start()
    # запускаем ноду
    n1 = Process(target=run, args=("127.0.0.2", 5000,))
    n1.start()
    # запускаем еще одну ноду
    n2 = Process(target=run, args=("127.0.0.3", 5000,))
    n2.start()


    '''Обращаясь к прокси, добавляем данные, считываем обратно, проверяем что все нормально'''
    with open(BOOKLIST_JSON_PATH) as file:
        test_content = json.loads(file.read())

    for i in range(len(test_content)):
        requests.put("/".join([f"http://{PROXY_IP}:{PROXY_PORT}", "api", str(i)]), json.dumps(test_content[str(i)]))

    result_dict = dict()
    for i in range(len(test_content)):
        r = requests.get("/".join([f"http://{PROXY_IP}:{PROXY_PORT}",  "api",  str(i)]))
        result_dict[str(i)] = r.text

    assert result_dict, test_content

    #проверить, что данные равномерно распределяются по нодам
    #останавливаем все процессы
    p.close()
    n1.close()
    n2.close()
    #запускаем прокси и 4 ноды
    p = Process(target=run_server)
    p.start()
    # запускаем ноду
    n1 = Process(target=run, args=("127.0.0.2", 5000,))
    n1.start()
    # запускаем еще одну ноду
    n2 = Process(target=run, args=("127.0.0.3", 5000,))
    n2.start()

    n3 = Process(target=run, args=("127.0.0.4", 5000,))
    n3.start()






if __name__ == "__main__":
    test_sharding()
