CREATE TABLE [dbo].[aka_name] ([id]            INT           NOT NULL,     [person_id]     INT           NOT NULL,     [name]          VARCHAR (MAX) NOT NULL,     [imdb_index]    VARCHAR (12)  NULL,     [name_pcode_cf] VARCHAR (5)   NULL,     [name_pcode_nf] VARCHAR (5)   NULL,     [surname_pcode] VARCHAR (5)   NULL,     [md5sum]        VARCHAR (32)  NULL,     CONSTRAINT [PK_aka_name] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[aka_title] (     [id]              INT           NOT NULL,     [movie_id]        INT           NOT NULL,     [title]           VARCHAR (MAX) NOT NULL,     [imdb_index]      VARCHAR (12)  NULL,     [kind_id]         INT           NOT NULL,     [production_year] INT           NULL,     [phonetic_code]   VARCHAR (5)   NULL,     [episode_of_id]   INT           NULL,     [season_nr]       INT           NULL,     [episode_nr]      INT           NULL,     [note]            VARCHAR (MAX) NULL,     [md5sum]          VARCHAR (32)  NULL,     CONSTRAINT [PK_aka_title] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[cast_info] (     [id]             INT           NOT NULL,     [person_id]      INT           NOT NULL,     [movie_id]       INT           NOT NULL,     [person_role_id] INT           NULL,     [note]           VARCHAR (MAX) NULL,     [nr_order]       INT           NULL,     [role_id]        INT           NOT NULL,     CONSTRAINT [PK_cast_info] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[char_name] (     [id]            INT           NOT NULL,     [name]          VARCHAR (MAX) NOT NULL,     [imdb_index]    VARCHAR (12)  NULL,     [imdb_id]       INT           NULL,     [name_pcode_nf] VARCHAR (5)   NULL,     [surname_pcode] VARCHAR (5)   NULL,     [md5sum]        VARCHAR (32)  NULL,     CONSTRAINT [PK_char_name] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[company_name] (     [id]            INT           NOT NULL,     [name]          VARCHAR (MAX) NOT NULL,     [country_code]  VARCHAR (255) NULL,     [imdb_id]       INT           NULL,     [name_pcode_nf] VARCHAR (5)   NULL,     [name_pcode_sf] VARCHAR (5)   NULL,     [md5sum]        VARCHAR (32)  NULL,     CONSTRAINT [PK_company_name] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[company_type] (     [id]   INT          NOT NULL,     [kind] VARCHAR (32) NOT NULL,     CONSTRAINT [PK_company_type] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[complete_cast] (     [id]         INT NOT NULL,     [movie_id]   INT NULL,     [subject_id] INT NOT NULL,     [status_id]  INT NOT NULL,     CONSTRAINT [PK_complete_cast] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[comp_cast_type] (     [id]   INT          NOT NULL,     [kind] VARCHAR (32) NOT NULL,     CONSTRAINT [PK_comp_cast_type] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[info_type] (     [id]   INT          NOT NULL,     [info] VARCHAR (32) NOT NULL,     CONSTRAINT [PK_info_type] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[keyword] (     [id]            INT           NOT NULL,     [keyword]       VARCHAR (MAX) NOT NULL,     [phonetic_code] VARCHAR (5)   NULL,     CONSTRAINT [PK_keyword] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[kind_type] (     [id]   INT          NOT NULL,     [kind] VARCHAR (15) NOT NULL,     CONSTRAINT [PK_kind_type] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[link_type] (     [id]   INT          NOT NULL,     [link] VARCHAR (32) NOT NULL,     CONSTRAINT [PK_link_type] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[movie_companies] (     [id]              INT           NOT NULL,     [movie_id]        INT           NOT NULL,     [company_id]      INT           NOT NULL,     [company_type_id] INT           NOT NULL,     [note]            VARCHAR (MAX) NULL,     CONSTRAINT [PK_movie_companies] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[movie_info] (     [id]           INT           NOT NULL,     [movie_id]     INT           NOT NULL,     [info_type_id] INT           NOT NULL,     [info]         VARCHAR (MAX) NOT NULL,     [note]         VARCHAR (MAX) NULL,     CONSTRAINT [PK_movie_info] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[movie_info_idx] (     [id]           INT           NOT NULL,     [movie_id]     INT           NOT NULL,     [info_type_id] INT           NOT NULL,     [info]         VARCHAR (MAX) NOT NULL,     [note]         VARCHAR (MAX) NULL,     CONSTRAINT [PK_movie_info_idx] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[movie_keyword] (     [id]         INT NOT NULL,     [movie_id]   INT NOT NULL,     [keyword_id] INT NOT NULL,     CONSTRAINT [PK_movie_keyword] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[movie_link] (     [id]              INT NOT NULL,     [movie_id]        INT NOT NULL,     [linked_movie_id] INT NOT NULL,     [link_type_id]    INT NOT NULL,     CONSTRAINT [PK_movie_link] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[name] (     [id]            INT           NOT NULL,     [name]          VARCHAR (MAX) NOT NULL,     [imdb_index]    VARCHAR (12)  NULL,     [imdb_id]       INT           NULL,     [gender]        VARCHAR (1)   NULL,     [name_pcode_cf] VARCHAR (5)   NULL,     [name_pcode_nf] VARCHAR (5)   NULL,     [surname_pcode] VARCHAR (5)   NULL,     [md5sum]        VARCHAR (32)  NULL,     CONSTRAINT [PK_name] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[person_info] (     [id]           INT           NOT NULL,     [person_id]    INT           NOT NULL,     [info_type_id] INT           NOT NULL,     [info]         VARCHAR (MAX) NOT NULL,     [note]         VARCHAR (MAX) NULL,     CONSTRAINT [PK_person_info] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[role_type] (     [id]   INT          NOT NULL,     [role] VARCHAR (32) NOT NULL,     CONSTRAINT [PK_role_type] PRIMARY KEY CLUSTERED ([id] ASC) );

 CREATE TABLE [dbo].[title] (     [id]              INT           NOT NULL,     [title]           VARCHAR (MAX) NOT NULL,     [imdb_index]      VARCHAR (12)  NULL,     [kind_id]         INT           NOT NULL,     [production_year] INT           NULL,     [imdb_id]         INT           NULL,     [phonetic_code]   VARCHAR (5)   NULL,     [episode_of_id]   INT           NULL,     [season_nr]       INT           NULL,     [episode_nr]      INT           NULL,     [series_years]    VARCHAR (49)  NULL,     [md5sum]          VARCHAR (32)  NULL,     CONSTRAINT [PK_title] PRIMARY KEY CLUSTERED ([id] ASC) );


### load data into table and set index

docker cp aka_name.csv sql_server_test:/
BULK INSERT aka_name FROM '/aka_name.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp aka_title.csv sql_server_test:/
BULK INSERT aka_title FROM '/aka_title.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp cast_info.csv sql_server_test:/
BULK INSERT cast_info FROM '/cast_info.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp char_name.csv sql_server_test:/
BULK INSERT char_name FROM '/char_name.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp comp_cast_type.csv sql_server_test:/
BULK INSERT comp_cast_type FROM '/comp_cast_type.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp company_name.csv sql_server_test:/
BULK INSERT company_name FROM '/company_name.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp company_type.csv sql_server_test:/
BULK INSERT company_type FROM '/company_type.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp complete_cast.csv sql_server_test:/
BULK INSERT complete_cast FROM '/complete_cast.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp info_type.csv sql_server_test:/
BULK INSERT info_type FROM '/info_type.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp keyword.csv sql_server_test:/
BULK INSERT keyword FROM '/keyword.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp kind_type.csv sql_server_test:/
BULK INSERT kind_type FROM '/kind_type.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp link_type.csv sql_server_test:/
BULK INSERT link_type FROM '/link_type.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp movie_companies.csv sql_server_test:/
BULK INSERT movie_companies FROM '/movie_companies.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp movie_info.csv sql_server_test:/
BULK INSERT movie_info FROM '/movie_info.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp movie_info_idx.csv sql_server_test:/
BULK INSERT movie_info_idx FROM '/movie_info_idx.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp movie_keyword.csv sql_server_test:/
BULK INSERT movie_keyword FROM '/movie_keyword.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp movie_link.csv sql_server_test:/
BULK INSERT movie_link FROM '/movie_link.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp name.csv sql_server_test:/
BULK INSERT name FROM '/name.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp person_info.csv sql_server_test:/
BULK INSERT person_info FROM '/person_info.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp role_type.csv sql_server_test:/
BULK INSERT role_type FROM '/role_type.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');


docker cp title.csv sql_server_test:/
BULK INSERT title FROM '/title.csv' WITH (FIELDTERMINATOR = '|', ROWTERMINATOR = '\n');
