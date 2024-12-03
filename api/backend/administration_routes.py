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
# Retrieve statistical dashboards
@admin.route('/statistics', methods=['GET'])
def get_statistics():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT * FROM Statistics''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
