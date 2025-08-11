#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste direto dos endpoints da API
"""

import requests
import json

# URL base da API no Render
BASE_URL = "https://gabarita-ai-backend.onrender.com"

print("🔍 Testando endpoint HOME (/)...")
try:
    response = requests.get(f"{BASE_URL}/", timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Erro: {e}")

print("\n" + "="*50)
print("🔐 Testando endpoint LOGIN...")
try:
    payload = {"email": "teste@gabarita.ai", "password": "123456"}
    response = requests.post(f"{BASE_URL}/api/auth/login", json=payload, timeout=30)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content: {response.text}")
except Exception as e:
    print(f"Erro: {e}")

print("\n" + "="*50)
print("🤖 Testando endpoint GERAR QUESTÃO...")
try:
    payload = {"usuario_id": "teste-123", "cargo": "Enfermeiro", "bloco": "Saúde"}
    response = requests.post(f"{BASE_URL}/api/questoes/gerar", json=payload, timeout=60)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content: {response.text[:500]}...")
except Exception as e:
    print(f"Erro: {e}")