BEGIN TRANSACTION;
CREATE TABLE "auth_permission" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
);
INSERT INTO "auth_permission" VALUES(1,'Can add permission',1,'add_permission');
INSERT INTO "auth_permission" VALUES(2,'Can change permission',1,'change_permission');
INSERT INTO "auth_permission" VALUES(3,'Can delete permission',1,'delete_permission');
INSERT INTO "auth_permission" VALUES(4,'Can add group',2,'add_group');
INSERT INTO "auth_permission" VALUES(5,'Can change group',2,'change_group');
INSERT INTO "auth_permission" VALUES(6,'Can delete group',2,'delete_group');
INSERT INTO "auth_permission" VALUES(7,'Can add user',3,'add_user');
INSERT INTO "auth_permission" VALUES(8,'Can change user',3,'change_user');
INSERT INTO "auth_permission" VALUES(9,'Can delete user',3,'delete_user');
INSERT INTO "auth_permission" VALUES(10,'Can add message',4,'add_message');
INSERT INTO "auth_permission" VALUES(11,'Can change message',4,'change_message');
INSERT INTO "auth_permission" VALUES(12,'Can delete message',4,'delete_message');
INSERT INTO "auth_permission" VALUES(13,'Can add content type',5,'add_contenttype');
INSERT INTO "auth_permission" VALUES(14,'Can change content type',5,'change_contenttype');
INSERT INTO "auth_permission" VALUES(15,'Can delete content type',5,'delete_contenttype');
INSERT INTO "auth_permission" VALUES(16,'Can add session',6,'add_session');
INSERT INTO "auth_permission" VALUES(17,'Can change session',6,'change_session');
INSERT INTO "auth_permission" VALUES(18,'Can delete session',6,'delete_session');
INSERT INTO "auth_permission" VALUES(19,'Can add site',7,'add_site');
INSERT INTO "auth_permission" VALUES(20,'Can change site',7,'change_site');
INSERT INTO "auth_permission" VALUES(21,'Can delete site',7,'delete_site');
INSERT INTO "auth_permission" VALUES(22,'Can add log entry',8,'add_logentry');
INSERT INTO "auth_permission" VALUES(23,'Can change log entry',8,'change_logentry');
INSERT INTO "auth_permission" VALUES(24,'Can delete log entry',8,'delete_logentry');
INSERT INTO "auth_permission" VALUES(25,'Can add boundary',9,'add_boundary');
INSERT INTO "auth_permission" VALUES(26,'Can change boundary',9,'change_boundary');
INSERT INTO "auth_permission" VALUES(27,'Can delete boundary',9,'delete_boundary');
INSERT INTO "auth_permission" VALUES(31,'Can add school',11,'add_school');
INSERT INTO "auth_permission" VALUES(32,'Can change school',11,'change_school');
INSERT INTO "auth_permission" VALUES(33,'Can delete school',11,'delete_school');
INSERT INTO "auth_permission" VALUES(34,'Can add child',12,'add_child');
INSERT INTO "auth_permission" VALUES(35,'Can change child',12,'change_child');
INSERT INTO "auth_permission" VALUES(36,'Can delete child',12,'delete_child');
INSERT INTO "auth_permission" VALUES(40,'Can add academic_ year',14,'add_academic_year');
INSERT INTO "auth_permission" VALUES(41,'Can change academic_ year',14,'change_academic_year');
INSERT INTO "auth_permission" VALUES(42,'Can delete academic_ year',14,'delete_academic_year');
INSERT INTO "auth_permission" VALUES(43,'Can add student',15,'add_student');
INSERT INTO "auth_permission" VALUES(44,'Can change student',15,'change_student');
INSERT INTO "auth_permission" VALUES(45,'Can delete student',15,'delete_student');
INSERT INTO "auth_permission" VALUES(46,'Can add school_ category',16,'add_school_category');
INSERT INTO "auth_permission" VALUES(47,'Can change school_ category',16,'change_school_category');
INSERT INTO "auth_permission" VALUES(48,'Can delete school_ category',16,'delete_school_category');
INSERT INTO "auth_permission" VALUES(49,'Can add moi_ type',17,'add_moi_type');
INSERT INTO "auth_permission" VALUES(50,'Can change moi_ type',17,'change_moi_type');
INSERT INTO "auth_permission" VALUES(51,'Can delete moi_ type',17,'delete_moi_type');
INSERT INTO "auth_permission" VALUES(52,'Can add school_ management',18,'add_school_management');
INSERT INTO "auth_permission" VALUES(53,'Can change school_ management',18,'change_school_management');
INSERT INTO "auth_permission" VALUES(54,'Can delete school_ management',18,'delete_school_management');
INSERT INTO "auth_permission" VALUES(55,'Can add boundary_ type',19,'add_boundary_type');
INSERT INTO "auth_permission" VALUES(56,'Can change boundary_ type',19,'change_boundary_type');
INSERT INTO "auth_permission" VALUES(57,'Can delete boundary_ type',19,'delete_boundary_type');
INSERT INTO "auth_permission" VALUES(64,'Can add assessment',22,'add_assessment');
INSERT INTO "auth_permission" VALUES(65,'Can change assessment',22,'change_assessment');
INSERT INTO "auth_permission" VALUES(66,'Can delete assessment',22,'delete_assessment');
INSERT INTO "auth_permission" VALUES(67,'Can add question',23,'add_question');
INSERT INTO "auth_permission" VALUES(68,'Can change question',23,'change_question');
INSERT INTO "auth_permission" VALUES(69,'Can delete question',23,'delete_question');
INSERT INTO "auth_permission" VALUES(76,'Can add answer',26,'add_answer');
INSERT INTO "auth_permission" VALUES(77,'Can change answer',26,'change_answer');
INSERT INTO "auth_permission" VALUES(78,'Can delete answer',26,'delete_answer');
INSERT INTO "auth_permission" VALUES(88,'Can add relations',30,'add_relations');
INSERT INTO "auth_permission" VALUES(89,'Can change relations',30,'change_relations');
INSERT INTO "auth_permission" VALUES(90,'Can delete relations',30,'delete_relations');
INSERT INTO "auth_permission" VALUES(91,'Can add student group',31,'add_studentgroup');
INSERT INTO "auth_permission" VALUES(92,'Can change student group',31,'change_studentgroup');
INSERT INTO "auth_permission" VALUES(93,'Can delete student group',31,'delete_studentgroup');
INSERT INTO "auth_permission" VALUES(94,'Can add boundary_ category',32,'add_boundary_category');
INSERT INTO "auth_permission" VALUES(95,'Can change boundary_ category',32,'change_boundary_category');
INSERT INTO "auth_permission" VALUES(96,'Can delete boundary_ category',32,'delete_boundary_category');
INSERT INTO "auth_permission" VALUES(100,'Can add programme',34,'add_programme');
INSERT INTO "auth_permission" VALUES(101,'Can change programme',34,'change_programme');
INSERT INTO "auth_permission" VALUES(102,'Can delete programme',34,'delete_programme');
INSERT INTO "auth_permission" VALUES(103,'Can add programme_ school_ category',35,'add_programme_school_category');
INSERT INTO "auth_permission" VALUES(104,'Can change programme_ school_ category',35,'change_programme_school_category');
INSERT INTO "auth_permission" VALUES(105,'Can delete programme_ school_ category',35,'delete_programme_school_category');
CREATE TABLE "auth_group_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("group_id", "permission_id")
);
CREATE TABLE "auth_group" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
);
CREATE TABLE "auth_user_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("user_id", "permission_id")
);
CREATE TABLE "auth_user_groups" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    UNIQUE ("user_id", "group_id")
);
CREATE TABLE "auth_user" (
    "id" integer NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "is_superuser" bool NOT NULL,
    "last_login" datetime NOT NULL,
    "date_joined" datetime NOT NULL
);
INSERT INTO "auth_user" VALUES(1,'akshara','','','charantej.s@mahiti.org','sha1$63cf3$8f956e8a14f8cc00e90ddbaa7b8e8d78cd816c10',1,1,1,'2010-12-03 18:34:00.711834','2010-08-25 08:26:10.645669');
CREATE TABLE "auth_message" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "message" text NOT NULL
);
CREATE TABLE "django_content_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
);
INSERT INTO "django_content_type" VALUES(1,'permission','auth','permission');
INSERT INTO "django_content_type" VALUES(2,'group','auth','group');
INSERT INTO "django_content_type" VALUES(3,'user','auth','user');
INSERT INTO "django_content_type" VALUES(4,'message','auth','message');
INSERT INTO "django_content_type" VALUES(5,'content type','contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES(6,'session','sessions','session');
INSERT INTO "django_content_type" VALUES(7,'site','sites','site');
INSERT INTO "django_content_type" VALUES(8,'log entry','admin','logentry');
INSERT INTO "django_content_type" VALUES(9,'boundary','schools','boundary');
INSERT INTO "django_content_type" VALUES(11,'school','schools','school');
INSERT INTO "django_content_type" VALUES(12,'child','schools','child');
INSERT INTO "django_content_type" VALUES(14,'academic_ year','schools','academic_year');
INSERT INTO "django_content_type" VALUES(15,'student','schools','student');
INSERT INTO "django_content_type" VALUES(16,'school_ category','schools','school_category');
INSERT INTO "django_content_type" VALUES(17,'moi_ type','schools','moi_type');
INSERT INTO "django_content_type" VALUES(18,'school_ management','schools','school_management');
INSERT INTO "django_content_type" VALUES(19,'boundary_ type','schools','boundary_type');
INSERT INTO "django_content_type" VALUES(22,'assessment','schools','assessment');
INSERT INTO "django_content_type" VALUES(23,'question','schools','question');
INSERT INTO "django_content_type" VALUES(26,'answer','schools','answer');
INSERT INTO "django_content_type" VALUES(30,'relations','schools','relations');
INSERT INTO "django_content_type" VALUES(31,'student group','schools','studentgroup');
INSERT INTO "django_content_type" VALUES(32,'boundary_ category','schools','boundary_category');
INSERT INTO "django_content_type" VALUES(34,'programme','schools','programme');
INSERT INTO "django_content_type" VALUES(35,'programme_ school_ category','schools','programme_school_category');
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" datetime NOT NULL
);
INSERT INTO "django_session" VALUES('84a174c73caf0b16a7edc5fddf692362','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LmJkOTc5Y2E5ZjdmOTVkMzQzMDQ0
Y2I3YjEyNGE3MTE4
','2010-09-08 08:27:13.583045');
INSERT INTO "django_session" VALUES('3179a33448b42fe61ffee42976c5e2ec','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LmJkOTc5Y2E5ZjdmOTVkMzQzMDQ0
Y2I3YjEyNGE3MTE4
','2010-09-16 06:10:34.543917');
INSERT INTO "django_session" VALUES('7dc653f913be45a1f9a79ec52cf834b8','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-10-07 03:34:43.186270');
INSERT INTO "django_session" VALUES('f601cf82c720e822716717873cb93b46','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-10-08 07:14:54.510692');
INSERT INTO "django_session" VALUES('9bffc76240ad643fd733d52353469c57','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-10-21 11:11:56.361627');
INSERT INTO "django_session" VALUES('95b5c0912872f96a91fd9b070c6cf506','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-11-08 01:24:07.292794');
INSERT INTO "django_session" VALUES('a8f6d66760664d56c602b83afec1c626','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-11-23 06:20:43.525537');
INSERT INTO "django_session" VALUES('61c6266499c2a389ff9efc503dcc791a','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-11-25 04:12:52.170511');
INSERT INTO "django_session" VALUES('0de57579785b1bb562086e5a01fb136d','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-11-26 07:02:31.899449');
INSERT INTO "django_session" VALUES('e8d22bdba949abacc9b170956491ac85','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-12-02 07:12:44.941491');
INSERT INTO "django_session" VALUES('b0048914ed8b2fde88fd0b195a71faf6','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-12-03 01:32:51.765594');
INSERT INTO "django_session" VALUES('b266f9f070e5c92e741856541fcba199','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-12-09 06:23:51.240701');
INSERT INTO "django_session" VALUES('7860455a1e88960ac50e2e12592e1599','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-12-15 15:44:45.671999');
INSERT INTO "django_session" VALUES('d434c92f22e7abc54b8399b31acbf5eb','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-12-16 10:40:02.960427');
INSERT INTO "django_session" VALUES('3b141d0200a4508ff69d985546e81b83','gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k
cy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LmJkOTc5Y2E5ZjdmOTVkMzQzMDQ0
Y2I3YjEyNGE3MTE4
','2010-12-17 18:34:01.046317');
INSERT INTO "django_session" VALUES('a9a66ce66a48d661abea778569aafe29','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-12-20 12:16:53.928189');
INSERT INTO "django_session" VALUES('22ce2b49a18cd35d7cba7569c8200f1b','gAJ9cQEuOGFiODVmZjIwNThhMTg3NzI1YzA5M2E3Yzg5NmFjNjc=
','2010-12-20 12:59:35.600913');
INSERT INTO "django_session" VALUES('4d6aed3d12f8c3ba34dde1a8171f52dd','gAJ9cQFVD3Nlc3Npb25fc2NoX3R5cHECWAEAAAAxcy41Njg5Yjk1ZWNkNWE1NGVhMDJkZjAzMmY1
MGNjOWExMQ==
','2010-12-20 06:33:51.984352');
INSERT INTO "django_session" VALUES('9e09affde03f566654cfb3fcd5b30ab7','gAJ9cQFVD3Nlc3Npb25fc2NoX3R5cHECWAEAAAAycy5mYmFjNzA3MDNjYjk3ZDMxYzQ1OGMxNDgw
Y2I1NDhlMg==
','2010-12-20 23:07:08.084660');
CREATE TABLE "django_site" (
    "id" integer NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
);
INSERT INTO "django_site" VALUES(1,'example.com','example.com');
CREATE TABLE "django_admin_log" (
    "id" integer NOT NULL PRIMARY KEY,
    "action_time" datetime NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "content_type_id" integer REFERENCES "django_content_type" ("id"),
    "object_id" text,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint unsigned NOT NULL,
    "change_message" text NOT NULL
);
CREATE TABLE "schools_school_category" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL
, categoryType int);
INSERT INTO "schools_school_category" VALUES(1,'lps',0);
INSERT INTO "schools_school_category" VALUES(2,'lps and hps',0);
INSERT INTO "schools_school_category" VALUES(3,'lps, hps and hs',0);
INSERT INTO "schools_school_category" VALUES(4,'hps',0);
INSERT INTO "schools_school_category" VALUES(5,'hps and hs',0);
INSERT INTO "schools_school_category" VALUES(6,'hs',0);
INSERT INTO "schools_school_category" VALUES(7,'hs and puc',0);
INSERT INTO "schools_school_category" VALUES(8,'special',0);
INSERT INTO "schools_school_category" VALUES(9,'chs',0);
INSERT INTO "schools_school_category" VALUES(10,'chps and chs',0);
INSERT INTO "schools_school_category" VALUES(11,'anganwadiType',1);
INSERT INTO "schools_school_category" VALUES(12,'anganwadi New',1);
INSERT INTO "schools_school_category" VALUES(13,'Ang Typ',1);
INSERT INTO "schools_school_category" VALUES(14,'sch typ',0);
INSERT INTO "schools_school_category" VALUES(15,'new sch typ',0);
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
CREATE TABLE "schools_school_languages" (
    "id" integer NOT NULL PRIMARY KEY,
    "school_id" integer NOT NULL,
    "moi_type_id" integer NOT NULL REFERENCES "schools_moi_type" ("id"),
    UNIQUE ("school_id", "moi_type_id")
);
INSERT INTO "schools_school_languages" VALUES(163,3,1);
INSERT INTO "schools_school_languages" VALUES(164,3,2);
INSERT INTO "schools_school_languages" VALUES(165,3,3);
INSERT INTO "schools_school_languages" VALUES(166,3,4);
INSERT INTO "schools_school_languages" VALUES(167,3,5);
INSERT INTO "schools_school_languages" VALUES(177,7,1);
INSERT INTO "schools_school_languages" VALUES(178,7,2);
INSERT INTO "schools_school_languages" VALUES(179,7,3);
INSERT INTO "schools_school_languages" VALUES(180,8,1);
INSERT INTO "schools_school_languages" VALUES(181,8,2);
INSERT INTO "schools_school_languages" VALUES(182,9,1);
INSERT INTO "schools_school_languages" VALUES(183,9,2);
INSERT INTO "schools_school_languages" VALUES(184,9,3);
INSERT INTO "schools_school_languages" VALUES(185,9,4);
INSERT INTO "schools_school_languages" VALUES(186,10,1);
INSERT INTO "schools_school_languages" VALUES(187,10,2);
INSERT INTO "schools_school_languages" VALUES(188,10,3);
INSERT INTO "schools_school_languages" VALUES(189,10,4);
INSERT INTO "schools_school_languages" VALUES(190,11,1);
INSERT INTO "schools_school_languages" VALUES(191,11,2);
INSERT INTO "schools_school_languages" VALUES(192,11,3);
INSERT INTO "schools_school_languages" VALUES(193,11,4);
INSERT INTO "schools_school_languages" VALUES(194,12,1);
INSERT INTO "schools_school_languages" VALUES(195,12,2);
INSERT INTO "schools_school_languages" VALUES(196,12,4);
INSERT INTO "schools_school_languages" VALUES(197,13,1);
INSERT INTO "schools_school_languages" VALUES(198,13,2);
INSERT INTO "schools_school_languages" VALUES(199,13,3);
INSERT INTO "schools_school_languages" VALUES(200,14,1);
INSERT INTO "schools_school_languages" VALUES(201,14,2);
INSERT INTO "schools_school_languages" VALUES(202,14,3);
INSERT INTO "schools_school_languages" VALUES(203,14,4);
INSERT INTO "schools_school_languages" VALUES(204,15,1);
INSERT INTO "schools_school_languages" VALUES(205,15,2);
INSERT INTO "schools_school_languages" VALUES(206,16,2);
INSERT INTO "schools_school_languages" VALUES(207,16,4);
INSERT INTO "schools_school_languages" VALUES(208,17,1);
INSERT INTO "schools_school_languages" VALUES(209,17,3);
INSERT INTO "schools_school_languages" VALUES(210,18,1);
INSERT INTO "schools_school_languages" VALUES(211,18,3);
INSERT INTO "schools_school_languages" VALUES(212,18,4);
INSERT INTO "schools_school_languages" VALUES(213,18,6);
INSERT INTO "schools_school_languages" VALUES(214,19,1);
INSERT INTO "schools_school_languages" VALUES(215,19,2);
INSERT INTO "schools_school_languages" VALUES(216,19,4);
INSERT INTO "schools_school_languages" VALUES(217,20,1);
INSERT INTO "schools_school_languages" VALUES(218,20,2);
INSERT INTO "schools_school_languages" VALUES(219,20,3);
INSERT INTO "schools_school_languages" VALUES(220,21,1);
INSERT INTO "schools_school_languages" VALUES(221,21,3);
INSERT INTO "schools_school_languages" VALUES(222,21,4);
INSERT INTO "schools_school_languages" VALUES(223,22,1);
INSERT INTO "schools_school_languages" VALUES(224,22,2);
INSERT INTO "schools_school_languages" VALUES(225,22,3);
INSERT INTO "schools_school_languages" VALUES(226,22,4);
INSERT INTO "schools_school_languages" VALUES(227,23,1);
INSERT INTO "schools_school_languages" VALUES(228,23,2);
INSERT INTO "schools_school_languages" VALUES(229,23,3);
INSERT INTO "schools_school_languages" VALUES(230,23,4);
INSERT INTO "schools_school_languages" VALUES(231,24,1);
INSERT INTO "schools_school_languages" VALUES(232,24,2);
INSERT INTO "schools_school_languages" VALUES(233,24,3);
INSERT INTO "schools_school_languages" VALUES(234,24,4);
INSERT INTO "schools_school_languages" VALUES(235,25,1);
INSERT INTO "schools_school_languages" VALUES(236,25,2);
INSERT INTO "schools_school_languages" VALUES(237,25,3);
INSERT INTO "schools_school_languages" VALUES(238,26,1);
INSERT INTO "schools_school_languages" VALUES(239,26,2);
INSERT INTO "schools_school_languages" VALUES(240,26,3);
INSERT INTO "schools_school_languages" VALUES(241,26,4);
INSERT INTO "schools_school_languages" VALUES(242,27,1);
INSERT INTO "schools_school_languages" VALUES(243,27,2);
INSERT INTO "schools_school_languages" VALUES(244,27,3);
INSERT INTO "schools_school_languages" VALUES(245,27,4);
INSERT INTO "schools_school_languages" VALUES(246,28,1);
INSERT INTO "schools_school_languages" VALUES(247,28,2);
INSERT INTO "schools_school_languages" VALUES(248,28,3);
INSERT INTO "schools_school_languages" VALUES(249,28,4);
INSERT INTO "schools_school_languages" VALUES(250,29,1);
INSERT INTO "schools_school_languages" VALUES(251,29,2);
INSERT INTO "schools_school_languages" VALUES(252,30,1);
INSERT INTO "schools_school_languages" VALUES(253,30,2);
INSERT INTO "schools_school_languages" VALUES(254,30,3);
INSERT INTO "schools_school_languages" VALUES(255,30,4);
INSERT INTO "schools_school_languages" VALUES(256,31,1);
INSERT INTO "schools_school_languages" VALUES(257,31,2);
INSERT INTO "schools_school_languages" VALUES(258,31,3);
INSERT INTO "schools_school_languages" VALUES(259,31,4);
INSERT INTO "schools_school_languages" VALUES(260,32,1);
INSERT INTO "schools_school_languages" VALUES(261,32,2);
INSERT INTO "schools_school_languages" VALUES(262,32,3);
INSERT INTO "schools_school_languages" VALUES(263,32,4);
INSERT INTO "schools_school_languages" VALUES(264,33,1);
INSERT INTO "schools_school_languages" VALUES(265,34,1);
INSERT INTO "schools_school_languages" VALUES(266,34,2);
INSERT INTO "schools_school_languages" VALUES(267,34,3);
INSERT INTO "schools_school_languages" VALUES(268,34,4);
INSERT INTO "schools_school_languages" VALUES(269,35,1);
INSERT INTO "schools_school_languages" VALUES(270,35,2);
INSERT INTO "schools_school_languages" VALUES(271,35,3);
INSERT INTO "schools_school_languages" VALUES(272,35,4);
INSERT INTO "schools_school_languages" VALUES(273,36,1);
INSERT INTO "schools_school_languages" VALUES(274,36,2);
INSERT INTO "schools_school_languages" VALUES(275,36,3);
INSERT INTO "schools_school_languages" VALUES(276,36,4);
INSERT INTO "schools_school_languages" VALUES(281,37,1);
INSERT INTO "schools_school_languages" VALUES(282,37,3);
INSERT INTO "schools_school_languages" VALUES(283,6,1);
INSERT INTO "schools_school_languages" VALUES(284,6,2);
INSERT INTO "schools_school_languages" VALUES(285,38,1);
INSERT INTO "schools_school_languages" VALUES(286,38,2);
INSERT INTO "schools_school_languages" VALUES(287,38,4);
INSERT INTO "schools_school_languages" VALUES(288,38,5);
INSERT INTO "schools_school_languages" VALUES(289,39,1);
INSERT INTO "schools_school_languages" VALUES(290,39,2);
INSERT INTO "schools_school_languages" VALUES(291,39,3);
INSERT INTO "schools_school_languages" VALUES(292,40,1);
INSERT INTO "schools_school_languages" VALUES(293,40,2);
INSERT INTO "schools_school_languages" VALUES(294,40,3);
INSERT INTO "schools_school_languages" VALUES(295,40,4);
INSERT INTO "schools_school_languages" VALUES(296,41,1);
INSERT INTO "schools_school_languages" VALUES(297,41,3);
INSERT INTO "schools_school_languages" VALUES(298,41,5);
INSERT INTO "schools_school_languages" VALUES(299,42,1);
INSERT INTO "schools_school_languages" VALUES(300,42,2);
INSERT INTO "schools_school_languages" VALUES(301,42,3);
INSERT INTO "schools_school_languages" VALUES(302,42,4);
INSERT INTO "schools_school_languages" VALUES(303,43,1);
INSERT INTO "schools_school_languages" VALUES(304,43,2);
INSERT INTO "schools_school_languages" VALUES(305,43,3);
INSERT INTO "schools_school_languages" VALUES(306,43,4);
INSERT INTO "schools_school_languages" VALUES(307,44,1);
INSERT INTO "schools_school_languages" VALUES(308,44,2);
INSERT INTO "schools_school_languages" VALUES(309,44,3);
INSERT INTO "schools_school_languages" VALUES(310,44,4);
INSERT INTO "schools_school_languages" VALUES(311,45,1);
INSERT INTO "schools_school_languages" VALUES(312,45,2);
INSERT INTO "schools_school_languages" VALUES(313,45,3);
INSERT INTO "schools_school_languages" VALUES(314,45,4);
INSERT INTO "schools_school_languages" VALUES(315,46,1);
INSERT INTO "schools_school_languages" VALUES(316,46,2);
INSERT INTO "schools_school_languages" VALUES(317,46,3);
INSERT INTO "schools_school_languages" VALUES(318,46,4);
INSERT INTO "schools_school_languages" VALUES(319,47,3);
INSERT INTO "schools_school_languages" VALUES(320,47,4);
INSERT INTO "schools_school_languages" VALUES(321,47,5);
INSERT INTO "schools_school_languages" VALUES(322,47,6);
INSERT INTO "schools_school_languages" VALUES(323,47,7);
INSERT INTO "schools_school_languages" VALUES(324,48,1);
INSERT INTO "schools_school_languages" VALUES(325,48,2);
INSERT INTO "schools_school_languages" VALUES(326,48,4);
INSERT INTO "schools_school_languages" VALUES(327,49,1);
INSERT INTO "schools_school_languages" VALUES(328,49,2);
INSERT INTO "schools_school_languages" VALUES(329,49,3);
INSERT INTO "schools_school_languages" VALUES(330,49,4);
INSERT INTO "schools_school_languages" VALUES(331,49,5);
INSERT INTO "schools_school_languages" VALUES(332,49,6);
INSERT INTO "schools_school_languages" VALUES(333,49,7);
INSERT INTO "schools_school_languages" VALUES(334,50,1);
INSERT INTO "schools_school_languages" VALUES(335,50,2);
INSERT INTO "schools_school_languages" VALUES(336,50,3);
INSERT INTO "schools_school_languages" VALUES(337,50,4);
INSERT INTO "schools_school_languages" VALUES(338,51,1);
INSERT INTO "schools_school_languages" VALUES(339,51,2);
INSERT INTO "schools_school_languages" VALUES(340,51,3);
INSERT INTO "schools_school_languages" VALUES(341,51,4);
INSERT INTO "schools_school_languages" VALUES(342,52,1);
INSERT INTO "schools_school_languages" VALUES(343,52,2);
INSERT INTO "schools_school_languages" VALUES(344,52,3);
INSERT INTO "schools_school_languages" VALUES(345,52,4);
INSERT INTO "schools_school_languages" VALUES(346,53,1);
INSERT INTO "schools_school_languages" VALUES(347,53,2);
INSERT INTO "schools_school_languages" VALUES(348,53,3);
INSERT INTO "schools_school_languages" VALUES(349,53,4);
INSERT INTO "schools_school_languages" VALUES(350,54,1);
INSERT INTO "schools_school_languages" VALUES(351,54,2);
INSERT INTO "schools_school_languages" VALUES(352,54,3);
INSERT INTO "schools_school_languages" VALUES(353,54,4);
INSERT INTO "schools_school_languages" VALUES(354,55,1);
INSERT INTO "schools_school_languages" VALUES(355,55,2);
INSERT INTO "schools_school_languages" VALUES(356,55,3);
INSERT INTO "schools_school_languages" VALUES(357,55,4);
INSERT INTO "schools_school_languages" VALUES(358,56,1);
INSERT INTO "schools_school_languages" VALUES(359,56,2);
INSERT INTO "schools_school_languages" VALUES(360,56,3);
INSERT INTO "schools_school_languages" VALUES(361,57,1);
INSERT INTO "schools_school_languages" VALUES(362,57,2);
INSERT INTO "schools_school_languages" VALUES(363,57,3);
INSERT INTO "schools_school_languages" VALUES(364,57,4);
INSERT INTO "schools_school_languages" VALUES(365,58,1);
INSERT INTO "schools_school_languages" VALUES(366,58,2);
INSERT INTO "schools_school_languages" VALUES(367,58,3);
INSERT INTO "schools_school_languages" VALUES(368,58,4);
INSERT INTO "schools_school_languages" VALUES(369,59,1);
INSERT INTO "schools_school_languages" VALUES(370,59,2);
INSERT INTO "schools_school_languages" VALUES(371,4,1);
INSERT INTO "schools_school_languages" VALUES(372,4,2);
INSERT INTO "schools_school_languages" VALUES(373,4,3);
INSERT INTO "schools_school_languages" VALUES(374,4,4);
INSERT INTO "schools_school_languages" VALUES(379,5,1);
INSERT INTO "schools_school_languages" VALUES(380,5,2);
INSERT INTO "schools_school_languages" VALUES(381,5,3);
INSERT INTO "schools_school_languages" VALUES(382,1,1);
INSERT INTO "schools_school_languages" VALUES(383,1,2);
INSERT INTO "schools_school_languages" VALUES(384,1,3);
INSERT INTO "schools_school_languages" VALUES(385,2,1);
INSERT INTO "schools_school_languages" VALUES(386,2,2);
INSERT INTO "schools_school_languages" VALUES(387,2,3);
CREATE TABLE "schools_academic_year" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(20) NOT NULL UNIQUE
);
INSERT INTO "schools_academic_year" VALUES(1,'2008-2009');
INSERT INTO "schools_academic_year" VALUES(2,'2009-2010');
INSERT INTO "schools_academic_year" VALUES(3,'2010-2011');
INSERT INTO "schools_academic_year" VALUES(4,'2011-2012');
CREATE TABLE "schools_boundary_category" (
    "id" integer NOT NULL PRIMARY KEY,
    "boundary_category" varchar(100) NOT NULL
);
INSERT INTO "schools_boundary_category" VALUES(1,'District');
INSERT INTO "schools_boundary_category" VALUES(2,'Block');
INSERT INTO "schools_boundary_category" VALUES(3,'Project');
INSERT INTO "schools_boundary_category" VALUES(4,'Cluster');
INSERT INTO "schools_boundary_category" VALUES(5,'Circle');
CREATE TABLE "schools_boundary_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "boundary_type" varchar(100) NOT NULL
);
INSERT INTO "schools_boundary_type" VALUES(1,'Pre-School');
INSERT INTO "schools_boundary_type" VALUES(2,'Primary-School');
CREATE TABLE "schools_boundary_boundary_category" (
    "id" integer NOT NULL PRIMARY KEY,
    "boundary_id" integer NOT NULL,
    "boundary_category_id" integer NOT NULL REFERENCES "schools_boundary_category" ("id"),
    UNIQUE ("boundary_id", "boundary_category_id")
);
INSERT INTO "schools_boundary_boundary_category" VALUES(1,2,1);
INSERT INTO "schools_boundary_boundary_category" VALUES(2,3,2);
INSERT INTO "schools_boundary_boundary_category" VALUES(3,4,4);
INSERT INTO "schools_boundary_boundary_category" VALUES(4,5,3);
INSERT INTO "schools_boundary_boundary_category" VALUES(5,6,5);
CREATE TABLE "schools_boundary_boundary_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "boundary_id" integer NOT NULL,
    "boundary_type_id" integer NOT NULL REFERENCES "schools_boundary_type" ("id"),
    UNIQUE ("boundary_id", "boundary_type_id")
);
INSERT INTO "schools_boundary_boundary_type" VALUES(1,2,1);
INSERT INTO "schools_boundary_boundary_type" VALUES(2,2,2);
INSERT INTO "schools_boundary_boundary_type" VALUES(3,3,2);
INSERT INTO "schools_boundary_boundary_type" VALUES(4,4,2);
INSERT INTO "schools_boundary_boundary_type" VALUES(5,5,1);
INSERT INTO "schools_boundary_boundary_type" VALUES(6,6,1);
CREATE TABLE "schools_boundary" (
    "id" integer NOT NULL PRIMARY KEY,
    "parent_id" integer,
    "topParent_id" integer,
    "name" varchar(300) NOT NULL,
    "geo_code" varchar(300) NOT NULL,
    "active" bool NOT NULL
);
INSERT INTO "schools_boundary" VALUES(1,NULL,NULL,'No Parent','11111',1);
INSERT INTO "schools_boundary" VALUES(2,1,NULL,'Bangalore','12000',1);
INSERT INTO "schools_boundary" VALUES(3,2,NULL,'BangBlk','12000',1);
INSERT INTO "schools_boundary" VALUES(4,3,2,'Bang Cluster','12000',1);
INSERT INTO "schools_boundary" VALUES(5,2,NULL,'Pre Proj','12000',1);
INSERT INTO "schools_boundary" VALUES(6,5,2,'Pre Cir','12000',1);
CREATE TABLE "schools_school" (
    "id" integer NOT NULL PRIMARY KEY,
    "boundary_id" integer NOT NULL REFERENCES "schools_boundary" ("id"),
    "dise_code" varchar(14),
    "name" varchar(300) NOT NULL,
    "cat_id" integer REFERENCES "schools_school_category" ("id"),
    "school_type" varchar(10) NOT NULL,
    "mgmt_id" integer NOT NULL REFERENCES "schools_school_management" ("id"),
    "address" varchar(1000) NOT NULL,
    "landmark" varchar(1000),
    "pincode" varchar(1000),
    "active" bool NOT NULL
);
INSERT INTO "schools_school" VALUES(1,4,'','Sch',2,'co-ed',1,'addr','','',1);
INSERT INTO "schools_school" VALUES(2,6,'','Ang1',11,'co-ed',1,'addr','','',1);
CREATE TABLE "schools_relations" (
    "id" integer NOT NULL PRIMARY KEY,
    "father" varchar(100),
    "mother" varchar(100)
);
INSERT INTO "schools_relations" VALUES(1,'bbb','aaa');
INSERT INTO "schools_relations" VALUES(2,'','we');
INSERT INTO "schools_relations" VALUES(3,'','cv');
INSERT INTO "schools_relations" VALUES(4,'','xc');
INSERT INTO "schools_relations" VALUES(5,'','sdd');
INSERT INTO "schools_relations" VALUES(6,'','qqq');
INSERT INTO "schools_relations" VALUES(7,'','we');
INSERT INTO "schools_relations" VALUES(8,'ssdsd','sdsd');
INSERT INTO "schools_relations" VALUES(9,'zzz','zz');
CREATE TABLE "schools_child" (
    "id" integer NOT NULL PRIMARY KEY,
    "boundary_id" integer NOT NULL REFERENCES "schools_boundary" ("id"),
    "firstName" varchar(100) NOT NULL,
    "lastName" varchar(100) NOT NULL,
    "dob" date,
    "gender" varchar(10) NOT NULL,
    "mt_id" integer NOT NULL REFERENCES "schools_moi_type" ("id"),
    "relations_id" integer REFERENCES "schools_relations" ("id")
);
INSERT INTO "schools_child" VALUES(1,6,'aa','bbb','2000-11-01','male',1,1);
INSERT INTO "schools_child" VALUES(2,4,'dfgdf','dgdf','2010-12-30','male',1,8);
INSERT INTO "schools_child" VALUES(3,4,'zz','zz','2010-12-30','male',1,9);
CREATE TABLE "schools_studentgroup" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "section" varchar(10) NOT NULL,
    "active" bool NOT NULL,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id"),
    "object_id" integer unsigned NOT NULL,
    "group_type" varchar(10) NOT NULL
);
INSERT INTO "schools_studentgroup" VALUES(1,'1','A',1,11,1,'Class');
INSERT INTO "schools_studentgroup" VALUES(2,'0','',1,11,2,'Class');
INSERT INTO "schools_studentgroup" VALUES(3,'1','B',1,11,1,'Class');
CREATE TABLE "schools_student" (
    "id" integer NOT NULL PRIMARY KEY,
    "student_group_id" integer NOT NULL REFERENCES "schools_studentgroup" ("id"),
    "name_id" integer NOT NULL REFERENCES "schools_child" ("id"),
    "academic_id" integer NOT NULL REFERENCES "schools_academic_year" ("id"),
    "active" bool NOT NULL
);
INSERT INTO "schools_student" VALUES(1,2,1,3,1);
INSERT INTO "schools_student" VALUES(2,1,2,3,1);
INSERT INTO "schools_student" VALUES(3,3,3,3,1);
CREATE TABLE "schools_assessment" (
    "id" integer NOT NULL PRIMARY KEY,
    "programme_id" integer NOT NULL REFERENCES "schools_programme" ("id"),
    "name" varchar(100) NOT NULL,
    "startDate" date NOT NULL,
    "endDate" date NOT NULL,
    "query" varchar(500),
    "active" bool NOT NULL
);
CREATE TABLE "schools_question" (
    "id" integer NOT NULL PRIMARY KEY,
    "assessment_id" integer NOT NULL REFERENCES "schools_assessment" ("id"),
    "name" varchar(200) NOT NULL,
    "questionType" varchar(30) NOT NULL,
    "scoreMin" decimal,
    "scoreMax" decimal,
    "grade" varchar(100),
    "doubleEntry" bool NOT NULL,
    "required" bool NOT NULL,
    "active" bool NOT NULL
);
CREATE TABLE "schools_answer" (
    "id" integer NOT NULL PRIMARY KEY,
    "question_id" integer NOT NULL REFERENCES "schools_question" ("id"),
    "student_id" integer NOT NULL REFERENCES "schools_student" ("id"),
    "answerScore" decimal,
    "answerGrade" varchar(30),
    "doubleEntry" integer
);
CREATE TABLE "schools_programme_school_category" (
    "id" integer NOT NULL PRIMARY KEY,
    "category" varchar(100) NOT NULL
);
INSERT INTO "schools_programme_school_category" VALUES(1,'Pre-School');
INSERT INTO "schools_programme_school_category" VALUES(2,'Primary-School');
CREATE TABLE "schools_programme_programme_school_category" (
    "id" integer NOT NULL PRIMARY KEY,
    "programme_id" integer NOT NULL,
    "programme_school_category_id" integer NOT NULL REFERENCES "schools_programme_school_category" ("id"),
    UNIQUE ("programme_id", "programme_school_category_id")
);
INSERT INTO "schools_programme_programme_school_category" VALUES(1,1,2);
INSERT INTO "schools_programme_programme_school_category" VALUES(2,2,1);
CREATE TABLE "schools_programme" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "description" varchar(500),
    "startDate" date NOT NULL,
    "endDate" date NOT NULL,
    "active" bool NOT NULL
);
INSERT INTO "schools_programme" VALUES(1,'Programme1','Programme1','2010-12-06','2011-04-30',1);
INSERT INTO "schools_programme" VALUES(2,'Pre Programme1','Pre Programme1','2010-12-06','2011-04-30',1);
CREATE INDEX "auth_permission_1bb8f392" ON "auth_permission" ("content_type_id");
CREATE INDEX "auth_group_permissions_425ae3c4" ON "auth_group_permissions" ("group_id");
CREATE INDEX "auth_group_permissions_1e014c8f" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_user_user_permissions_403f60f" ON "auth_user_user_permissions" ("user_id");
CREATE INDEX "auth_user_user_permissions_1e014c8f" ON "auth_user_user_permissions" ("permission_id");
CREATE INDEX "auth_user_groups_403f60f" ON "auth_user_groups" ("user_id");
CREATE INDEX "auth_user_groups_425ae3c4" ON "auth_user_groups" ("group_id");
CREATE INDEX "auth_message_403f60f" ON "auth_message" ("user_id");
CREATE INDEX "django_admin_log_403f60f" ON "django_admin_log" ("user_id");
CREATE INDEX "django_admin_log_1bb8f392" ON "django_admin_log" ("content_type_id");
CREATE INDEX "schools_school_languages_1ebdc00a" ON "schools_school_languages" ("school_id");
CREATE INDEX "schools_school_languages_5978c710" ON "schools_school_languages" ("moi_type_id");
CREATE INDEX "schools_boundary_boundary_category_2879d902" ON "schools_boundary_boundary_category" ("boundary_id");
CREATE INDEX "schools_boundary_boundary_category_4f75fc4c" ON "schools_boundary_boundary_category" ("boundary_category_id");
CREATE INDEX "schools_boundary_boundary_type_2879d902" ON "schools_boundary_boundary_type" ("boundary_id");
CREATE INDEX "schools_boundary_boundary_type_40bab4" ON "schools_boundary_boundary_type" ("boundary_type_id");
CREATE INDEX "schools_boundary_63f17a16" ON "schools_boundary" ("parent_id");
CREATE INDEX "schools_boundary_7fa0e0" ON "schools_boundary" ("topParent_id");
CREATE INDEX "schools_school_2879d902" ON "schools_school" ("boundary_id");
CREATE INDEX "schools_school_5120efd1" ON "schools_school" ("cat_id");
CREATE INDEX "schools_school_7ba2cdd9" ON "schools_school" ("mgmt_id");
CREATE INDEX "schools_child_2879d902" ON "schools_child" ("boundary_id");
CREATE INDEX "schools_child_1bd7e033" ON "schools_child" ("mt_id");
CREATE INDEX "schools_child_1c8d8cc6" ON "schools_child" ("relations_id");
CREATE INDEX "schools_studentgroup_1bb8f392" ON "schools_studentgroup" ("content_type_id");
CREATE INDEX "schools_student_2c9338e8" ON "schools_student" ("student_group_id");
CREATE INDEX "schools_student_632e075f" ON "schools_student" ("name_id");
CREATE INDEX "schools_student_7f1c97ad" ON "schools_student" ("academic_id");
CREATE INDEX "schools_assessment_d981227" ON "schools_assessment" ("programme_id");
CREATE INDEX "schools_question_3e970d24" ON "schools_question" ("assessment_id");
CREATE INDEX "schools_answer_1f92e550" ON "schools_answer" ("question_id");
CREATE INDEX "schools_answer_42ff452e" ON "schools_answer" ("student_id");
CREATE INDEX "schools_programme_programme_school_category_d981227" ON "schools_programme_programme_school_category" ("programme_id");
CREATE INDEX "schools_programme_programme_school_category_69c5c6eb" ON "schools_programme_programme_school_category" ("programme_school_category_id");
COMMIT;
