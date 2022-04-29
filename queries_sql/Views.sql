Create view Route_pas As
Select P.Ticket_id, P.Adhaar_no, R.Start_station_id, R.End_station_id
from Passenger P, route R
where P.Route_id=R.route_id;
select * from Route_pas;

CREATE VIEW some_passenge AS
SELECT Users.first_name AS Name, DOB, e_mail, Ticket_id
FROM Passenger
JOIN Users
ON Passenger.adhaar_no = Users.adhaar_no;
select * from some_passenge;

CREATE VIEW Train_seat AS
SELECT Seats_general, seats_AC1, seats_ac2, Route.train_id
FROM Route
JOIN train
ON Route.train_id = Train.train_id;
select * from Train_seat;

Create view Route_map AS
select start_station_id, End_station_id, Train.train_id, train_name
from Route
JOIN
Train ON train.train_id=Route.train_id;
select * from Route_map;