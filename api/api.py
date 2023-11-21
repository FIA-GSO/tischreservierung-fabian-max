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

# To show all reservations that have been made
@app.route('/api/v1/reservations/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_tables = cur.execute('SELECT * FROM reservierungen;').fetchall()
    
    return jsonify(all_tables)

# To reserv a table in a given timeframe
@app.route('/api/v1/reservations', methods=['GET','POST'])
def api_add():
    zeitpunkt = request.form.get('zeitpunkt')
    tischnummer = request.form.get('tischnummer')
    pin = request.form.get('pin')
    storniert = 'False'

    if not zeitpunkt or not tischnummer or not pin:
        conn.close()
        return jsonify({"error": f"All parameters are required. You provided {zeitpunkt}, {tischnummer}, {pin}"}), 400

    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query = '''
    INSERT INTO reservierungen (zeitpunkt, tischnummer, pin, storniert)
    VALUES (?, ?, ?, ?)
    '''

    cur.execute(query, (zeitpunkt, tischnummer, pin, storniert))
    conn.commit()
    conn.close()

    return jsonify({"success": True}), 201
    



# To show all tables that exist in the restaurant
@app.route('/api/v1/tables/all', methods=['GET'])
def api_tables():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    api_tables = cur.execute('''
        SELECT *
        FROM tische
     ''').fetchall()
    conn.close()
    return jsonify(api_tables)

#To show all available tables in a given timeframe
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
    conn.close()
    return jsonify(available_tables)

# To show all reserved tables ordered by time
@app.route('/api/v1/tables/reserved', methods=['GET'])
def api_reserved():
    conn = sqlite3.connect('restaurant.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    api_tables = cur.execute('''
        SELECT tischNummer, zeitpunkt
        FROM reservierungen
        ORDER BY zeitpunkt ASC
        
    ''').fetchall()
    conn.close()
    return jsonify(api_tables)





if __name__ == "__main__":
    app.run()