from . import conn, interests
from app.auth import decorators
from flask import request, render_template, redirect, url_for, session

@interests.route('/register', methods=['GET', 'POST'])
@decorators.login_required
def register():
    username = session['username']

    if request.method == 'GET':
        return render_template('interests_register.html', form_data={})

    elif request.method == 'POST':
        unit_id = request.form['unit_id']
        roommate_count = request.form['roommate_count']
        move_in_date = request.form['move_in_date']

        cursor = conn.cursor()

        query = 'SELECT * FROM Interest WHERE username = %s AND unit_id = %s'
        cursor.execute(query, (username, unit_id))
        interest = cursor.fetchone()

        if interest:
            error = f'You have already registered an interest for this unit.'
            return render_template('interests_register.html', error=error, form_data=request.form)
        else:
            insert_interest_query = 'INSERT INTO Interest (username, unit_id, roommate_count, move_in_date) VALUES (%s, %s, %s, %s)'
            cursor.execute(insert_interest_query, (username, unit_id, roommate_count, move_in_date))

            conn.commit()

            cursor.close()

            return redirect(url_for('apartment.get_unit', unit_id=unit_id))
