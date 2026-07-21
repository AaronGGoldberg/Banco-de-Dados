SELECT a.nome, p.tipo_periodo, p.tipo_acomp, c.status
FROM alunos a
JOIN contratos c ON a.id = c.aluno_id
JOIN planos p ON c.plano_id = p.id
WHERE c.status = 'ativo';