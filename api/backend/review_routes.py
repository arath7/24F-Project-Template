########################################################
#Review blueprint of endpoints
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
review = Blueprint('review', __name__)


#------------------------------------------------------------
# Get all reviews from the system
@review.route('/review', methods=['GET'])
def get_customers():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Review
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add a new review to the system
@review.route('/review', methods=['POST'])
def add_new_review():
    # In a POST request, there is a 
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    StudentNUID = the_data['StudentNUID']
    learningOpportunities = the_data['learningOpportunities']
    workCulture = the_data['workCulture']
    overallSatisfaction = the_data['overallSatisfaction']
    Mentorship = the_data['Mentorship']
    textReview = the_data['textReview']
    JobID = the_data['JobID']
    
    query = f''' INSERT INTO Review (StudentNUID, learningOpportunities, workCulture, overallSatisfaction, Mentorship, textReview, JobID) VALUES
      ('{StudentNUID}', '{learningOpportunities}', '{workCulture}', '{overallSatisfaction}', '{Mentorship}', '{textReview}', '{JobID}') 
    '''
    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully added review")
    response.status_code = 200
    return response
    

#------------------------------------------------------------
# Get review details for a particular reviewID
@review.route('/review/<reviewID>', methods=['GET'])
def get_review(reviewID):
    current_app.logger.info('GET /review/<reviewID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Review WHERE reviewID = {0}'.format(reviewID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#Update an existing review with a particular reviewID
@review.route('/review/<reviewID>', methods=['PUT'])
def update_review(reviewID):

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
    query = f"UPDATE Review SET {set_clause} WHERE reviewID = %s"

    # Extract values from the_data to match the parameterized query
    values = list(the_data.values())
    values.append(reviewID)  # Add reviewID for the WHERE clause


    
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    response = make_response("Successfully updated review")
    response.status_code = 200
    return response


#Delete an existing review with a particular reviewID
@review.route('/review/<reviewID>', methods=['DELETE'])
def delete_review(reviewID):
    current_app.logger.info('DELETE /review/<reviewID> route')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM Review WHERE reviewID = {0}'.format(reviewID))
    db.get_db().commit()
    
    response = make_response("Successfully deleted review")
    response.status_code = 200
    return response

@review.route('/review/starred/<reviewID>', methods=['DELETE'])
def delete_starred_review(reviewID):
    cursor = db.get_db().cursor()

    # Use parameterized queries to avoid SQL injection
    cursor.execute('DELETE FROM Starred_Reviews WHERE reviewID = %s', (reviewID,))
    db.get_db().commit()

    # Respond with a success message
    response = make_response("Successfully deleted review")
    response.status_code = 200
    return response






#Get all the reviews written by a student, given the studentNUID
@review.route('/review/student/<StudentNUID>', methods=['GET'])
def get_student(StudentNUID):
    current_app.logger.info('GET /review/student/<StudentNUID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Review WHERE StudentNUID = {0}'.format(StudentNUID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#Get all the reviews written for a job, given the JobID
@review.route('/review/job/<JobID>', methods=['GET'])
def get_job(JobID):
    current_app.logger.info('GET /review/job/<JobID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Review WHERE JobID = {0}'.format(JobID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#Get all the reviews written for a job, given the JobID
@review.route('/review/starred/<NUID>', methods=['GET'])
def get_starred_reviews(NUID):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Starred_Reviews WHERE NUID = {0}'.format(NUID))

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# ------------------------------------------------------------
# Add a new review to the system
@review.route('/review/starred', methods=['POST'])
def add_new_starred_review():
    # In a POST request, there is a
    # collecting data from the request object
    the_data = request.json
    current_app.logger.info(the_data)

    # extracting the variable
    StudentNUID = the_data['NUID']
    ReviewID = the_data['ReviewID']

    query = f''' INSERT INTO Starred_Reviews (ReviewID, NUID) VALUES
  ('{ReviewID}', '{StudentNUID}');
    '''

    current_app.logger.info(query)
    # executing and committing the insert statement
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    response = make_response("Successfully added review")
    response.status_code = 200
    return response


