#!/usr/bin/env python3
"""
Configuração de Produção - Gabarita-AI
Configura credenciais reais para monetização
"""

import os
import json
import secrets
from pathlib import Path

def print_header():
    """Imprime o cabeçalho"""
    print("\n" + "=" * 60)
    print("💰 CONFIGURAÇÃO DE PRODUÇÃO - GABARITA-AI")
    print("🚀 Configure suas credenciais reais e comece a faturar!")
    print("=" * 60)

def obter_credenciais_openai():
    """Obtém credenciais da OpenAI"""
    print("\n🤖 CONFIGURAÇÃO OPENAI")
    print("-" * 30)
    print("1. Acesse: https://platform.openai.com/api-keys")
    print("2. Faça login na sua conta")
    print("3. Clique em 'Create new secret key'")
    print("4. Copie a chave gerada")
    
    while True:
        api_key = input("\n🔑 Cole sua OpenAI API Key: ").strip()
        if api_key.startswith('sk-') and len(api_key) > 40:
            return api_key
        print("❌ Chave inválida. Deve começar com 'sk-' e ter mais de 40 caracteres")

def obter_credenciais_perplexity():
    """Obtém credenciais da Perplexity"""
    print("\n🔍 CONFIGURAÇÃO PERPLEXITY")
    print("-" * 30)
    print("1. Acesse: https://www.perplexity.ai/settings/api")
    print("2. Faça login na sua conta")
    print("3. Clique em 'Generate API Key'")
    print("4. Copie a chave gerada")
    
    while True:
        api_key = input("\n🔑 Cole sua Perplexity API Key: ").strip()
        if api_key.startswith('pplx-') and len(api_key) > 40:
            return api_key
        print("❌ Chave inválida. Deve começar com 'pplx-' e ter mais de 40 caracteres")

def obter_credenciais_firebase():
    """Obtém credenciais do Firebase"""
    print("\n🔥 CONFIGURAÇÃO FIREBASE")
    print("-" * 30)
    print("1. Acesse: https://console.firebase.google.com/")
    print("2. Clique em 'Criar um projeto'")
    print("3. Nome: gabarita-ai-[seu-nome]")
    print("4. Ative Authentication > Sign-in method > Email/senha")
    print("5. Ative Firestore Database > Criar banco de dados")
    print("6. Vá em Configurações > Contas de serviço")
    print("7. Clique em 'Gerar nova chave privada'")
    print("8. Baixe o arquivo JSON")
    
    # Solicitar arquivo JSON
    while True:
        json_path = input("\n📁 Caminho para o arquivo JSON baixado: ").strip().replace('"', '')
        if Path(json_path).exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    firebase_data = json.load(f)
                
                return {
                    'FIREBASE_PROJECT_ID': firebase_data['project_id'],
                    'FIREBASE_CLIENT_EMAIL': firebase_data['client_email'],
                    'FIREBASE_PRIVATE_KEY': firebase_data['private_key'],
                    'FIREBASE_PRIVATE_KEY_ID': firebase_data['private_key_id'],
                    'FIREBASE_DATABASE_URL': f"https://{firebase_data['project_id']}-default-rtdb.firebaseio.com/",
                    'FIREBASE_STORAGE_BUCKET': f"{firebase_data['project_id']}.appspot.com"
                }
            except Exception as e:
                print(f"❌ Erro ao ler arquivo: {e}")
        else:
            print("❌ Arquivo não encontrado")

