########################################################
# Admin blueprint of endpoints ____ NOT FINAL
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
admin = Blueprint('admin', __name__)

#------------------------------------------------------------
# Retrieve a list of all users
@admin.route('/student', methods=['GET'])
def get_all_users():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Student''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Delete a user account by ID
@admin.route('/student/<id>', methods=['DELETE'])
def delete_user_account(id):
    current_app.logger.info(f'DELETE /student/{id} route')

    query = f'''DELETE FROM Student WHERE studentID = {id}'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted user account")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Retrieve flagged content for review
@admin.route('/flaggedcontent', methods=['GET'])
def get_flagged_content():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Flagged_Content''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Delete flagged content by ID
@admin.route('/flaggedcontent/<flagID>', methods=['DELETE'])
def delete_flagged_content(flagID):
    current_app.logger.info(f'DELETE /flaggedcontent/{flagID} route')

    query = f'''DELETE FROM Flagged_Content WHERE flagID = {flagID}'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted flagged content")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Retrieve statistical dashboards
@admin.route('/statistics', methods=['GET'])
def get_statistics():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Statistics''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
