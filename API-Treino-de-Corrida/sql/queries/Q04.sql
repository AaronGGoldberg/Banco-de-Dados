SELECT g.nome, COUNT(ag.aluno_id) AS quantidade_alunos
FROM grupos g
LEFT JOIN aluno_grupo ag ON g.id = ag.grupo_id
GROUP BY g.nome;