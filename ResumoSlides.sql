CREATE SCHEMA dbo;

CREATE TABLE IF NOT EXISTS dbo.cidade(
	ID INTEGER GENERATED ALWAYS AS IDENTITY,
  	nome VARCHAR(150) NOT NULL,
 	estado CHAR(2) NOT NULL,
  
 	CONSTRAINT cidade_pk PRIMARY KEY (ID),
  
 	CONSTRAINT nome_estado_unique UNIQUE (nome, estado)
);

CREATE TABLE dbo.localizacao (
	latitude FLOAT NOT NULL,
  	longitude FLOAT not NULL,
 	id_cidade INTEGER NOT NULL,
  
 	CONSTRAINT cidade_fk
 		fOREIGN KEY (id_cidade) REFERENCES dbo.cidade(ID),
);