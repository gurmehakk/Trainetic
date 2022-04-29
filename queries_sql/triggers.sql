use railway_system;

DROP TRIGGER IF EXISTS check_pass;
DELIMITER $$
CREATE TRIGGER check_pass
    BEFORE INSERT
    ON users FOR EACH ROW
BEGIN
    if(length(new.passwords)<7) then
		signal sqlstate '45000' set message_text = "Password length cannot be less than 7 characters"; 
	end if;
END$$    
DELIMITER ;

drop trigger if exists after_ticket_canceled;
DELIMITER $$


DELIMITER $$

CREATE TRIGGER terminal_update
    BEFORE UPDATE
    ON Route FOR EACH ROW
BEGIN
	set @prevstartterminal = old.Start_terminal_id;
    set @prevendterminal = old.End_terminal_id;
    set @startterminal = new.Start_terminal_id;
    set @endterminal = new.End_terminal_id;
    set @trainid = old.Train_id;
    set @check1 =(SELECT p.Start_terminal_id FROM Passenger p WHERE p.Train_id = @trainid);
    set @check2 =(SELECT p.End_terminal_id FROM Passenger p WHERE p.Train_id = @trainid);
	
    UPDATE Passenger set Start_terminal_id= @startterminal WHERE @check1= @prevstartterminal AND Train_id = @trainid;
    UPDATE Passenger set End_terminal_id= @endterminal WHERE @check2= @prevendterminal AND Train_id = @trainid;
END$$    

DELIMITER ;

drop trigger if exists after_ticket_canceled;
DELIMITER $$
CREATE TRIGGER after_ticket_canceled
BEFORE DELETE
ON passenger FOR EACH ROW
BEGIN
	UPDATE Train 
    set Available_seats = Available_seats + 1
    where Train.Train_id = old.Train_id;
END$$
DELIMITER ;

drop trigger if exists after_ticket_booked;
DELIMITER $$
CREATE TRIGGER after_ticket_booked
BEFORE DELETE
ON passenger FOR EACH ROW
BEGIN
	UPDATE Train 
    set Available_seats = Available_seats - 1
    where Train.Train_id = old.Train_id;
END$$
DELIMITER ;
