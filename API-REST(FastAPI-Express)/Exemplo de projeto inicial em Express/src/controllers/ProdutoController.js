const { Produto } = require("../models");

const ProdutoController = {
  async listar(req, res) {
    const produtos = await Produto.findAll();
    res.json(produtos);
  },
  async buscar(req, res) {
    const id = parseInt(req.params.id);
    const produto = await Produto.findByPk(id);
    if (!produto) return res.status(404).json({ erro: "Não encontrado" });
    res.json(produto);
  },
  async criar(req, res) {
    const novo = await Produto.create(req.body);
    res.status(201).json(novo);
  },
  async atualizar(req, res) {
    const id = parseInt(req.params.id);
    const produto = await Produto.findByPk(id);
    if (!produto) return res.status(404).json({ erro: "Não encontrado" });
    await produto.update(req.body);
    res.json(produto);
  },
  async remover(req, res) {
    const id = parseInt(req.params.id);
    const produto = await Produto.findByPk(id);
    if (!produto) return res.status(404).json({ erro: "Não encontrado" });
    await produto.destroy();
    res.status(204).send();
  },
};
module.exports = ProdutoController;
