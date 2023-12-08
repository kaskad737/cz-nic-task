from flask import Flask, jsonify, make_response
import os
import mimetypes 

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000

MOCK_DATABASE = {
    '1': {'uuid': 1, 'file_path': './files/', 'file_name': 'test_file_1.txt'},
    '2': {'uuid': 2, 'file_path': './files/', 'file_name': 'test_file_2.txt'},
    '3': {'uuid': 3, 'file_path': './files/', 'file_name': 'test_file_3.txt'},
    '4': {'uuid': 4, 'file_path': './files/', 'file_name': 'test_file_4.txt'},
}

@app.route('/file/<uuid>/stat/', methods=['GET'])
def file_metadata(uuid):
    data_from_db = MOCK_DATABASE.get(uuid)
    if data_from_db:
        file_path = data_from_db['file_path'] + data_from_db['file_name']
        file_name = os.path.basename(file_path)
        if not os.path.isfile(file_path):
            return 'File not found. Error code 404', 404
        else:
            create_datetime = os.path.getmtime(file_path)
            size = os.path.getsize(file_path)
            mimetype = mimetypes.guess_type(file_path)[0]
            name = os.path.splitext(file_name)[0]

            file_metadata = {
                'create_datetime': create_datetime,
                'size': size,
                'mimetype': mimetype,
                'name': name,
            }

            return jsonify(file_metadata)
    else:
        return 'File not found. Error code 404', 404
    
@app.route('/file/<uuid>/read/', methods=['GET'])
def read_file(uuid):
    data_from_db = MOCK_DATABASE.get(uuid)
    if data_from_db:
        file_path = data_from_db['file_path'] + data_from_db['file_name']
        file_name = os.path.basename(file_path)

        if not os.path.isfile(file_path):
            return 'File not found. Error code 404', 404

        mimetype = mimetypes.guess_type(file_path)

        with open(file_path, 'r') as f:
            file_content = f.read()

        resp = make_response(file_content, 200)
        resp.headers['Content-Disposition'] = f'inline; filename="{file_name}"'
        resp.headers['Content-Type'] = mimetype[0]

        return resp
    else:
        return 'File not found. Error code 404', 404

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
