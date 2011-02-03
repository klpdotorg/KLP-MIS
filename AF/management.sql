BEGIN TRANSACTION;
CREATE TABLE "schools_school_management" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL
);
INSERT INTO "schools_school_management" VALUES(1,'ed');
INSERT INTO "schools_school_management" VALUES(2,'swd');
INSERT INTO "schools_school_management" VALUES(3,'local');
INSERT INTO "schools_school_management" VALUES(4,'p-a');
INSERT INTO "schools_school_management" VALUES(5,'p-ua');
INSERT INTO "schools_school_management" VALUES(6,'others');
INSERT INTO "schools_school_management" VALUES(7,'approved');
INSERT INTO "schools_school_management" VALUES(8,'ssa');
INSERT INTO "schools_school_management" VALUES(9,'kgbv');
INSERT INTO "schools_school_management" VALUES(10,'p-a-sc');
INSERT INTO "schools_school_management" VALUES(11,'p-a-st');
INSERT INTO "schools_school_management" VALUES(12,'jawahar');
INSERT INTO "schools_school_management" VALUES(13,'central');
INSERT INTO "schools_school_management" VALUES(14,'sainik');
INSERT INTO "schools_school_management" VALUES(15,'central govt');
INSERT INTO "schools_school_management" VALUES(16,'nri');
INSERT INTO "schools_school_management" VALUES(17,'madrasa-a');
INSERT INTO "schools_school_management" VALUES(18,'madrasa-ua');
INSERT INTO "schools_school_management" VALUES(19,'arabic-a');
INSERT INTO "schools_school_management" VALUES(20,'arabic-ua');
INSERT INTO "schools_school_management" VALUES(21,'sanskrit-a');
INSERT INTO "schools_school_management" VALUES(22,'sanskrit-ua');
INSERT INTO "schools_school_management" VALUES(23,'p-ua-sc');
INSERT INTO "schools_school_management" VALUES(24,'p-ua-st');
INSERT INTO "schools_school_management" VALUES(25,'mgm');
COMMIT;
