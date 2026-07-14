import sqlite3
from datetime import datetime

DATABASE = "database.db"


# -----------------------------
# Database Connection
# -----------------------------
def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Create Tables
# -----------------------------
def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        role TEXT

    )
    """)

    # Predictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        temp REAL,

        humidity REAL,

        cloud_cover REAL,

        annual REAL,

        jan_feb REAL,

        mar_may REAL,

        jun_sep REAL,

        oct_dec REAL,

        avgjune REAL,

        subdivision REAL,

        prediction TEXT,

        prediction_date TEXT,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# Register User
# -----------------------------
def register_user(name, email, password, role):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users(name,email,password,role)
        VALUES(?,?,?,?)
        """,
        (name, email, password, role)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Login User
# -----------------------------
def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email=? AND password=?
        """,
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# -----------------------------
# Save Prediction
# -----------------------------
def save_prediction(user_id,
                    temp,
                    humidity,
                    cloud_cover,
                    annual,
                    jan_feb,
                    mar_may,
                    jun_sep,
                    oct_dec,
                    avgjune,
                    subdivision,
                    prediction):

    conn = get_connection()
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    cursor.execute("""
        INSERT INTO predictions(
            user_id,
            temp,
            humidity,
            cloud_cover,
            annual,
            jan_feb,
            mar_may,
            jun_sep,
            oct_dec,
            avgjune,
            subdivision,
            prediction,
            prediction_date
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
        user_id,
        temp,
        humidity,
        cloud_cover,
        annual,
        jan_feb,
        mar_may,
        jun_sep,
        oct_dec,
        avgjune,
        subdivision,
        prediction,
        current_date
    ))

    conn.commit()
    conn.close()


# -----------------------------
# Prediction History
# -----------------------------
def get_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM predictions
        WHERE user_id=?
        ORDER BY id DESC
    """, (user_id,))

    history = cursor.fetchall()

    conn.close()

    return history