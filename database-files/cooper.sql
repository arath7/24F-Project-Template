DROP DATABASE IF EXISTS cooper;
CREATE DATABASE IF NOT EXISTS cooper;
USE cooper;


-- Drop tables if they exist
DROP TABLE IF EXISTS Flagged_Content;
DROP TABLE IF EXISTS Administrator;
DROP TABLE IF EXISTS Notifications;
DROP TABLE IF EXISTS Starred_Employers;
DROP TABLE IF EXISTS Starred_Jobs;
DROP TABLE IF EXISTS Starred_Reviews;
DROP TABLE IF EXISTS Review;
DROP TABLE IF EXISTS Employer;
DROP TABLE IF EXISTS Job;
DROP TABLE IF EXISTS JobCategory;
DROP TABLE IF EXISTS Statistics;
DROP TABLE IF EXISTS Student;


-- Create JobCategory table first as it's referenced in Job table
CREATE TABLE JobCategory
(
   JobCategoryID INT AUTO_INCREMENT PRIMARY KEY,
   Name VARCHAR(100) NOT NULL
);


-- Employer table creation
CREATE TABLE Employer
(
   employerID  INT AUTO_INCREMENT PRIMARY KEY,
   Name        VARCHAR(100) NOT NULL,
   Email       VARCHAR(100) NOT NULL,
   Address     VARCHAR(255) NOT NULL,
   phoneNumber VARCHAR(20)  NOT NULL,
   numJobs     INT, # need to cascade update when linked to jobs, or get rid of later
   Rating      DECIMAL(3, 2), # cascade update when linked to reviews
   UNIQUE (Email),
   UNIQUE (phoneNumber),
   UNIQUE (Address)
);


-- Job table creation (now it can reference JobCategory)
CREATE TABLE Job
(
   JobID            INT AUTO_INCREMENT PRIMARY KEY,
   employerID       INT          NOT NULL,
   JobCategoryID    INT          NOT NULL,
   Name             VARCHAR(100) NOT NULL,
   Description      TEXT         NOT NULL,
   numOpenings      INT          NOT NULL,
   returnOffers     INT          NOT NULL,
   Salary           DOUBLE       NOT NULL,
   numReviews       INT          NOT NULL,
   AggregatedReview TEXT, -- need to cascade and make later
   Rating           INT, -- cascade and make later
   FOREIGN KEY (JobCategoryID) REFERENCES JobCategory (JobCategoryID),
   FOREIGN KEY (employerID) REFERENCES Employer (employerID)
);

-- Student table creation
CREATE TABLE Student
(
   NUID             INT          NOT NULL,
   bDate            DATETIME     NOT NULL,
   firstName        VARCHAR(100) NOT NULL,
   lastName         VARCHAR(100) NOT NULL,
   Email            VARCHAR(100) NOT NULL,
   school           VARCHAR(100) NOT NULL,
   major            VARCHAR(100) NOT NULL,
   GradYear         INT          NOT NULL,
   searchStatus     BOOLEAN      NOT NULL,
#    jobID            INT,
#    employerID       INT,
#    starredJobs      TEXT,
#    starredEmployers TEXT,
#    starredReviews   TEXT,
   PRIMARY KEY (NUID),
   UNIQUE (Email)
#    FOREIGN KEY (jobID) REFERENCES Job (jobID),
#    FOREIGN KEY (employerID) REFERENCES Employer (employerID)
);

-- the job that a student has currently or did have
CREATE TABLE StudentJobs
(
    NUID        INT NOT NULL,
    jobID       INT NOT NULL,
    StartDate   DATETIME NOT NULL,
    EndDate     DATETIME NOT NULL,
    PRIMARY KEY (NUID, jobID),
    FOREIGN KEY (jobID) REFERENCES Job (jobID)

);

-- Review table creation
CREATE TABLE Review
(
   reviewID              INT AUTO_INCREMENT PRIMARY KEY,
   StudentNUID           INT NOT NULL,
   learningOpportunities INT NOT NULL,
   workCulture           INT NOT NULL,
   overallSatisfaction   INT NOT NULL,
   Mentorship            INT NOT NULL,
   textReview            TEXT,
   JobID                 INT NOT NULL,
#    employerID            INT NOT NULL,
   FOREIGN KEY (JobID) REFERENCES Job (JobID),
#    FOREIGN KEY (employerID) REFERENCES Employer (employerID),
   FOREIGN KEY (StudentNUID) REFERENCES Student (NUID)
);


-- Notifications table creation
CREATE TABLE Notifications
(
   notifID INT AUTO_INCREMENT PRIMARY KEY,
   NUID INT,
   employerID INT,
   sentDate   DATETIME NOT NULL,
   Content    TEXT     NOT NULL,
   FOREIGN KEY (NUID) REFERENCES Student (NUID),
   FOREIGN KEY (employerID) REFERENCES Employer (employerID)
);


-- Starred Employers table creation
CREATE TABLE Starred_Employers
(
   employerID INT NOT NULL,
   NUID INT NOT NULL,
   PRIMARY KEY (employerID, NUID),
   FOREIGN KEY (NUID) REFERENCES Student (NUID),
   FOREIGN KEY (employerID) REFERENCES Employer (employerID)
);


-- Starred Jobs table creation
CREATE TABLE Starred_Jobs
(
   JobID INT NOT NULL,
   NUID INT NOT NULL,
   PRIMARY KEY (JobID, NUID),
   FOREIGN KEY (NUID) REFERENCES Student (NUID),
   FOREIGN KEY (JobID) REFERENCES Job (JobID)
);


