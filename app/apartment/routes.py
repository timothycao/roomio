from . import conn, apartment
from flask import request, render_template, session

@apartment.route('/buildings', methods=['GET'])
def get_buildings():
    cursor = conn.cursor()

    select_clause = 'SELECT company_name, building_name, street_number, street_name, city, state, zip_code, year_built, COUNT(*) AS unit_count'
    from_clause = ' FROM ApartmentBuilding NATURAL JOIN ApartmentUnit'
    conditions = []
    params = []
    group_by_clause = ' GROUP BY company_name, building_name'

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

    query = select_clause + from_clause
    if conditions:
        query += f' WHERE {' AND '.join(conditions)}'
    query += group_by_clause

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

    get_units_query = (
        'SELECT unit_id, unit_number, monthly_rent, unit_size, available_date, '
        'SUM(CASE WHEN room_name LIKE %s THEN 1 ELSE 0 END) AS bedroom_count, '
        'SUM(CASE WHEN room_name LIKE %s THEN 1 ELSE 0 END) AS bathroom_count '
        'FROM ApartmentUnit NATURAL JOIN Room '
        'WHERE company_name = %s AND building_name = %s '
        'GROUP BY unit_id'
    )
    cursor.execute(get_units_query, (f'bedroom%', f'bathroom%', company_name, building_name))
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

    get_building_amenities_query = 'SELECT DISTINCT amenity_name FROM BuildingAmenity'
    cursor.execute(get_building_amenities_query)
    building_amenities = cursor.fetchall()

    get_unit_amenities_query = 'SELECT DISTINCT amenity_name FROM UnitAmenity'
    cursor.execute(get_unit_amenities_query)
    unit_amenities = cursor.fetchall()

    # bedroom and bathroom count
    with_clause = (
        'WITH RoomCount AS ('
            'SELECT au.unit_id, '
            'SUM(CASE WHEN r.room_name LIKE %s THEN 1 ELSE 0 END) AS bedroom_count, '
            'SUM(CASE WHEN r.room_name LIKE %s THEN 1 ELSE 0 END) AS bathroom_count '
            'FROM ApartmentUnit au JOIN Room r ON au.unit_id = r.unit_id '
            'GROUP BY au.unit_id'
        ')'
    )
    select_clause = (
        ' SELECT au.company_name AS company_name, '
        'au.building_name AS building_name, '
        'au.unit_id AS unit_id, '
        'au.unit_number AS unit_number, '
        'au.monthly_rent AS monthly_rent, '
        'au.unit_size AS unit_size, '
        'au.available_date AS available_date, '
        'rc.bedroom_count AS bedroom_count, '
        'rc.bathroom_count AS bathroom_count, '
        'GROUP_CONCAT(DISTINCT ua.amenity_name SEPARATOR %s) AS unit_amenities, '
        'GROUP_CONCAT(DISTINCT ba.amenity_name SEPARATOR %s) AS building_amenities'
    )
    from_clause = (
        ' FROM ApartmentUnit AS au NATURAL JOIN RoomCount AS rc '
        'LEFT JOIN UnitAmenity AS ua ON au.unit_id = ua.unit_id '
        'LEFT JOIN BuildingAmenity AS ba ON au.company_name = ba.company_name AND au.building_name = ba.building_name'
    )
    conditions = []
    params = [f'bedroom%', f'bathroom%', ', ', ', ']
    group_by_clause = ' GROUP BY au.unit_id'

    pet_count = 0

    if request.args:
        # unit attributes
        min_monthly_rent = request.args.get('min_monthly_rent')
        max_monthly_rent = request.args.get('max_monthly_rent')
        min_unit_size = request.args.get('min_unit_size')
        available_date = request.args.get('available_date')
        company_name = request.args.get('company_name')
        building_name = request.args.get('building_name')

        if min_monthly_rent:
            conditions.append('au.monthly_rent >= %s')
            params.append(min_monthly_rent)

        if max_monthly_rent:
            conditions.append('au.monthly_rent <= %s')
            params.append(max_monthly_rent)

        if min_unit_size:
            conditions.append('au.unit_size >= %s')
            params.append(min_unit_size)

        if available_date:
            conditions.append('au.available_date = %s')
            params.append(available_date)

        if company_name:
            conditions.append('au.company_name LIKE %s')
            params.append(f'%{company_name}%')

        if building_name:
            conditions.append('au.building_name LIKE %s')
            params.append(f'%{building_name}%')

        # building attributes
        city = request.args.get('city')
        state = request.args.get('state')
        zip_code = request.args.get('zip_code')

        if any([city, state, zip_code]):    # ApartmentUnit already contains company_name and building_name
            select_clause += ', ab.city AS city, ab.state AS state, ab.zip_code AS zip_code'
            from_clause += ' NATURAL JOIN ApartmentBuilding AS ab'

            if city:
                conditions.append('ab.city = %s')
                params.append(city)

            if state:
                conditions.append('ab.state = %s')
                params.append(state)

            if zip_code:
                conditions.append('ab.zip_code = %s')
                params.append(zip_code)

        # amenities

        selected_building_amenities = request.args.getlist('building_amenities')
        if selected_building_amenities:
            condition = '(SELECT COUNT(DISTINCT amenity_name) FROM BuildingAmenity WHERE company_name = au.company_name AND building_name = au.building_name AND amenity_name IN ('
            for i, building_amenity in enumerate(selected_building_amenities):
                if i == len(selected_building_amenities) - 1:
                    condition += '%s'
                else:
                    condition += '%s, '
                params.append(building_amenity)
            condition += ')) = %s'
            conditions.append(condition)
            params.append(len(selected_building_amenities))

        selected_unit_amenities = request.args.getlist('unit_amenities')
        if selected_unit_amenities:
            condition = '(SELECT COUNT(DISTINCT amenity_name) FROM UnitAmenity WHERE unit_id = au.unit_id AND amenity_name IN ('
            for i, unit_amenity in enumerate(selected_unit_amenities):
                if i == len(selected_unit_amenities) - 1:
                    condition += '%s'
                else:
                    condition += '%s, '
                params.append(unit_amenity)
            condition += ')) = %s'
            conditions.append(condition)
            params.append(len(selected_unit_amenities))

        # pet policies
        if 'username' in session and 'pets' in session:
            pet_count = len(session['pets'])
            pet_conditions = []
            for i, pet in enumerate(session['pets']):
                select_clause += f', pp{i}.pet_type AS pp{i}_pet_type, pp{i}.pet_size AS pp{i}_pet_size, pp{i}.is_pet_allowed AS pp{i}_is_pet_allowed'
                from_clause += f' JOIN PetPolicy AS pp{i} ON au.company_name = pp{i}.company_name AND au.building_name = pp{i}.building_name'
                pet_conditions.append(f'(pp{i}.pet_type = %s AND pp{i}.pet_size = %s)')
                params.append(pet['pet_type'])
                params.append(pet['pet_size'])

            if pet_conditions:
                conditions.append(f'({' AND '.join(pet_conditions)})')

    query = with_clause + select_clause + from_clause
    if conditions:
        query += f' WHERE {' AND '.join(conditions)}'
    query += group_by_clause

    cursor.execute(query, params)
    units = cursor.fetchall()

    cursor.close()

    # print('query: ', query, flush=True)
    # print('units: ', units, flush=True)

    return render_template('apartment_units.html', units=units, pet_count=pet_count, building_amenities=building_amenities, unit_amenities=unit_amenities, has_searched=bool(request.args))

