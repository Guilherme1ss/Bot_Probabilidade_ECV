#!/bin/bash

# Script utilitário para executar o Vitória Bot

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função de ajuda
show_help() {
    echo "🔴⚫ Vitória Bot - Script de Execução"
    echo ""
    echo "Uso: ./run.sh [comando]"
    echo ""
    echo "Comandos:"
    echo "  test        Executa em modo teste (não posta no Twitter)"
    echo "  run         Executa o bot normalmente (posta no Twitter)"
    echo "  force       Força postagem mesmo se dados não mudaram"
    echo "  install     Instala as dependências"
    echo "  setup       Configuração inicial (instala deps e cria .env)"
    echo "  logs        Mostra os últimos logs"
    echo "  cache       Mostra o cache atual"
    echo "  clear-cache Limpa o cache (força próximo post)"
    echo "  clean       Limpa arquivos temporários e cache"
    echo "  help        Mostra esta mensagem"
    echo ""
}

# Verifica se Python está instalado
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 não encontrado. Por favor, instale Python 3.${NC}"
        exit 1
    fi
}

# Instala dependências
install_deps() {
    echo -e "${YELLOW}📦 Instalando dependências...${NC}"
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependências instaladas!${NC}"
}

# Setup inicial
setup() {
    echo -e "${YELLOW}🔧 Configurando Vitória Bot...${NC}"
    
    # Instala dependências
    install_deps
    
    # Cria .env se não existir
    if [ ! -f .env ]; then
        echo -e "${YELLOW}📝 Criando arquivo .env...${NC}"
        cp .env.example .env
        echo -e "${GREEN}✅ Arquivo .env criado!${NC}"
        echo -e "${YELLOW}⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais do Twitter${NC}"
    else
        echo -e "${GREEN}✅ Arquivo .env já existe${NC}"
    fi
    
    # Cria diretório de logs
    mkdir -p logs
    
    echo -e "${GREEN}✅ Setup concluído!${NC}"
}

# Executa em modo teste
run_test() {
    check_python
    echo -e "${YELLOW}🧪 Executando em modo teste...${NC}"
    python3 main.py --test
}

# Executa normalmente
run_bot() {
    check_python
    echo -e "${GREEN}🚀 Executando bot...${NC}"
    python3 main.py
}

# Executa forçado
run_force() {
    check_python
    echo -e "${YELLOW}⚠️  Executando bot em modo FORÇADO...${NC}"
    echo -e "${YELLOW}    (postará mesmo se dados não mudaram)${NC}"
    python3 main.py --force
}

# Mostra cache
show_cache() {
    if [ -f last_post_cache.json ]; then
        echo -e "${YELLOW}📦 Cache atual:${NC}"
        cat last_post_cache.json | python3 -m json.tool 2>/dev/null || cat last_post_cache.json
    else
        echo -e "${RED}❌ Arquivo de cache não encontrado${NC}"
        echo "    O cache será criado após o primeiro post bem-sucedido."
    fi
}

# Limpa cache
clear_cache() {
    if [ -f last_post_cache.json ]; then
        rm last_post_cache.json
        echo -e "${GREEN}✅ Cache limpo com sucesso${NC}"
        echo "    O próximo post será forçado."
    else
        echo -e "${YELLOW}⚠️  Cache não existe${NC}"
    fi
}

# Mostra logs
show_logs() {
    if [ -f logs/vitoria_bot.log ]; then
        echo -e "${YELLOW}📋 Últimas 50 linhas do log:${NC}"
        tail -n 50 logs/vitoria_bot.log
    else
        echo -e "${RED}❌ Arquivo de log não encontrado${NC}"
    fi
}

# Limpa arquivos temporários
clean() {
    echo -e "${YELLOW}🧹 Limpando arquivos temporários...${NC}"
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
    find . -type f -name "*.pyc" -delete 2>/dev/null
    find . -type f -name "*.pyo" -delete 2>/dev/null
    echo -e "${GREEN}✅ Limpeza concluída!${NC}"
}

# Processa comando
case "$1" in
    test)
        run_test
        ;;
    run)
        run_bot
        ;;
    force)
        run_force
        ;;
    install)
        install_deps
        ;;
    setup)
        setup
        ;;
    logs)
        show_logs
        ;;
    cache)
        show_cache
        ;;
    clear-cache)
        clear_cache
        ;;
    clean)
        clean
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo -e "${RED}❌ Comando desconhecido: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac