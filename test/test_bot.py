"""
Exemplos de testes unitários para o bot
Para executar: pytest tests/
"""
import unittest
from unittest.mock import Mock, patch
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scraper import normalizar_texto
from src.formatter import formatar_classificacao, formatar_probabilidade


class TestScraper(unittest.TestCase):
    """Testes para o módulo scraper"""
    
    def test_normalizar_texto(self):
        """Testa normalização de texto"""
        self.assertEqual(normalizar_texto("Vitória"), "VITORIA")
        self.assertEqual(normalizar_texto("São Paulo"), "SAO PAULO")
        self.assertEqual(normalizar_texto("Grêmio"), "GREMIO")
    
    def test_normalizar_texto_minusculas(self):
        """Testa que minúsculas são convertidas"""
        self.assertEqual(normalizar_texto("flamengo"), "FLAMENGO")


class TestFormatter(unittest.TestCase):
    """Testes para o módulo formatter"""
    
    def test_formatar_classificacao(self):
        """Testa formatação da classificação"""
        dados = {
            "Posicao": "12º",
            "Pnts": "45",
            "Jogos": "38/38",
            "Vitorias": "12",
            "Empates": "9",
            "Derrotas": "17",
            "SG": "-8",
            "Rendimento": "39.47%"
        }
        
        resultado = formatar_classificacao(dados)
        
        self.assertIn("12º", resultado)
        self.assertIn("45", resultado)
        self.assertIn("38/38", resultado)
        self.assertIn("V: 12", resultado)
    
    def test_formatar_probabilidade(self):
        """Testa formatação de probabilidade"""
        resultado = formatar_probabilidade("rebaixamento", "15,5")
        
        self.assertIn("15.50%", resultado)
        self.assertIn("Rebaixamento", resultado)
    
    def test_formatar_probabilidade_valor_invalido(self):
        """Testa formatação com valor inválido"""
        resultado = formatar_probabilidade("libertadores", "N/A")
        
        self.assertIn("N/A", resultado)


class TestTwitterClient(unittest.TestCase):
    """Testes para o cliente do Twitter"""
    
    @patch('src.twitter_client.tweepy.Client')
    def test_postar_tweet(self, mock_client):
        """Testa postagem de tweet"""
        from src.twitter_client import TwitterClient
        
        # Mock da resposta
        mock_response = Mock()
        mock_response.data = {"id": "123456"}
        mock_client.return_value.create_tweet.return_value = mock_response
        
        # Simula credenciais
        with patch('src.twitter_client.TWITTER_CONFIG', {
            'consumer_key': 'test',
            'consumer_secret': 'test',
            'access_token': 'test',
            'access_token_secret': 'test'
        }):
            cliente = TwitterClient()
            resultado = cliente.postar_tweet("Tweet de teste")
            
            self.assertIsNotNone(resultado)
            self.assertEqual(resultado["id"], "123456")


if __name__ == '__main__':
    unittest.main()