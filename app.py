from flask import Flask, redirect, render_template, request, url_for
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'd',
    'database': 'web_app',
    'port': 3306
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG, cursorclass=DictCursor)
        
def get_user_data(username, password):
    search_sql = "SELECT * FROM auth_data WHERE username=%s AND password=%s;"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(search_sql, (username, password))
            rows = cursor.fetchall()
            if rows:
                user_data = rows[0]
                return user_data
            else:
                return {}

def check_username(username):
    search_sql = "SELECT * FROM auth_data WHERE username=%s;"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(search_sql, (username))
            rows = cursor.fetchall()
            if rows:
                return True
            else:
                return False

def add_new_user(username, password):
    write_sql = "INSERT INTO auth_data (username, password) VALUES (%s, %s)"
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(write_sql, (username, password))
            connection.commit()
        

@app.route('/')
def home():
    message = request.args.get('message')
    return render_template('home.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = request.args.get('message')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        # check if the username already exists
        user_exist = check_username(username)

        if not username or not password or not password_confirm:
            return redirect(url_for('register', message='All fields are required.'))
        if password != password_confirm:
            return redirect(url_for('register', message='Passwords do not match.'))
        if user_exist == True:
            return redirect(url_for('login', message='Username already exists. Please login instead.'))
        
        return redirect(url_for('home', message='You are now registered.'))
    
    return render_template('register.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = request.args.get('message')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # get the data from the DB
        user_data = get_user_data(username, password)
        if user_data and username == user_data['username'] and password == user_data['password']:
            return redirect(url_for('home', message='You are now logged in.'))
        else:
            return redirect(url_for('login', message='Invalid username or password. Please try again.'))
        
    return render_template('login.html', message=message)


if __name__=='__main__':
    #app.run()
    add_new_user('Carl', 'HELLOCARL')
    print(check_username('Carl'))