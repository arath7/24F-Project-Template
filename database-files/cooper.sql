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


# job categories:

# (1, 1, 'Software Engineer', 'Develop and maintain cutting-edge software applications.', 5, 2, 120000, 150, 'Highly collaborative team and innovative projects.', 5),
# (2, 2, 'Data Scientist', 'Analyze data and create predictive models to guide business decisions.', 3, 1, 115000, 120, 'Great work-life balance and technical challenges.', 4),
# (3, 3, 'Graphic Designer', 'Design digital assets for marketing campaigns and branding.', 4, 1, 65000, 80, 'Creative and dynamic team.', 4),
# (4, 4, 'Cloud Architect', 'Build and maintain scalable cloud infrastructure.', 2, 1, 135000, 90, 'Challenging projects with supportive colleagues.', 5),
# (5, 5, 'Environmental Engineer', 'Design sustainable solutions for waste management and energy.', 3, 0, 95000, 70, 'Focus on green initiatives and innovation.', 4),
# (6, 6, 'Marketing Specialist', 'Develop marketing strategies and execute campaigns.', 6, 2, 70000, 110, 'Fast-paced and creative environment.', 4),
# (7, 1, 'AI Research Scientist', 'Conduct research in artificial intelligence and machine learning.', 2, 1, 140000, 50, 'Cutting-edge research opportunities.', 5),
# (8, 5, 'Urban Planner', 'Plan city layouts and optimize land use.', 3, 1, 85000, 60, 'Impactful work in city development.', 4),
# (9, 7, 'Robotics Engineer', 'Design and program robotic systems for automation.', 4, 1, 125000, 75, 'Excellent learning and growth opportunities.', 4),
# (10, 1, 'Mobile App Developer', 'Develop and maintain iOS and Android applications.', 5, 2, 110000, 85, 'Supportive team and exciting projects.', 4),
# (11, 8, 'Healthcare Analyst', 'Analyze healthcare data to improve outcomes.', 3, 0, 90000, 70, 'Work with meaningful data to save lives.', 4),
# (12, 1, 'Front-End Developer', 'Create user interfaces for web applications.', 4, 2, 95000, 100, 'Focus on user experience and performance.', 4),
# (13, 6, 'SEO Specialist', 'Optimize website traffic and improve search engine rankings.', 6, 3, 75000, 95, 'Dynamic team with measurable impact.', 4),
# (14, 1, 'Back-End Developer', 'Build scalable server-side applications.', 5, 2, 105000, 85, 'Supportive team and exciting projects.', 5),
# (15, 9, 'Biomedical Engineer', 'Design medical devices and health monitoring systems.', 2, 1, 110000, 45, 'Great benefits and meaningful projects.', 4),
# (16, 5, 'Civil Engineer', 'Design and oversee public infrastructure projects.', 3, 1, 90000, 65, 'Hands-on projects in urban development.', 4),
# (17, 4, 'Cloud Security Specialist', 'Ensure the security of cloud-based systems.', 3, 1, 130000, 50, 'Focus on cutting-edge cybersecurity.', 5),
# (18, 10, 'Game Developer', 'Develop engaging games with unique mechanics.', 4, 1, 85000, 80, 'Creative and innovative team environment.', 4),
# (19, 3, 'UI/UX Designer', 'Design intuitive and visually appealing user experiences.', 4, 1, 90000, 90, 'Focus on creativity and user needs.', 4),
# (20, 1, 'DevOps Engineer', 'Streamline software development processes and deployments.', 4, 1, 120000, 100, 'Great focus on collaboration and technology.', 5),
# (21, 11, 'Nurse Practitioner', 'Provide advanced healthcare services.', 5, 2, 110000, 110, 'Rewarding and patient-focused work.', 5),
# (22, 8, 'Data Analyst', 'Interpret and visualize data to support decision-making.', 4, 1, 85000, 75, 'Collaborative and data-driven team.', 4),
# (23, 1, 'ML Engineer', 'Develop machine learning algorithms and applications.', 3, 2, 130000, 70, 'Fast-paced and exciting projects.', 5),
# (24, 4, 'Cloud Developer', 'Develop applications for cloud environments.', 3, 1, 125000, 80, 'Challenging and rewarding environment.', 5),
# (25, 9, 'Medical Device Developer', 'Create innovative solutions in medical technology.', 3, 1, 115000, 55, 'Excellent learning opportunities.', 4),
# (26, 7, 'Automation Engineer', 'Design and test automation systems.', 3, 1, 100000, 70, 'Cutting-edge projects and collaboration.', 4),
# (27, 10, 'Game Designer', 'Conceptualize and design video games.', 2, 1, 80000, 60, 'Creative and engaging work environment.', 4),
# (28, 6, 'Social Media Manager', 'Develop and manage social media strategies.', 5, 2, 70000, 90, 'Focus on creativity and audience engagement.', 4),
# (29, 12, 'Accounting Manager', 'Oversee financial reporting and compliance.', 4, 2, 95000, 80, 'Supportive team and growth opportunities.', 4),
# (30, 4, 'Cloud Software Engineer', 'Develop software optimized for cloud platforms.', 4, 1, 120000, 75, 'Fast-paced and dynamic work environment.', 5),
# (31, 5, 'Renewable Energy Consultant', 'Advise on sustainable energy solutions.', 3, 1, 90000, 50, 'Impactful work with green initiatives.', 4),
# (32, 8, 'Biostatistician', 'Analyze biological data for research studies.', 3, 1, 95000, 60, 'Rewarding and research-focused role.', 4),
# (33, 11, 'Medical Researcher', 'Conduct research to advance medical science.', 3, 1, 115000, 50, 'Exciting opportunities for discovery.', 5),
# (34, 6, 'PR Specialist', 'Manage public relations and brand reputation.', 4, 1, 80000, 85, 'Creative work with measurable impact.', 4),
# (35, 10, 'Level Designer', 'Design and refine levels for video games.', 2, 1, 85000, 70, 'Supportive team and fun projects.', 4),
# (36, 1, 'Blockchain Developer', 'Develop and deploy blockchain-based applications.', 3, 1, 130000, 50, 'Focus on innovation and security.', 5),
# (37, 3, 'Art Director', 'Oversee artistic direction for media projects.', 2, 1, 100000, 65, 'Creative and leadership-focused role.', 4),
# (38, 7, 'Mechatronics Engineer', 'Develop systems that integrate mechanical and electronic components.', 3, 1, 120000, 60, 'Exciting and innovative projects.', 4),
# (39, 9, 'Clinical Trials Coordinator', 'Manage clinical trials for new medications.', 3, 1, 95000, 45, 'Work on life-saving innovations.', 4),
# (40, 11, 'Physician Assistant', 'Provide healthcare under the supervision of a doctor.', 4, 2, 115000, 95, 'Rewarding patient-focused role.', 5);


