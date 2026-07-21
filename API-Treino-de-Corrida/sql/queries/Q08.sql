SELECT a.nome, t.distancia_km, c.meta_km
FROM alunos a
JOIN treinos t ON a.id = t.aluno_id
JOIN cronogramas c ON t.cronograma_id = c.id
WHERE t.status = 'concluido'
AND t.distancia_km > c.meta_km;