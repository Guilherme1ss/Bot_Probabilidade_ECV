"""
Módulo responsável por extrair dados das páginas do UFMG
"""
import requests
from bs4 import BeautifulSoup
import unicodedata
from typing import Optional, Dict
import logging

from config.settings import REQUEST_TIMEOUT

logger = logging.getLogger(__name__)


def normalizar_texto(texto: str) -> str:
    """
    Normaliza texto removendo acentos e convertendo para maiúsculas
    
    Args:
        texto: String para normalizar
        
    Returns:
        String normalizada em maiúsculas sem acentos
    """
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto.upper()


def fazer_requisicao(url: str) -> BeautifulSoup:
    """
    Faz requisição HTTP e retorna objeto BeautifulSoup
    
    Args:
        url: URL para fazer a requisição
        
    Returns:
        Objeto BeautifulSoup com o HTML parseado
        
    Raises:
        requests.RequestException: Erro na requisição HTTP
    """
    try:
        logger.info(f"Fazendo requisição para: {url}")
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        logger.error(f"Erro na requisição para {url}: {e}")
        raise


def extrair_classificacao_geral(url: str, time_alvo: str) -> Optional[Dict[str, str]]:
    """
    Extrai dados da classificação geral do campeonato
    
    Args:
        url: URL da página de classificação geral
        time_alvo: Nome do time normalizado (ex: "VITORIA")
        
    Returns:
        Dicionário com dados da classificação ou None se não encontrado
    """
    try:
        soup = fazer_requisicao(url)
        tabela = soup.find("table")
        
        if not tabela:
            logger.warning("Tabela não encontrada na página")
            return None
            
        linhas = tabela.find_all("tr")

        for linha in linhas:
            cols = [c.get_text(strip=True) for c in linha.find_all("td")]
            
            if len(cols) < 11:
                continue
                
            if normalizar_texto(cols[1]) == time_alvo:
                logger.info(f"Time {time_alvo} encontrado na posição {cols[0]}")
                return {
                    "Posicao": cols[0] + "º",
                    "Pnts": cols[2],
                    "Jogos": cols[3] + "/38",
                    "Vitorias": cols[4],
                    "Empates": cols[5],
                    "Derrotas": cols[6],
                    "SG": cols[9],
                    "Rendimento": cols[10] + "%",
                }
        
        logger.warning(f"Time {time_alvo} não encontrado na tabela")
        return None
        
    except Exception as e:
        logger.error(f"Erro ao extrair classificação geral: {e}")
        return None


def extrair_probabilidade(url: str, time_alvo: str) -> Optional[str]:
    """
    Extrai probabilidade de um objetivo específico (Libertadores, Sula, Rebaixamento)
    
    Args:
        url: URL da página de probabilidades
        time_alvo: Nome do time normalizado (ex: "VITORIA")
        
    Returns:
        String com a probabilidade ou None se não encontrado
    """
    try:
        soup = fazer_requisicao(url)
        tabela = soup.find("table")
        
        if not tabela:
            logger.warning("Tabela não encontrada na página")
            return None
            
        linhas = tabela.find_all("tr")

        for linha in linhas:
            cols = [c.get_text(strip=True) for c in linha.find_all("td")]
            
            if len(cols) < 3:
                continue
                
            if normalizar_texto(cols[1]) == time_alvo:
                logger.info(f"Probabilidade encontrada para {time_alvo}: {cols[2]}")
                return cols[2]
        
        logger.warning(f"Probabilidade não encontrada para {time_alvo}")
        return None
        
    except Exception as e:
        logger.error(f"Erro ao extrair probabilidade: {e}")
        return None