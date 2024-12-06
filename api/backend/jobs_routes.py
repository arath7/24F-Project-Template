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
jobs = Blueprint('jobs', __name__)


#------------------------------------------------------------
# Get all jobs from the system
@jobs.route('/jobs', methods=['GET'])
def get_jobs():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Job
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a new job listing to the system
@jobs.route('/jobs', methods=['POST'])
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
    
    query = f''' INSERT INTO Job (employerID, JobCategoryID, Name, Description, numOpenings, returnOffers, Salary)
      VALUES ('{employerID}', '{JobCategoryID}', '{Name}', '{Description}', '{numOpenings}', '{returnOffers}', '{Salary}') 
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
@jobs.route('/jobs/<jobID>', methods=['GET'])
def get_job(jobID):
    current_app.logger.info('GET /jobs/<jobID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Job WHERE JobID = {0}'.format(jobID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Get job details for a job with a particular jobID
@jobs.route('/jobs/<employerID>/employer', methods=['GET'])
def get_job_employer(employerID):
    current_app.logger.info('GET /jobs/<employerID>/employer route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Job WHERE JobID = {0}'.format(employerID))

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
#Update an existing job listing with a particular jobID
@jobs.route('/jobs/<jobID>', methods=['PUT'])
def update_job(jobID):

    the_data = request.json
    current_app.logger.info(the_data)

    fields_to_update = []
    values = []

    for field, value in the_data.items():
        fields_to_update.append(f"{field} = %s")
        values.append(value)

    # Check if there are valid fields to update
    if not fields_to_update:
        response = make_response({"error": "No valid fields to update"}, 400)
        return response

    # Build query
    set_clause = ", ".join(fields_to_update)
    query = f"UPDATE Job SET {set_clause} WHERE jobID = %s"
    values.append(jobID)  # Add jobID for WHERE clause

    current_app.logger.info(query)


    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()
    response = make_response("Successfully updated job")
    return response


#Delete an existing job listing with a particular jobID
@jobs.route('/jobs/<jobID>', methods=['DELETE'])
def delete_job(jobID):
    current_app.logger.info('DELETE /jobs/<jobID> route')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Job WHERE JobID = {0}'.format(jobID))
    db.get_db().commit()
    
    response = make_response("Successfully deleted job")
    response.status_code = 200
    return response


#Get employer name from a jobID
@jobs.route('/jobs/employer/<jobID>', methods=['GET'])
def get_employer_name(jobID):
    current_app.logger.info('GET /jobs/employer/<jobID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT e.Name FROM Employer e JOIN Job j ON e.employerID = j.employerID WHERE j.JobID = {0}'.format(jobID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Get jobs a student has done or is doing
@jobs.route('/jobs/student/<NUID>', methods=['GET'])
def get_student_jobs(NUID):
    current_app.logger.info('GET /jobs/student/<NUID> route')
    cursor = db.get_db().cursor()
    query = '''
         SELECT j.JobID, j.employerID, j.Name
         FROM Job j 
         JOIN StudentJobs sj ON j.JobID = sj.jobID 
         JOIN Student s ON s.NUID = sj.NUID 
         WHERE s.NUID = %s
     '''
    cursor.execute(query, (NUID,))

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#Get average overall satisfaction rating for a job with a particular jobID
@jobs.route('/jobs/averageRating/<jobID>', methods=['GET'])
def get_job_average_rating(jobID):
    current_app.logger.info('GET /jobs/averageRating/<jobID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT AVG(overallSatisfaction) FROM Review WHERE jobID = {0}'.format(jobID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
    return the_response

