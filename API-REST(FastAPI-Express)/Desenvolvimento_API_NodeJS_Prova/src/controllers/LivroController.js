const Livro = require('../models/Livro');

module.exports = {
  async listar(req, res) {
    try {
      const livros = await Livro.findAll();
      return res.status(200).json(livros);
    } catch (error) {
      return res.status(500).json({
        erro: 'Erro ao listar livros',
        codigo: 500,
      });
    }
  },

  async buscar(req, res) {
    try {
      const { id } = req.params;

      const livro = await Livro.findByPk(id);

      if (!livro) {
        return res.status(404).json({
          erro: 'Livro não encontrado',
          codigo: 404,
        });
      }

      return res.status(200).json(livro);
    } catch (error) {
      return res.status(500).json({
        erro: 'Erro ao buscar livro',
        codigo: 500,
      });
    }
  },

  async criar(req, res) {
    try {
      const livro = await Livro.create(req.body);
      return res.status(201).json(livro);
    } catch (error) {
      return res.status(400).json({
        erro: 'Erro ao criar livro',
        codigo: 400,
      });
    }
  },

  async atualizar(req, res) {
    try {
      const { id } = req.params;

      const livro = await Livro.findByPk(id);

      if (!livro) {
        return res.status(404).json({
          erro: 'Livro não encontrado',
          codigo: 404,
        });
      }

      await livro.update(req.body);

      return res.status(200).json(livro);
    } catch (error) {
      return res.status(400).json({
        erro: 'Erro ao atualizar livro',
        codigo: 400,
      });
    }
  },

  async remover(req, res) {
    try {
      const { id } = req.params;

      const livro = await Livro.findByPk(id);

      if (!livro) {
        return res.status(404).json({
          erro: 'Livro não encontrado',
          codigo: 404,
        });
      }

      await livro.destroy();

      return res.status(204).send();
    } catch (error) {
      return res.status(500).json({
        erro: 'Erro ao remover livro',
        codigo: 500,
      });
    }
  },
};