# cs5224_project

## Prerequisite
Installation: MySQL, flask, React.
python version 3.9
scikit-learn version 1.2.2
AWS RDS MySql version 8.0

## Setup Guide
MYSQL: create a user with:
`username: root`
`password: admin`
and create a database `flask`. Start the mysql service (If windows, go services - MySQL80, manually start it up).

Start two terminals. 
One of the terminal to start frontend server: 
`cd project-app`
`npm start`

The other terminal to start backend server:
`cd server`
`py run.py`

Go to `localhost:3000`, click on the 'search result page' to check on the changes. 
