########################################################
#Jobs blueprint of endpoints
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
customers = Blueprint('jobs', __name__)


#------------------------------------------------------------
# Get all jobs from the system
@customers.route('/jobs', methods=['GET'])
def get_customers():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Job
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a new job listing to the system
@customers.route('/jobs', methods=['POST'])
def add_new_job():
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    employerID = the_data['employerID']
    JobCategoryID = the_data['JobCategoryID']
    Name = the_data['Name']
    Description = the_data['Description']
    numOpenings = the_data['numOpenings']
    returnOffers = the_data['returnOffers']
    Salary = the_data['Salary']
    numReviews = the_data['numReviews']
    
    query = f''' INSERT INTO Job (employerID, JobCategoryID, Name, Description, numOpenings, returnOffers, Salary, numReviews)
      VALUES ('{employerID}', '{JobCategoryID}', '{Name}', '{Description}', '{numOpenings}', '{returnOffers}', '{Salary}', '{numReviews}') 
    '''
    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added job")
    response.status_code = 200
    return response
    

#------------------------------------------------------------
# Get job details for a job with a particular jobID
@customers.route('/jobs/<jobID>', methods=['GET'])
def get_customer(jobID):
    current_app.logger.info('GET /jobs/<jobID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Job WHERE JobID = {0}'.format(jobID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
#Update an existing job listing with a particular jobID
@customers.route('/jobs/<jobID>', methods=['PUT'])
def update_job(jobID):

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
    query = f"UPDATE Job SET {set_clause} WHERE JobID = %s"

    # Extract values from the_data to match the parameterized query
    values = list(the_data.values())
    values.append(jobID)  # Add JobID for the WHERE clause

    # #extracting the variable
    # employerID = the_data['employerID']
    # JobCategoryID = the_data['JobCategoryID']
    # Name = the_data['Name']
    # Description = the_data['Description']
    # numOpenings = the_data['numOpenings']
    # returnOffers = the_data['returnOffers']
    # Salary = the_data['Salary']
    # numReviews = the_data['numReviews']
    
    # query = f''' UPDATE Job
    #   SET employerID = '{employerID}', JobCategoryID = '{JobCategoryID}', Name = '{Name}', Description = '{Description}', numOpenings = '{numOpenings}', returnOffers = '{returnOffers}', Salary = '{Salary}', numReviews = '{numReviews}'
    #   WHERE JobID = {jobID}
    # '''
    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully updated job")
    response.status_code = 200
    return response

#Delete an existing job listing with a particular jobID
@customers.route('/jobs/<jobID>', methods=['DELETE'])
def delete_job(jobID):
    current_app.logger.info('DELETE /jobs/<jobID> route')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Job WHERE JobID = {0}'.format(jobID))
    db.get_db().commit()
    
    response = make_response("Successfully deleted job")
    response.status_code = 200
    return response