def obter_credenciais_mercadopago():
    """Obtém credenciais do Mercado Pago"""
    print("\n💳 CONFIGURAÇÃO MERCADO PAGO")
    print("-" * 30)
    print("1. Acesse: https://www.mercadopago.com.br/developers")
    print("2. Faça login na sua conta")
    print("3. Vá em 'Suas integrações' > 'Criar aplicação'")
    print("4. Nome: Gabarita-AI")
    print("5. Modelo de negócio: Marketplace")
    print("6. Copie as credenciais de PRODUÇÃO")
    
    print("\n⚠️ IMPORTANTE: Use credenciais de PRODUÇÃO para receber pagamentos reais!")
    
    while True:
        access_token = input("\n🔑 Access Token de PRODUÇÃO: ").strip()
        if access_token.startswith('APP_USR-') and len(access_token) > 50:
            break
        print("❌ Token inválido. Deve começar com 'APP_USR-' e ter mais de 50 caracteres")
    
    while True:
        public_key = input("🔑 Public Key de PRODUÇÃO: ").strip()
        if public_key.startswith('APP_USR-') and len(public_key) > 30:
            break
        print("❌ Chave inválida. Deve começar com 'APP_USR-' e ter mais de 30 caracteres")
    
    webhook_secret = secrets.token_urlsafe(32)
    
    return {
        'MERCADOPAGO_ACCESS_TOKEN': access_token,
        'MERCADOPAGO_PUBLIC_KEY': public_key,
        'MERCADOPAGO_WEBHOOK_SECRET': webhook_secret
    }

def configurar_urls_producao():
    """Configura URLs de produção"""
    print("\n🌐 CONFIGURAÇÃO DE URLs")
    print("-" * 30)
    
    print("Escolha sua plataforma de deploy:")
    print("1. Render.com (Recomendado)")
    print("2. Vercel")
    print("3. Railway")
    print("4. Heroku")
    print("5. Outro/Personalizado")
    
    choice = input("\nEscolha (1-5): ").strip()
    
    if choice == '1':
        app_name = input("Nome da sua aplicação no Render: ").strip()
        base_url = f"https://{app_name}.onrender.com"
    elif choice == '2':
        app_name = input("Nome da sua aplicação no Vercel: ").strip()
        base_url = f"https://{app_name}.vercel.app"
    elif choice == '3':
        app_name = input("Nome da sua aplicação no Railway: ").strip()
        base_url = f"https://{app_name}.up.railway.app"
    elif choice == '4':
        app_name = input("Nome da sua aplicação no Heroku: ").strip()
        base_url = f"https://{app_name}.herokuapp.com"
    else:
        base_url = input("URL completa da sua aplicação: ").strip()
    
    return {
        'FRONTEND_URL': base_url,
        'BACKEND_URL': base_url,
        'CORS_ORIGINS': f"{base_url},http://localhost:3000,http://localhost:5000"
    }

