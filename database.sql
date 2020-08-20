CREATE TABLE "pet" (
  "id" SERIAL PRIMARY KEY,
  "name"  VARCHAR(50),
  "breed" VARCHAR(30),
  "color" VARCHAR(20),
  "checkedIn" BOOLEAN DEFAULT FALSE
);

INSERT INTO "pet" ("name", "breed", "color", "checkedIn")
VALUES 
('Charlie', 'Shit-tzu', 'Black', FALSE),
('Thorin', 'Rabbit', 'White', FALSE),
('Gatsby', 'Cat', 'White', TRUE),
('Juniper', 'Cat', 'Tabby', FALSE);


CREATE TABLE "pet_owner" (
  "id" SERIAL PRIMARY KEY,
  "pet_id" INT,
  "owner_id" INT REFERENCES "owner"
);


INSERT INTO "owner" ("name")
VALUES 
('Chris'),
('Ally'),
('Dane');

CREATE TABLE "owner" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(100),
    "deleted" BOOLEAN DEFAULT FALSE
);