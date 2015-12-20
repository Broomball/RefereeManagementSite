DELIMITER //
USE Broomball//
DROP TABLE IF EXISTS user//
DROP TABLE IF EXISTS rank//
DROP TABLE IF EXISTS refShift//
DROP TABLE IF EXISTS emailCode//
DROP TABLE IF EXISTS refShiftSignUp//


CREATE TABLE user(      username VARCHAR(40), 
                        fullName VARCHAR(40), 
                        permissions VARCHAR(40), 
                        email VARCHAR(30), 
                        rank INT(2) DEFAULT 0,  
                        password VARCHAR(256),
                        PRIMARY KEY(username) 
                    ) //


CREATE TABLE rank(      id INT(11) NOT NULL AUTO_INCREMENT, 
                        refUser VARCHAR(40), 
                        superUser VARCHAR(40), 
                        rank INT(2),
                        date DATE, 
                        confirmed BOOLEAN DEFAULT FALSE,
                        PRIMARY KEY( id ) 
                    ) //

CREATE TABLE refShift(  id INT(11) NOT NULL AUTO_INCREMENT,  
                        date DATE NOT NULL, 
                        shiftNum INT(2) NOT NULL, 
                        rink VARCHAR(10),
                        refUser1 VARCHAR(10),
                        refUser2 VARCHAR(10),
                        canceled BOOLEAN DEFAULT FALSE , 
                        isOpen BOOLEAN DEFAULT TRUE, 
                        PRIMARY KEY ( id ) 
                    ) // 

CREATE TABLE emailCode( username VARCHAR(40) NOT NULL,
                        code VARCHAR(50) NOT NULL,
                        PRIMARY KEY ( username ),
                        FOREIGN KEY ( username ) 
                            REFERENCES user  ( username )
                            ON UPDATE CASCADE
                            ON DELETE CASCADE
                        ) //

CREATE TABLE refShiftSignUp(   id INT(11) NOT NULL AUTO_INCREMENT,
                            username VARCHAR(40) NOT NULL, 
                            date DATE, 
                            shiftNum INT(2) NOT NULL, 
                            PRIMARY KEY ( id )
                        ) //
DELIMITER ;
