import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def init_db():
    try:
        with sqlite3.connect("restaurant.db") as con:
            with open("schema.sql", "r") as f:
                con.executescript(f.read())
    except Exception as e:
        print(f"Error initializing database: {e}")

init_db()

@app.route('/', methods=['GET'])
def home():
    return "<h1>Tischreservierung</h1>"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/api/v1/reservations/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_tables = cur.execute('SELECT * FROM reservierungen;').fetchall()
    
    return jsonify(all_tables)

@app.route('/api/v1/tables/all', methods=['GET'])
def api_tables():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    api_tables = cur.execute('''
        SELECT *
        FROM tische
     ''').fetchall()
    
    return jsonify(api_tables)

@app.route('/api/v1/tables/available', methods=['GET'])
def api_available_within_timeframe():
    start_zeitpunkt = request.args.get('start_zeitpunkt')
    end_zeitpunkt = request.args.get('end_zeitpunkt')

    if not start_zeitpunkt or not end_zeitpunkt:
        return jsonify({"error": "Both start_zeitpunkt and end_zeitpunkt are required"}), 400

    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query = '''
    SELECT t.tischnummer, t.anzahlPlaetze
    FROM tische AS t
    WHERE t.tischnummer NOT IN (
        SELECT r.tischnummer
        FROM reservierungen AS r
        WHERE r.zeitpunkt BETWEEN ? AND ?
    )
    '''
    
    available_tables = cur.execute(query, (start_zeitpunkt, end_zeitpunkt)).fetchall()
    
    return jsonify(available_tables)




if __name__ == "__main__":
    app.run()