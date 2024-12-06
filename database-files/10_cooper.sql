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
DROP TABLE IF EXISTS StudentJobs;
DROP TABLE IF EXISTS JobCategory;
-- DROP TABLE IF EXISTS Statistics;
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
   numJobs     INT, -- need to update when linked to jobs
   Rating      DECIMAL(3, 2), -- update when linked to reviews
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
   returnOffers     BOOLEAN      NOT NULL,
   Salary           DOUBLE       NOT NULL,
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
   searchStatus     BOOLEAN      NOT NULL, -- true if looking for a job, false if not 
   PRIMARY KEY (NUID),
   UNIQUE (Email)
);

-- the job that a student has currently or did have
CREATE TABLE StudentJobs
(
    NUID        INT NOT NULL,
    jobID       INT NOT NULL,
    StartDate   DATETIME NOT NULL,
    EndDate     DATETIME NOT NULL, -- can be in the future if job ends later
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
   overallSatisfaction   INT NOT NULL, -- will this be the overall rating? or use an average to get overall rating
   Mentorship            INT NOT NULL,
   textReview            TEXT,
   JobID                 INT NOT NULL,
   FOREIGN KEY (JobID) REFERENCES Job (JobID),
   FOREIGN KEY (StudentNUID) REFERENCES Student (NUID)
);


-- Notifications table creation
CREATE TABLE Notifications -- what happens to a notif if a student is deleted
(
   notifID INT AUTO_INCREMENT PRIMARY KEY,
   NUID INT NOT NULL,
   sentDate   DATETIME NOT NULL,
   Content    TEXT     NOT NULL,
   FOREIGN KEY (NUID) REFERENCES Student (NUID)
);


-- Starred Employers table creation
CREATE TABLE Starred_Employers  -- delete all starred employers if a student is deleted
(
   employerID INT NOT NULL,
   NUID INT NOT NULL,
   PRIMARY KEY (employerID, NUID),
   FOREIGN KEY (NUID) REFERENCES Student (NUID),
   FOREIGN KEY (employerID) REFERENCES Employer (employerID)
);


-- Starred Jobs table creation
CREATE TABLE Starred_Jobs -- delete all starred jobs if a student is deleted
(
   JobID INT NOT NULL,
   NUID INT NOT NULL,
   PRIMARY KEY (JobID, NUID),
   FOREIGN KEY (NUID) REFERENCES Student (NUID),
   FOREIGN KEY (JobID) REFERENCES Job (JobID)
);


-- Starred Reviews table creation
CREATE TABLE Starred_Reviews -- delete all starred reviews if a student is deleted
(
   ReviewID INT NOT NULL,
   NUID INT NOT NULL,
   PRIMARY KEY (reviewID, NUID),
   FOREIGN KEY (NUID) REFERENCES Student (NUID),
   FOREIGN KEY (ReviewID) REFERENCES Review (ReviewID)
);



CREATE TABLE Administrator -- what happens to a notif if the admin is deleted
(
   AdminID INT AUTO_INCREMENT PRIMARY KEY,
   Name    VARCHAR(100) NOT NULL,
   Email   VARCHAR(100) NOT NULL,
   Role    VARCHAR(255) NOT NULL, -- either co-op advisor or database admin
   UNIQUE (Email) 
);




-- Flagged Content table creation
CREATE TABLE Flagged_Content
(
   FlagID          INT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
   ReviewID        INT      NOT NULL,
   adminID         INT      NOT NULL, -- admin who flagged it, but what happens if the admin is deleted?
   ReasonSubmitted TEXT     NOT NULL,
   DateFlagged     DATETIME NOT NULL,
   FOREIGN KEY (ReviewID) REFERENCES Review (ReviewID),
   FOREIGN KEY (adminID) REFERENCES Administrator (adminID)
);


-- Statistics table creation
-- maybe turn into a backend query instead, executed as someone wants to see data
-- CREATE TABLE Statistics
-- (
--    statisticsID   INT AUTO_INCREMENT PRIMARY KEY,
--    totalUsers     INT      NOT NULL,
--    totalJobs      INT      NOT NULL,
--    totalReviews   INT      NOT NULL,
--    totalEmployers INT      NOT NULL,
--    generatedDate  DATETIME NOT NULL
-- );
