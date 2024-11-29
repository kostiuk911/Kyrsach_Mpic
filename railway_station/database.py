import sqlite3

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # Таблиця для користувачів
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                patronymic TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        # Інші таблиці
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS train_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                seat_count INTEGER NOT NULL,
                price_multiplier REAL NOT NULL,
                speed_multiplier REAL NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS routes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                departure TEXT NOT NULL,
                destination TEXT NOT NULL,
                departure_time TEXT NOT NULL,
                arrival_time TEXT NOT NULL,
                base_price REAL NOT NULL,
                train_type_id INTEGER NOT NULL,
                FOREIGN KEY (train_type_id) REFERENCES train_types (id)
            )
        ''')
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS seats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        route_id INTEGER NOT NULL,
        seat_number INTEGER NOT NULL,
        class TEXT NOT NULL,
        price REAL NOT NULL,
        is_booked INTEGER DEFAULT 0,
        FOREIGN KEY (route_id) REFERENCES routes (id)
    )
''')
        conn.commit()