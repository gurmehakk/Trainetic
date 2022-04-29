use railway_system;

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

drop trigger if exists after_ticket_canceled;
DELIMITER $$

CREATE TRIGGER after_ticket_canceled
BEFORE DELETE
ON passenger FOR EACH ROW
BEGIN
	set @trainid=old.Train_id; 
	set @ticketno=old.Ticket_id;
    SET @coach = (SELECT p.Coach_id 
               FROM passenger p 
               WHERE p.ticket_no = @ticketno);
	if @coach= 'General' then 
		UPDATE Route set Seats_General = Seats_General +1 WHERE Train_id = @trainid;
	elseif @coach='AC_1' then        
		UPDATE Route set Seats_AC1 = Seats_AC1+1 WHERE Train_id = @trainid ;   
	elseif @coach='AC_2' then       
		UPDATE Route set Seats_AC2 = Seats_AC2+1 WHERE Train_id = @trainid ;
	end if;
END$$
DELIMITER ;

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

DELIMITER $$

CREATE TRIGGER after_ticket_booked
BEFORE INSERT
ON passenger FOR EACH ROW
BEGIN
	set @trainid=new.Train_id; 
	set @ticketno=new.Ticket_id;
    SET @coach = (SELECT p.Coach_id 
               FROM passenger p 
               WHERE p.ticket_no = @ticketno);
	if @coach= 'General' then 
		UPDATE Route set Seats_General = Seats_General -1 WHERE Train_id = @trainid;
	elseif @coach='AC_1' then        
		UPDATE Route set Seats_AC1 = Seats_AC1-1 WHERE Train_id = @trainid ;   
	elseif @coach='AC_2' then       
		UPDATE Route set Seats_AC2 = Seats_AC2-1 WHERE Train_id = @trainid ;
	end if;
END$$
DELIMITER ;