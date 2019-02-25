import json
from flask import Flask, request
from config import DATABASE_NAME, DATABASE_DIRECTORY
import os

app = Flask(__name__)
app.config["DEBUG"] = True

database_path = os.path.join(DATABASE_DIRECTORY, DATABASE_NAME)


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
    if not os.path.exists(DATABASE_DIRECTORY):
        os.makedirs(DATABASE_DIRECTORY)
    db_json_file = open(database_path)
    return json.loads(db_json_file.read())


def write_data_to_db(db_data):
    with open(database_path, 'w') as fout:
        json.dump(db_data, fout)


def handle_bad_request():
    return "No data with this id in database!"


app.register_error_handler(500, handle_bad_request)
app.run(threaded=True)

