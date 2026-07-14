require('dotenv').config();

const express = require('express');
const logger = require('./src/middlewares/logger');
const livrosRoutes = require('./src/routes/livros');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(logger);

app.get('/', (req, res) => {
  res.json({ mensagem: 'API da Livraria funcionando' });
});

app.use('/livros', livrosRoutes);

app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});