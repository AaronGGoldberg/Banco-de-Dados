-- Trabalho Prático 1


-- Instrutor

INSERT INTO instrutores (nome, email, telefone, especialidade)
VALUES
('Carlos Silva', 'carlos@email.com', '(84)99999-1111', 'Corrida');


-- Alunos

INSERT INTO alunos (nome, email, data_nascimento, nivel_condicionamento, instrutor_id)
VALUES
('Ana', 'ana@email.com', '2000-03-15', 'inicial', 1),
('Bruno', 'bruno@email.com', '1998-07-22', 'intermediario', 1),
('Camila', 'camila@email.com', '2001-11-08', 'avancado', 1),
('Diego', 'diego@email.com', '1999-05-30', 'intermediario', 1),
('Eduarda', 'eduarda@email.com', '2002-01-12', 'inicial', 1);


-- Grupos

INSERT INTO grupos (nome, descricao, instrutor_id)
VALUES
('Grupo Manha', 'Treinos pela manha', 1),
('Grupo 5K', 'Foco em corrida de 5km', 1);


-- Ligacao aluno-grupo

INSERT INTO aluno_grupo (aluno_id, grupo_id, data_entrada)
VALUES
(1, 1, '2026-04-01'),
(2, 1, '2026-04-01'),
(3, 2, '2026-04-01'),
(4, 2, '2026-04-01');


-- Planos

INSERT INTO planos (tipo_periodo, tipo_acomp, valor, descricao)
VALUES
('mensal', 'individual', 150, 'Mensal individual'),
('mensal', 'grupo', 100, 'Mensal grupo'),
('trimestral', 'individual', 400, 'Trimestral individual'),
('trimestral', 'grupo', 250, 'Trimestral grupo'),
('semestral', 'individual', 700, 'Semestral individual'),
('semestral', 'grupo', 450, 'Semestral grupo');


-- Contratos

INSERT INTO contratos (aluno_id, plano_id, data_inicio, data_fim, status)
VALUES
(1, 2, '2026-04-01', '2026-04-30', 'ativo'),
(2, 1, '2026-04-01', '2026-04-30', 'ativo'),
(3, 4, '2026-03-01', '2026-05-31', 'ativo'),
(4, 3, '2026-01-01', '2026-03-31', 'encerrado'),
(5, 6, '2026-04-01', '2026-09-30', 'ativo');


-- Cronogramas

-- cronograma de grupo
INSERT INTO cronogramas (semana_ref, meta_km, descricao, grupo_id, aluno_id)
VALUES
('2026-04-06', 20, 'Treino da semana grupo', 1, NULL);

-- cronograma individual
INSERT INTO cronogramas (semana_ref, meta_km, descricao, grupo_id, aluno_id)
VALUES
('2026-04-06', 25, 'Treino individual Bruno', NULL, 2);


-- Treinos (grupo)

INSERT INTO treinos (cronograma_id, aluno_id, data, distancia_km, duracao_min, status)
VALUES
(1, 1, '2026-04-07', 4, 30, 'concluido'),
(1, 1, '2026-04-08', 3, 25, 'concluido'),
(1, 2, '2026-04-09', 5, 35, 'concluido'),
(1, 2, '2026-04-10', 4, 30, 'pendente'),
(1, 1, '2026-04-11', 6, 40, 'concluido');


-- Treinos (individual)

INSERT INTO treinos (cronograma_id, aluno_id, data, distancia_km, duracao_min, status)
VALUES
(2, 2, '2026-04-07', 5, 34, 'concluido'),
(2, 2, '2026-04-08', 4, 28, 'concluido'),
(2, 2, '2026-04-09', 6, 45, 'concluido'),
(2, 2, '2026-04-10', 3, 22, 'pendente'),
(2, 2, '2026-04-11', 7, 48, 'concluido');