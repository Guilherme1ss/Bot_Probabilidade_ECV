
# 🔴⚫ Bot Twitter - EC Vitória

Bot automatizado que posta diariamente no Twitter as estatísticas do Esporte Clube Vitória no Campeonato Brasileiro Série A, incluindo classificação geral e probabilidades matemáticas.

## 📋 Funcionalidades

O bot coleta e posta automaticamente:

* **📊 Classificação Geral** : Posição, pontos, jogos, vitórias, empates, derrotas, saldo de gols e rendimento
* **⬇️🛑 Probabilidade de Rebaixamento** : Chance matemática de queda para Série B
* **🏆 Probabilidade de Classificação para Sul-Americana** : Chance de vaga na competição continental
* **🏆 Probabilidade de Classificação para Libertadores** : Chance de vaga na principal competição da América do Sul

### Exemplo de Tweet

```
EC VITÓRIA 🔴⚫
📅 29/12/25

📊 Serie A
Posicao: 11º
Pnts: 45
Jogos: 38/38
🎯 V: 12 | E: 9 | D: 17
SG: -8
Rendimento: 39.47%

⬇️🛑 Risco de Rebaixamento
(%): 0.00%

🏆 Classificação Sula
(%): 15.30%

🏆 Classificação Libertadores
(%): 0.50%

Fonte: UFMG
```

## 🚀 Como Usar

### Pré-requisitos

* Conta no Twitter/X com API access
* Conta no GitHub
* Python 3.13+ (para testes locais)

### Configuração

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```
2. **Obtenha as credenciais da API do Twitter**
   * Acesse [Twitter Developer Portal](https://developer.twitter.com/)
   * Crie um novo app ou use um existente
   * Gere as seguintes credenciais:
     * API Key (Consumer Key)
     * API Secret (Consumer Secret)
     * Access Token
     * Access Token Secret
3. **Configure os Secrets no GitHub**
   * Vá em `Settings` → `Secrets and variables` → `Actions`
   * Adicione os seguintes secrets:
     * `API_KEY`
     * `API_SECRET`
     * `ACCESS_TOKEN`
     * `ACCESS_TOKEN_SECRET`
4. **Crie o arquivo requirements.txt**
   ```txt
   requests==2.31.0
   beautifulsoup4==4.12.3
   tweepy==4.14.0
   ```

### Execução Local (Testes)

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
export API_KEY="sua_api_key"
export API_SECRET="sua_api_secret"
export ACCESS_TOKEN="seu_access_token"
export ACCESS_TOKEN_SECRET="seu_access_token_secret"

# Executar o script
python main.py
```

### Automação via GitHub Actions

O bot está configurado para rodar automaticamente:

* **Horário** : Todos os dias às 14h UTC (11h horário de Brasília)
* **Execução manual** : Disponível através da aba `Actions` no GitHub

Para executar manualmente:

1. Vá em `Actions` no repositório
2. Selecione `Post diario no Twitter`
3. Clique em `Run workflow`

## 🔧 Personalização

### Alterar o time

No arquivo `main.py`, modifique a variável:

```python
TIME_ALVO = "VITORIA"  # Altere para o nome do seu time
```

### Alterar o horário de postagem

No arquivo `daily_post.yml`, modifique a linha do cron:

```yaml
- cron: '0 14 * * *'  # Formato: minuto hora dia mês dia-da-semana
```

Exemplos:

* `0 12 * * *` - Meio-dia UTC (9h Brasília)
* `0 18 * * *` - 18h UTC (15h Brasília)
* `0 21 * * 1-5` - 21h UTC apenas em dias úteis

## 📦 Estrutura do Projeto

```
.
├── main.py              # Script principal do bot
├── daily_post.yml       # Configuração do GitHub Actions
├── requirements.txt     # Dependências Python
└── README.md           # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

* **Python 3.13** : Linguagem principal
* **Tweepy** : Biblioteca para API do Twitter
* **BeautifulSoup4** : Web scraping dos dados
* **Requests** : Requisições HTTP
* **GitHub Actions** : Automação e agendamento

## 📊 Fonte dos Dados

Os dados são obtidos do site de estatísticas de futebol da **UFMG** (Universidade Federal de Minas Gerais):

* https://www.mat.ufmg.br/futebol/

## ⚠️ Observações

* O bot respeita o limite de 280 caracteres do Twitter
* Se o tweet ultrapassar o limite, será truncado automaticamente
* As probabilidades são calculadas matematicamente pela UFMG
* O horário padrão é 11h (horário de Brasília) durante toda a temporada

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto é de código aberto e está disponível para uso pessoal e educacional.

## 👤 Autor

Criado com ❤️ por [@Guilherme1ss](https://github.com/Guilherme1ss) — um torcedor do Vitória!

---

**Pega Leão! 🔴⚫**
