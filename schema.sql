DROP TABLE IF EXISTS SHARING;
DROP TABLE IF EXISTS PARKING_PLACE;
DROP TABLE IF EXISTS USER_sp;
DROP TABLE IF EXISTS VALET;


CREATE TABLE USER_sp (
	name varchar2(20),
	utype number,
	id varchar2(10) PRIMARY KEY,
	pw varchar2(10),
	phone varchar2(13),
	age number,
	sex varchar2(5),
	accid number
);

CREATE TABLE PARKING_PLACE (
	Place_ID number PRIMARY KEY,
	Owner_ID VARCHAR2(10),
	Adr VARCHAR2(100),
	Price number,
	CONSTRAINT own FOREIGN KEY (Owner_ID) REFERENCES USER_sp(id)
);


CREATE TABLE SHARING (
	Sharing_ID number PRIMARY KEY,
	Sdate varchar2(20),
	Edate varchar2(20),
	User_ID varchar2(10),
	Owner_ID varchar2(10),
	Place_ID number,
	fee number,
	CONSTRAINT borrower FOREIGN KEY (User_ID) REFERENCES USER_sp(id),
	CONSTRAINT lender FOREIGN KEY (Owner_ID) REFERENCES USER_sp(id),
	CONSTRAINT place FOREIGN KEY (Place_ID) REFERENCES PARKING_PLACE(Place_id)
);

CREATE TABLE VALET (
	Valet_ID number PRIMARY KEY,
	Sdate varchar2(20),
	Edate varchar2(20),
	User_ID varchar2(10),
	parker_ID varchar2(10),
	pickup varchar2(20),
	Place_ID number,
	fee number,
	status_now number,
	CONSTRAINT borrower FOREIGN KEY (User_ID) REFERENCES USER_sp(id),
	CONSTRAINT borrower FOREIGN KEY (Parker_ID) REFERENCES USER_sp(id),
	CONSTRAINT place FOREIGN KEY (Place_ID) REFERENCES PARKING_PLACE(Place_id)
);

INSERT INTO USER_sp VALUES ('admin', 0,'admin','admin','0000','23','M',0);
INSERT INTO USER_sp VALUES ('1', 0,'1234','1234','01023432344','22','M',0);
INSERT INTO USER_sp VALUES ('2', 0,'kim','kim','01023432343','23','F',0);
INSERT INTO USER_sp VALUES ('3', 0,'dd1234','1234','01034568876','23','M',0);

INSERT INTO PARKING_PLACE VALUES (0, 'kim','Kyungpook National University',4000);
INSERT INTO PARKING_PLACE VALUES (1, 'kim','Dong Daegu station',5000);
