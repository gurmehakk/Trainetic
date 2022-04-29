use railway_system;

-- Query:1 -> Show all passengers Boarding Rajdhani Express
select Users.First_name, Users.Last_name, Users.Adhaar_no 
from Users 
inner join passenger
on (users.Adhaar_no = passenger.Adhaar_no) and (passenger.Train_id = 12703);

-- Query:2 -> Show all trains going through Delhi
select distinct T.Train_id, T.Train_name
from Train T, Route R 
where (T.Train_id = R.Train_id) and (R.Start_Station_id = 100 or R.End_Station_id = 100);

-- Query:3 -> Show all stations where Shan-e-Punjab travells through
select S.Station_name, S.Station_id 
from Station S, Route R 
where (S.Station_id = R.Start_station_id) and (R.Train_id=16519);

-- Query:4 -> Show all Passengers whose DOB in May
select P.Ticket_id, U.First_name, U.Last_name, u.DOB
from Users U, Passenger P 
where (P.Adhaar_no = U.Adhaar_no) and (month(U.DOB)=5);

-- Query:5 -> Number of seats available in Genral Coach in Shatabdi Express
select R.Seats_General, R.start_station_id, R.end_station_id
from Route R 
where (R.Train_id = 14484);

-- Query:6 -> Show all Passengers having seats in AC2 coach
select P.Ticket_id, P.Train_id, U.First_name, U.last_name
from Passenger P, Users U, Coach C
where (P.Adhaar_no = U.Adhaar_no) and (P.Coach_id = C.Coach_id) and (C.Coach_name = "AC_2");

-- Query:7 -> Names of all trains in Mumbai Station between 19/04/2022 and 21/04/2022
select distinct T.train_name, T.Train_id 
from Train T, Route R
where (T.Train_id = R.Train_id) and (R.Start_station_id = 113) and 
(((date(R.Arrival_time) >= "2022-04-19") and (date(R.Arrival_time) <= "2022-04-21")) or
((date(R.Departure_time) >= "2022-04-19") and (date(R.Departure_time) <= "2022-04-21")));

-- Query:8 -> Count trains Arriving at terminal 1122
select count(R.Start_terminal_id)
from Route R
where R.Start_terminal_id = 1122;

-- Query:9 -> Show all tickets booked by user Matthew Cameron
select P.Ticket_id, P.Date_of_Booking, P.Train_id
from Passenger P, Users U 
where (U.Adhaar_no = P.Adhaar_no) and (U.First_name = "Matthew" and U.Last_name="Cameron");

-- Query:10 -> show all trains with AC1 coach with available seats 
select distinct T.Train_id, T.Train_name, R.Seats_AC1
from Train T, Route R 
where (T.Train_id = R.Train_id) and (R.Seats_AC1>0);

-- Query:11 -> View all Trains going through Mumbai Station
drop view mumbai_trains;
create view Mumbai_Trains as 
select distinct T.Train_id, T.Train_name
from Train T, Route R 
where (T.Train_id = R.Train_id) and (R.Start_Station_id = 113 or R.End_Station_id = 113);
select * from mumbai_trains;

-- Query:12 -> Add a User with name Ishita Sindhwani
INSERT INTO Users (Adhaar_no,Username,e_mail,Mobile,DOB,First_name,Last_name)
VALUES
  (256982140,"octopus","abcsample123@gmail.com",123586012,"2002-07-31","Ishita","Sindhwani");
  
-- Query:13 -> Delete User Ivor Knox
DELETE from Users where
User_id = "Iknoxx_00";

-- Query:14 -> users who have start station as new delhi or whose first name is ciara

select U.Adhaar_no
from Users U
where U.first_name='Ciara'
or
U.Adhaar_no IN (
	select P.Adhaar_no
	from Passenger P 
	where P.Start_station_id=100
);

-- Query:15 -> find the difference between avg of total seats of all trains and avg of available seats of all train

select T1.avg1-T2.avg2
from (
	select Avg(T.Total_Seats) AS
	avg1
	from train T)AS T1, 
	(select Avg(T.Available_Seats) AS
	avg2
	from train T) AS T2;

-- Query:16 -> routes on which the start station has less than 2 terminals
select R.Route_id
from Route R
where not exists (
	select S.Station_id
	from Station S where R.Start_station_id=S.Station_id
	and
	S.No_of_terminals>1);



 