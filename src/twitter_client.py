"""
Módulo responsável por interagir com a API do Twitter
"""
import tweepy
import logging
from typing import Optional

from config.settings import TWITTER_CONFIG

logger = logging.getLogger(__name__)


class TwitterClient:
    """Cliente para interação com a API do Twitter"""
    
    def __init__(self):
        """Inicializa o cliente do Twitter com as credenciais"""
        self._validar_credenciais()
        self.client = self._criar_cliente()
    
    def _validar_credenciais(self) -> None:
        """
        Valida se todas as credenciais necessárias estão disponíveis
        
        Raises:
            ValueError: Se alguma credencial estiver faltando
        """
        credenciais_faltantes = [
            key for key, value in TWITTER_CONFIG.items() 
            if not value
        ]
        
        if credenciais_faltantes:
            erro = f"Credenciais faltando: {', '.join(credenciais_faltantes)}"
            logger.error(erro)
            raise ValueError(erro)
    
    def _criar_cliente(self) -> tweepy.Client:
        """
        Cria instância do cliente do Twitter
        
        Returns:
            Cliente configurado do tweepy
        """
        try:
            return tweepy.Client(
                consumer_key=TWITTER_CONFIG["consumer_key"],
                consumer_secret=TWITTER_CONFIG["consumer_secret"],
                access_token=TWITTER_CONFIG["access_token"],
                access_token_secret=TWITTER_CONFIG["access_token_secret"]
            )
        except Exception as e:
            logger.error(f"Erro ao criar cliente do Twitter: {e}")
            raise
    
    def postar_tweet(self, texto: str) -> Optional[dict]:
        """
        Posta um tweet
        
        Args:
            texto: Conteúdo do tweet
            
        Returns:
            Dados do tweet postado ou None em caso de erro
        """
        try:
            logger.info(f"Postando tweet ({len(texto)} caracteres)")
            response = self.client.create_tweet(text=texto)
            logger.info(f"Tweet postado com sucesso. ID: {response.data.get('id')}")
            return response.data
        except tweepy.TweepyException as e:
            logger.error(f"Erro ao postar tweet: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao postar tweet: {e}")
            return None
    
    def postar_thread(self, tweets: list[str]) -> Optional[list[dict]]:
        """
        Posta uma thread de tweets
        
        Args:
            tweets: Lista de textos para postar em sequência
            
        Returns:
            Lista com dados de cada tweet postado ou None em caso de erro
        """
        try:
            resultados = []
            tweet_anterior_id = None
            
            for i, texto in enumerate(tweets, 1):
                logger.info(f"Postando tweet {i}/{len(tweets)}")
                
                if tweet_anterior_id:
                    response = self.client.create_tweet(
                        text=texto,
                        in_reply_to_tweet_id=tweet_anterior_id
                    )
                else:
                    response = self.client.create_tweet(text=texto)
                
                tweet_anterior_id = response.data.get('id')
                resultados.append(response.data)
                logger.info(f"Tweet {i} postado. ID: {tweet_anterior_id}")
            
            logger.info(f"Thread de {len(tweets)} tweets postada com sucesso")
            return resultados
            
        except tweepy.TweepyException as e:
            logger.error(f"Erro ao postar thread: {e}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao postar thread: {e}")
            return None
    
    def deletar_tweet(self, tweet_id: str) -> bool:
        """
        Deleta um tweet
        
        Args:
            tweet_id: ID do tweet a ser deletado
            
        Returns:
            True se deletado com sucesso, False caso contrário
        """
        try:
            logger.info(f"Deletando tweet ID: {tweet_id}")
            self.client.delete_tweet(tweet_id)
            logger.info("Tweet deletado com sucesso")
            return True
        except tweepy.TweepyException as e:
            logger.error(f"Erro ao deletar tweet: {e}")
            return False
        except Exception as e:
            logger.error(f"Erro inesperado ao deletar tweet: {e}")
            return False