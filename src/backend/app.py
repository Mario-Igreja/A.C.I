import os
from flask import Flask, request, jsonify
from tinydb import TinyDB, Query

# Flask App
app = Flask(__name__)
db_file = os.getenv("DB_FILE", "db.json")
db = TinyDB(db_file)

@app.route('/data', methods=['POST'])
def save_data():
    data = request.json
    db.insert(data)
    return jsonify({"message": "Data saved"}), 201

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(db.all()), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501)
