#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a API do Gabarita-AI no Render
"""

import requests
import json
from datetime import datetime

# URL base da API no Render
BASE_URL = "https://gabarita-ai-backend.onrender.com"

def testar_health():
    """Testa o endpoint de health check"""
    print("🔍 Testando Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check OK: {data}")
            return True
        else:
            print(f"❌ Health Check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no Health Check: {e}")
        return False

def testar_home():
    """Testa o endpoint home"""
    print("\n🏠 Testando endpoint Home...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Home OK: {data.get('message', 'N/A')}")
            print(f"📊 Versão: {data.get('version', 'N/A')}")
            print(f"🕐 Timestamp: {data.get('timestamp', 'N/A')}")
            return True
        else:
            print(f"❌ Home falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no Home: {e}")
        return False

def testar_login():
    """Testa o endpoint de login"""
    print("\n🔐 Testando Login...")
    try:
        payload = {
            "email": "teste@gabarita.ai",
            "password": "123456"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", 
                               json=payload, 
                               timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Login OK: {data.get('success', False)}")
            print(f"👤 Usuário: {data.get('user', {}).get('nome', 'N/A')}")
            return True
        else:
            print(f"❌ Login falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no Login: {e}")
        return False

def testar_gerar_questao():
    """Testa o endpoint de geração de questões"""
    print("\n🤖 Testando Geração de Questões...")
    try:
        payload = {
            "usuario_id": "teste-123",
            "cargo": "Enfermeiro",
            "bloco": "Saúde"
        }
        response = requests.post(f"{BASE_URL}/api/questoes/gerar", 
                               json=payload, 
                               timeout=60)  # Timeout maior para IA
        if response.status_code == 200:
            data = response.json()
            questao = data.get('questao', {})
            print(f"✅ Questão gerada com sucesso!")
            print(f"📝 Enunciado: {questao.get('enunciado', 'N/A')[:100]}...")
            print(f"🎯 Tema: {questao.get('tema', 'N/A')}")
            print(f"📊 Dificuldade: {questao.get('dificuldade', 'N/A')}")
            print(f"🆔 ID: {questao.get('id', 'N/A')}")
            print(f"🔤 Alternativas: {len(questao.get('alternativas', []))} opções")
            return True
        else:
            print(f"❌ Geração de questão falhou: {response.status_code}")
            print(f"📄 Resposta: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"❌ Erro na geração de questão: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 TESTANDO API GABARITA-AI NO RENDER")
    print(f"🌐 URL Base: {BASE_URL}")
    print(f"🕐 Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Lista de testes
    testes = [
        ("Health Check", testar_health),
        ("Home", testar_home),
        ("Login", testar_login),
        ("Gerar Questão", testar_gerar_questao)
    ]
    
    resultados = []
    
    for nome, funcao in testes:
        try:
            resultado = funcao()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"❌ Erro crítico em {nome}: {e}")
            resultados.append((nome, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    sucessos = 0
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome}: {status}")
        if resultado:
            sucessos += 1
    
    print(f"\n🎯 RESULTADO FINAL: {sucessos}/{len(resultados)} testes passaram")
    
    if sucessos == len(resultados):
        print("🎉 TODOS OS TESTES PASSARAM! API está funcionando perfeitamente!")
    elif sucessos > 0:
        print("⚠️ ALGUNS TESTES FALHARAM. Verifique as configurações.")
    else:
        print("🚨 TODOS OS TESTES FALHARAM. Verifique se o serviço está online.")
    
    print("\n💡 PRÓXIMOS PASSOS:")
    if sucessos >= 2:  # Health e Home funcionando
        print("1. ✅ Backend está online e respondendo")
        print("2. 🔧 Configure as variáveis de ambiente no Render se algum teste falhou")
        print("3. 🚀 Faça o deploy do frontend")
        print("4. 💰 Sua plataforma estará pronta para monetização!")
    else:
        print("1. 🔧 Verifique se o deploy foi concluído no Render")
        print("2. 📋 Adicione as variáveis de ambiente necessárias")
        print("3. 🔄 Reinicie o serviço se necessário")

if __name__ == "__main__":
    main()