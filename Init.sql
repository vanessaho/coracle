# Master list of of all the SQL statements that we call to intialize the database.
# We will leave the dynamic SQL calls in the other code files. No need to include them here.

CREATE TABLE Accounts (
	Username CHAR(50),
	Password CHAR(70) NOT NULL,
	Email CHAR(60) NOT NULL UNIQUE,
	PRIMARY KEY (Username),
	CHECK (LEN(Password) > 6)
);

CREATE TABLE Locations (
	LocationId INT,
	CityName CHAR(50),
	Country CHAR(30) NOT NULL,
  	State CHAR(20),
	PRIMARY KEY(LocationId),
	CHECK (LocationId > 0)
);

CREATE TABLE Reviews (
	ReviewId INT,
	Rating INT NOT NULL,
	AttractionId INT NOT NULL,
	ReviewText VARCHAR(15000) NOT NULL,
	PostDate Date NOT NULL,
	PRIMARY KEY (ReviewId),
	CHECK (ReviewId > 0)
);


CREATE TABLE WritesReview (
	ReviewId INT,
  	Username CHAR(50),
  	PRIMARY KEY (ReviewId, Username),
  	FOREIGN KEY (ReviewId) REFERENCES Reviews(ReviewId),
  	FOREIGN KEY (Username) REFERENCES Accounts(Username)
);


CREATE TABLE Trips (
	TripId INT,
  	Username CHAR(50),
  	FromLocationId INT,
  	ToLocationId INT,
  	StartDate DATE,
  	EndDate DATE,
  	TransportationId INT,
  	AccommodationId INT,
  	PaymentId INT,
  	NumPeople INT,
  	PRIMARY KEY (TripId),
	FOREIGN KEY (Username) REFERENCES Accounts(Username),
    FOREIGN KEY (FromLocationId) REFERENCES Locations(LocationId),
  	FOREIGN KEY (ToLocationId) REFERENCES Locations(LocationId),
    FOREIGN KEY (TransportationId) REFERENCES Transportation(TransportationId),
    FOREIGN KEY (AccommodationId) REFERENCES Accommodation(AccommodationId),
  	FOREIGN KEY (PaymentId) REFERENCES Payment(PaymentId),
  	CHECK (NumPeople > 0)
);

CREATE TABLE TripAttractions(
  	TripId INT,
  	AttractionId INT,
  	PRIMARY KEY (TripId, AttractionId),
  	FOREIGN KEY (TripId) REFERENCES Trips(TripId),
  	FOREIGN KEY (AttractionId) REFERENCES Attractions(AttractionId)
);

CREATE TABLE Attractions (
  	AttractionId INT,
	Name CHAR(100),
	LocationId INT,
	Description VARCHAR(2500),
	PRIMARY KEY (AttractionId),
  	FOREIGN KEY (LocationId) REFERENCES Locations (LocationId),
	CHECK (Cost >= 0)
);

CREATE TABLE Accommodation (
	AccommodationId INT,
	AccommodationType CHAR(10) NOT NULL,
	RatePerNight DECIMAL(20, 2) NOT NULL,
	Facilities CHAR(50),
	PRIMARY KEY (AccommodationId),
	CHECK (AccommodationType='Hotel' OR AccommodationType='Airbnb'),
	CHECK (AccommodationId > 0),
	CHECK (RatePerNight >= 0)
);

CREATE TABLE Payment (
  	PaymentId INT AUTO_INCREMENT,
	CardNumber INT,
	CardSecurityCode INT,
	Amount DECIMAL(20, 2) NOT NULL,
	ExpirationDate Date,
	PaymentDate DATETIME NOT NULL,
	CardName CHAR(60),
	PRIMARY KEY (PaymentId),
	CHECK (CardNumber > 0 AND CardSecruityCode > 0),
	CHECK (Amount >= 0)
);

CREATE TABLE Transportation(
	TransportationId INTEGER,
    TransportationType CHAR(15),
    Cost DECIMAL(20, 2) NOT NULL,
	BeginTime CHAR(10),
	EndTime CHAR(10),
    PRIMARY KEY(TransportationId),
    CHECK(TransportationType = 'Train' OR TransportationType = 'Flight' OR TransportationType = 'Car' OR TransportationType = 'Cruise')
);

# Run cities and attractions script

INSERT INTO Transportation VALUES (1, 'Flight', 300);
INSERT INTO Transportation VALUES (2, 'Cruise', 150);
INSERT INTO Transportation VALUES (3, 'Train', 100);
INSERT INTO Transportation VALUES (4, 'Car', 80);

INSERT INTO Accommodation VALUES (1, 'Hotel', 150, 'Free wifi, Free breakfast, TV, Swimming Pool');
INSERT INTO Accommodation VALUES (2, 'Airbnb', 75, 'Free wifi, TV');


# For dropping tables to test:

DROP TABLE TripAttractions;
DROP TABLE Trips;
DROP TABLE Attractions;
DROP TABLE Locations;