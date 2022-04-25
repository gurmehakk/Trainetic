use railway_system;

create index user_speed on users(Adhaar_no, password);
create index train_speed on train(Train_id, Train_name);
create index route_speed on route(Route_id, Train_id, Start_station_id, End_station_id);
create index passenger_speed on passenger(Ticket_id, Adhaar_no, Train_id);
