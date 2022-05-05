drop database Railway_System;
create database Railway_System;
show databases;

use railway_system;
create table Train(
	Train_id int primary key,
    Train_name varchar(250),
    Total_seats int,
    Available_seats int,
    Arrival_time datetime,
    Departure_time datetime
);

create table Coach(
	Coach_id int primary key,
    Coach_name varchar(50),
    Number_of_Seats int,
    Train_id int,
    foreign key(Train_id) references Train(Train_id) on delete cascade
);

ALTER TABLE Coach
ADD Train_name varchar(250);

-- ALTER TABLE Coach
-- ADD FOREIGN KEY(Train_name)
-- REFERENCES Train(Train_name)
-- ON DELETE SET NULL;

ALTER TABLE Train
ADD Source_id int;

ALTER TABLE Train
ADD Destination_id int;

create table Station(
	Station_id int primary key,
    Station_name varchar(250),
    No_of_terminals int
);

ALTER TABLE Train
ADD FOREIGN KEY(Source_id)
REFERENCES Station(Station_id)
ON DELETE SET NULL;

ALTER TABLE Train
ADD FOREIGN KEY(Destination_id)
REFERENCES Station(Station_id)
ON DELETE SET NULL;

create table Terminal(
	Terminal_id int primary key,
    Station_id int,
    foreign key(Station_id) references Station(Station_id) on delete cascade
);

create table Users(
	Adhaar_no int primary key,
    Username varchar(250),
    e_mail varchar(250),
    Mobile int,
    DOB date,
    First_name varchar(250),
    Last_name varchar(250),
    passwords varchar(250)
);


create table Route(
	Route_id int primary key,
    Number_of_seats int,
    Start_terminal_id int,
    End_terminal_id int,
    Arrival_time datetime,
    Departure_time datetime,
    Start_station_id int,
    End_station_id int,
    foreign key(Start_station_id) references Station(Station_id) on delete set null,
    foreign key(End_station_id) references Station(Station_id) on delete set null,
    foreign key(Start_terminal_id) references Terminal(Terminal_id) on delete set null,
    foreign key(End_terminal_id) references Terminal(Terminal_id) on delete set null
);

-- ALTER TABLE Route
-- DROP COLUMN Arrival_time;
-- ALTER TABLE Route
-- ADD COLUMN Arrival_time timestamp;
-- ALTER TABLE Route
-- DROP COLUMN Departure_time;
-- ALTER TABLE Route
-- ADD COLUMN Departure_time timestamp;

ALTER TABLE Route
ADD Train_id int;

ALTER TABLE Route
ADD FOREIGN KEY(Train_id)
REFERENCES Train(Train_id)
ON DELETE SET NULL;

create table Passenger(
	Ticket_id int primary key,
    Adhaar_no int,
    foreign key(Adhaar_no) references Users(Adhaar_no) on delete cascade,
    Date_of_Booking datetime,
    Coach_id int,
    foreign key(Coach_id) references Coach(Coach_id) on delete set null,
    Route_id int,
    foreign key(Route_id) references Route(Route_id) on delete set null,
    Start_station_id int,
    End_station_id int,
    foreign key(Start_station_id) references Station(Station_id) on delete set null,
    foreign key(End_station_id) references Station(Station_id) on delete set null,
    Start_terminal_id int,
    End_terminal_id int,
	foreign key(Start_terminal_id) references Terminal(Terminal_id) on delete set null,
    foreign key(End_terminal_id) references Terminal(Terminal_id) on delete set null
);

ALTER TABLE Route
DROP Number_of_seats;

ALTER TABLE Route
ADD Seats_General int;
ALTER TABLE Route
ADD Seats_AC1 int;
ALTER TABLE Route
ADD Seats_AC2 int;

Alter table Passenger
Add Train_id int;

ALTER TABLE Passenger
ADD FOREIGN KEY(Train_id)
REFERENCES Train(Train_id)
ON DELETE SET NULL;

-- alter table Passenger drop foreign key Route_id;
-- ALTER TABLE Passenger
-- DROP Route_id;

-- ALTER TABLE Route
-- ADD FOREIGN KEY(Seats_General)
-- REFERENCES Coach(Number_of_Seats)
-- ON DELETE SET NULL;
-- ALTER TABLE Route
-- ADD FOREIGN KEY(Seats_AC1)
-- REFERENCES Coach(Number_of_Seats)
-- ON DELETE SET NULL;
-- ALTER TABLE Route
-- ADD FOREIGN KEY(Seats_AC2)
-- REFERENCES Coach(Number_of_Seats)
-- ON DELETE SET NULL;

select * from Train;
select * from Route;
select * from Coach;
select * from Station;
select * from Terminal;
select * from Users;
select * from Passenger;
show tables;