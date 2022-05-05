use railway_system;
-- Query1: users who have start station as new delhi or whose first name is ciara
select U.Adhaar_no
from Users U
where U.first_name='Ciara'
or
U.Adhaar_no IN (
	select P.Adhaar_no
	from Passenger P 
	where P.Start_station_id=100
);

-- Query2:find the difference between avg of total seats of all trains and avg of available seats of all train
select T1.avg1-T2.avg2
from (
	select Avg(T.Total_Seats) AS
	avg1
	from train T)AS T1, 
	(select Avg(T.Available_Seats) AS
	avg2
	from train T) AS T2;

-- Query3:Sum of total seats of train going through station with id 101 (Kota)
select sum(T.total_seats)
from Train T, Route R 
where (T.Train_id = R.Train_id) 
and (R.Start_Station_id = 101 or R.End_Station_id = 101);

-- Query4: Route which have trains with total seats greater than 150 and available seats greater than 100 
SELECT R.Route_id
FROM Train T, Route R
WHERE T.total_seats>150 AND
R.train_id = T.train_id AND EXISTS (
	SELECT T2.train_id
	FROM train T2, Route R2
	WHERE T2.available_seats>100 AND T.train_id=
	R.train_id AND T2.train_id = R2.train_id);

-- Query5: routes on which the start station has less than 2 terminals
select R.Route_id
from Route R
where not exists (
	select S.Station_id
	from Station S where R.Start_station_id=S.Station_id
	and
	S.No_of_terminals>1);

-- Query6:Select train names where available seats are less than the minimum of total seats and total seats are greater than 10
SELECT DISTINCT T.train_name
FROM train T
WHERE T.available_seats< 
(	SELECT MIN(T2.total_seats)
	from train T2
	where (T2.total_seats>10));



-- Query7:Names of all trains and their train id which have Genral are in Mumbai statiom between 18/04/2022 and 23/04/2022
select distinct T.train_name, T.Train_id 
	from Train T, Route R, Coach C
	where (T.Train_id = R.Train_id) and (R.Start_station_id = 113) and 
	(C.train_id=T.train_id) and (C.coach_name="Genral") and
	(((date(R.Arrival_time) >= "2022-04-15") and (date(R.Arrival_time) <= "2022-04-23")) or
	((date(R.Departure_time) >= "2022-04-15") and (date(R.Departure_time) <= "2022-04-23")));

-- Query8:Find general, Ac1 AC2 seats and train_id from Route and train and group by seats general
SELECT Seats_general, seats_AC1, seats_ac2, Route.train_id
FROM Route
JOIN train
ON Route.train_id = Train.train_id
group by Seats_general;

-- Query9: Arrange in ascending order of ticket id for passengers having seats in genral coach or AC 2 coach
select P.Ticket_id, U.First_name, U.last_name, U.DOB
from Passenger P, Users U, Coach C
where (P.Adhaar_no = U.Adhaar_no) and (P.Coach_id = C.Coach_id) and ((C.Coach_name = "Genral") or (C.coach_name="AC_2"))
order by P.ticket_id asc;

-- Query10: Train_id and Route_id where total seats are more than 75 and it has AC_1 coach also
Select T.train_id, R.route_id
FROM train T, Route R 
WHERE R.train_id =T.train_id 
and (T.total_seats > 75)
and exists(
select T2.train_id
from train T2, Coach C
where T2.train_id=C.train_id and C.coach_name="AC_1" and T.train_id=T2.train_id);


