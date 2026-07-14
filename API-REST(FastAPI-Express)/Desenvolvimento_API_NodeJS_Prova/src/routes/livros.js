const express = require('express');
const LivroController = require('../controllers/LivroController');
const validarLivro = require('../middlewares/validarLivro');

const router = express.Router();

router.get('/', LivroController.listar);
router.get('/:id', LivroController.buscar);
router.post('/', validarLivro, LivroController.criar);
router.put('/:id', validarLivro, LivroController.atualizar);
router.delete('/:id', LivroController.remover);

module.exports = router;