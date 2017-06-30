DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Systems;
DROP TABLE IF EXISTS Clients;
DROP TABLE IF EXISTS Areas;
DROP TABLE IF EXISTS Features;

CREATE TABLE Users(
	username VARCHAR(30) UNIQUE NOT NULL,
	password TEXT,
	auth BIT,
	PRIMARY KEY(username)
);
	
CREATE TABLE Systems(
	sys_id VARCHAR(120) UNIQUE NOT NULL,
	disc TEXT,
	num_feat SMALLINT,
	status VARCHAR(30),
	PRIMARY KEY (sys_id)
);
	
CREATE TABLE Clients(
	client_name VARCHAR(30) NOT NULL,
	sys_id VARCHAR(120) NOT NULL,
	PRIMARY KEY (client_name, sys_id),
	FOREIGN KEY (sys_id) REFERENCES Systems(sys_id)
);

CREATE TABLE Areas(
	product_area VARCHAR(120) NOT NULL,
	sys_id VARCHAR(120) NOT NULL,
	PRIMARY KEY (product_area, sys_id),
	FOREIGN KEY (sys_id) REFERENCES Systems(sys_id)
);

CREATE TABLE Features(
	sys_id VARCHAR(120) NOT NULL,
	feat_title VARCHAR(120) NOT NULL,
	feat_disc TEXT,
	feat_date VARCHAR(10),
	client_name VARCHAR(30) NOT NULL,
	feat_priority SMALLINT,
	PRIMARY KEY (sys_id, feat_title),
	FOREIGN KEY (sys_id) REFERENCES Systems(sys_id),
	FOREIGN KEY (client_name) REFERENCES Clients(client_name)
);