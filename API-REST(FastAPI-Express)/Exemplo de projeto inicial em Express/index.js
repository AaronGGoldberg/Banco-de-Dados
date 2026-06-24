const express = require("express");
const sequelize = require("./src/database/connection");
const app = express();
const PORT = 3000;
app.use(express.json());
// Testar conexão ao iniciar o servidor
async function iniciar() {
  try {
    await sequelize.authenticate();
    console.log("✓ Conectado ao PostgreSQL com sucesso!");

    // Configurar rotas de produtos
    const produtosRouter = require("./src/routes/produtos");
    app.use("/produtos", produtosRouter);

    app.listen(PORT, () => {
      console.log(`Servidor rodando em http://localhost:${PORT}`);
    });
  } catch (erro) {
    console.error("✗ Erro ao conectar ao banco:", erro.message);
    process.exit(1);
  }
}
iniciar();
