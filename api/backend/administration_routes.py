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
# Retrieve percentage of jobs that offer return offers
@admin.route('/admin/return_offer_percentage', methods=['GET'])
def get_return_offer_percentage():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT COUNT(JobID) FROM Job WHERE return_offer = 1''')


    totalOffers = cursor.fetchall()

    cursor.execute('''SELECT COUNT(JobID) FROM Job''')
    totalJobs = cursor.fetchall()

    theData = totalOffers[0][0]/totalJobs[0][0]

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#Retrieve total number of students
@admin.route('/admin/total_students', methods=['GET'])
def get_total_students():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT COUNT(studentID) FROM Student''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#Retrieve total number of jobs
@admin.route('/admin/total_jobs', methods=['GET'])
def get_total_jobs():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT COUNT(JobID) FROM Job''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#Retrieve total number of reviews
@admin.route('/admin/total_reviews', methods=['GET'])
def get_total_reviews():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT COUNT(reviewID) FROM Review''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#Retrieve total number of employers
@admin.route('/admin/total_employers', methods=['GET'])
def get_total_employers():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT COUNT(employerID) FROM Employer''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#Retrieve total number of jobs within each job category
@admin.route('/admin/jobs_by_category', methods=['GET'])
def get_jobs_by_category():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT category, COUNT(JobID) FROM Job GROUP BY category''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


