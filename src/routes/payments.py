"""
Routas de Pagamento - Mercado Pago Integration
Gabarit-AI Backend
"""

from flask import Blueprint, request, jsonify
import os
import mercadopago
import firebase_admin
from firebase_admin import firestore
from datetime import datetime, timedelta
import hashlib
import hmac

payments_bp = Blueprint('payments', __name__)
db = firestore.client()

# Configurar Mercado Pago
sdk = mercadopago.SDK(os.getenv('MERCADO_PAGO_ACCESS_TOKEN'))

@payments_bp.route('/api/pagamentos/criar', methods=['POST'])
def criar_pagamento():
    """Criar preferência de pagamento no Mercado Pago"""
    try:
        data = request.get_json()
        plano = data.get('plano')
        user_id = data.get('userId')
        user_email = data.get('userEmail')
        
        # Definir planos
        planos = {
            'mensal': {'title': 'Plano Mensal', 'price': 29.90, 'duration': 30},
            'trimestral': {'title': 'Plano Trimestral', 'price': 79.90, 'duration': 90},
            'anual': {'title': 'Plano Anual', 'price': 299.90, 'duration': 365}
        }
        
        if plano not in planos:
            return jsonify({'error': 'Plano inválido'}), 400
            
        plano_info = planos[plano]
        
        # Criar preferência no Mercado Pago
        preference_data = {
            "items": [{
                "title": plano_info['title'],
                "quantity": 1,
                "unit_price": plano_info['price']
            }],
            "payer": {
                "email": user_email
            },
            "back_urls": {
                "success": f"{os.getenv('FRONTEND_URL')}/retorno?status=success",
                "failure": f"{os.getenv('FRONTEND_URL')}/retorno?status=failure",
                "pending": f"{os.getenv('FRONTEND_URL')}/retorno?status=pending"
            },
            "auto_return": "approved",
            "notification_url": f"{os.getenv('BACKEND_URL')}/api/pagamentos/webhook",
            "external_reference": f"{user_id}_{plano}_{datetime.now().timestamp()}"
        }
        
        preference_response = sdk.preference().create(preference_data)
        
        if preference_response["status"] == 201:
            preference = preference_response["response"]
            
            # Salvar transação no Firebase
            transaction_data = {
                'userId': user_id,
                'userEmail': user_email,
                'plano': plano,
                'valor': plano_info['price'],
                'duracao': plano_info['duration'],
                'preferenceId': preference['id'],
                'status': 'pending',
                'createdAt': datetime.now(),
                'externalReference': preference_data['external_reference']
            }
            
            db.collection('transactions').add(transaction_data)
            
            return jsonify({
                'preferenceId': preference['id'],
                'initPoint': preference['init_point'],
                'sandboxInitPoint': preference['sandbox_init_point']
            })
        else:
            return jsonify({'error': 'Erro ao criar pagamento'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/api/pagamentos/webhook', methods=['POST'])
def webhook_pagamento():
    """Webhook para notificações do Mercado Pago"""
    try:
        # Validar assinatura do webhook
        x_signature = request.headers.get('x-signature')
        x_request_id = request.headers.get('x-request-id')
        
        if not validate_webhook_signature(request.data, x_signature, x_request_id):
            return jsonify({'error': 'Assinatura inválida'}), 401
            
        data = request.get_json()
        
        if data.get('type') == 'payment':
            payment_id = data['data']['id']
            
            # Buscar informações do pagamento
            payment_info = sdk.payment().get(payment_id)
            
            if payment_info['status'] == 200:
                payment = payment_info['response']
                external_reference = payment.get('external_reference')
                status = payment.get('status')
                
                # Atualizar transação no Firebase
                transactions_ref = db.collection('transactions')
                query = transactions_ref.where('externalReference', '==', external_reference)
                docs = query.get()
                
                for doc in docs:
                    doc.reference.update({
                        'status': status,
                        'paymentId': payment_id,
                        'updatedAt': datetime.now()
                    })
                    
                    # Se pagamento aprovado, ativar plano
                    if status == 'approved':
                        transaction_data = doc.to_dict()
                        ativar_plano_usuario(transaction_data)
                        
        return jsonify({'status': 'ok'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/api/pagamentos/status/<payment_id>', methods=['GET'])
def status_pagamento(payment_id):
    """Verificar status de um pagamento"""
    try:
        payment_info = sdk.payment().get(payment_id)
        
        if payment_info['status'] == 200:
            return jsonify(payment_info['response'])
        else:
            return jsonify({'error': 'Pagamento não encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@payments_bp.route('/api/pagamentos/ativar-plano', methods=['POST'])
def ativar_plano():
    """Ativar plano manualmente (para testes)"""
    try:
        data = request.get_json()
        user_id = data.get('userId')
        plano = data.get('plano')
        
        if not user_id or not plano:
            return jsonify({'error': 'userId e plano são obrigatórios'}), 400
            
        # Simular dados da transação
        transaction_data = {
            'userId': user_id,
            'plano': plano,
            'duracao': {'mensal': 30, 'trimestral': 90, 'anual': 365}.get(plano, 30)
        }
        
        result = ativar_plano_usuario(transaction_data)
        
        if result:
            return jsonify({'message': 'Plano ativado com sucesso'})
        else:
            return jsonify({'error': 'Erro ao ativar plano'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def validate_webhook_signature(data, x_signature, x_request_id):
    """Validar assinatura do webhook do Mercado Pago"""
    try:
        webhook_secret = os.getenv('MERCADO_PAGO_WEBHOOK_SECRET')
        if not webhook_secret:
            return True  # Em desenvolvimento, pular validação
            
        # Extrair ts e hash da assinatura
        parts = x_signature.split(',')
        ts = None
        hash_signature = None
        
        for part in parts:
            if part.startswith('ts='):
                ts = part[3:]
            elif part.startswith('v1='):
                hash_signature = part[3:]
                
        if not ts or not hash_signature:
            return False
            
        # Criar string para validação
        manifest = f"id:{x_request_id};request-id:{x_request_id};ts:{ts};"
        
        # Calcular HMAC
        expected_signature = hmac.new(
            webhook_secret.encode(),
            manifest.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(expected_signature, hash_signature)
        
    except Exception:
        return False

def ativar_plano_usuario(transaction_data):
    """Ativar plano do usuário no Firebase"""
    try:
        user_id = transaction_data['userId']
        duracao = transaction_data['duracao']
        plano = transaction_data['plano']
        
        # Calcular data de expiração
        data_expiracao = datetime.now() + timedelta(days=duracao)
        
        # Atualizar usuário no Firebase
        user_ref = db.collection('users').document(user_id)
        user_ref.update({
            'planoAtivo': plano,
            'dataExpiracao': data_expiracao,
            'questoesRestantes': 1000 if plano != 'free' else 5,
            'updatedAt': datetime.now()
        })
        
        return True
        
    except Exception as e:
        print(f"Erro ao ativar plano: {e}")
        return False
