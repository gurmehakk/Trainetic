CREATE USER 'Big_Boss'@'Localhost';
CREATE USER 'Admin_railway'@'Root';
CREATE USER 'User'@'Localhost';
CREATE USER 'Worker'@'Localhost';

-- Big_Boss
GRANT ALL
ON *.*
TO 'Big_Boss'@'Localhost';

-- Admin_railway
GRANT SELECT
ON Route_pas
TO 'Admin_railway'@'Root';

GRANT SELECT
ON Train_seat
TO 'Admin_railway'@'Root';

GRANT SELECT
ON Route_map
TO 'Admin_railway'@'Root';

-- User
GRANT SELECT
ON Train_seat
TO 'User'@'Localhost';

GRANT SELECT
ON some_passenge
TO 'User'@'Root';

-- workshop organizer
GRANT SELECT
ON Route_pas
TO 'Worker'@'Localhost';

GRANT SELECT
ON Route_map
TO 'Worker'@'Root';

