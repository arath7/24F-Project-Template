fakedata = {
  "JobCategory": [
    {
      "JobCategoryID": 1,
      "Name": "Software Development"
    },
    {
      "JobCategoryID": 2,
      "Name": "Data Science"
    },
    {
      "JobCategoryID": 3,
      "Name": "Marketing"
    },
    {
      "JobCategoryID": 4,
      "Name": "Design"
    },
    {
      "JobCategoryID": 5,
      "Name": "Human Resources"
    }
  ],

  "Employer": [
    {
      "employerID": 1,
      "Name": "Tech Corp",
      "Email": "techcorp@example.com",
      "Address": "123 Tech Street, Silicon Valley, CA",
      "phoneNumber": "123-456-7890",
      "numJobs": 5,
      "Rating": 4.2
    },
    {
      "employerID": 2,
      "Name": "Data Solutions",
      "Email": "datasolutions@example.com",
      "Address": "456 Data Blvd, New York, NY",
      "phoneNumber": "234-567-8901",
      "numJobs": 3,
      "Rating": 4.5
    },
    {
      "employerID": 3,
      "Name": "Creative Agency",
      "Email": "creativeagency@example.com",
      "Address": "789 Design Ave, Los Angeles, CA",
      "phoneNumber": "345-678-9012",
      "numJobs": 2,
      "Rating": 4.7
    }
  ],

  "Job": [
    {
      "JobID": 1,
      "employerID": 1,
      "JobCategoryID": 1,
      "Name": "Software Engineer",
      "Description": "Develop software applications and systems.",
      "numOpenings": 5,
      "returnOffers": 3,
      "Salary": 90000,
      "numReviews": 10,
      "AggregatedReview": "Good work-life balance, great learning opportunities.",
      "Rating": 4
    },
    {
      "JobID": 2,
      "employerID": 2,
      "JobCategoryID": 2,
      "Name": "Data Analyst",
      "Description": "Analyze large datasets and provide insights.",
      "numOpenings": 3,
      "returnOffers": 2,
      "Salary": 80000,
      "numReviews": 5,
      "AggregatedReview": "Great team, but challenging workload.",
      "Rating": 4
    },
    {
      "JobID": 3,
      "employerID": 3,
      "JobCategoryID": 3,
      "Name": "Marketing Manager",
      "Description": "Oversee marketing strategies for clients.",
      "numOpenings": 2,
      "returnOffers": 1,
      "Salary": 70000,
      "numReviews": 7,
      "AggregatedReview": "Creative and fast-paced environment.",
      "Rating": 5
    }
  ],

  "Student": [
    {
      "NUID": 1001,
      "bDate": "2000-05-15",
      "firstName": "Mark",
      "lastName": "Johnson",
      "Email": "mark.johnson@example.com",
      "school": "University of X",
      "major": "Computer Science",
      "GradYear": 2024,
      "searchStatus": 'true'
    },
    {
      "NUID": 1002,
      "bDate": "1999-08-25",
      "firstName": "Ashley",
      "lastName": "Davis",
      "Email": "ashley.davis@example.com",
      "school": "University of Y",
      "major": "Marketing",
      "GradYear": 2024,
      "searchStatus": 'false'
    }
  ],

  "StudentJobs": [
    {
      "NUID": 1001,
      "jobID": 1,
      "StartDate": "2023-06-01",
      "EndDate": "2023-12-01"
    },
    {
      "NUID": 1002,
      "jobID": 2,
      "StartDate": "2023-01-01",
      "EndDate": "2023-06-01"
    }
  ],

  "Review": [
    {
      "reviewID": 1,
      "StudentNUID": 1001,
      "learningOpportunities": 5,
      "workCulture": 4,
      "overallSatisfaction": 4,
      "Mentorship": 3,
      "textReview": "Great experience overall with opportunities to learn.",
      "JobID": 1
    },
    {
      "reviewID": 2,
      "StudentNUID": 1002,
      "learningOpportunities": 4,
      "workCulture": 3,
      "overallSatisfaction": 4,
      "Mentorship": 5,
      "textReview": "Challenging work, but great mentorship and guidance.",
      "JobID": 2
    }
  ],

  "Notifications": [
    {
      "notifID": 1,
      "NUID": 1001,
      "employerID": 1,
      "sentDate": "2024-11-18 10:00:00",
      "Content": "New job posting for Software Engineer at Tech Corp."
    },
    {
      "notifID": 2,
      "NUID": 1002,
      "employerID": 2,
      "sentDate": "2024-11-19 12:30:00",
      "Content": "Data Analyst job posted by Data Solutions."
    }
  ],

  "Starred_Employers": [
    {
      "employerID": 1,
      "NUID": 1001
    },
    {
      "employerID": 2,
      "NUID": 1002
    }
  ],

  "Starred_Jobs": [
    {
      "JobID": 1,
      "NUID": 1001
    },
    {
      "JobID": 2,
      "NUID": 1002
    }
  ],

  "Starred_Reviews": [
    {
      "ReviewID": 1,
      "NUID": 1001
    },
    {
      "ReviewID": 2,
      "NUID": 1002
    }
  ],

  "Administrator": [
    {
      "AdminID": 1,
      "Name": "Alice Johnson",
      "Email": "alice.johnson@example.com",
      "Role": "Admin"
    },
    {
      "AdminID": 2,
      "Name": "Bob Brown",
      "Email": "bob.brown@example.com",
      "Role": "Moderator"
    }
  ],

  "Flagged_Content": [
    {
      "FlagID": 1,
      "ReviewID": 1,
      "adminID": 1,
      "ReasonSubmitted": "Inappropriate language in review",
      "DateFlagged": "2024-11-18 14:00:00"
    },
    {
      "FlagID": 2,
      "ReviewID": 2,
      "adminID": 2,
      "ReasonSubmitted": "Offensive comments about the employer",
      "DateFlagged": "2024-11-19 09:30:00"
    }
  ],

  "Statistics": [
    {
      "statisticsID": 1,
      "totalUsers": 5,
      "totalJobs": 3,
      "totalReviews": 2,
      "totalEmployers": 3,
      "generatedDate": "2024-11-19 12:00:00"
    }
  ]
}
