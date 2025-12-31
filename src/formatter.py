"""
Módulo responsável por formatar tweets com os dados coletados
"""
from datetime import datetime
from typing import Dict, Optional
import logging

from config.settings import (
    EMOJIS, LABELS, MAX_TWEET_LENGTH, 
    TIME_ALVO, EMOJI_TIME
)

logger = logging.getLogger(__name__)


def formatar_classificacao(dados: Dict[str, str]) -> str:
    """
    Formata seção da classificação geral
    
    Args:
        dados: Dicionário com dados da classificação
        
    Returns:
        String formatada com dados da classificação
    """
    vitorias = dados.get("Vitorias", "0")
    empates = dados.get("Empates", "0")
    derrotas = dados.get("Derrotas", "0")
    
    return (
        f"\n{EMOJIS['classificacao']} Serie A\n"
        f"Posicao: {dados['Posicao']}\n"
        f"Pnts: {dados['Pnts']}\n"
        f"Jogos: {dados['Jogos']}\n"
        f"{EMOJIS['gols']} V: {vitorias} | E: {empates} | D: {derrotas}\n"
        f"SG: {dados['SG']}\n"
        f"Rendimento: {dados['Rendimento']}"
    )


def formatar_probabilidade(tipo: str, probabilidade: str) -> str:
    """
    Formata linha de probabilidade
    
    Args:
        tipo: Tipo da probabilidade (rebaixamento, sulamericana, libertadores)
        probabilidade: Valor da probabilidade
        
    Returns:
        String formatada com emoji, label e probabilidade
    """
    try:
        prob_float = float(probabilidade.replace(",", "."))
        emoji = EMOJIS.get(tipo, "")
        label = LABELS.get(tipo, tipo.capitalize())
        return f"{emoji} {label}\n(%): {prob_float:.2f}%"
    except ValueError:
        logger.warning(f"Erro ao converter probabilidade: {probabilidade}")
        return f"{EMOJIS.get(tipo, '')} {LABELS.get(tipo, tipo)}: {probabilidade}"


def gerar_tweet(
    classificacao: Optional[Dict[str, str]],
    probabilidades: Dict[str, Optional[str]]
) -> str:
    """
    Gera o texto completo do tweet
    
    Args:
        classificacao: Dados da classificação geral
        probabilidades: Dicionário com probabilidades de cada objetivo
        
    Returns:
        String com o tweet formatado
    """
    # Cabeçalho
    partes = [
        f"EC VITÓRIA {EMOJI_TIME}",
        f"{EMOJIS['calendario']} {datetime.now().strftime('%d/%m/%y')}"
    ]

    # Classificação Geral
    if classificacao:
        partes.append(formatar_classificacao(classificacao))
    else:
        logger.warning("Dados de classificação não disponíveis")
        partes.append(f"\n{EMOJIS['classificacao']} Dados indisponíveis")

    # Probabilidades
    for tipo, prob in probabilidades.items():
        if prob:
            partes.append(formatar_probabilidade(tipo, prob))
        else:
            logger.warning(f"Probabilidade de {tipo} não disponível")

    # Rodapé
    partes.append("\nFonte: UFMG")

    tweet = "\n".join(partes)

    # Limitar tamanho
    if len(tweet) > MAX_TWEET_LENGTH:
        logger.warning(f"Tweet excedeu {MAX_TWEET_LENGTH} caracteres ({len(tweet)})")
        tweet = tweet[:MAX_TWEET_LENGTH - 3] + "..."

    return tweet


def criar_thread(texto_longo: str, max_length: int = 280) -> list[str]:
    """
    Divide texto longo em múltiplos tweets para thread
    
    Args:
        texto_longo: Texto completo a ser dividido
        max_length: Tamanho máximo de cada tweet
        
    Returns:
        Lista de strings, cada uma representando um tweet
    """
    # Implementação futura para threads
    linhas = texto_longo.split("\n")
    tweets = []
    tweet_atual = ""
    
    for linha in linhas:
        if len(tweet_atual) + len(linha) + 1 <= max_length:
            tweet_atual += linha + "\n"
        else:
            if tweet_atual:
                tweets.append(tweet_atual.strip())
            tweet_atual = linha + "\n"
    
    if tweet_atual:
        tweets.append(tweet_atual.strip())
    
    return tweets