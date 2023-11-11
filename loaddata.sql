CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "DemotionQueue" (
  "action" varchar,
  "admin_id" INTEGER,
  "approver_one_id" INTEGER,
  FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
  PRIMARY KEY (action, admin_id, approver_one_id)
);


CREATE TABLE "Subscriptions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "image_url" varchar,
  "content" varchar,
  "approved" bit,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

CREATE TABLE "Reactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar,
  "image_url" varchar
);

CREATE TABLE "PostReactions" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "reaction_id" INTEGER,
  "post_id" INTEGER,
  FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
  FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);

CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('SQL');
INSERT INTO PostTags ('post_id', 'tag_id') VALUES ('1', '3');
INSERT INTO PostTags ('tag_id') VALUES ('3');
INSERT INTO Reactions ('label', 'image_url') VALUES ('happy', 'https://pngtree.com/so/happy');

DELETE from posts
WHERE id == 1

SELECT * FROM PostTags
SELECT * from posts
DELETE from Posts
where id == 3

SELECT * FROM Users
WHERE id = 2
SELECT * FROM tags

SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            u.first_name,
            u.last_name
        FROM Posts p
        JOIN Users u
        ON p.user_id = u.id

INSERT INTO Categories ('label') VALUES ('Obituaries');

INSERT INTO USERS (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('David', 'Poole', 'dbpoole7@gmail.com', 'Member of Alpha Q', 'dbpoole', 'password', NULL, '2023-11-01 18:59:07.001179', 1);
INSERT INTO USERS (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('Mason', 'Austin', 'mason47austin@gmail.com', 'Member of Alpha Q', 'crazymace', 'password', NULL, '2023-11-01 20:38:37.110268', 1);
INSERT INTO USERS (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('Michael', 'Brantley', 'mbrantley@gmail.com', 'Member of Alpha Q', 'candyeater', 'password', NULL, '2023-11-01 20:46:41.040093', 1);
INSERT INTO USERS (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('Kyle', 'Berry', 'Kberry@gmail.com', 'Member of Alpha Q', 'HomeDepot', 'password', NULL, '2023-11-01 20:47:16.078988', 1);
INSERT INTO USERS (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('Stacey', 'Vanyo', 'svanyo@gmail.com', 'Member of Alpha Q', 'Code Mom', 'password', NULL, '2023-11-01 20:47:50.292648', 1);
INSERT INTO USERS (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('3rd Test', 'Saturday', 'test@gmail.com', 'Member of Alpha Q', 'Test Member', 'password', NULL, '2023-11-01 20:47:50.292648', 1);
INSERT INTO USERS (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('Saturday', 'Test', 'test@gmail.com', 'Member of Alpha Q', 'Test Member', 'password', NULL, '2023-11-01 20:47:50.292648', 1);
INSERT INTO USERS (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('David', 'Poole', 'dbpoole7@gmail.com', 'Member of E23 Alpha Q', 'dbpoole', 'alphaqpw', NULL, '2023-11-04 13:37:02.539087', 1);
INSERT INTO USERS (first_name, last_name, email, bio, username, password, profile_image_url, created_on, active)
VALUES ('MVP Test Member', 'Delete me', 'test@gmail.com', 'Member of Alpha Q', 'Saturday Create Member SUCCESS', '123Delete', NULL, '2023-11-05 17:33:18.021384', 1);



