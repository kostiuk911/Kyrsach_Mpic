import sqlite3

def populate_train_types():
    train_types = [
        ("Інтерсіті", 100, 1.5, 1.2),  # 100 місць, дорожче, швидше
        ("Нічний експрес", 50, 1.0, 0.8),  # 50 місць, стандартна ціна
        ("Приміський", 200, 0.8, 1.0)  # 200 місць, дешевше
    ]

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO train_types (name, seat_count, price_multiplier, speed_multiplier) VALUES (?, ?, ?, ?)', train_types)
        conn.commit()

    print(f"{len(train_types)} train types added successfully!")

if __name__ == '__main__':
    populate_train_types()
