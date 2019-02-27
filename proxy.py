import os

from flask import Flask, request
import requests
import json
from config import PROXY_IP, PROXY_PORT, PROXY_DIRECTORY

app = Flask(__name__)
nodes = list()


@app.route('/', methods=['POST'])
def save_node_ip():
    global nodes
    ip_node = request.data.decode('ascii')
    if ip_node not in nodes:
        nodes.append(ip_node)
    print(nodes)
    resharding()
    return "OK"


@app.route('/api/<id>', methods=['GET', 'PUT', 'DELETE'])
def process_data(id):
    global nodes
    n_shard = len(nodes)
    node_number = sharding(int(id), n_shard)
    api_node = "".join(["http://", nodes[node_number], f":{5000}"])
    if request.method == "GET":
        data = requests.get("/".join([api_node, str(id)]))
        return data.text
    if request.method == "PUT":
        data = request.data.decode('ascii')
        requests.put("/".join([api_node, str(id)]), json.dumps(data))
        return "OK"
    if request.method == "DELETE":
        requests.delete("/".join([api_node, str(id)]))
        return "OK"


def sharding(id, n_shard):
    node = id % n_shard
    return node


def resharding():
    global nodes
    n_shard = len(nodes)
    folders = os.listdir(PROXY_DIRECTORY)
    for fold in folders:
        fold_items = [i for i in os.listdir(os.path.join(PROXY_DIRECTORY, fold)) if i.endswith(".json")]
        for db in fold_items:
            db_json_file = open(os.path.join(PROXY_DIRECTORY, fold, db))
            data = json.loads(db_json_file.read())
            for key, value in data.items():
                if fold != nodes[sharding(int(key), n_shard)]:
                    api_node = "".join(["http://", nodes[sharding(int(key), n_shard)], f":{5000}"])
                    requests.put("/".join([api_node, str(key)]), json.dumps(data[key]))
                    del data[key]


def run_server():
    app.run(host=PROXY_IP, port=PROXY_PORT)
