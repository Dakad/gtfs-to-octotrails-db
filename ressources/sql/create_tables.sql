
CREATE TABLE feedversions (
	id VARCHAR(100) NOT NULL, 
	size INTEGER, 
	registred_date TIMESTAMP, 
	start_date VARCHAR(10), 
	finish_date VARCHAR(10), 
	download_url VARCHAR(250), 
	PRIMARY KEY (id), 
	UNIQUE (download_url)
)

CREATE TABLE lines (
	"number" VARCHAR(10) NOT NULL, 
	description VARCHAR(100), 
	"from" VARCHAR(100), 
	"to" VARCHAR(100), 
	route_color VARCHAR(10), 
	route_text_color VARCHAR(10), 
	"type" VARCHAR(5), 
	PRIMARY KEY (number), 
	CONSTRAINT linetype CHECK (type IN ('Tram', 'Metro', 'TBus', 'Bus'))
)

CREATE TABLE stops (
	feed_id VARCHAR(10) NOT NULL, 
	tech_id VARCHAR(10), 
	description_fr VARCHAR(100), 
	description_nl VARCHAR(100), 
	PRIMARY KEY (feed_id)
)

CREATE TABLE lines_stops (
	line_number VARCHAR, 
	stop_feed_id VARCHAR, 
	FOREIGN KEY(line_number) REFERENCES lines (number), 
	FOREIGN KEY(stop_feed_id) REFERENCES stops (feed_id)
)

CREATE TABLE localisations (
	stop_id VARCHAR NOT NULL, 
	longitude FLOAT, 
	latitude FLOAT, 
	address_fr VARCHAR(250), 
	address_nl VARCHAR(250), 
	PRIMARY KEY (stop_id), 
	FOREIGN KEY(stop_id) REFERENCES stops (feed_id)
)

