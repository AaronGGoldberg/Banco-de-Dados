SELECT data, distancia_km, duracao_min, status
FROM treinos
WHERE aluno_id = 2
AND data BETWEEN '2026-04-01' AND '2026-04-30';