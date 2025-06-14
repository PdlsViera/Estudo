const express = require('express')
const app = express()
const port = 2000

app.use(express.json());

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})


function somar(a, b) {
  return a + b;
}

app.get('/', (req, res) => {
  res.send('Função get funcionando')
})

app.post('/', (req, res) => {
  res.send('Função post funcionando')
})

app.post('/user', (req, res) => {
  const dados = req.body;
  console.log(dados)
  res.json({
    mensagem: 'Informações recebidas com sucesso',
    dadosRecebidos: dados,
    numeroDeItens: Object.keys(req.body).length
  });
});

app.post('/somar', (req, res) => {
   const {a,b} = req.body;
   const resultado = somar(a,b);
   console.log(req.body)
   res.json({resultado});
});

app.put('/user', (req, res) => {
  res.send('Função put funcionando')
})


