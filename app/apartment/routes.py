from . import conn, apartment
from flask import request, render_template

@apartment.route('/buildings', methods=['GET'])
def get_buildings():
    cursor = conn.cursor()

    query = 'SELECT * FROM ApartmentBuilding'
    
    if request.args:
        where_clauses = []
        params = []

        for key, value in request.args.items():
            where_clauses.append(f'{key}= %s')
            params.append(value)
        
        if where_clauses:
            query += ' WHERE ' + ' AND '.join(where_clauses)
        
        cursor.execute(query, params)
    
    else:
        cursor.execute(query)

    buildings = cursor.fetchall()
    
    cursor.close()
    
    return render_template('apartment_buildings.html', buildings=buildings)
