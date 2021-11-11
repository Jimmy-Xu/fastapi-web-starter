--
-- 由SQLiteStudio v3.3.3 产生的文件 周四 11月 11 22:41:28 2021
--
-- 文本编码：System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

------------------------------------------------------------------------------
-- 表：posts
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id         INTEGER        PRIMARY KEY AUTOINCREMENT,
    text       VARCHAR (1024),
    owner_id   INTEGER,
    created_at TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);


------------------------------------------------------------------------------
-- 表：users
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id       INTEGER       PRIMARY KEY AUTOINCREMENT,
    username VARCHAR (20),
    password VARCHAR (128),
    is_admin INTEGER,
    UNIQUE (
        username
    )
    ON CONFLICT REPLACE
);

INSERT INTO users (
                      id,
                      username,
                      password,
                      is_admin
                  )
                  VALUES (
                      1,
                      'gnep',
                      '$2b$12$QMTNqYFOT6Sa.Vo4hXyoWeXSSRjF4BzjDeuJmlORFab0/y5SLGDCW',
                      1
                  );

------------------------------------------------------------------------------
-- 触发器：ModifyPostUpdatedAt
DROP TRIGGER IF EXISTS ModifyPostUpdatedAt;
CREATE TRIGGER ModifyPostUpdatedAt
         AFTER UPDATE
            ON posts
      FOR EACH ROW
          WHEN NEW.updated_at <= OLD.updated_at
BEGIN
    UPDATE test
       SET updated_at = CURRENT_TIMESTAMP
     WHERE id = OLD.id;
END;


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
