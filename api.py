from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = 'free_food.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/events', methods=['GET'])
def get_events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM food_events WHERE status = "PENDING"').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in events])

@app.route('/api/events/<int:event_id>/approve', methods=['POST'])
def approve_event(event_id):
    conn = get_db_connection()
    conn.execute('UPDATE food_events SET status = "APPROVED" WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/events/<int:event_id>/reject', methods=['POST'])
def reject_event(event_id):
    conn = get_db_connection()
    conn.execute('UPDATE food_events SET status = "REJECTED" WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/downloads/<path:filename>')
def serve_image(filename):
    return send_from_directory('downloads', filename)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
