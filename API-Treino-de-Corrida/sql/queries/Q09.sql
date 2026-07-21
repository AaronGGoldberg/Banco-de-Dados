SELECT a.nome, SUM(p.valor) AS total_pago
FROM alunos a
JOIN contratos c ON a.id = c.aluno_id
JOIN planos p ON c.plano_id = p.id
GROUP BY a.nome;