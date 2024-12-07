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
DROP TABLE IF EXISTS Student;

CREATE TABLE JobCategory
(
   JobCategoryID INT AUTO_INCREMENT PRIMARY KEY,
   Name VARCHAR(100) NOT NULL
);

CREATE TABLE Employer
(
   employerID  INT AUTO_INCREMENT PRIMARY KEY,
   Name        VARCHAR(100) NOT NULL,
   Email       VARCHAR(100) NOT NULL,
   Address     VARCHAR(255) NOT NULL,
   phoneNumber VARCHAR(20)  NOT NULL,
   UNIQUE (Email),
   UNIQUE (phoneNumber),
   UNIQUE (Address)
);

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
   FOREIGN KEY (JobCategoryID) REFERENCES JobCategory (JobCategoryID) ON DELETE RESTRICT,
   FOREIGN KEY (employerID) REFERENCES Employer (employerID) ON DELETE RESTRICT
);

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
    FOREIGN KEY (jobID) REFERENCES Job (jobID) ON DELETE CASCADE,
    FOREIGN KEY (NUID) REFERENCES Student (NUID) ON DELETE CASCADE
);

CREATE TABLE Review
(
   reviewID              INT AUTO_INCREMENT PRIMARY KEY,
   StudentNUID           INT NOT NULL,
   learningOpportunities INT NOT NULL,
   workCulture           INT NOT NULL,
   overallSatisfaction   INT NOT NULL, -- overall rating of co-op
   Mentorship            INT NOT NULL,
   textReview            TEXT,
   JobID                 INT NOT NULL,
   FOREIGN KEY (JobID) REFERENCES Job (JobID) ON DELETE CASCADE,
   FOREIGN KEY (StudentNUID) REFERENCES Student (NUID) ON DELETE RESTRICT
);

CREATE TABLE Notifications
(
   notifID INT AUTO_INCREMENT PRIMARY KEY,
   NUID INT NOT NULL,
   sentDate   DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
   Content    TEXT     NOT NULL,
   FOREIGN KEY (NUID) REFERENCES Student (NUID) ON DELETE CASCADE
);

CREATE TABLE Starred_Employers
(
   employerID INT NOT NULL,
   NUID INT NOT NULL,
   PRIMARY KEY (employerID, NUID),
   FOREIGN KEY (NUID) REFERENCES Student (NUID) ON DELETE CASCADE,
   FOREIGN KEY (employerID) REFERENCES Employer (employerID) ON DELETE CASCADE
);

CREATE TABLE Starred_Jobs
(
   JobID INT NOT NULL,
   NUID INT NOT NULL,
   PRIMARY KEY (JobID, NUID),
   FOREIGN KEY (NUID) REFERENCES Student (NUID) ON DELETE CASCADE,
   FOREIGN KEY (JobID) REFERENCES Job (JobID) ON DELETE CASCADE
);

CREATE TABLE Starred_Reviews
(
   ReviewID INT NOT NULL,
   NUID INT NOT NULL,
   PRIMARY KEY (reviewID, NUID),
   FOREIGN KEY (NUID) REFERENCES Student (NUID) ON DELETE CASCADE, -- delete all starred reviews if a student is deleted
   FOREIGN KEY (ReviewID) REFERENCES Review (ReviewID) ON DELETE CASCADE -- delete starred review if review is deleted
);

CREATE TABLE Administrator
(
   AdminID INT AUTO_INCREMENT PRIMARY KEY,
   Name    VARCHAR(100) NOT NULL,
   Email   VARCHAR(100) NOT NULL,
   Role    VARCHAR(255) NOT NULL, -- either co-op advisor or database admin
   UNIQUE (Email) 
);

CREATE TABLE Flagged_Content
(
   FlagID          INT      NOT NULL AUTO_INCREMENT PRIMARY KEY,
   ReviewID        INT      NOT NULL,
   adminID         INT, -- can have an admin, but can also be null if admin was deleted
   ReasonSubmitted TEXT     NOT NULL,
   DateFlagged     DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
   FOREIGN KEY (ReviewID) REFERENCES Review (ReviewID) ON DELETE CASCADE, -- if a review is deleted, no need for flagged content within it
   FOREIGN KEY (adminID) REFERENCES Administrator (adminID) ON DELETE SET NULL
);
