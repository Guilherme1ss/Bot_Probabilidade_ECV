"""
Configurações centralizadas do bot
"""
import os
from typing import Dict
from pathlib import Path

# Carrega variáveis de ambiente do arquivo .env
try:
    from dotenv import load_dotenv
    # Procura o .env na raiz do projeto
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
except ImportError:
    # Se python-dotenv não estiver instalado, continua sem ele
    # (variáveis podem vir do sistema operacional)
    pass

# URLs de dados do UFMG
URLS: Dict[str, str] = {
    "classificacao_geral": "https://www.mat.ufmg.br/futebol/classificacao-geral_seriea/",
    "rebaixamento": "https://www.mat.ufmg.br/futebol/rebaixamento_seriea/",
    "sulamericana": "https://www.mat.ufmg.br/futebol/classificacao-para-sulamericana_seriea/",
    "libertadores": "https://www.mat.ufmg.br/futebol/classificacao-para-libertadores_seriea/"
}

# Configurações do time
TIME_ALVO = "VITORIA"
EMOJI_TIME = "🔴⚫"

# Emojis para as seções
EMOJIS = {
    "rebaixamento": "⬇🛑",
    "sulamericana": "🏆",
    "libertadores": "🏆",
    "classificacao": "📊",
    "calendario": "📅",
    "gols": "🎯"
}

# Labels personalizados
LABELS = {
    "rebaixamento": "Risco de Rebaixamento",
    "sulamericana": "Classificação Sula",
    "libertadores": "Classificação Libertadores"
}

# Configurações do Twitter
TWITTER_CONFIG = {
    "consumer_key": os.getenv("API_KEY"),
    "consumer_secret": os.getenv("API_SECRET"),
    "access_token": os.getenv("ACCESS_TOKEN"),
    "access_token_secret": os.getenv("ACCESS_TOKEN_SECRET")
}

# Configurações de requisição
REQUEST_TIMEOUT = 15
MAX_TWEET_LENGTH = 280

# Configurações de log
LOG_DIR = "logs"
LOG_FILE = "vitoria_bot.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"