function validarProduto(req, res, next) {
  const { nome, preco } = req.body;
  if (!nome || typeof nome !== "string" || nome.trim() === "") {
    return res.status(400).json({ erro: 'O campo "nome" é obrigatório' });
  }
  if (preco === undefined || typeof preco !== "number" || preco < 0) {
    return res
      .status(400)
      .json({ erro: 'O campo "preco" deve ser um número positivo' });
  }
  next(); // dados válidos, segue para a rota
}
module.exports = validarProduto;
