# 🚂Trainetic 
Welcome To *Trainetic*!! A Web-Tool made for booking tickets for Trains. 
Made for DBMS/CSE202 course project, Using Tools *Python Flask, MySQL, HTML and CSS.*

## Getting Started 
First Download the zip of this project and then install all the required files by running the following commands on your PC terminal.
### Windows
    py -2 -m pip install virtualenv
    pip install Flask
### MacOs
    sudo python2 -m pip install virtualenv
    pip install Flask
   
### Debian/Ubuntu Linux
    sudo apt install python-virtualenv
    pip install Flask
    
### CentOS/Fedora/Red Hat Linux
    sudo yum install python-virtualenv
    pip install Flask

Download MySQL workbench, and create a new user with following credentials:

> Username: root <br />
> Host: Localhost <br />
> Password: AbCd@123

Now create a Database by running the primary database create query file given at:
[Database_Create](https://github.com/krishnamomar/Trainetic/blob/main/queries_sql/Primary/database_create.sql)
Now simply run the file as 

    python -m flask run
    
Open your browser and run the link

    http://127.0.0.1:5000/


### Populating Database
Initially all the primary CSV files are provided with all required data for primary working.
Run required MySQL command to run populate all the databases. 
[CSV Files](https://github.com/krishnamomar/Trainetic/tree/main/All_Database_CSV)

## Schematic Diagram of The DATABASE

## All Major Screens 
 
### Main Page

### Browsing Trains 

### User Login Page

###  User Info Page

### All Booked Ticket List 

### Browse Trains

### Book a Ticket

### Registration Screen

### Admin Login

> Please note admin can only login through following credentials:<br />
> Username:  *\_octopus\_* <br />
> Password: *monkey_man*

## Other Queries 
There are more mysql query files, meant for running the database related function without the frontend being involved. 
[All Queries](https://github.com/krishnamomar/Trainetic/tree/main/queries_sql)

## Project Report
Project Repost can be accessed from the following Link.
[Project Repost Complete](https://github.com/krishnamomar/Trainetic/blob/main/Report/Project%20report_DBMS.pdf)

***Thank You***
<br/>
*Made By:*
 - [Ishita Sindhwani](https://github.com/iishh2002)
 - [Gurmehak Kaur](https://github.com/gurmehakk)
 - [Darsh Parikh](https://github.com/darsh20560)
 - [Krishnam Omar](https://github.com/krishnamomar)
