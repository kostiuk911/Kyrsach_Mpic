from flask import Flask, render_template, request, redirect, flash, session
from database import init_db  # Імпортуємо функцію для ініціалізації бази даних
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Перевіряємо або створюємо базу даних
if not os.path.exists('database.db'):
    init_db()

# Початкова сторінка з вибором між реєстрацією та входом
@app.route('/')
def home():
    user_name = session.get('user_name', None)
    return render_template('home.html', user_name=user_name)

# Сторінка логіну
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
            user = cursor.fetchone()

        if user:
            # Збереження ID і імені користувача у сесії
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            flash('Login successful!', 'success')
            return redirect('/routes')  # Перенаправлення на сторінку маршрутів
        else:
            flash('Invalid email or password!', 'error')
            return redirect('/login')  # Повернення на сторінку входу
    return render_template('login.html')

# Сторінка реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        patronymic = request.form['patronymic']

        if not all([first_name, last_name, patronymic]):
            flash('All fields are required!', 'error')
            return redirect('/register')

        session['first_name'] = first_name
        session['last_name'] = last_name
        session['patronymic'] = patronymic

        return redirect('/register-step-2')

    return render_template('register_step_1.html')

@app.route('/register-step-2', methods=['GET', 'POST'])
def register_step_2():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect('/register-step-2')

        first_name = session.get('first_name')
        last_name = session.get('last_name')
        patronymic = session.get('patronymic')

        if not all([first_name, last_name, patronymic]):
            flash('Session data is missing. Please restart registration.', 'error')
            return redirect('/register')

        try:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (first_name, last_name, patronymic, email, password) VALUES (?, ?, ?, ?, ?)',
                               (first_name, last_name, patronymic, email, password))
                conn.commit()
            session.clear()
            flash('Registration successful! Please login.', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')

    return render_template('register_step_2.html')

# Сторінка перегляду всіх маршрутів
@app.route('/routes')
def routes():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # Об'єднання таблиць routes і train_types для отримання назви типу поїзда
        cursor.execute('''
            SELECT routes.id, routes.departure, routes.destination, routes.departure_time,
                   routes.arrival_time, train_types.name
            FROM routes
            JOIN train_types ON routes.train_type_id = train_types.id
        ''')
        routes = cursor.fetchall()  # Отримуємо всі дані про рейси
    return render_template('routes.html', routes=routes)



# Сторінка перегляду місць для обраного рейсу
@app.route('/seats/<int:route_id>')
def view_seats(route_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM seats WHERE route_id = ?', (route_id,))
        seats = cursor.fetchall()
        cursor.execute('SELECT departure, destination FROM routes WHERE id = ?', (route_id,))
        route = cursor.fetchone()

    return render_template('seats.html', seats=seats, route=route)




# Бронювання місця
@app.route('/book/<int:seat_id>', methods=['POST'])
def book_seat(seat_id):
    # Отримання класу вагона з форми
    wagon_class = request.form.get('wagon_class')

    if not wagon_class:
        flash('Wagon class is missing. Please try again.', 'error')
        return redirect(request.referrer)

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        # Бронювання місця
        cursor.execute('UPDATE seats SET is_booked = 1 WHERE id = ? AND is_booked = 0', (seat_id,))
        conn.commit()
        if cursor.rowcount > 0:
            flash(f'Seat successfully booked in {wagon_class.capitalize()} class!', 'success')
        else:
            flash('Seat is already booked.', 'error')
    return redirect(request.referrer)



if __name__ == '__main__':
    app.run(debug=True)
import sqlite3