########################################################
# Student blueprint of endpoints
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
students = Blueprint('Student', __name__)

#------------------------------------------------------------
# Get all students from the system
@students.route('/Student', methods=['GET'])
def get_students():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Student''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a new student to the system
@students.route('/Student', methods=['POST'])
def add_new_student():
    # Collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    # Extracting the variables
    NUID = the_data['NUID']
    firstName = the_data['firstName']
    lastName = the_data['lastName']
    Email = the_data['Email']
    major = the_data['major']
    GradYear = the_data['GradYear']

    query = f''' INSERT INTO Student (studentID, firstName, lastName, email, major, grad_year)
      VALUES ('{NUID}', '{firstName}', '{lastName} '{Email}', '{major}', '{GradYear}') 
    '''
    
    current_app.logger.info(query)

    # Executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added student")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get details for a specific student by ID
@students.route('/Student/<id>', methods=['GET'])
def get_student(id):
    current_app.logger.info('GET /Student/<id> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Student WHERE NUID = {0}'.format(id))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Update an existing student by ID
@students.route('/Student/<id>', methods=['PUT'])
def update_student(id):

    the_data = request.json
    current_app.logger.info(the_data)

    # Dynamically build the SET clause of the query
    fields_to_update = []
    for field, value in the_data.items():
        # Avoid SQL injection by using parameterized queries
        fields_to_update.append(f"{field} = %s")

    # Join the fields to create the SET clause
    set_clause = ", ".join(fields_to_update)

    # Prepare the SQL query
    query = f"UPDATE Student SET {set_clause} WHERE NUID = %s"

    # Extract values from the_data to match the parameterized query
    values = list(the_data.values())
    values.append(id)  # Add studentID for the WHERE clause

    current_app.logger.info(query)

    # Executing and committing the update statement 
    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    
    response = make_response("Successfully updated student")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Delete an existing student by ID
@students.route('/Student/<id>', methods=['DELETE'])
def delete_student(id):
    current_app.logger.info('DELETE /Student/<id> route')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Student WHERE NUID = {0}'.format(id))
    db.get_db().commit()
    
    response = make_response("Successfully deleted student")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Add a job application for a specific student
@students.route('/student/<id>/jobs', methods=['POST'])
def add_job_application(id):
    the_data = request.json
    current_app.logger.info(the_data)

    jobID = the_data['jobID']

    query = f'''INSERT INTO StudentJobs (NUID, jobID)
      VALUES ('{id}', '{jobID}')'''
    
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added job application")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Delete a job application for a specific student
@students.route('/student/<id>/jobs', methods=['DELETE'])
def delete_job_application(id):
    the_data = request.json
    current_app.logger.info(the_data)

    jobID = the_data['jobID']

    query = f'''DELETE FROM StudentJobs WHERE studentID = '{id}' AND jobID = '{jobID}' '''
    
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted job application")
    response.status_code = 200
    return response