def criar_env_producao(credenciais):
    """Cria arquivo .env de produção"""
    print("\n📝 CRIANDO ARQUIVO .env DE PRODUÇÃO")
    print("-" * 40)
    
    # Gerar SECRET_KEY segura
    secret_key = secrets.token_urlsafe(32)
    
    env_content = "# Configuração de Produção - Gabarita-AI\n"
    env_content += "# CREDENCIAIS REAIS - MANTENHA SEGURO!\n\n"
    
    # APIs
    env_content += "# APIs\n"
    env_content += f"OPENAI_API_KEY={credenciais['openai']}\n"
    env_content += f"PERPLEXITY_API_KEY={credenciais['perplexity']}\n\n"
    
    # Flask
    env_content += "# Flask\n"
    env_content += f"SECRET_KEY={secret_key}\n"
    env_content += "FLASK_ENV=production\n"
    env_content += "FLASK_DEBUG=False\n"
    env_content += "PORT=5000\n"
    env_content += "HOST=0.0.0.0\n\n"
    
    # Firebase
    env_content += "# Firebase\n"
    for key, value in credenciais['firebase'].items():
        if key == 'FIREBASE_PRIVATE_KEY':
            value = value.replace('\n', '\\n')
        env_content += f"{key}={value}\n"
    env_content += "\n"
    
    # Mercado Pago
    env_content += "# Mercado Pago\n"
    for key, value in credenciais['mercadopago'].items():
        env_content += f"{key}={value}\n"
    env_content += "\n"
    
    # URLs
    env_content += "# URLs e CORS\n"
    for key, value in credenciais['urls'].items():
        env_content += f"{key}={value}\n"
    
    # Salvar arquivo
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Arquivo .env de produção criado!")
    
    # Criar backup
    with open('.env.backup', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Backup salvo em .env.backup")

def testar_configuracao_producao():
    """Testa a configuração de produção"""
    print("\n🧪 TESTANDO CONFIGURAÇÃO DE PRODUÇÃO")
    print("-" * 40)
    
    try:
        # Recarregar variáveis de ambiente
        from dotenv import load_dotenv
        load_dotenv(override=True)
        
        # Testar OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key and openai_key.startswith('sk-'):
            print("✅ OpenAI: Configurado")
        else:
            print("❌ OpenAI: Não configurado")
        
        # Testar Perplexity
        perplexity_key = os.getenv('PERPLEXITY_API_KEY')
        if perplexity_key and perplexity_key.startswith('pplx-'):
            print("✅ Perplexity: Configurado")
        else:
            print("❌ Perplexity: Não configurado")
        
        # Testar Firebase
        firebase_project = os.getenv('FIREBASE_PROJECT_ID')
        firebase_email = os.getenv('FIREBASE_CLIENT_EMAIL')
        if firebase_project and firebase_email:
            print("✅ Firebase: Configurado")
        else:
            print("❌ Firebase: Não configurado")
        
        # Testar Mercado Pago
        mp_token = os.getenv('MERCADOPAGO_ACCESS_TOKEN')
        if mp_token and mp_token.startswith('APP_USR-'):
            print("✅ Mercado Pago: Configurado (PRODUÇÃO)")
        else:
            print("❌ Mercado Pago: Não configurado")
        
        print("\n🎉 CONFIGURAÇÃO DE PRODUÇÃO CONCLUÍDA!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal"""
    print_header()
    
    print("\n🎯 Este script vai configurar suas credenciais REAIS de produção")
    print("💰 Após a configuração, você poderá receber pagamentos reais!")
    
    continuar = input("\n👆 Continuar? (S/n): ").strip().lower()
    if continuar in ['n', 'no', 'não']:
        print("\n⏹️ Configuração cancelada")
        return
    
    try:
        credenciais = {}
        
        # Obter credenciais
        print("\n📋 COLETANDO CREDENCIAIS")
        print("=" * 30)
        
        credenciais['openai'] = obter_credenciais_openai()
        credenciais['perplexity'] = obter_credenciais_perplexity()
        credenciais['firebase'] = obter_credenciais_firebase()
        credenciais['mercadopago'] = obter_credenciais_mercadopago()
        credenciais['urls'] = configurar_urls_producao()
        
        # Criar arquivo .env
        criar_env_producao(credenciais)
        
        # Testar configuração
        if testar_configuracao_producao():
            print("\n" + "=" * 60)
            print("🎉 PARABÉNS! SUA PLATAFORMA ESTÁ PRONTA PARA PRODUÇÃO!")
            print("=" * 60)
            
            print("\n✅ CREDENCIAIS CONFIGURADAS:")
            print("   🤖 OpenAI - Para IA")
            print("   🔍 Perplexity - Para pesquisas")
            print("   🔥 Firebase - Para dados")
            print("   💳 Mercado Pago - Para pagamentos REAIS")
            
            print("\n🚀 PRÓXIMOS PASSOS:")
            print("   1. Teste localmente: python src/main.py")
            print("   2. Faça o deploy: python deploy_automatico.py")
            print("   3. Configure preços e planos")
            print("   4. COMECE A FATURAR! 💰")
            
            print("\n💡 DICAS DE MONETIZAÇÃO:")
            print("   📊 Freemium: 5 questões grátis")
            print("   💎 Premium: R$ 29,90/mês")
            print("   🎓 Mentoria: R$ 99,90/mês")
            print("   🏆 VIP: R$ 199,90/mês")
            
            print("\n🎯 SUA PLATAFORMA ESTÁ PRONTA PARA GERAR RECEITA!")
            
        else:
            print("\n⚠️ Configuração concluída com avisos")
            print("💡 Verifique as credenciais e tente novamente")
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Configuração cancelada pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro na configuração: {e}")
        print("💡 Tente executar novamente")

if __name__ == "__main__":
    main()