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
    cursor.execute('''SELECT COUNT(JobID) FROM Job WHERE returnOffers = TRUE''')


    totalOffers = cursor.fetchone()["COUNT(JobID)"]

    cursor.execute('''SELECT COUNT(JobID) FROM Job''')
    totalJobs = cursor.fetchone()["COUNT(JobID)"]

    if totalJobs == 0:
        theData = 0
    else:
        theData = (totalOffers / totalJobs) * 100

    the_response = make_response({"returnOfferPercentage" : totalJobs})
    the_response.status_code = 200
    return the_response

#Retrieve total number of students
@admin.route('/admin/total_students', methods=['GET'])
def get_total_students():
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT COUNT(NUID) FROM Student''')

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
    cursor.execute('''SELECT jc.Name, COUNT(j.JobID) 
    FROM Job j
    JOIN JobCategory jc ON j.JobCategoryID = jc.JobCategoryID
    GROUP BY jc.Name''')

    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


