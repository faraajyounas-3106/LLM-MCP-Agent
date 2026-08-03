import sqlite3
import os
from datetime import datetime

# Place database file in the same directory as this db.py file
DB_PATH = os.path.join(os.path.dirname(__file__), "weather_log.db")

def init_db():
    """Initializes the database and creates tables if they do not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS request_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            requested_date TEXT,
            status TEXT,
            condition TEXT,
            temp_c REAL,
            humidity_pct INTEGER,
            error_message TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Auto-initialize database on import
init_db()

def log_request(city: str, requested_date: str, result: dict) -> None:
    """Logs the details of a weather request into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    status = result.get("status", "error")
    condition = None
    temp_c = None
    humidity_pct = None
    error_message = None
    
    if status == "success":
        condition = result.get("condition")
        temp_c = result.get("temp_c")
        humidity_pct = result.get("humidity_pct") or result.get("humidity")
    else:
        error_message = result.get("message", "Unknown error occurred.")
        
    cursor.execute("""
        INSERT INTO request_log (city, requested_date, status, condition, temp_c, humidity_pct, error_message, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        city,
        requested_date,
        status,
        condition,
        temp_c,
        humidity_pct,
        error_message,
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

def get_recent_logs(limit: int = 10) -> list[dict]:
    """Returns the most recent N logged requests, newest first, as a list of dicts."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, city, requested_date, status, condition, temp_c, humidity_pct, error_message, timestamp
        FROM request_log
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    results = [dict(row) for row in rows]
    conn.close()
    return results
