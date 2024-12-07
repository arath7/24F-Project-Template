########################################################
# Notifications blueprint of endpoints
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
notifications = Blueprint('notifications', __name__)

#------------------------------------------------------------
# Create a notification for a specific student
@notifications.route('/Notifications', methods=['POST'])
def create_notification():
    the_data = request.json
    current_app.logger.info(the_data)

    NUID = the_data['NUID']
    Content = the_data['Content']

    query = f'''INSERT INTO Notifications (NUID, Content)
                VALUES ('{NUID}', '{Content}')'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully created notification")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Get all notifications for a specific student
@notifications.route('/Notifications/<NUID>', methods=['GET'])
def get_notifications(NUID):
    current_app.logger.info(f'GET /Notifications/{NUID} route')

    query = f'''SELECT * FROM Notifications WHERE NUID = {NUID}'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Delete a specific notification by ID
@notifications.route('/Notifications/<notifID>', methods=['DELETE'])
def delete_notification(notifID):
    current_app.logger.info(f'DELETE /Notifications/{notifID} route')

    query = f'''DELETE FROM Notifications WHERE notifID = {notifID}'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted notification")
    response.status_code = 200
    return response
