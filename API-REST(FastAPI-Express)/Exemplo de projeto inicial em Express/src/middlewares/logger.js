function logger(req, res, next) {
  const agora = new Date().toISOString();
  console.log(`[${agora}] ${req.method} ${req.url}`);
  next(); // OBRIGATÓRIO: passa para o próximo middleware/rota
}
module.exports = logger;
