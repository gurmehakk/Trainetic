CREATE USER 'Big_Boss'@'Root';
CREATE USER 'Admin_railway'@'Root';
CREATE USER 'User'@'Root';
CREATE USER 'Worker'@'Root';

-- Big_Boss
GRANT ALL
ON *.*
TO 'Big_Boss'@'Root';

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
TO 'User'@'Root';

GRANT SELECT
ON some_passenge
TO 'User'@'Root';

-- workshop organizer
GRANT SELECT
ON Route_pas
TO 'Worker'@'Root';

GRANT SELECT
ON Route_map
TO 'Worker'@'Root';

