# Roomio

### Roomio is an application that helps people find roommates and/or rooms in apartments.

### Required Features:

1. **Login & User Session Handle:** Users should be able to **register a new account**. Besides, only registered users are allowed to **log in** to the website. Roomio should add salt to the hashed password whenever a password is required at the database level. On login, if the salted and hashed password matches the record in the database, the user should then be redirected to the main page. If not, the user should be informed of the failure and no session will be created. The application should support **user sessions**, storing relevant data on a successful login.

2. **Search Certain Apartment Units:** The user should be able to search certain apartment units based on the following options:
   - Given the exact building name and company name, the application should return a list of units for rent and their basic information (monthly rent, square footage, available date for move-in, xbxb etc.)
   - Based on the registered information of the user's pet, the system shows whether the pet is allowed.

3. **Register Pet:** The user should be able to **register** pets associated with their accounts. Besides, they should also be able to **edit** registered pets' information.

4. **Post and View Interests:** When viewing a specific apartment unit, the user should be able to **view** others’ interests so that the user can **post** their interest to the unit.

5. **Display Unit and Building Info:** There should be some way for a user to search for a specific building or unit and get information about the building/unit: Roomio should display detailed information including address, year built, a summary of amenities and number of available units for rent (for building), monthly rent, square footage, available date for move-in, xbxb (for unit).

6. **Necessary Security Mechanisms:** The application should have the necessary mechanism to prevent SQL Injection and XSS (cross-site script) attacks.

### Additional Features:

7. **More Advanced Search of Units:** The user provides information like expected monthly rent or requirements for specific amenities like an in-door washing machine (unit amenities) or gym (public amenities), and the application returns units that meet the requirements. If there is no match, the application should tell the user to modify the search requirements.

8. **Search Interest:** The user should be able to search for an interest in a certain unit based on the move-in date and roommate count attributes. The user should also be able to have a look at the information of the initiator to decide on whether to contact for renting together.

9. **Estimate Monthly Rent:** The user can select a zipcode and the number of rooms (xbxb) requirement. The application should calculate the average monthly rent that suits the requirements of the user.

10. **Favorite:** The user can add certain units to their favorite to quickly see the details of the unit through a specific entry.

11. **Extra View on Rent Price:** For a unit, together with the price, display the average price of similar footage (footage less than 10% in difference) within the same city.

12. **Recommend System:** For a unit, the system should recommend similar units within and outside the same buildings.

13. **Comment System:** The user can leave a comment and rating for certain units.

14. **Join Interest:** The user can join a certain interest group.
