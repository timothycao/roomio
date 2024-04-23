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

@apartment.route('/buildings/<company_name>/<building_name>', methods=['GET'])
def get_building(company_name, building_name):
    cursor = conn.cursor()

    get_building_query = 'SELECT * FROM ApartmentBuilding WHERE company_name = %s AND building_name = %s'
    cursor.execute(get_building_query, (company_name, building_name))
    building = cursor.fetchone()

    get_units_query = 'SELECT * FROM ApartmentUnit WHERE company_name = %s AND building_name = %s'
    cursor.execute(get_units_query, (company_name, building_name))
    units = cursor.fetchall()

    get_pet_policies_query = 'SELECT * FROM PetPolicy WHERE company_name = %s AND building_name = %s'
    cursor.execute(get_pet_policies_query, (company_name, building_name))
    pet_policies = cursor.fetchall()

    get_amenities_query = 'SELECT * FROM Amenity NATURAL JOIN BuildingAmenity WHERE company_name = %s AND building_name = %s'
    cursor.execute(get_amenities_query, (company_name, building_name))
    amenities = cursor.fetchall()

    cursor.close()

    if building:
        return render_template('apartment_building.html', building=building, units=units, pet_policies=pet_policies, amenities=amenities)
    else:
        return "Building not found"
