
from flask import Flask, request, jsonify, g
import sqlite3
import json
import re

app = Flask(__name__)

DATABASE = 'users.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    """Health check endpoint."""
    return "User Management System", 200


@app.route('/users', methods=['GET'])
def get_all_users():
    """Get all users."""
    db = get_db()
    try:
        users = db.execute("SELECT id, name, email FROM users").fetchall()
        users_list = [dict(user) for user in users]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID."""
    db = get_db()
    try:
        user = db.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,)).fetchone()
        if user:
            return jsonify(dict(user)), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user."""
    db = get_db()
    try:
        data = request.get_json(force=True)
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        if not name or not email or not password:
            return jsonify({'error': 'Missing required fields'}), 400
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'error': 'Invalid email format'}), 400
        db.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        db.commit()
        return jsonify({'message': 'User created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user's name and email."""
    db = get_db()
    try:
        data = request.get_json(force=True)
        name = data.get('name')
        email = data.get('email')
        if not name or not email:
            return jsonify({'error': 'Missing required fields'}), 400
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'error': 'Invalid email format'}), 400
        cur = db.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        db.commit()
        if cur.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': 'User updated'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by ID."""
    db = get_db()
    try:
        cur = db.execute("DELETE FROM users WHERE id = ?", (user_id,))
        db.commit()
        if cur.rowcount == 0:
            return jsonify({'error': 'User not found'}), 404
        return jsonify({'message': f'User {user_id} deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/search', methods=['GET'])
def search_users():
    """Search users by name."""
    db = get_db()
    name = request.args.get('name')
    if not name:
        return jsonify({'error': 'Please provide a name to search'}), 400
    try:
        users = db.execute("SELECT id, name, email FROM users WHERE name LIKE ?", (f"%{name}%",)).fetchall()
        users_list = [dict(user) for user in users]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    """User login."""
    db = get_db()
    try:
        data = request.get_json(force=True)
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400
        user = db.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
        if user:
            return jsonify({"status": "success", "user_id": user[0]}), 200
        else:
            return jsonify({"status": "failed"}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)