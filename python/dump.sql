BEGIN TRANSACTION;
CREATE TABLE users(id INTEGER PRIMARY KEY, username text, email text, phone text, website text, regdate text);
INSERT INTO "users" VALUES(1,'Kim','kim@naver.com','010-0000-0000','kim.com','2021-03-18 15:46:15');
INSERT INTO "users" VALUES(2,'Park','Park@daum.net','010-1111-1111','park,com','2021-03-18 15:46:15');
INSERT INTO "users" VALUES(3,'Lee','Lee@naver.com','010-2222-2222','Lee.com','2021-03-18 15:46:15');
INSERT INTO "users" VALUES(4,'cho','cho@naver.com','010-2222-2222','cho.com','2021-03-18 15:46:15');
INSERT INTO "users" VALUES(5,'You','You@naver.com','010-2232-2222','You.com','2021-03-18 15:46:15');
COMMIT;
