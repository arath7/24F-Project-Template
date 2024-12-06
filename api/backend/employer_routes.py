########################################################
#Employer blueprint of endpoints
########################################################
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
employer = Blueprint('employer', __name__)


#------------------------------------------------------------
# Get all employers from the system
@employer.route('/employer', methods=['GET'])
def get_employers():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Employer
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a new employer to the system
@employer.route('/employer', methods=['POST'])
def add_new_employer():
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    Name = the_data['Name']
    Email = the_data['Email']
    Address = the_data['Address']
    phoneNumber = the_data['phoneNumber']
    
    
    query = f''' INSERT INTO Employer (Name, Email, Address, phoneNumber)
    VALUES ('{Name}', '{Email}', '{Address}', '{phoneNumber}') 
    '''
    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added employer")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Add a new employer to the system
@employer.route('/employer/starred', methods=['POST'])
def add_new_starred_employer():

    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    employerID = the_data['employerID']
    NUID = the_data['NUID']


    query = f''' INSERT INTO Starred_Employers (employerID, NUID)
    VALUES ('{employerID}', '{NUID}') 
    '''

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added employer")
    response.status_code = 200
    return response




# Get employer details for an employer with a particular employerID
@employer.route('/employer/<employerID>', methods=['GET'])
def get_starred_employer(employerID):
    current_app.logger.info('GET /employer/<employerID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Employer WHERE employerID = {0}'.format(employerID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Get employer details for an employer with a particular employerID
@employer.route('/employer/starred/<NUID>', methods=['GET'])
def get_employer(NUID):
    current_app.logger.info('GET /employer/<NUID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Starred_Employers WHERE NUID = {0}'.format(NUID))

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
#Update an existing employer's info with a particular employerID
@employer.route('/employer/<employerID>', methods=['PUT'])
def update_employer(employerID):
    the_data = request.json
    current_app.logger.info(the_data)

    # Validate fields
    allowed_fields = {"Name", "Email", "Address", "phoneNumber"}  # Define allowed columns
    fields_to_update = []
    values = []

    for field, value in the_data.items():
        if field in allowed_fields:
            fields_to_update.append(f"{field} = %s")
            values.append(value)
        else:
            current_app.logger.warning(f"Ignoring invalid field: {field}")

    # Check if there are valid fields to update
    if not fields_to_update:
        response = make_response({"error": "No valid fields to update"}, 400)
        return response

    # Build query
    set_clause = ", ".join(fields_to_update)
    query = f"UPDATE Employer SET {set_clause} WHERE employerID = %s"
    values.append(employerID)  # Add employerID for WHERE clause

    current_app.logger.info(query)


    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()

    # Success response
    response = make_response("Successfully updated employer")
    return response


#Delete an existing employer with a particular employerID
@employer.route('/employer/<employerID>', methods=['DELETE'])
def delete_employer(employerID):
    current_app.logger.info('DELETE /employer/<employerID> route')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Employer WHERE employerID = {0}'.format(employerID))
    db.get_db().commit()
    
    response = make_response("Successfully deleted employer")
    response.status_code = 200
    return response


#Delete an existing employer with a particular employerID
@employer.route('/employer/starred/<employerID>', methods=['DELETE'])
def delete_starred_employer(employerID):
    current_app.logger.info('DELETE /employer/<employerID> route')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Starred_Employers WHERE employerID = {0}'.format(employerID))
    db.get_db().commit()

    response = make_response("Successfully deleted employer")
    response.status_code = 200
    return response

#Get all jobs listed by a specific employer
@employer.route('/employer/<employerID>/jobs', methods=['GET'])
def get_jobs_by_employer(employerID):
    current_app.logger.info('GET /employer/<employerID>/jobs route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Job WHERE employerID = {0}'.format(employerID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#Get the total number of jobs listed by a specific employer
@employer.route('/employer/<employerID>/jobs/total', methods=['GET'])
def get_total_jobs_by_employer(employerID):
    current_app.logger.info('GET /employer/<employerID>/jobs/total route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT COUNT(*) FROM Job WHERE employerID = {0}'.format(employerID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response