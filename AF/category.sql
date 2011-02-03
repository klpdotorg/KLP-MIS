BEGIN TRANSACTION;
CREATE TABLE "schools_school_category" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL
);
INSERT INTO "schools_school_category" VALUES(1,'lps');
INSERT INTO "schools_school_category" VALUES(2,'lps and hps');
INSERT INTO "schools_school_category" VALUES(3,'lps, hps and hs');
INSERT INTO "schools_school_category" VALUES(4,'hps');
INSERT INTO "schools_school_category" VALUES(5,'hps and hs');
INSERT INTO "schools_school_category" VALUES(6,'hs');
INSERT INTO "schools_school_category" VALUES(7,'hs and puc');
INSERT INTO "schools_school_category" VALUES(8,'special');
INSERT INTO "schools_school_category" VALUES(9,'chs');
INSERT INTO "schools_school_category" VALUES(10,'chps and chs');
INSERT INTO "schools_school_category" VALUES(11,'new');
COMMIT;
