DROP TRIGGER IF EXISTS check_pass;
DELIMITER $$
CREATE TRIGGER check_pass
    BEFORE INSERT
    ON users FOR EACH ROW
BEGIN
    if(length(new.passwords)<7) then
		signal sqlstate '45000' set message_text = "Paswsword length cannot be less than 7 characters"; 
	end if;
END$$    
DELIMITER ;