from . import conn, apartment
from flask import request, render_template

@apartment.route('/buildings', methods=['GET'])
def get_buildings():
    cursor = conn.cursor()

    query = 'SELECT * FROM ApartmentBuilding'
    
    conditions = []
    params = []

    if request.args:
        company_name = request.args.get('company_name')
        building_name = request.args.get('building_name')
        city = request.args.get('city')
        state = request.args.get('state')
        zip_code = request.args.get('zip_code')

        if company_name:
            conditions.append('company_name LIKE %s')
            params.append(f'%{company_name}%')
        
        if building_name:
            conditions.append('building_name LIKE %s')
            params.append(f'%{building_name}%')
        
        if city:
            conditions.append('city = %s')
            params.append(city)
        
        if state:
            conditions.append('state = %s')
            params.append(state)
        
        if zip_code:
            conditions.append('zip_code = %s')
            params.append(zip_code)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
    
    cursor.execute(query, params)
    buildings = cursor.fetchall()
    
    cursor.close()
    
    return render_template('apartment_buildings.html', buildings=buildings, has_searched=bool(request.args))

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

    conditions = []
    params = []

    if request.args:
        # unit attributes
        min_monthly_rent = request.args.get('min_monthly_rent')
        max_monthly_rent = request.args.get('max_monthly_rent')
        min_unit_size = request.args.get('min_unit_size')
        available_date = request.args.get('available_date')
        company_name = request.args.get('company_name')
        building_name = request.args.get('building_name')

        if min_monthly_rent:
            conditions.append('monthly_rent >= %s')
            params.append(min_monthly_rent)
        
        if max_monthly_rent:
            conditions.append('monthly_rent <= %s')
            params.append(max_monthly_rent)
        
        if min_unit_size:
            conditions.append('unit_size >= %s')
            params.append(min_unit_size)
        
        if available_date:
            conditions.append('available_date = %s')
            params.append(available_date)
        
        if company_name:
            conditions.append('company_name LIKE %s')
            params.append(f'%{company_name}%')
        
        if building_name:
            conditions.append('building_name LIKE %s')
            params.append(f'%{building_name}%')
        
        # building attributes
        city = request.args.get('city')
        state = request.args.get('state')
        zip_code = request.args.get('zip_code')

        if any([city, state, zip_code]):    # ApartmentUnit already contains company_name and building_name
            query += ' NATURAL JOIN ApartmentBuilding'
            
            if city:
                conditions.append('city = %s')
                params.append(city)
            
            if state:
                conditions.append('state = %s')
                params.append(state)
            
            if zip_code:
                conditions.append('zip_code = %s')
                params.append(zip_code)
    
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

    cursor.execute(query, params)
    units = cursor.fetchall()
    
    cursor.close()
    
    return render_template('apartment_units.html', units=units, has_searched=bool(request.args))

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
