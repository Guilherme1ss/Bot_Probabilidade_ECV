import logging
import sys
from typing import Dict, Optional

from config.settings import URLS, TIME_ALVO, LOG_DIR, LOG_FILE, LOG_FORMAT
from src.scraper import extrair_classificacao_geral, extrair_probabilidade
from src.formatter import gerar_tweet
from src.twitter_client import TwitterClient
from src.cache import salvar_dados_cache, carregar_dados_cache, dados_mudaram


def configurar_logging() -> None:
    """Configura o sistema de logging"""
    import os
    
    # Cria diretório de logs se não existir
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # Configura logging com encoding UTF-8 para Windows
    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE), encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Fix para encoding no Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def coletar_dados() -> tuple[Optional[Dict], Dict[str, Optional[str]]]:
    """
    Coleta todos os dados necessários das páginas do UFMG
    
    Returns:
        Tupla com (classificação geral, dicionário de probabilidades)
    """
    logger = logging.getLogger(__name__)
    logger.info("Iniciando coleta de dados")
    
    # Classificação geral
    classificacao = extrair_classificacao_geral(
        URLS["classificacao_geral"], 
        TIME_ALVO
    )
    
    # Probabilidades
    probabilidades = {}
    for tipo in ["rebaixamento", "sulamericana", "libertadores"]:
        prob = extrair_probabilidade(URLS[tipo], TIME_ALVO)
        probabilidades[tipo] = prob
    
    logger.info("Coleta de dados finalizada")
    return classificacao, probabilidades


def executar_bot(modo_teste: bool = False, forcar_post: bool = False) -> bool:
    """
    Executa o fluxo completo do bot
    
    Args:
        modo_teste: Se True, apenas exibe o tweet sem postar
        forcar_post: Se True, posta mesmo se os dados não mudaram
        
    Returns:
        True se executado com sucesso, False caso contrário
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Coleta dados
        classificacao, probabilidades = coletar_dados()
        
        # Carrega cache anterior
        cache = carregar_dados_cache()
        
        # Verifica se os dados mudaram
        if not forcar_post and not dados_mudaram(classificacao, probabilidades, cache):
            logger.info("=" * 60)
            logger.info("⏭️  DADOS NÃO MUDARAM - Post cancelado")
            logger.info("=" * 60)
            logger.info("Os dados são idênticos ao último post.")
            logger.info("Nenhum tweet será postado para evitar duplicação.")
            logger.info("Use --force para forçar postagem mesmo assim.")
            return True  # Não é erro, apenas não há nada para postar
        
        # Gera tweet
        tweet = gerar_tweet(classificacao, probabilidades)
        logger.info(f"Tweet gerado:\n{'-'*50}\n{tweet}\n{'-'*50}")
        
        if modo_teste:
            logger.info("Modo teste ativado - tweet não será postado")
            print("\n" + "="*60)
            print("PREVIEW DO TWEET:")
            print("="*60)
            print(tweet)
            print("="*60)
            print(f"Caracteres: {len(tweet)}/280")
            print("="*60)
            return True
        
        # Posta no Twitter
        logger.info("Iniciando postagem no Twitter")
        cliente = TwitterClient()
        resultado = cliente.postar_tweet(tweet)
        
        if resultado:
            logger.info("✅ Bot executado com sucesso!")
            # Salva dados no cache após postagem bem-sucedida
            salvar_dados_cache(classificacao, probabilidades)
            logger.info("Cache atualizado com sucesso")
            return True
        else:
            logger.error("❌ Falha ao postar tweet")
            return False
            
    except Exception as e:
        logger.error(f"Erro durante execução do bot: {e}", exc_info=True)
        return False


def main():
    """Função principal"""
    configurar_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("="*60)
    logger.info("Iniciando Vitória Bot")
    logger.info("="*60)
    
    # Verifica flags
    modo_teste = "--test" in sys.argv or "-t" in sys.argv
    forcar_post = "--force" in sys.argv or "-f" in sys.argv
    
    if forcar_post:
        logger.info("⚠️  Modo FORÇAR ativado - postará mesmo se dados não mudaram")
    
    sucesso = executar_bot(modo_teste=modo_teste, forcar_post=forcar_post)
    
    if sucesso:
        logger.info("Bot finalizado com sucesso")
        sys.exit(0)
    else:
        logger.error("Bot finalizado com erros")
        sys.exit(1)


if __name__ == "__main__":
    main()