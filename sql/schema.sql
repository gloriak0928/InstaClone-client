PRAGMA foreign_keys = ON;

CREATE TABLE users(
  username varchar(20) primary key, 
  fullname varchar(40), 
  email varchar(40), 
  filename varchar(40), 
  password varchar(256), 
  created datetime not null default current_timestamp
);

CREATE TABLE posts(
  postid INTEGER PRIMARY KEY AUTOINCREMENT, 
  filename VARCHAR(64),
  owner VARCHAR(20), 
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE following(
  username1 VARCHAR(20), 
  username2 VARCHAR(20), 
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
  PRIMARY KEY (username1, username2), 
  FOREIGN KEY (username1) REFERENCES users(username) ON DELETE CASCADE, 
  FOREIGN KEY (username2) REFERENCES users(username) ON DELETE CASCADE
);

CREATE TABLE comments(
  commentid INTEGER PRIMARY KEY AUTOINCREMENT,
  owner VARCHAR(20),
  postid INTEGER,
  text VARCHAR(1024),
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE,
  FOREIGN KEY (postid) REFERENCES posts(postid) ON DELETE CASCADE
);

CREATE TABLE likes(
  likeid INTEGER PRIMARY KEY AUTOINCREMENT,
  owner VARCHAR(20),
  postid INTEGER,
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE,
  FOREIGN KEY (postid) REFERENCES posts(postid) ON DELETE CASCADE
);