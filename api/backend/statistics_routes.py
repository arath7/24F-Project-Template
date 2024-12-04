########################################################
# Statistics blueprint of endpoints
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
statistics = Blueprint('statistics', __name__)

#------------------------------------------------------------
# Retrieve dashboards showing reviews, job satisfaction, flagged content, etc.
@statistics.route('/statistics', methods=['GET'])
def get_dashboards():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Dashboards''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Retrieve statistics by specific ID
@statistics.route('/statistics/<statID>', methods=['GET'])
def get_statistics_by_id(statID):
    current_app.logger.info(f'GET /statistics/{statID} route')

    query = f'''SELECT * FROM Statistics WHERE statID = {statID}'''
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


