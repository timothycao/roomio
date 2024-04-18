from . import conn, pets
from app.auth import decorators
from flask import request, render_template, redirect, url_for, session

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

@pets.route('/<pet_name>/<pet_type>', methods=['GET'])
@decorators.login_required
def get_one(pet_name, pet_type):
    username = session['username']

    cursor = conn.cursor()

    query = 'SELECT * FROM Pet WHERE pet_name = %s AND pet_type = %s AND username = %s'
    cursor.execute(query, (pet_name, pet_type, username))
    pet = cursor.fetchone()

    cursor.close()

    if pet:
        return render_template('pets_one.html', username=username, pet=pet)
    else:
        return "Pet not found"

@pets.route('/<pet_name>/<pet_type>/update', methods=['GET', 'POST'])
@decorators.login_required
def update(pet_name, pet_type):
    username = session['username']

    cursor = conn.cursor()

    query = 'SELECT * FROM Pet WHERE pet_name = %s AND pet_type = %s AND username = %s'
    cursor.execute(query, (pet_name, pet_type, username))
    current_pet = cursor.fetchone()

    cursor.close()

    if request.method == 'GET':
        if current_pet:
            return render_template('pets_update.html', username=username, form_data={}, pet=current_pet)
        else:
            return "Pet not found"
    
    elif request.method == 'POST':
        new_pet_name = request.form['pet_name']
        new_pet_type = request.form['pet_type']
        new_pet_size = request.form['pet_size']

        cursor = conn.cursor()

        query = 'SELECT * FROM Pet WHERE pet_name = %s AND pet_type = %s AND username = %s'
        cursor.execute(query, (new_pet_name, new_pet_type, username))
        pet = cursor.fetchone()

        if pet:
            error = f"You already have another {new_pet_type} named {new_pet_name}."
            return render_template('pets_update.html', error=error, form_data=request.form, pet=current_pet)
        else:
            update_pet_query = 'UPDATE Pet SET pet_name = %s, pet_type = %s, pet_size = %s WHERE pet_name = %s AND pet_type = %s AND username = %s'
            cursor.execute(update_pet_query, (new_pet_name, new_pet_type, new_pet_size, pet_name, pet_type, username))

            conn.commit()

            cursor.close()

            return redirect(url_for('pets.get_one', pet_name=new_pet_name, pet_type=new_pet_type))
