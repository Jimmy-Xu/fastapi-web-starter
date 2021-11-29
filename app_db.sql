--
-- 由SQLiteStudio v3.3.3 产生的文件 周二 11月 30 00:26:03 2021
--
-- 文本编码：System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- 表：api_keys
DROP TABLE IF EXISTS api_keys;

CREATE TABLE api_keys (
    id         INTEGER       PRIMARY KEY AUTOINCREMENT,
    app_name   VARCHAR (20),
    api_key    VARCHAR (128),
    secret_key VARCHAR (128),
    is_default BOOLEAN       DEFAULT (0),
    owner_id   INTEGER,
    created_at TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO api_keys (
                         id,
                         app_name,
                         api_key,
                         secret_key,
                         is_default,
                         owner_id,
                         created_at
                     )
                     VALUES (
                         4,
                         'ftx',
                         '111',
                         'e6782063242d4aba3f568672f4750374582f2becc1bb10d98ae1a8b6',
                         1,
                         1,
                         '2021-11-24 18:16:07'
                     );

INSERT INTO api_keys (
                         id,
                         app_name,
                         api_key,
                         secret_key,
                         is_default,
                         owner_id,
                         created_at
                     )
                     VALUES (
                         5,
                         'ftx',
                         '222',
                         'f1f9ee3e3a8e83c861236a62952d0963e5faafd7ad56df4f29beeddfb50d5ca7d4c1d1dd',
                         0,
                         1,
                         '2021-11-24 18:16:10'
                     );

INSERT INTO api_keys (
                         id,
                         app_name,
                         api_key,
                         secret_key,
                         is_default,
                         owner_id,
                         created_at
                     )
                     VALUES (
                         10,
                         'binance',
                         'YfJgA9fdAHKrm1vOWVUy0JHktr6HoWOUsGKEZiKnt6jgcixmVeZBaJT4TGciKIIC',
                         'f6fa7509deb5e8ed5b2ad9a48d26b2142c8844b919a8ed77b391b65f8b5e3589b5be1d323f6c43685cb28304cef53bca2662e35af4fd4f15f8f2fa00f60f9fdda9a31ed8fe50629baa3adf055eb3975b',
                         1,
                         1,
                         '2021-11-27 15:09:19'
                     );


-- 表：posts
DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id         INTEGER        PRIMARY KEY AUTOINCREMENT,
    text       VARCHAR (1024),
    owner_id   INTEGER,
    created_at TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP
);


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
                      '$2b$12$wjpYVz7X.Iy792NDyoIC2ehK9MCE.HIFn.Ws4/g44TwgUb52N0x2y',
                      1
                  );


-- 索引：indexAPIKey
DROP INDEX IF EXISTS indexAPIKey;

CREATE UNIQUE INDEX indexAPIKey ON api_keys (
    app_name,
    api_key
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
