#!/usr/bin/env python3
"""
Script Automatizado - Configuração de Credenciais
Gabarita-AI Backend
"""

import os
import json
import sys
from pathlib import Path

def print_header():
    """Imprime o cabeçalho do script"""
    print("\n" + "=" * 60)
    print("🚀 CONFIGURADOR AUTOMÁTICO - GABARITA-AI")
    print("💰 Configure e comece a ganhar dinheiro hoje!")
    print("=" * 60)

def configure_firebase():
    """Configura as credenciais do Firebase"""
    print("\n🔥 CONFIGURAÇÃO FIREBASE")
    print("-" * 30)
    
    print("\n📋 INSTRUÇÕES:")
    print("1. Acesse: https://console.firebase.google.com/")
    print("2. Crie um projeto (se não tiver)")
    print("3. Vá em Configurações > Contas de serviço")
    print("4. Clique em 'Gerar nova chave privada'")
    print("5. Baixe o arquivo JSON")
    print("6. Informe o caminho do arquivo abaixo")
    
    while True:
        json_path = input("\n📁 Caminho do arquivo JSON do Firebase (ou 'pular'): ").strip()
        
        if json_path.lower() == 'pular':
            print("⏭️ Pulando configuração do Firebase")
            return {}
        
        if not json_path:
            continue
            
        # Expandir ~ para home directory
        json_path = os.path.expanduser(json_path)
        
        # Remover aspas se houver
        json_path = json_path.strip('"\'')
        
        if not os.path.exists(json_path):
            print(f"❌ Arquivo não encontrado: {json_path}")
            continue
            
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                firebase_data = json.load(f)
            
            # Extrair informações necessárias
            config = {
                'FIREBASE_PROJECT_ID': firebase_data.get('project_id', ''),
                'FIREBASE_PRIVATE_KEY_ID': firebase_data.get('private_key_id', ''),
                'FIREBASE_PRIVATE_KEY': firebase_data.get('private_key', '').replace('\n', '\\n'),
                'FIREBASE_CLIENT_EMAIL': firebase_data.get('client_email', ''),
                'FIREBASE_CLIENT_ID': firebase_data.get('client_id', ''),
                'FIREBASE_AUTH_URI': firebase_data.get('auth_uri', 'https://accounts.google.com/o/oauth2/auth'),
                'FIREBASE_TOKEN_URI': firebase_data.get('token_uri', 'https://oauth2.googleapis.com/token'),
            }
            
            print("\n✅ Arquivo JSON lido com sucesso!")
            print(f"📊 Projeto: {config['FIREBASE_PROJECT_ID']}")
            print(f"📧 Email: {config['FIREBASE_CLIENT_EMAIL']}")
            
            return config
            
        except json.JSONDecodeError:
            print("❌ Erro: Arquivo JSON inválido")
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")

def configure_mercadopago():
    """Configura as credenciais do Mercado Pago"""
    print("\n💳 CONFIGURAÇÃO MERCADO PAGO")
    print("-" * 30)
    
    print("\n📋 INSTRUÇÕES:")
    print("1. Acesse: https://www.mercadopago.com.br/developers/")
    print("2. Faça login na sua conta")
    print("3. Vá em 'Suas integrações'")
    print("4. Crie uma aplicação (se não tiver)")
    print("5. Copie o Access Token")
    
    config = {}
    
    while True:
        access_token = input("\n🔑 Access Token do Mercado Pago (ou 'pular'): ").strip()
        
        if access_token.lower() == 'pular':
            print("⏭️ Pulando configuração do Mercado Pago")
            break
            
        if not access_token:
            continue
            
        # Validar formato do token
        if access_token.startswith('TEST-') or access_token.startswith('APP-'):
            config['MERCADO_PAGO_ACCESS_TOKEN'] = access_token
            
            if access_token.startswith('TEST-'):
                print("✅ Token de TESTE configurado - use cartões de teste")
            else:
                print("✅ Token de PRODUÇÃO configurado - pagamentos reais!")
            break
        else:
            print("❌ Token inválido. Deve começar com 'TEST-' ou 'APP-'")
    
    # Webhook secret (opcional)
    webhook_secret = input("\n🔐 Webhook Secret (opcional, Enter para pular): ").strip()
    if webhook_secret:
        config['MERCADO_PAGO_WEBHOOK_SECRET'] = webhook_secret
        print("✅ Webhook Secret configurado")
    
    return config

def configure_other_apis():
    """Configura outras APIs necessárias"""
    print("\n🤖 CONFIGURAÇÃO OUTRAS APIs")
    print("-" * 30)
    
    config = {}
    
    # OpenAI
    print("\n🧠 OpenAI API Key:")
    print("- Acesse: https://platform.openai.com/api-keys")
    print("- Crie uma chave se não tiver")
    
    openai_key = input("🔑 OpenAI API Key (ou Enter para pular): ").strip()
    if openai_key:
        config['OPENAI_API_KEY'] = openai_key
        print("✅ OpenAI configurado")
    
    # Perplexity
    print("\n🔍 Perplexity API Key:")
    print("- Acesse: https://www.perplexity.ai/settings/api")
    print("- Gere uma chave se não tiver")
    
    perplexity_key = input("🔑 Perplexity API Key (ou Enter para pular): ").strip()
    if perplexity_key:
        config['PERPLEXITY_API_KEY'] = perplexity_key
        print("✅ Perplexity configurado")
    
    # Secret Key
    import secrets
    secret_key = secrets.token_urlsafe(32)
    config['SECRET_KEY'] = secret_key
    print(f"✅ Secret Key gerado automaticamente")
    
    # URLs
    config['FRONTEND_URL'] = 'http://localhost:3000'
    config['BACKEND_URL'] = 'http://localhost:5000'
    config['CORS_ORIGINS'] = 'http://localhost:3000,https://seu-dominio.com'
    
    return config

