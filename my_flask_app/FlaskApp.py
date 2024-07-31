from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return jsonify([dict(row) for row in users])

@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO users (name, age) VALUES (?, ?)',
                 (new_user['name'], new_user['age']))
    conn.commit()
    conn.close()
    return jsonify(new_user), 201

if __name__ == '__main__':
    app.run(debug=True)
