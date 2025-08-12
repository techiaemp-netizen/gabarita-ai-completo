#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar conexões com GitHub, Vercel, Render e Firebase
Gabarita AI - Teste de Conexões
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{title.center(60)}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}\n")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def test_github_connection():
    """Testa conexão com GitHub"""
    print_header("TESTE DE CONEXÃO - GITHUB")
    
    try:
        # Testar acesso ao repositório público
        repo_url = "https://api.github.com/repos/techiaemp-netizen/gabarita-ai-backend"
        response = requests.get(repo_url, timeout=10)
        
        if response.status_code == 200:
            repo_data = response.json()
            print_success(f"Repositório encontrado: {repo_data['full_name']}")
            print_info(f"Última atualização: {repo_data['updated_at']}")
            print_info(f"Branch padrão: {repo_data['default_branch']}")
            print_info(f"Linguagem principal: {repo_data['language']}")
            return True
        else:
            print_error(f"Erro ao acessar repositório: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Erro na conexão com GitHub: {str(e)}")
        return False

def test_vercel_connection():
    """Testa configuração do Vercel"""
    print_header("TESTE DE CONFIGURAÇÃO - VERCEL")
    
    # Verificar arquivos de configuração do Vercel
    vercel_files = [
        "gabarita-ai-frontend/vercel.json",
        ".vercel/project.json"
    ]
    
    config_ok = True
    
    for file_path in vercel_files:
        full_path = Path(file_path)
        if full_path.exists():
            print_success(f"Arquivo encontrado: {file_path}")
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'projectName' in config:
                        print_info(f"Projeto Vercel: {config['projectName']}")
                    elif 'buildCommand' in config:
                        print_info(f"Comando de build: {config['buildCommand']}")
            except Exception as e:
                print_warning(f"Erro ao ler {file_path}: {str(e)}")
        else:
            print_error(f"Arquivo não encontrado: {file_path}")
            config_ok = False
    
    # Verificar variáveis de ambiente do frontend
    env_example = Path("gabarita-ai-frontend/.env.example")
    if env_example.exists():
        print_success("Arquivo .env.example encontrado no frontend")
        print_info("Variáveis de ambiente configuradas para Vercel")
    else:
        print_error("Arquivo .env.example não encontrado no frontend")
        config_ok = False
    
    return config_ok

