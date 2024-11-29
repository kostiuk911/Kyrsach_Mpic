import sqlite3

def add_routes_with_seats():
    routes = [
        ("Kyiv", "Lviv", "08:00", "14:00", 1, 300),  # Інтерсіті
        ("Odessa", "Kharkiv", "06:00", "15:00", 2, 400),  # Нічний експрес
        ("Dnipro", "Zaporizhzhia", "10:30", "11:30", 3, 150),  # Приміський
    ]

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()

        # Додаємо маршрути
        cursor.executemany('''
            INSERT INTO routes (departure, destination, departure_time, arrival_time, train_type_id, base_price)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', routes)
        conn.commit()

        # Отримуємо ID маршрутів
        cursor.execute('SELECT id, base_price FROM routes')
        route_data = cursor.fetchall()

        # Додаємо місця
        for route_id, base_price in route_data:
            seats = []
            for class_type, price_multiplier, seat_count in [
                ('economy', 1.0, 10),
                ('standard', 1.5, 5),
                ('luxury', 2.0, 2),
            ]:
                for seat_number in range(1, seat_count + 1):
                    price = base_price * price_multiplier
                    seats.append((route_id, seat_number, class_type, price, 0))
            cursor.executemany('''
                INSERT INTO seats (route_id, seat_number, class, price, is_booked)
                VALUES (?, ?, ?, ?, ?)
            ''', seats)
        conn.commit()

if __name__ == '__main__':
    add_routes_with_seats()
