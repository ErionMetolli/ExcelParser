CREATE TABLE cities
(
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL
);
CREATE TABLE contractors
(
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(200),
    cityid INTEGER,
    islocal BOOLEAN,
    CONSTRAINT table_name_cities_id_fk FOREIGN KEY (cityid) REFERENCES cities (id)
);
CREATE UNIQUE INDEX table_name_int_uindex ON contractors (id);
CREATE TABLE projects
(
    id INTEGER PRIMARY KEY NOT NULL,
    name VARCHAR(200),
    date DATE,
    city VARCHAR(20),
    year INTEGER,
    estimatedcost DOUBLE PRECISION,
    finalcost DOUBLE PRECISION,
    annexcost DOUBLE PRECISION,
    contractorid INTEGER,
    CONSTRAINT projects_contractors_id_fk FOREIGN KEY (contractorid) REFERENCES contractors (id)
);
CREATE UNIQUE INDEX projects_id_uindex ON projects (id);