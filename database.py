import sqlite3

DB = "aviator.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS multipliers (id INTEGER PRIMARY KEY, value REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    c.execute('CREATE TABLE IF NOT EXISTS predictions (id INTEGER PRIMARY KEY, result REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    conn.close()

def save_multiplier(v):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('INSERT INTO multipliers (value) VALUES (?)', (v,))
    conn.commit()
    conn.close()

def save_prediction(r):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('INSERT INTO predictions (result) VALUES (?)', (r,))
    conn.commit()
    conn.close()

def get_last_predictions(n=10):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT result, timestamp FROM predictions ORDER BY timestamp DESC LIMIT ?', (n,))
    res = c.fetchall()
    conn.close()
    return res

def get_last_multipliers(n=20):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT value FROM multipliers ORDER BY timestamp DESC LIMIT ?', (n,))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]