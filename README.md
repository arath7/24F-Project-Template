# CO-OPer Rates: CS 3200 Final Project

Group Members: Ananya Rath, Anika Thankachen, Sree Kandula, Tishya Kasliwal

Project Name: CO-OPer Rates

Link to Demo Video: https://drive.google.com/file/d/1hU1fNoD_DsAFBhvM4VpBGR96NvoHJAwY/view?usp=share_link 

## Project Overview

CO-OPer Rates is a data-driven application that focuses on student experiences and opinions within the Co-op and early career space.
Students can leave reviews for their co-op positions that other students can view, save, and use to inform their own decision-making about co-ops to apply to, career paths to pursue, and employers to network with and apply for jobs with. Our UI focuses on students searching for co-ops/viewing reviews, students leaving reviews for co-op experiences, co-op advisors, and systems/database administrators for the application. 

This project was completed as a final project at Northeastern University's CS3200 class. 

## Prerequisites

- A GitHub Account
- A terminal-based or GUI git client
- VSCode with the Python Plugin
- A distrobution of Python running on your laptop (Choco (for Windows), brew (for Macs), miniconda, Anaconda, etc). 

## Project Components

There are three major components which will each run in their own Docker Containers:

- Streamlit App in the `./app` directory
- Flask REST api in the `./api` directory
- SQL files for your data model and data base in the `./database-files` directory

## Project Tech Stack
- Frontend: Streamlit framework
- Backend: Python, Flask
- Database: MySQL
- Containerization: Docker containers



### Getting Started with CO-OPer Rates
## Follow these steps to download and run the application

1. Clone the repository from GitHub
2. Ensure the following tools are installed
    - Docker and Docker Compose (download Docker Desktop)
    - Git
    - Python 3.xx
3. Configure .env file in the project root directory

```ini
SECRET_KEY=someCrazyS3cR3T!Key.!
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=cooper
MYSQL_ROOT_PASSWORD=12345
```
4. Build and start CO-OPer Rates:
    - `docker compose build` -- builds containers
    - `docker compose up -d` to start all the containers in the background

5. Access CO-OPer Rates Application
    - Frontend: http://localhost:8501/
    - API: http://localhost:4000/ 
    - Database connections at client port `3306`

6. Stop the Application:
    - `docker compose down` to shutdown and delete the containers 