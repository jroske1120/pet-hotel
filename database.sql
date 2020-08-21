CREATE TABLE "pet" (
  "id" SERIAL PRIMARY KEY,
  "pets_name"  VARCHAR(50),
  "breed" VARCHAR(30),
  "color" VARCHAR(20),
  "checkedIn" BOOLEAN DEFAULT FALSE,
  "owner_id" INT
);

INSERT INTO "pet" ("pets_name", "breed", "color", "owner_id")
VALUES
('Charlie', 'Shit-tzu', 'Black', 1),
('Thorin', 'Rabbit', 'White', 2),
('Gatsby', 'Cat', 'White', 3),
('Juniper', 'Cat', 'Tabby', 3);

CREATE TABLE "owner" (
  "id" SERIAL PRIMARY KEY,
  "owners_name" VARCHAR(100),
  "deleted" BOOLEAN DEFAULT FALSE
);

INSERT INTO "owner" ("owners_name")
VALUES
('Chris'),
('Ally'),
('Dane');
