#!/usr/bin/env python3
"""
Script de Teste - Configuração Firebase e Mercado Pago
Gabarita-AI Backend
"""

import os
import sys
from dotenv import load_dotenv

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

load_dotenv()

def test_firebase_config():
    """Testa a configuração do Firebase"""
    print("\n🔥 TESTANDO CONFIGURAÇÃO FIREBASE")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    firebase_vars = {
        'FIREBASE_PROJECT_ID': os.getenv('FIREBASE_PROJECT_ID'),
        'FIREBASE_PRIVATE_KEY_ID': os.getenv('FIREBASE_PRIVATE_KEY_ID'),
        'FIREBASE_PRIVATE_KEY': os.getenv('FIREBASE_PRIVATE_KEY'),
        'FIREBASE_CLIENT_EMAIL': os.getenv('FIREBASE_CLIENT_EMAIL'),
        'FIREBASE_CLIENT_ID': os.getenv('FIREBASE_CLIENT_ID'),
    }
    
    missing = []
    configured = []
    
    for var, value in firebase_vars.items():
        if not value or value.strip() == '' or 'your_' in value or 'YOUR_' in value:
            missing.append(var)
            print(f"❌ {var}: NÃO CONFIGURADO")
        else:
            configured.append(var)
            # Mostrar apenas parte da chave privada por segurança
            if 'PRIVATE_KEY' in var and len(value) > 50:
                display_value = value[:30] + "..." + value[-20:]
            elif 'EMAIL' in var:
                display_value = value
            else:
                display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"✅ {var}: {display_value}")
    
    print(f"\n📊 RESUMO FIREBASE:")
    print(f"✅ Configuradas: {len(configured)}/5")
    print(f"❌ Faltando: {len(missing)}/5")
    
    if missing:
        print(f"\n🚨 VARIÁVEIS FALTANDO: {', '.join(missing)}")
        print("📝 Configure essas variáveis no arquivo .env")
        return False
    else:
        print("\n🎉 FIREBASE: Todas as variáveis configuradas!")
        
        # Testar conexão
        try:
            from config.firebase_config import firebase_config
            if firebase_config.is_connected():
                print("✅ CONEXÃO: Firebase conectado com sucesso!")
                return True
            else:
                print("❌ CONEXÃO: Erro ao conectar com Firebase")
                return False
        except Exception as e:
            print(f"❌ ERRO DE CONEXÃO: {e}")
            return False

def test_mercadopago_config():
    """Testa a configuração do Mercado Pago"""
    print("\n💳 TESTANDO CONFIGURAÇÃO MERCADO PAGO")
    print("=" * 50)
    
    # Verificar variáveis de ambiente
    mp_vars = {
        'MERCADO_PAGO_ACCESS_TOKEN': os.getenv('MERCADO_PAGO_ACCESS_TOKEN'),
        'MERCADO_PAGO_WEBHOOK_SECRET': os.getenv('MERCADO_PAGO_WEBHOOK_SECRET'),
    }
    
    missing = []
    configured = []
    
    for var, value in mp_vars.items():
        if not value or value.strip() == '' or 'your_' in value:
            missing.append(var)
            print(f"❌ {var}: NÃO CONFIGURADO")
        else:
            configured.append(var)
            # Mostrar apenas parte do token por segurança
            if 'TOKEN' in var:
                if value.startswith('TEST-'):
                    display_value = value[:15] + "..." + value[-10:] + " (TESTE)"
                else:
                    display_value = value[:15] + "..." + value[-10:] + " (PRODUÇÃO)"
            else:
                display_value = value[:20] + "..." if len(value) > 20 else value
            print(f"✅ {var}: {display_value}")
    
    print(f"\n📊 RESUMO MERCADO PAGO:")
    print(f"✅ Configuradas: {len(configured)}/2")
    print(f"❌ Faltando: {len(missing)}/2")
    
    if missing:
        print(f"\n🚨 VARIÁVEIS FALTANDO: {', '.join(missing)}")
        print("📝 Configure essas variáveis no arquivo .env")
        return False
    else:
        print("\n🎉 MERCADO PAGO: Todas as variáveis configuradas!")
        
        # Verificar se é teste ou produção
        token = os.getenv('MERCADO_PAGO_ACCESS_TOKEN')
        if token.startswith('TEST-'):
            print("🧪 MODO: Teste (use cartões de teste)")
        else:
            print("🚀 MODO: Produção (pagamentos reais)")
        
        return True

def test_other_configs():
    """Testa outras configurações importantes"""
    print("\n⚙️ TESTANDO OUTRAS CONFIGURAÇÕES")
    print("=" * 50)
    
    configs = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'PERPLEXITY_API_KEY': os.getenv('PERPLEXITY_API_KEY'),
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'FRONTEND_URL': os.getenv('FRONTEND_URL'),
        'BACKEND_URL': os.getenv('BACKEND_URL'),
    }
    
    for var, value in configs.items():
        if not value or value.strip() == '':
            print(f"❌ {var}: NÃO CONFIGURADO")
        else:
            # Mostrar apenas parte das chaves por segurança
            if 'KEY' in var and len(value) > 30:
                display_value = value[:15] + "..." + value[-10:]
            else:
                display_value = value
            print(f"✅ {var}: {display_value}")

def main():
    """Função principal"""
    print("🧪 TESTE DE CONFIGURAÇÃO - GABARITA-AI")
    print("=" * 60)
    print("Este script verifica se Firebase e Mercado Pago estão configurados")
    
    # Testar Firebase
    firebase_ok = test_firebase_config()
    
    # Testar Mercado Pago
    mercadopago_ok = test_mercadopago_config()
    
    # Testar outras configurações
    test_other_configs()
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📋 RESUMO FINAL")
    print("=" * 60)
    
    if firebase_ok:
        print("✅ Firebase: CONFIGURADO E FUNCIONANDO")
    else:
        print("❌ Firebase: NÃO CONFIGURADO")
        print("   📖 Consulte: CONFIGURACAO_FIREBASE_MERCADOPAGO.md")
    
    if mercadopago_ok:
        print("✅ Mercado Pago: CONFIGURADO")
    else:
        print("❌ Mercado Pago: NÃO CONFIGURADO")
        print("   📖 Consulte: CONFIGURACAO_FIREBASE_MERCADOPAGO.md")
    
    if firebase_ok and mercadopago_ok:
        print("\n🎉 PARABÉNS! Tudo configurado corretamente!")
        print("🚀 Seu Gabarita-AI está pronto para produção!")
    else:
        print("\n⚠️  Ainda há configurações pendentes.")
        print("📝 Configure as variáveis faltantes no arquivo .env")
        print("📖 Consulte o arquivo CONFIGURACAO_FIREBASE_MERCADOPAGO.md")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()