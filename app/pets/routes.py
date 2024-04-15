from . import conn, pets
from app.auth import decorators
from flask import request, render_template, redirect, url_for, session

@pets.route('/', methods=['GET'])
@decorators.login_required
def get_all():
    username = session['username']
    
    cursor = conn.cursor()
   
    query = 'SELECT * FROM Pet WHERE username = %s'
    cursor.execute(query, (username))
    pets = cursor.fetchall()
    
    cursor.close()
    
    return render_template('pets.html', username=username, pets=pets)

@pets.route('/register', methods=['GET', 'POST'])
@decorators.login_required
def register():
    username = session['username']

    if request.method == 'GET':
        return render_template('pets_register.html', form_data={})
    
    elif request.method == 'POST':
        pet_name = request.form['pet_name']
        pet_type = request.form['pet_type']
        pet_size = request.form['pet_size']

        cursor = conn.cursor()
        
        query = 'SELECT * FROM Pet WHERE pet_name = %s AND pet_type = %s AND username = %s'
        cursor.execute(query, (pet_name, pet_type, username))
        pet = cursor.fetchone()

        if pet:
            error = f"You have already registered a {pet_type} named {pet_name}."
            return render_template('pets_register.html', error=error, form_data=request.form)
        else:
            insert_pet_query = 'INSERT INTO Pet (pet_name, pet_type, pet_size, username) VALUES (%s, %s, %s, %s)'
            cursor.execute(insert_pet_query, (pet_name, pet_type, pet_size, username))

            conn.commit()

            cursor.close()

            return redirect(url_for('pets.get_all'))
