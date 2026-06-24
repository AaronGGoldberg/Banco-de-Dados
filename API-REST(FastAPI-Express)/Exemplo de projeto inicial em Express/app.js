// index.js
const express = require("express");
const app = express();

// Middleware: habilita leitura de JSON no corpo das requisições
app.use(express.json());

// Define a porta onde o servidor vai escutar
const PORT = 3000;

// Rota raiz: GET /
app.get("/", (req, res) => {
  res.send("Olá, Mundo! Minha primeira API com Express.");
});

let produtos = [
  { id: 1, nome: "Notebook", preco: 2500.0 },
  { id: 2, nome: "Mouse", preco: 89.9 },
  { id: 3, nome: "Teclado", preco: 149.0 },
];

// GET /produtos — retorna todos os produtos
app.get("/produtos", (req, res) => {
  res.status(200).json(produtos);
});

app.get("/produtos/:id", (req, res) => {
  const id = parseInt(req.params.id);
  const produto = produtos.find((p) => p.id === id);

  if (produto) {
    res.status(200).json(produto);
  } else {
    res.status(404).json({ mensagem: "Produto não encontrado" });
  }
});

app.post("/produtos", (req, res) => {
  const { nome, preco } = req.body;

  // Validação básica
  if (!nome || preco === undefined) {
    return res.status(400).json({ mensagem: "Nome e preço são obrigatórios" });
  }

  // Gera um ID incremental simples
  const novoId =
    produtos.length > 0 ? Math.max(...produtos.map((p) => p.id)) + 1 : 1;

  //Criando novo produto e adicionando à lista
  const novoProduto = { id: novoId, nome, preco };
  produtos.push(novoProduto);
  res.status(201).json(novoProduto); // 201 Created
});

// Inicia o servidor
app.listen(PORT, () => {
  console.log(`Servidor rodando em http://localhost:${PORT}`);
});
