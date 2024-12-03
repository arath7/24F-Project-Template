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
notifications = Blueprint('Notifications', __name__)

#------------------------------------------------------------
# Create a notification for a specific user
@notifications.route('/Notifications', methods=['POST'])
def create_notification():
    the_data = request.json
    current_app.logger.info(the_data)

    NUID = the_data['NUID']
    Content = the_data['Content']
    sentDate = the_data['sentDate']

    query = f'''INSERT INTO Notifications (NUID, Content, sentDate)
                VALUES ('{NUID}', '{Content}', '{SentDate}')'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully created notification")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Update the content of a specific notification
@notifications.route('/Notifications/<notifID>', methods=['PUT'])
def update_notification(notifID):
    the_data = request.json
    current_app.logger.info(the_data)

    fields_to_update = []
    for field, value in the_data.items():
        fields_to_update.append(f"{field} = %s")

    set_clause = ", ".join(fields_to_update)
    query = f"UPDATE Notifications SET {set_clause} WHERE notificationID = %s"

    values = list(the_data.values())
    values.append(notifID)

    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query, values)
    db.get_db().commit()

    response = make_response("Successfully updated notification")
    response.status_code = 200
    return response

#------------------------------------------------------------
# Delete a specific notification by ID
@notifications.route('/Notifications/<notifID>', methods=['DELETE'])
def delete_notification(notifID):
    current_app.logger.info(f'DELETE /Notifications/{notifID} route')

    query = f'''DELETE FROM Notifications WHERE notificationID = {notifID}'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    response = make_response("Successfully deleted notification")
    response.status_code = 200
    return response
