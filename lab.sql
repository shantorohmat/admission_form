use lab;
CREATE TABLE  STUDENT_INFORMATION 
   (	
    start_date date,
    end_date date,
	NAME VARCHAR(60) NOT NULL , 
	EMAIL VARCHAR(60) NOT NULL unique,
	INSTITUTION VARCHAR(60) NOT NULL , 
	PHONE numeric NOT NULL unique, 
	ADDRESS VARCHAR(60) NOT NULL , 
	GENDER VARCHAR(60) NOT NULL , 
	cgpa double,
	STATUS VARCHAR(60),
    ID int not null auto_increment,
    PRIMARY KEY (ID) 
    
)


