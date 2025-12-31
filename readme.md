# 🔴⚫ Vitória Bot - Bot do EC Vitória

Bot automatizado que coleta estatísticas do EC Vitória do site da UFMG e posta atualizações no Twitter.

## 🤖 Automação

## 📋 Funcionalidades

* ✅ Coleta dados da classificação geral do Brasileirão Série A
* ✅ Extrai probabilidades de rebaixamento
* ✅ Extrai probabilidades de classificação para Libertadores
* ✅ Extrai probabilidades de classificação para Sul-Americana
* ✅ **Verifica se dados mudaram antes de postar (evita duplicação)**
* ✅ Formata tweet com todas as informações
* ✅ Posta automaticamente no Twitter
* ✅ **Roda 2x por dia: 9h e 22h**
* ✅ Sistema de logs completo
* ✅ Modo de teste para visualizar tweet antes de postar

## 🏗️ Estrutura do Projeto

```
vitoria-bot/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configurações centralizadas
├── src/
│   ├── __init__.py 
│   ├── cache.py
│   ├── scraper.py           # Coleta de dados (web scraping)
│   ├── formatter.py         # Formatação de tweets
│   └── twitter_client.py    # Integração com Twitter API
├── tests/
│   └── test_bot.py
├── logs/
│   └── vitoria_bot.log      # Arquivo de log
├── main.py                  # Script principal
├── requirements.txt         # Dependências
└── README.md               # Este arquivo
```

## 🚀 Instalação

### 1. Clone o repositório (ou copie os arquivos)

### 2. Instale as dependências

bash

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` ou exporte as variáveis:

bash

```bash
exportAPI_KEY="sua_consumer_key"
exportAPI_SECRET="sua_consumer_secret"
exportACCESS_TOKEN="seu_access_token"
exportACCESS_TOKEN_SECRET="seu_access_token_secret"
```

#### Como obter credenciais do Twitter:

1. Acesse [https://developer.twitter.com/](https://developer.twitter.com/)
2. Crie um App no Twitter Developer Portal
3. Gere as credenciais necessárias (API Key, API Secret, Access Token, Access Token Secret)
4. Configure as permissões de leitura e escrita

## 💻 Uso

### Modo Normal (posta no Twitter)

bash

```bash
python main.py
```

 **Importante** : Só posta se os dados mudaram desde o último post!

### Modo Teste (apenas visualiza o tweet)

bash

```bash
python main.py --test
# ou
python main.py -t
```

O modo teste é útil para:

* Verificar se os dados estão sendo coletados corretamente
* Visualizar como o tweet ficará formatado
* Testar sem fazer postagens reais

### Modo Forçar (posta mesmo se dados não mudaram)

bash

```bash
python main.py --force
# ou
python main.py -f
```

### Combinar flags

bash

```bash
# Testar modo forçado sem postar
python main.py --test --force
```

## 🎯 Personalização

### Alterar o time

Edite `config/settings.py`:

python

```python
TIME_ALVO ="NOME_DO_TIME"# Em maiúsculas, sem acentos
EMOJI_TIME ="🔵⚪"# Emojis do seu time
```

### Alterar emojis e labels

Edite os dicionários `EMOJIS` e `LABELS` em `config/settings.py`

### Modificar formato do tweet

Edite as funções em `src/formatter.py`

## 📊 Exemplo de Tweet

```
EC VITÓRIA 🔴⚫
📅 31/12/25

📊 Serie A
Posicao: 12º
Pnts: 45
Jogos: 38/38
🎯 V: 12 | E: 9 | D: 17
SG: -8
Rendimento: 39.47%
⬇🛑 Risco de Rebaixamento
(%): 0.02%
🏆 Classificação Sula
(%): 0.00%
🏆 Classificação Libertadores
(%): 0.00%

Fonte: UFMG
```

## 🔧 Manutenção

### Logs

Os logs são salvos em `logs/vitoria_bot.log` e contêm:

* Requisições HTTP realizadas
* Dados extraídos
* Tweets gerados
* Erros e avisos

### Tratamento de Erros

O bot possui tratamento de erros para:

* Falhas de conexão
* Páginas indisponíveis
* Dados incompletos
* Erros de autenticação do Twitter
* Limites de API

### GitHub Actions

Exemplo de workflow (`.github/workflows/bot.yml`):

```yaml
name: Vitória Bot

on:
  schedule:
    - cron: '0 18 * * *'  # Diariamente às 18h UTC
  workflow_dispatch:  # Permite execução manual

jobs:
  run-bot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
  
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
  
      - name: Install dependencies
        run: pip install -r requirements.txt
  
      - name: Run bot
        env:
          API_KEY: ${{ secrets.API_KEY }}
          API_SECRET: ${{ secrets.API_SECRET }}
          ACCESS_TOKEN: ${{ secrets.ACCESS_TOKEN }}
          ACCESS_TOKEN_SECRET: ${{ secrets.ACCESS_TOKEN_SECRET }}
        run: python main.py
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

* Reportar bugs
* Sugerir novas funcionalidades
* Enviar pull requests

## ⚠️ Avisos Importantes

1. **Respeite os limites da API do Twitter** - não execute o bot com muita frequência
2. **Verifique os Termos de Uso** da UFMG antes de fazer scraping em larga escala
3. **Mantenha suas credenciais seguras** - nunca commite credenciais no git

## 📄 Licença

Este projeto é open source. Use-o livremente para fins educacionais e pessoais.

## 🙏 Créditos

* Dados: [UFMG - Matemática do Futebol](https://www.mat.ufmg.br/futebol/)
* Time: EC Vitória 🔴⚫

## 👤 Autor

Criado com ❤️ por [@Guilherme1ss](https://github.com/Guilherme1ss) — um torcedor do Vitória, para a torcida do Colossal!

---

**Pega Leão! 🔴⚫**
