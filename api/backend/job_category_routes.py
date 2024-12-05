########################################################
#Job Category blueprint of endpoints
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
job_category = Blueprint('job_category', __name__)


#------------------------------------------------------------
# Get all job categories from the system
@job_category.route('/jobCategory', methods=['GET'])
def get_customers():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM JobCategory
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a new job category to the system
@job_category.route('/jobCategory', methods=['POST'])
def add_new_job():
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    JobCategoryID = the_data['JobCategoryID']
    Name = the_data['Name']
    
    
    query = f''' INSERT INTO JobCategory (JobCategoryID, Name)
      VALUES ('{JobCategoryID}', '{Name}') 
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
# Get job category details for a job category with a particular jobCategoryID
@job_category.route('/jobCategory/<JobCategoryID>', methods=['GET'])
def get_customer(JobCategoryID):
    current_app.logger.info('GET /jobCategory/<JobCategoryID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM JobCategory WHERE JobCategoryID = {0}'.format(JobCategoryID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
#Update an existing job category with a particular jobCategoryID
@job_category.route('/jobCategory/<JobCategoryID>', methods=['PUT'])
def update_jobcategory(JobCategoryID):

    the_data = request.json
    current_app.logger.info(the_data)

    Name = the_data['Name']


    # Prepare the SQL query
    query = f"UPDATE JobCategory SET Name = '{Name}' WHERE JobCategoryID = {JobCategoryID}"

    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully updated job category")
    response.status_code = 200
    return response

#Delete an existing job category with a particular jobCategoryID
@job_category.route('/jobCategory/<JobCategoryID>', methods=['DELETE'])
def delete_jobcategory(JobCategoryID):
    current_app.logger.info('DELETE /jobCategory/<JobCategoryID> route')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM JobCategory WHERE JobCategoryID = {0}'.format(JobCategoryID))
    db.get_db().commit()
    
    response = make_response("Successfully deleted job category")
    response.status_code = 200
    return response

