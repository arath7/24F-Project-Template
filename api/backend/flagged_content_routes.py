########################################################
# Flagged Content blueprint of endpoints
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
flagged_content = Blueprint('flagged_content', __name__)

#------------------------------------------------------------
# Retrieve all flagged content
@flagged_content.route('/flagged_content', methods=['GET'])
def get_all_flagged_content():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Flagged_Content''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Retrieve flagged content by ID
@flagged_content.route('/flagged_content/<flagID>', methods=['GET'])
def get_flagged_content_by_id(flagID):
    current_app.logger.info(f'GET /flagged_content/{flagID} route')

    query = f'''SELECT * FROM Flagged_Content WHERE flagID = {flagID}'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add new flagged content
@flagged_content.route('/flagged_content', methods=['POST'])
def add_flagged_content():
    the_data = request.json
    current_app.logger.info(the_data)

    reviewID = the_data['ReviewID']
    adminID = the_data['AdminID']
    reason = the_data['ReasonSubmitted']
    date = the_data['DateFlagged']

    query = f'''INSERT INTO Flagged_Content (ReviewID, adminID, ReasonSubmitted, DateFlagged)
                VALUES ('{reviewID}', '{adminID}', '{reason}', '{date}')'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully added flagged content")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Delete flagged content by ID
@flagged_content.route('/flagged_content/<flagID>', methods=['DELETE'])
def delete_flagged_content(flagID):
    current_app.logger.info(f'DELETE /flagged_content/{flagID} route')

    query = f'''DELETE FROM Flagged_Content WHERE flagID = {flagID}'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted flagged content")
    response.status_code = 200
    return response
