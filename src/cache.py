"""
Módulo para gerenciar cache do último post
"""
import json
import os
import logging
from typing import Optional, Dict
from pathlib import Path

logger = logging.getLogger(__name__)

CACHE_FILE = "last_post_cache.json"


def salvar_dados_cache(classificacao: Dict, probabilidades: Dict[str, str]) -> None:
    """
    Salva os dados do último post em cache
    
    Args:
        classificacao: Dados da classificação geral
        probabilidades: Dicionário com probabilidades
    """
    try:
        cache_data = {
            "classificacao": classificacao,
            "probabilidades": probabilidades
        }
        
        cache_path = Path(CACHE_FILE)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Cache salvo em: {cache_path}")
        
    except Exception as e:
        logger.error(f"Erro ao salvar cache: {e}")


def carregar_dados_cache() -> Optional[Dict]:
    """
    Carrega os dados do último post do cache
    
    Returns:
        Dicionário com dados do cache ou None se não existir
    """
    try:
        cache_path = Path(CACHE_FILE)
        
        if not cache_path.exists():
            logger.info("Arquivo de cache não existe ainda")
            return None
        
        with open(cache_path, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        logger.info("Cache carregado com sucesso")
        return cache_data
        
    except Exception as e:
        logger.error(f"Erro ao carregar cache: {e}")
        return None


def dados_mudaram(
    classificacao_nova: Dict, 
    probabilidades_novas: Dict[str, str],
    cache: Optional[Dict]
) -> bool:
    """
    Compara dados novos com o cache para verificar se houve mudança
    
    Args:
        classificacao_nova: Dados novos da classificação
        probabilidades_novas: Probabilidades novas
        cache: Dados do cache anterior
        
    Returns:
        True se os dados mudaram, False se são iguais
    """
    if cache is None:
        logger.info("Sem cache anterior - dados considerados como novos")
        return True
    
    try:
        classificacao_antiga = cache.get("classificacao")
        probabilidades_antigas = cache.get("probabilidades")
        
        # Compara classificação
        if classificacao_nova != classificacao_antiga:
            logger.info("Classificação mudou!")
            logger.debug(f"Antiga: {classificacao_antiga}")
            logger.debug(f"Nova: {classificacao_nova}")
            return True
        
        # Compara probabilidades
        if probabilidades_novas != probabilidades_antigas:
            logger.info("Probabilidades mudaram!")
            logger.debug(f"Antigas: {probabilidades_antigas}")
            logger.debug(f"Novas: {probabilidades_novas}")
            return True
        
        logger.info("Dados NÃO mudaram - nenhuma alteração detectada")
        return False
        
    except Exception as e:
        logger.error(f"Erro ao comparar dados: {e}")
        # Em caso de erro, considera como mudado para não perder post
        return True


def limpar_cache() -> bool:
    """
    Remove o arquivo de cache
    
    Returns:
        True se removido com sucesso, False caso contrário
    """
    try:
        cache_path = Path(CACHE_FILE)
        
        if cache_path.exists():
            cache_path.unlink()
            logger.info("Cache removido com sucesso")
            return True
        else:
            logger.info("Cache não existe")
            return False
            
    except Exception as e:
        logger.error(f"Erro ao remover cache: {e}")
        return False