@apartment.route('/units/<unit_id>', methods=['GET'])
def get_unit(unit_id):
    cursor = conn.cursor()

    get_unit_query = 'SELECT * FROM ApartmentUnit NATURAL JOIN ApartmentBuilding WHERE unit_id = %s'
    cursor.execute(get_unit_query, (unit_id))
    unit = cursor.fetchone()

    get_rooms_query = 'SELECT * FROM Room WHERE unit_id = %s'
    cursor.execute(get_rooms_query, (unit_id))
    rooms = cursor.fetchall()

    bedrooms = []
    bathrooms = []
    other_rooms = []
    for room in rooms:
        if room['room_name'].startswith('bedroom'):
            bedrooms.append(room)
        elif room['room_name'].startswith('bathroom'):
            bathrooms.append(room)
        else:
            other_rooms.append(room)

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

    # Interests
    username = ''
    interests = []
    if ('username' in session):
        username = session['username']
        get_interests_query = 'SELECT * FROM Interest WHERE unit_id = %s'
        cursor.execute(get_interests_query, (unit_id))
        interests = cursor.fetchall()

    cursor.close()

    if unit:
        return render_template('apartment_unit.html', unit=unit, bedrooms=bedrooms, bathrooms=bathrooms, other_rooms=other_rooms, unit_amenities=unit_amenities, pet_policies=pet_policies, building_amenities=building_amenities, interests=interests, username=username)
    else:
        return "Unit not found"
