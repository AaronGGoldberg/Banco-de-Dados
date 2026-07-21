SELECT a.nome, SUM(t.distancia_km) AS total_km
FROM alunos a
JOIN treinos t ON a.id = t.aluno_id
WHERE t.data BETWEEN '2026-04-01' AND '2026-04-30'
AND t.status = 'concluido'
GROUP BY a.nome;