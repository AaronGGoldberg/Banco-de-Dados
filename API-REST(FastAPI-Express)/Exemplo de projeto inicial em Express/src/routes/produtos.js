const express = require("express");
const router = express.Router();

const ProdutoController = require("../controllers/ProdutoController");
const validarProduto = require("../middlewares/validarProduto");

router.get("/", ProdutoController.listar);
router.get("/:id", ProdutoController.buscar);
router.post("/", validarProduto, ProdutoController.criar);
router.put("/:id", validarProduto, ProdutoController.atualizar);
router.delete("/:id", ProdutoController.remover);
module.exports = router;
