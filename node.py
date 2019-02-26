import json
import sys

from flask import Flask, request
import requests
from config import DATABASE_NAME, PROXY_IP, PROXY_PORT, PROXY_DIRECTORY
import os

app = Flask(__name__)
database_path = ""


def register_me(ip):
    requests.post(f"http://{PROXY_IP}:{PROXY_PORT}", data=ip)


@app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
def process_data(id):
    if request.method == 'GET':
        db_data = open_db()
        return db_data[id]
    if request.method == 'PUT':
        db_data = dict()
        if os.path.isfile(database_path):
            db_data = open_db()
        db_data[id] = request.data.decode('ascii')
        write_data_to_db(db_data)
        return "data was added to database"
    if request.method == 'DELETE':
        db_data = open_db()
        del db_data[id]
        write_data_to_db(db_data)
        return "data was deleted from database"


def open_db():
    db_json_file = open(database_path)
    return json.loads(db_json_file.read())


def write_data_to_db(db_data):
    with open(database_path, 'w') as fout:
        json.dump(db_data, fout)


def handle_bad_request():
    return "No data with this id in database!"


app.register_error_handler(500, handle_bad_request)


def run(ip, port):
    if not os.path.exists(os.path.join(PROXY_DIRECTORY, ip)):
        os.makedirs(os.path.join(PROXY_DIRECTORY, ip))
    global database_path
    database_path = os.path.join(PROXY_DIRECTORY, ip, DATABASE_NAME)
    register_me(ip)
    app.run(host=ip, port=port, threaded=True)


if __name__ == "__main__":
    node_ip = sys.argv[1]
    port = sys.argv[2]
    run(node_ip, port)
