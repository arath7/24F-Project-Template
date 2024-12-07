# `database-files` Folder
# Database Structure:
- The database schema and table creation is done in `10_cooper.sql` file
- Data is inserted into the tables of the database within the `11_cooper-data.sql` file

## To start the database files within Datagrip and update in real-time while using the application:
- Build docker with: `docker compose build`
- Start docker with: `docker compose up -d`


### Make a new project 
- Select "Attach Directory to Project" within the project folder
- Select the database-files folder of this repository as the directory to attach to Datagrip project
- Choose MySQL as language
- Make a Data Source for the project
- Host: localhost
- Port: 3200 or alter it if you choose to 
- User: root
- Password: <choose your own password>
- Start datagrip with: `docker compose up db -d`
- Test the connection
- Must attach directory to Datagrip before `docker compose up db -d`
- Run 10_cooper.sql
- Run 11_cooper-data.sql


`docker compose down` to shut down the container