-- Starred Reviews table creation
CREATE TABLE Starred_Reviews
(
   ReviewID INT NOT NULL,
   NUID INT NOT NULL,
   PRIMARY KEY (reviewID, NUID),
   FOREIGN KEY (NUID) REFERENCES Student (NUID),
   FOREIGN KEY (ReviewID) REFERENCES Review (ReviewID)
);




CREATE TABLE Administrator
(
   AdminID INT AUTO_INCREMENT PRIMARY KEY,
   Name    VARCHAR(100) NOT NULL,
   Email   VARCHAR(100) NOT NULL,
   Role    VARCHAR(255) NOT NULL,
   UNIQUE (Email)
);




-- Flagged Content table creation
CREATE TABLE Flagged_Content
(
   FlagID          INT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
   ReviewID        INT      NOT NULL,
   adminID         INT      NOT NULL,
   ReasonSubmitted TEXT     NOT NULL,
   DateFlagged     DATETIME NOT NULL,
   FOREIGN KEY (ReviewID) REFERENCES Review (ReviewID),
   FOREIGN KEY (adminID) REFERENCES Administrator (adminID)
);


-- Statistics table creation
-- maybe turn into a backend query instead, executed as someone wants to see data
CREATE TABLE Statistics
(
   statisticsID   INT AUTO_INCREMENT PRIMARY KEY,
   totalUsers     INT      NOT NULL,
   totalJobs      INT      NOT NULL,
   totalReviews   INT      NOT NULL,
   totalEmployers INT      NOT NULL,
   generatedDate  DATETIME NOT NULL
);


#####################
# Generate Data
####################
# INSERT INTO JobCategory (Name)
# VALUES ('Software Development'),
#       ('Data Science'),
#       ('Marketing'),
#       ('Design'),
#       ('Human Resources');
#
#
# INSERT INTO Employer (Name, Email, Address, phoneNumber, numJobs, Rating)
# VALUES ('Tech Corp', 'techcorp@example.com', '123 Tech Street, Silicon Valley, CA', '123-456-7890', 5, 4.2),
#       ('Data Solutions', 'datasolutions@example.com', '456 Data Blvd, New York, NY', '234-567-8901', 3, 4.5),
#       ('Creative Agency', 'creativeagency@example.com', '789 Design Ave, Los Angeles, CA', '345-678-9012', 2, 4.7);
#
#
# INSERT INTO Student (NUID, bDate, firstName, lastName, Email, school, major, GradYear, searchStatus, jobID, employerID,
#                     starredJobs, starredEmployers, starredReviews)
# VALUES (1001, '2000-05-15', 'John', 'Doe', 'johndoe@example.com', 'University of X', 'Computer Science', 2024,
#        'Looking', NULL, 1, '1,2', '3', '1'),
#       (1002, '1999-08-25', 'Jane', 'Smith', 'janesmith@example.com', 'University of Y', 'Marketing', 2025, 'Looking',
#        NULL, 2, '2', '1', '2');
#
#
# INSERT INTO Job (employerID, JobCategoryID, Name, Description, numOpenings, returnOffers, Salary, numReviews,
#                 AggregatedReview, Rating)
# VALUES (1, 1, 'Software Engineer', 'Develop software applications and systems.', 5, 3, 90000, 10,
#        'Good work-life balance, great learning opportunities', 4),
#       (2, 2, 'Data Analyst', 'Analyze large datasets and provide insights.', 3, 2, 80000, 5,
#        'Great team, but challenging workload', 4),
#       (3, 3, 'Marketing Manager', 'Oversee marketing strategies for clients.', 2, 1, 70000, 7,
#        'Creative and fast-paced environment', 5);
#
#
#
#
# INSERT INTO Review (StudentNUID, learningOpportunities, workCulture, overallSatisfaction, Mentorship, textReview, JobID,
#                    employerID)
# VALUES (1001, 5, 4, 4, 3, 'Great experience overall with opportunities to learn.', 1, 1),
#       (1002, 4, 3, 4, 5, 'Challenging work, but great mentorship and guidance.', 2, 2);
#
#
# INSERT INTO Notifications (userID, sentDate, Content)
# VALUES (1001, '2024-11-18 10:00:00', 'New job posting for Software Engineer at Tech Corp.'),
#       (1002, '2024-11-19 12:30:00', 'Data Analyst job posted by Data Solutions.');
#
#
#
#
# INSERT INTO Starred_Employers (employerID, NUID)
# VALUES (1, 1001),
#       (2, 1002);
#
#
# INSERT INTO Starred_Jobs (JobID, NUID)
# VALUES (1, 1001),
#       (2, 1002);
#
#
# INSERT INTO Starred_Reviews (ReviewID, NUID)
# VALUES (1, 1001),
#       (2, 1002);
#
#
# INSERT INTO Administrator (Name, Email, Role)
# VALUES ('Alice Johnson', 'alice.johnson@example.com', 'Admin'),
#       ('Bob Brown', 'bob.brown@example.com', 'Moderator');
#
#
# INSERT INTO Flagged_Content (ReviewID, adminID, ReasonSubmitted, DateFlagged)
# VALUES (1, 1, 'Inappropriate language in review', '2024-11-18 14:00:00'),
#       (2, 2, 'Offensive comments about the employer', '2024-11-19 09:30:00');
#
#
# INSERT INTO Statistics (totalUsers, totalJobs, totalReviews, totalEmployers, generatedDate)
# VALUES (5, 3, 2, 3, '2024-11-19 12:00:00');
