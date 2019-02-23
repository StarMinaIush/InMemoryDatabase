import json
from flask import Flask, request
from config import DATABASE_NAME


def run():
    app = Flask(__name__)
    app.config["DEBUG"] = True

    @app.route('/<id>', methods=['GET', 'PUT', 'DELETE'])
    def process_data(data_id):
        db_json_file = open(DATABASE_NAME)
        db_data = json.loads(db_json_file.read())

        if request.method == 'GET':
            return db_data[data_id]

        if request.method == 'PUT':
            db_data[data_id] = request.data.decode('ascii')
            write_data_to_db(db_data)
            return "data was added to database"

        if request.method == 'DELETE':
            del db_data[data_id]
            write_data_to_db(db_data)
            return "data was deleted from database"

    def write_data_to_db(db_data):
        with open(DATABASE_NAME, 'w') as fout:
            json.dump(db_data, fout)

    def handle_bad_request():
        return "No data with this id in database!"
    
    app.register_error_handler(500, handle_bad_request)
    app.run(threaded=True)
