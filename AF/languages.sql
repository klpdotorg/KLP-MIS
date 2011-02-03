BEGIN TRANSACTION;
CREATE TABLE "schools_moi_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL
);
INSERT INTO "schools_moi_type" VALUES(1,'kannada');
INSERT INTO "schools_moi_type" VALUES(2,'urdu');
INSERT INTO "schools_moi_type" VALUES(3,'tamil');
INSERT INTO "schools_moi_type" VALUES(4,'telugu');
INSERT INTO "schools_moi_type" VALUES(5,'english');
INSERT INTO "schools_moi_type" VALUES(6,'marathi');
INSERT INTO "schools_moi_type" VALUES(7,'malayalam');
INSERT INTO "schools_moi_type" VALUES(8,'hindi');
INSERT INTO "schools_moi_type" VALUES(9,'konkani');
INSERT INTO "schools_moi_type" VALUES(10,'sanskrit');
INSERT INTO "schools_moi_type" VALUES(11,'sindhi');
INSERT INTO "schools_moi_type" VALUES(12,'other');
INSERT INTO "schools_moi_type" VALUES(13,'gujarathi');
INSERT INTO "schools_moi_type" VALUES(14,'not known');
INSERT INTO "schools_moi_type" VALUES(15,'multi lng');
INSERT INTO "schools_moi_type" VALUES(16,'nepali');
INSERT INTO "schools_moi_type" VALUES(17,'oriya');
INSERT INTO "schools_moi_type" VALUES(18,'bengali');
INSERT INTO "schools_moi_type" VALUES(19,'jp');
COMMIT;
