SELECT 
    i.nome AS instrutor,
    COUNT(DISTINCT a.id) AS total_alunos
FROM instrutores i
JOIN alunos a ON a.instrutor_id = i.id
GROUP BY i.nome;