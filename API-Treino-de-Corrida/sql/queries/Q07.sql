SELECT a.nome, a.email
FROM alunos a
LEFT JOIN contratos c ON a.id = c.aluno_id AND c.status = 'ativo'
WHERE c.id IS NULL;