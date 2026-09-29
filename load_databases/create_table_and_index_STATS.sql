CREATE TABLE users ( Id INTEGER NOT NULL, Reputation INTEGER , CreationDate DATETIME , Views INTEGER , UpVotes INTEGER , DownVotes INTEGER, CONSTRAINT [PK_users] PRIMARY KEY CLUSTERED ([Id] ASC) );

 CREATE TABLE posts ( 	Id INTEGER NOT NULL, 	PostTypeId INTEGER , 	CreationDate DATETIME , 	Score INTEGER , 	ViewCount INTEGER, 	OwnerUserId INTEGER,   AnswerCount INTEGER ,   CommentCount INTEGER ,   FavoriteCount INTEGER,   LastEditorUserId INTEGER, CONSTRAINT [PK_posts] PRIMARY KEY CLUSTERED ([Id] ASC) );

 CREATE TABLE postlinks ( 	Id INTEGER NOT NULL, 	CreationDate DATETIME , 	PostId INTEGER , 	RelatedPostId INTEGER , 	LinkTypeId INTEGER,     CONSTRAINT [PK_postLinks] PRIMARY KEY CLUSTERED ([Id] ASC) );

 CREATE TABLE posthistory ( 	Id INTEGER NOT NULL , 	PostHistoryTypeId INTEGER , 	PostId INTEGER , 	CreationDate DATETIME , 	UserId INTEGER,     CONSTRAINT [PK_posthistory] PRIMARY KEY CLUSTERED ([Id] ASC) );

 CREATE TABLE comments ( 	Id INTEGER NOT NULL , 	PostId INTEGER , 	Score INTEGER ,   CreationDate DATETIME , 	UserId INTEGER,     CONSTRAINT [PK_comments] PRIMARY KEY CLUSTERED ([Id] ASC) );

 CREATE TABLE votes ( 	Id INTEGER NOT NULL , 	PostId INTEGER, 	VoteTypeId INTEGER , 	CreationDate DATETIME , 	UserId INTEGER, 	BountyAmount INTEGER,     CONSTRAINT [PK_votes] PRIMARY KEY CLUSTERED ([Id] ASC) );

 CREATE TABLE badges ( 	Id INTEGER NOT NULL , 	UserId INTEGER , 	Date DATETIME,     CONSTRAINT [PK_badges] PRIMARY KEY CLUSTERED ([Id] ASC) );

 CREATE TABLE tags ( 	Id INTEGER NOT NULL , 	Count INTEGER , 	ExcerptPostId INTEGER,     CONSTRAINT [PK_tags] PRIMARY KEY CLUSTERED ([Id] ASC) );


#### load data into tables and set index 
     
docker cp stats/badges.csv sql_server_test:/
BULK INSERT badges FROM '/badges.csv' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');


docker cp stats/comments.csv sql_server_test:/
BULK INSERT comments FROM '/comments.csv' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');


docker cp stats/postHistory.csv sql_server_test:/
BULK INSERT posthistory FROM '/postHistory.csv' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');


docker cp stats/postLinks.csv sql_server_test:/
BULK INSERT postlinks FROM '/postLinks.csv' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');


docker cp stats/posts.csv sql_server_test:/
BULK INSERT posts FROM '/posts.csv' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');


docker cp stats/tags.csv sql_server_test:/
BULK INSERT tags FROM '/tags.csv' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');


docker cp stats/users.csv sql_server_test:/
BULK INSERT users FROM '/users.csv' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');


docker cp stats/votes.csv sql_server_test:/
BULK INSERT votes FROM '/votes.csv' WITH (FIELDTERMINATOR = ',', ROWTERMINATOR = '\n');
                                   