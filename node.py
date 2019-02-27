import json
import sys
from werkzeug.exceptions import abort
from flask import Flask, request
import requests
from config import DATABASE_NAME, PROXY_IP, PROXY_PORT, PROXY_DIRECTORY, REPLICATION_MODEL
import os
import asyncio

app = Flask(__name__)
database_path = ""
slaves = list()


def register_me(ip):
    registered = False
    while not registered:
        try:
            requests.post(f"http://{PROXY_IP}:{PROXY_PORT}", data=ip)
            registered = True
        except requests.RequestException:
            continue
    print('cause i am try')


@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def process_data(id):
    if request.method == 'GET':
        db_data = open_db()
        if id in db_data:
            return db_data[id]
        else:
            abort(404)

    if request.method == 'PUT':
        db_data = dict()
        if os.path.isfile(database_path):
            db_data = open_db()
        db_data[id] = request.data.decode('utf-8')
        write_data_to_db(db_data)

        if REPLICATION_MODEL == "sync":
            replicate_data(db_data)
        if REPLICATION_MODEL == "async":
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(replicate_data(db_data))
            replicate_data(db_data)

        return "data was added to database"

    if request.method == 'DELETE':
        db_data = open_db()
        if id in db_data:
            del db_data[id]
        else:
            abort(404)
        write_data_to_db(db_data)
        return "data was deleted from database"


async def replicate_data(db_data):
    global slaves
    for i in slaves:
        slave_node = "".join(["http://", i, f":{5000}"])
        requests.put("/".join([slave_node, str(i)]), json.dumps(db_data[id]))


def open_db():
    db_json_file = open(database_path)
    return json.loads(db_json_file.read())


def write_data_to_db(db_data):
    with open(database_path, 'w') as fout:
        json.dump(db_data, fout)


def run(ip, port):
    if not os.path.exists(os.path.join(PROXY_DIRECTORY, ip)):
        os.makedirs(os.path.join(PROXY_DIRECTORY, ip))
    global database_path
    database_path = os.path.join(PROXY_DIRECTORY, ip, DATABASE_NAME)
    register_me(ip)
    app.run(host=ip, port=port, threaded=True)


def set_slaves(slave: list):
    global slaves
    slaves = slave


if __name__ == "__main__":
    node_ip = sys.argv[1]
    port = sys.argv[2]
    run(node_ip, port)
