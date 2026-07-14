function validarLivro(req, res, next) {
  const erros = [];
  const { titulo, autor, editora, isbn, preco, estoque, ano_publicacao } = req.body;

  if (!titulo) erros.push('O campo titulo é obrigatório');
  if (!autor) erros.push('O campo autor é obrigatório');
  if (!editora) erros.push('O campo editora é obrigatório');
  if (!isbn) erros.push('O campo isbn é obrigatório');

  if (preco === undefined) {
    erros.push('O campo preco é obrigatório');
  } else if (isNaN(preco) || Number(preco) <= 0) {
    erros.push('O preco deve ser um número positivo');
  }

  if (estoque === undefined) {
    erros.push('O campo estoque é obrigatório');
  } else if (!Number.isInteger(Number(estoque)) || Number(estoque) < 0) {
    erros.push('O estoque deve ser um número inteiro maior ou igual a zero');
  }

  if (ano_publicacao === undefined) {
    erros.push('O campo ano_publicacao é obrigatório');
  } else if (!Number.isInteger(Number(ano_publicacao)) || Number(ano_publicacao) < 1000) {
    erros.push('O ano_publicacao deve ser um ano válido');
  }

  if (erros.length > 0) {
    return res.status(400).json({ erros });
  }

  next();
}

module.exports = validarLivro;