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

 	CONSTRAINT localizacao_un UNIQUE (id_cidade)
);

CREATE TABLE dbo.tempo (
	ID INTEGER GENERATED ALWAYS AS IDENTITY,
 	tempo_min INTEGER NOT NULL,
 	tempo_max INTEGER NOT NULL,
	precip_pluviom REAL not NULL DEFAULT 0.0,
 	dh_coleta TIMESTAMP not NULL,
 	id_cidade INTEGER NOT NULL,
  
 	CONSTRAINT tempo_pk PRIMARY KEY(ID),
  
 	CONSTRAINT tempo_fk
 		FOREIGN KEY (id_cidade) REFERENCES dbo.cidade(id),
  
 	CONSTRAINT dhColeta_idCidade_un UNIQUE (dh_coleta, id_cidade)
);

SELECT * from dbo.tempo;

INSERT INTO dbo.tempo (tempo_min, tempo_max, precip_pluviom) VALUES
	(1, 10, 30),
    (3, 10, 50),
    (2, 20, 30),
    (5, 100, 50);
    
UPDATE dbo.tempo
	set tempo_min = 10
    WHERE tempo_max > 10 and precip_pluviom = 30;

CREATE TABLE dbo.central (
	codigo CHAR(5) NOT NULL,

CREATE TABLE dbo.central (
	codigo CHAR(5) NOT NULL,
  
 	CONSTRAINT central_pk PRIMARY key (codigo)
  
);

CREATE TABLE dbo.tempoCentral (
	id_tempo INTEGER not NULL,
 	codigo_central CHAR(5) not NULL,
  
 	CONSTRAINT tempocentral_pk PRIMARY KEY (id_tempo, codigo_central),
  
 	CONSTRAINT tempo_fk 
 		FOREIGN KEY (id_tempo) REFERENCES dbo.tempo(id),
  
 	CONSTRAINT central_fk
 		FOREIGN key (codigo_central) REFERENCES dbo.central(codigo)
);
 
-- exibindo o conteúdo da tabela
SELECT * FROM dbo.cidade;

-- inserindo cidades
INSERT INTO dbo.cidade (nome, estado) VALUES
	('Natal', 'RN');

INSERT INTO dbo.cidade (nome, estado) VALUES
	('Macaíba', 'RN'), ('Parnamirim', 'RN'), ('Recife', 'PE');

SELECT * from dbo.localizacao;

-- atribuindo localizações às cidades
INSERT INTO dbo.localizacao (latitude, longitude, id_cidade) VALUES
	('-5.234', 5.234, 1), (1.234, -4,56, 2), (5.89, -1.23, 3);

CREATE TABLE dbo.cliente (
 	cpf VARCHAR(14) not NULL,
    nome VARCHAR(150) not NULL,
    email VARCHAR(150) NULL,
 	CONSTRAINT cliente_pk PRIMARY key (cpf)
);

SELECT * from dbo.cliente;

insert into dbo.cliente (cpf, nome, email) VALUES
	('01234567890', 'C Heusser', 'heusser@email.com'),
    ('01234567891', 'M Machado', 'machado@email.com'),
    ('01234567892', 'S Silva', NULL);
    
DELETE from dbo.cliente WHERE email is NULL;

DELETE from dbo.cidade
	WHERE nome like '% Machado' or nome LIKE '% Machado %';

SELECT * from dbo.cliente
	WHERE nome like '_%a'

SELECT dh_coleta, tempo_min, tempo_max, precip_pluviom
	FROM dbo.tempo OFFSET 4 LIMIT 4;

-- exibir as diferentes temperaturas mínimas observadas
SELECT DISTINCT tempo_min FROM dbo.tempo;