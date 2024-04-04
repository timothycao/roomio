DROP TABLE IF EXISTS UnitAmenity;
DROP TABLE IF EXISTS BuildingAmenity;
DROP TABLE IF EXISTS Interest;
DROP TABLE IF EXISTS Amenity;
DROP TABLE IF EXISTS PetPolicy;
DROP TABLE IF EXISTS Room;
DROP TABLE IF EXISTS ApartmentUnit;
DROP TABLE IF EXISTS ApartmentBuilding;
DROP TABLE IF EXISTS Pet;
DROP TABLE IF EXISTS UserPhone;
DROP TABLE IF EXISTS UserEmail;
DROP TABLE IF EXISTS User;

CREATE TABLE User (
    username VARCHAR(20) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender TINYINT NOT NULL,
    password VARCHAR(200),
    PRIMARY KEY (username)
);

CREATE TABLE UserEmail (
    email_address VARCHAR(50) NOT NULL,
    username VARCHAR(20) NOT NULL,
    PRIMARY KEY (email_address, username),
    FOREIGN KEY (username) REFERENCES User (username)
);

CREATE TABLE UserPhone (
    phone_number VARCHAR(20) NOT NULL,
    username VARCHAR(20) NOT NULL,
    PRIMARY KEY (phone_number, username),
    FOREIGN KEY (username) REFERENCES User (username)
);

CREATE TABLE Pet (
    pet_name VARCHAR(20) NOT NULL,
    pet_type VARCHAR(20) NOT NULL,
    pet_size VARCHAR(20) NOT NULL,
    username VARCHAR(20) NOT NULL,
    PRIMARY KEY (pet_name, pet_type, username),
    FOREIGN KEY (username) REFERENCES User (username)
);

CREATE TABLE ApartmentBuilding (
    company_name VARCHAR(20) NOT NULL,
    building_name VARCHAR(20) NOT NULL,
    street_number INT NOT NULL,
    street_name VARCHAR(20) NOT NULL,
    city VARCHAR(20) NOT NULL,
    state VARCHAR(20) NOT NULL,
    zip_code VARCHAR(5) NOT NULL,
    year_built YEAR NOT NULL,
    PRIMARY KEY (company_name, building_name)
);

CREATE TABLE ApartmentUnit (
    unit_id INT NOT NULL AUTO_INCREMENT,
    unit_number VARCHAR(10) NOT NULL,
    monthly_rent INT NOT NULL,
    unit_size INT NOT NULL,
    available_date DATE NOT NULL,
    company_name VARCHAR(20) NOT NULL,
    building_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (unit_id),
    FOREIGN KEY (company_name, building_name) REFERENCES ApartmentBuilding (company_name, building_name)
);

CREATE TABLE Room (
    room_name VARCHAR(20) NOT NULL,
    room_size INT NOT NULL,
    room_description VARCHAR(100) NOT NULL,
    unit_id INT NOT NULL,
    PRIMARY KEY (room_name, unit_id),
    FOREIGN KEY (unit_id) REFERENCES ApartmentUnit (unit_id)
);

CREATE TABLE PetPolicy (
    pet_type VARCHAR(20) NOT NULL,
    pet_size VARCHAR(20) NOT NULL,
    is_pet_allowed BOOLEAN NOT NULL,
    pet_registration_fee INT NOT NULL,
    pet_monthly_fee INT NOT NULL,
    company_name VARCHAR(20) NOT NULL,
    building_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (pet_type, pet_size, company_name, building_name),
    FOREIGN KEY (company_name, building_name) REFERENCES ApartmentBuilding (company_name, building_name)
);

CREATE TABLE Amenity (
    amenity_name VARCHAR(20) NOT NULL,
    amenity_description VARCHAR(100) NOT NULL,
    PRIMARY KEY (amenity_name)
);

CREATE TABLE Interest (
    username VARCHAR(20) NOT NULL,
    unit_id INT NOT NULL,
    roommate_count TINYINT NOT NULL,
    move_in_date DATE NOT NULL,
    PRIMARY KEY (username, unit_id),
    FOREIGN KEY (username) REFERENCES User (username),
    FOREIGN KEY (unit_id) REFERENCES ApartmentUnit (unit_id)
);

CREATE TABLE BuildingAmenity (
    company_name VARCHAR(20) NOT NULL,
    building_name VARCHAR(20) NOT NULL,
    amenity_name VARCHAR(20) NOT NULL,
    amenity_fee INT NOT NULL,
    waiting_list INT NOT NULL,
    PRIMARY KEY (company_name, building_name, amenity_name),
    FOREIGN KEY (company_name, building_name) REFERENCES ApartmentBuilding (company_name, building_name),
    FOREIGN KEY (amenity_name) REFERENCES Amenity (amenity_name)
);

CREATE TABLE UnitAmenity (
    unit_id INT NOT NULL,
    amenity_name VARCHAR(20) NOT NULL,
    PRIMARY KEY (unit_id, amenity_name),
    FOREIGN KEY (unit_id) REFERENCES ApartmentUnit (unit_id),
    FOREIGN KEY (amenity_name) REFERENCES Amenity (amenity_name)
);
