-- Trabalho de Aaron e Ramon
-- Sistema de Acompanhamento de Treinos de Corrida

DROP TABLE IF EXISTS treinos CASCADE;
DROP TABLE IF EXISTS cronogramas CASCADE;
DROP TABLE IF EXISTS contratos CASCADE;
DROP TABLE IF EXISTS aluno_grupo CASCADE;
DROP TABLE IF EXISTS grupos CASCADE;
DROP TABLE IF EXISTS alunos CASCADE;
DROP TABLE IF EXISTS planos CASCADE;
DROP TABLE IF EXISTS instrutores CASCADE;

CREATE TABLE instrutores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    especialidade VARCHAR(80),
    criado_em TIMESTAMP DEFAULT NOW(),
    ativo BOOLEAN DEFAULT TRUE
);

CREATE TABLE alunos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    nivel_condicionamento VARCHAR(30) NOT NULL,
    instrutor_id INTEGER NOT NULL,
    criado_em TIMESTAMP DEFAULT NOW(),

    FOREIGN KEY (instrutor_id) REFERENCES instrutores(id),

    CHECK (nivel_condicionamento IN ('inicial', 'intermediario', 'avancado'))
);

CREATE TABLE grupos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    instrutor_id INTEGER NOT NULL,
    criado_em TIMESTAMP DEFAULT NOW(),

    FOREIGN KEY (instrutor_id) REFERENCES instrutores(id)
);

CREATE TABLE aluno_grupo (
    aluno_id INTEGER NOT NULL,
    grupo_id INTEGER NOT NULL,
    data_entrada DATE NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,

    PRIMARY KEY (aluno_id, grupo_id),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (grupo_id) REFERENCES grupos(id)
);

CREATE TABLE planos (
    id SERIAL PRIMARY KEY,
    tipo_periodo VARCHAR(20) NOT NULL,
    tipo_acomp VARCHAR(20) NOT NULL,
    valor NUMERIC(10,2) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,

    CHECK (tipo_periodo IN ('mensal', 'trimestral', 'semestral')),
    CHECK (tipo_acomp IN ('individual', 'grupo')),
    CHECK (valor > 0)
);

CREATE TABLE contratos (
    id SERIAL PRIMARY KEY,
    aluno_id INTEGER NOT NULL,
    plano_id INTEGER NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    status VARCHAR(20) NOT NULL,

    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (plano_id) REFERENCES planos(id),

    CHECK (status IN ('ativo', 'encerrado', 'cancelado')),
    CHECK (data_fim >= data_inicio)
);

CREATE TABLE cronogramas (
    id SERIAL PRIMARY KEY,
    semana_ref DATE NOT NULL,
    meta_km NUMERIC(6,2) NOT NULL,
    descricao TEXT,
    grupo_id INTEGER,
    aluno_id INTEGER,
    criado_em TIMESTAMP DEFAULT NOW(),

    FOREIGN KEY (grupo_id) REFERENCES grupos(id),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),

    CHECK (meta_km > 0),
    CHECK (grupo_id IS NOT NULL OR aluno_id IS NOT NULL)
);

CREATE TABLE treinos (
    id SERIAL PRIMARY KEY,
    cronograma_id INTEGER NOT NULL,
    aluno_id INTEGER NOT NULL,
    data DATE NOT NULL,
    distancia_km NUMERIC(6,2) NOT NULL,
    duracao_min INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    criado_em TIMESTAMP DEFAULT NOW(),

    FOREIGN KEY (cronograma_id) REFERENCES cronogramas(id),
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),

    CHECK (distancia_km >= 0),
    CHECK (duracao_min > 0),
    CHECK (status IN ('pendente', 'concluido', 'cancelado'))
);