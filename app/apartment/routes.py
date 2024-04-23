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

@apartment.route('/units', methods=['GET'])
def get_units():
    cursor = conn.cursor()

    query = 'SELECT * FROM ApartmentUnit'
    
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

    units = cursor.fetchall()
    
    cursor.close()
    
    return render_template('apartment_units.html', units=units)

@apartment.route('/units/<unit_id>', methods=['GET'])
def get_unit(unit_id):
    cursor = conn.cursor()

    get_unit_query = 'SELECT * FROM ApartmentUnit NATURAL JOIN ApartmentBuilding WHERE unit_id = %s'
    cursor.execute(get_unit_query, (unit_id))
    unit = cursor.fetchone()

    get_rooms_query = 'SELECT * FROM Room WHERE unit_id = %s'
    cursor.execute(get_rooms_query, (unit_id))
    rooms = cursor.fetchall()

    get_unit_amenities_query = 'SELECT * FROM Amenity NATURAL JOIN UnitAmenity WHERE unit_id = %s'
    cursor.execute(get_unit_amenities_query, (unit_id))
    unit_amenities = cursor.fetchall()

    # Building details
    company_name = unit['company_name']
    building_name = unit['building_name']

    get_pet_policies_query = 'SELECT * FROM PetPolicy WHERE company_name = %s AND building_name = %s'
    cursor.execute(get_pet_policies_query, (company_name, building_name))
    pet_policies = cursor.fetchall()

    get_building_amenities_query = 'SELECT * FROM Amenity NATURAL JOIN BuildingAmenity WHERE company_name = %s AND building_name = %s'
    cursor.execute(get_building_amenities_query, (company_name, building_name))
    building_amenities = cursor.fetchall()

    cursor.close()

    if unit:
        return render_template('apartment_unit.html', unit=unit, rooms=rooms, unit_amenities=unit_amenities, pet_policies=pet_policies, building_amenities=building_amenities)
    else:
        return "Unit not found"
