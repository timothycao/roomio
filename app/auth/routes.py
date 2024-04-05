from app import app, conn
from flask import request, render_template

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', form_data={})
    
    elif request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        email_address = request.form['email_address']
        phone_number = request.form['phone_number']
        password = request.form['password']

        cursor = conn.cursor()

        query = 'SELECT * FROM User WHERE username = %s'
        cursor.execute(query, (username))
        data = cursor.fetchone()

        if data:
            error = "This username is already taken"
            return render_template('register.html', error = error, form_data=request.form)
        else:
            insert_user_query = 'INSERT INTO User (username, first_name, last_name, date_of_birth, gender, password) VALUES (%s, %s, %s, %s, %s, %s)'
            cursor.execute(insert_user_query, (username, first_name, last_name, date_of_birth, gender, password))

            insert_email_query = 'INSERT INTO UserEmail (email_address, username) VALUES (%s, %s)'
            cursor.execute(insert_email_query, (email_address, username))

            insert_phone_query = 'INSERT INTO UserPhone (phone_number, username) VALUES (%s, %s)'
            cursor.execute(insert_phone_query, (phone_number, username))

            conn.commit()

            cursor.close()

            return render_template('login.html')