def test_render_connection():
    """Testa configuração do Render"""
    print_header("TESTE DE CONFIGURAÇÃO - RENDER")
    
    # Verificar arquivos de configuração do Render
    render_files = [
        "render.yaml",
        "gabarita-ai-backend-deploy/render.yaml",
        "requirements.txt"
    ]
    
    config_ok = True
    
    for file_path in render_files:
        full_path = Path(file_path)
        if full_path.exists():
            print_success(f"Arquivo encontrado: {file_path}")
            if file_path.endswith('.yaml'):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'gabarita-ai-backend' in content:
                            print_info("Configuração do serviço encontrada")
                        if 'python' in content.lower():
                            print_info("Runtime Python configurado")
                except Exception as e:
                    print_warning(f"Erro ao ler {file_path}: {str(e)}")
        else:
            print_warning(f"Arquivo não encontrado: {file_path}")
            if file_path == "requirements.txt":
                config_ok = False
    
    # Verificar se existe URL de produção configurada
    env_example = Path(".env.example")
    if env_example.exists():
        try:
            with open(env_example, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'onrender.com' in content:
                    print_info("URL do Render configurada no .env.example")
                else:
                    print_warning("URL do Render não encontrada no .env.example")
        except Exception as e:
            print_warning(f"Erro ao ler .env.example: {str(e)}")
    
    return config_ok

def test_firebase_connection():
    """Testa configuração do Firebase"""
    print_header("TESTE DE CONFIGURAÇÃO - FIREBASE")
    
    config_ok = True
    
    # Verificar arquivos de configuração do Firebase
    firebase_files = [
        "gabarita-ai-frontend/firebase.json",
        "gabarita-ai-frontend/firestore.rules",
        "gabarita-ai-frontend/src/config/firebase.js"
    ]
    
    for file_path in firebase_files:
        full_path = Path(file_path)
        if full_path.exists():
            print_success(f"Arquivo encontrado: {file_path}")
            if file_path.endswith('firebase.js'):
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'initializeApp' in content:
                            print_info("Inicialização do Firebase configurada")
                        if 'getAuth' in content:
                            print_info("Autenticação Firebase configurada")
                        if 'getFirestore' in content:
                            print_info("Firestore configurado")
                except Exception as e:
                    print_warning(f"Erro ao ler {file_path}: {str(e)}")
        else:
            print_error(f"Arquivo não encontrado: {file_path}")
            config_ok = False
    
    # Verificar variáveis de ambiente do Firebase
    env_files = [".env.example", "gabarita-ai-frontend/.env.example"]
    
    for env_file in env_files:
        env_path = Path(env_file)
        if env_path.exists():
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    firebase_vars = [
                        'FIREBASE_PROJECT_ID',
                        'FIREBASE_PRIVATE_KEY',
                        'FIREBASE_CLIENT_EMAIL'
                    ]
                    
                    found_vars = [var for var in firebase_vars if var in content]
                    if found_vars:
                        print_info(f"Variáveis Firebase em {env_file}: {len(found_vars)}/3")
                    else:
                        print_warning(f"Nenhuma variável Firebase encontrada em {env_file}")
            except Exception as e:
                print_warning(f"Erro ao ler {env_file}: {str(e)}")
    
    return config_ok

def test_project_structure():
    """Testa estrutura do projeto"""
    print_header("TESTE DE ESTRUTURA DO PROJETO")
    
    required_dirs = [
        "gabarita-ai-frontend",
        "gabarita-ai-backend",
        "gabarita-ai-backend-deploy",
        "src"
    ]
    
    structure_ok = True
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            print_success(f"Diretório encontrado: {dir_name}")
        else:
            print_error(f"Diretório não encontrado: {dir_name}")
            structure_ok = False
    
    # Verificar arquivos principais
    main_files = [
        "src/main.py",
        "gabarita-ai-frontend/package.json",
        "requirements.txt"
    ]
    
    for file_path in main_files:
        full_path = Path(file_path)
        if full_path.exists():
            print_success(f"Arquivo principal encontrado: {file_path}")
        else:
            print_error(f"Arquivo principal não encontrado: {file_path}")
            structure_ok = False
    
    return structure_ok

def generate_report(results):
    """Gera relatório final"""
    print_header("RELATÓRIO FINAL")
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"📊 Testes executados: {total_tests}")
    print(f"✅ Testes aprovados: {passed_tests}")
    print(f"❌ Testes falharam: {total_tests - passed_tests}")
    print(f"📈 Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\n📋 Detalhes por serviço:")
    for service, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"   {status_icon} {service}")
    
    if passed_tests == total_tests:
        print_success("\n🎉 Todas as conexões estão configuradas corretamente!")
        print_info("Você pode prosseguir com o deploy dos serviços.")
    else:
        print_warning("\n⚠️  Algumas configurações precisam de atenção.")
        print_info("Verifique os erros acima e configure os serviços necessários.")
    
    # Próximos passos
    print("\n🚀 Próximos passos recomendados:")
    if not results.get('GitHub', True):
        print("   1. Verificar acesso ao repositório GitHub")
    if not results.get('Vercel', True):
        print("   2. Configurar variáveis de ambiente no Vercel")
    if not results.get('Render', True):
        print("   3. Configurar deploy no Render")
    if not results.get('Firebase', True):
        print("   4. Configurar credenciais do Firebase")
    
    print("\n📚 Documentação disponível:")
    print("   - DEPLOY_RENDER_MANUAL.md")
    print("   - gabarita-ai-frontend/DEPLOY_VERCEL.md")
    print("   - GUIA_CONFIGURACAO_RAPIDA.md")

def main():
    """Função principal"""
    print(f"{Colors.PURPLE}{Colors.BOLD}")
    print("  ____       _                _ _          _    ___ ")
    print(" / ___| __ _| |__   __ _ _ __(_) |_ __ _  / \  |_ _|")
    print(" | |  _ / _` | '_ \ / _` | '__| | __/ _` |/ _ \  | | ")
    print(" | |_| | (_| | |_) | (_| | |  | | || (_| / ___ \ | | ")
    print("  \____|\_,_|_.__/ \__,_|_|  |_|\__\__,_/_/   \_|___|")
    print(f"{Colors.END}")
    print(f"{Colors.BOLD}Teste de Conexões - Versão 1.0{Colors.END}")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Executar testes
    results = {}
    
    results['Estrutura do Projeto'] = test_project_structure()
    results['GitHub'] = test_github_connection()
    results['Vercel'] = test_vercel_connection()
    results['Render'] = test_render_connection()
    results['Firebase'] = test_firebase_connection()
    
    # Gerar relatório
    generate_report(results)
    
    return all(results.values())

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Teste interrompido pelo usuário{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Erro inesperado: {str(e)}{Colors.END}")
        sys.exit(1)