def update_env_file(config):
    """Atualiza o arquivo .env com as configurações"""
    print("\n📝 ATUALIZANDO ARQUIVO .env")
    print("-" * 30)
    
    env_path = Path('.env')
    
    # Ler arquivo existente se houver
    existing_config = {}
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    existing_config[key] = value
    
    # Mesclar configurações
    existing_config.update(config)
    
    # Escrever arquivo atualizado
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write("# ===== CONFIGURAÇÃO GABARITA-AI =====\n")
        f.write("# Gerado automaticamente pelo configurador\n\n")
        
        # Firebase
        f.write("# ===== FIREBASE =====\n")
        firebase_keys = ['FIREBASE_PROJECT_ID', 'FIREBASE_PRIVATE_KEY_ID', 'FIREBASE_PRIVATE_KEY', 
                        'FIREBASE_CLIENT_EMAIL', 'FIREBASE_CLIENT_ID', 'FIREBASE_AUTH_URI', 'FIREBASE_TOKEN_URI']
        for key in firebase_keys:
            value = existing_config.get(key, '')
            if key == 'FIREBASE_PRIVATE_KEY' and value:
                f.write(f'{key}="{value}"\n')
            else:
                f.write(f'{key}={value}\n')
        
        # Mercado Pago
        f.write("\n# ===== MERCADO PAGO =====\n")
        mp_keys = ['MERCADO_PAGO_ACCESS_TOKEN', 'MERCADO_PAGO_WEBHOOK_SECRET']
        for key in mp_keys:
            value = existing_config.get(key, '')
            f.write(f'{key}={value}\n')
        
        # APIs
        f.write("\n# ===== APIs =====\n")
        api_keys = ['OPENAI_API_KEY', 'PERPLEXITY_API_KEY']
        for key in api_keys:
            value = existing_config.get(key, '')
            f.write(f'{key}={value}\n')
        
        # Outras configurações
        f.write("\n# ===== CONFIGURAÇÕES GERAIS =====\n")
        other_keys = ['SECRET_KEY', 'FRONTEND_URL', 'BACKEND_URL', 'CORS_ORIGINS']
        for key in other_keys:
            value = existing_config.get(key, '')
            f.write(f'{key}={value}\n')
    
    print(f"✅ Arquivo .env atualizado com sucesso!")
    print(f"📁 Localização: {env_path.absolute()}")

def test_configuration():
    """Testa a configuração"""
    print("\n🧪 TESTANDO CONFIGURAÇÃO")
    print("-" * 30)
    
    try:
        # Executar script de teste
        import subprocess
        result = subprocess.run([sys.executable, 'test_configuracao.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Teste executado com sucesso!")
            print(result.stdout)
        else:
            print("⚠️ Teste executado com avisos:")
            print(result.stdout)
            if result.stderr:
                print("Erros:")
                print(result.stderr)
                
    except subprocess.TimeoutExpired:
        print("⏰ Teste demorou muito para executar")
    except Exception as e:
        print(f"❌ Erro ao executar teste: {e}")
        print("\n💡 Execute manualmente: python test_configuracao.py")

def main():
    """Função principal"""
    print_header()
    
    print("\n🎯 Este script vai configurar automaticamente:")
    print("   🔥 Firebase (banco de dados e autenticação)")
    print("   💳 Mercado Pago (pagamentos)")
    print("   🤖 APIs de IA (OpenAI, Perplexity)")
    print("   ⚙️ Outras configurações necessárias")
    
    input("\n👆 Pressione Enter para continuar...")
    
    # Configurar serviços
    all_config = {}
    
    # Firebase
    firebase_config = configure_firebase()
    all_config.update(firebase_config)
    
    # Mercado Pago
    mp_config = configure_mercadopago()
    all_config.update(mp_config)
    
    # Outras APIs
    other_config = configure_other_apis()
    all_config.update(other_config)
    
    # Atualizar .env
    update_env_file(all_config)
    
    # Testar configuração
    test_config = input("\n🧪 Executar teste de configuração? (s/N): ").strip().lower()
    if test_config in ['s', 'sim', 'y', 'yes']:
        test_configuration()
    
    # Resumo final
    print("\n" + "=" * 60)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA!")
    print("=" * 60)
    
    configured_services = []
    if firebase_config:
        configured_services.append("🔥 Firebase")
    if mp_config:
        configured_services.append("💳 Mercado Pago")
    if other_config.get('OPENAI_API_KEY'):
        configured_services.append("🧠 OpenAI")
    if other_config.get('PERPLEXITY_API_KEY'):
        configured_services.append("🔍 Perplexity")
    
    if configured_services:
        print("\n✅ Serviços configurados:")
        for service in configured_services:
            print(f"   {service}")
    
    print("\n🚀 PRÓXIMOS PASSOS:")
    print("   1. Execute: python src/main.py")
    print("   2. Acesse: http://localhost:5000")
    print("   3. Teste todas as funcionalidades")
    print("   4. Faça o deploy para produção")
    print("   5. COMECE A GANHAR DINHEIRO! 💰")
    
    print("\n📚 DOCUMENTAÇÃO:")
    print("   📖 GUIA_CONFIGURACAO_RAPIDA.md")
    print("   📖 CONFIGURACAO_FIREBASE_MERCADOPAGO.md")
    
    print("\n🎯 BOA SORTE E MUITO SUCESSO!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Configuração cancelada pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        print("\n💡 Tente executar novamente ou configure manualmente")