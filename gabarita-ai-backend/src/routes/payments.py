from flask import Blueprint, request, jsonify
from datetime import datetime
import os
import mercadopago
from ..services.plano_service import PlanoService
from ..config.firebase_config import firebase_config
from firebase_admin import firestore

payments_bp = Blueprint('payments', __name__)
plano_service = PlanoService()

# Configurar MercadoPago
mp = mercadopago.SDK(os.getenv('MERCADO_PAGO_ACCESS_TOKEN'))

@payments_bp.route('/pagamentos/criar-preferencia', methods=['POST'])
def create_payment_preference():
    """Criar preferência de pagamento no MercadoPago"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['user_id', 'plan_type', 'user_email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Field {field} is required'}), 400
        
        user_id = data['user_id']
        plan_type = data['plan_type']
        user_email = data['user_email']
        
        # Verificar se o plano existe
        if plan_type not in plano_service.TIPOS_PLANOS:
            return jsonify({'error': 'Tipo de plano inválido'}), 400
        
        # Obter preço do plano
        price = plano_service.PRECOS_PLANOS.get(plan_type, 0)
        
        if price <= 0:
            return jsonify({'error': 'Plano gratuito não requer pagamento'}), 400
        
        # Criar preferência de pagamento
        preference_data = {
            "items": [
                {
                    "title": f"Plano {plan_type.title()} - Gabarita.AI",
                    "quantity": 1,
                    "unit_price": price,
                    "currency_id": "BRL"
                }
            ],
            "payer": {
                "email": user_email
            },
            "back_urls": {
                "success": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/retorno?status=success",
                "failure": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/retorno?status=failure",
                "pending": f"{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/retorno?status=pending"
            },
            "auto_return": "approved",
            "external_reference": f"{user_id}_{plan_type}_{datetime.now().timestamp()}",
            "notification_url": f"{os.getenv('BACKEND_URL', 'http://localhost:5000')}/api/payments/webhook"
        }
        
        preference_response = mp.preference().create(preference_data)
        
        if preference_response["status"] == 201:
            return jsonify({
                'preference_id': preference_response["response"]["id"],
                'init_point': preference_response["response"]["init_point"],
                'sandbox_init_point': preference_response["response"]["sandbox_init_point"]
            }), 201
        else:
            return jsonify({'error': 'Error creating payment preference'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

@payments_bp.route('/pagamentos/webhook', methods=['POST'])
def payment_webhook():
    """Webhook para receber notificações de pagamento do MercadoPago"""
    try:
        data = request.get_json()
        
        if data.get('type') == 'payment':
            payment_id = data.get('data', {}).get('id')
            
            if payment_id:
                # Buscar informações do pagamento
                payment_info = mp.payment().get(payment_id)
                
                if payment_info["status"] == 200:
                    payment_data = payment_info["response"]
                    
                    if payment_data["status"] == "approved":
                        # Processar pagamento aprovado
                        external_reference = payment_data.get("external_reference")
                        
                        if external_reference:
                            # Extrair informações da referência externa
                            parts = external_reference.split('_')
                            if len(parts) >= 2:
                                user_id = parts[0]
                                plan_type = parts[1]
                                
                                # Ativar plano para o usuário
                                success = activate_user_plan(user_id, plan_type, payment_id)
                                
                                if success:
                                    return jsonify({'status': 'success'}), 200
                                else:
                                    return jsonify({'error': 'Erro ao ativar plano'}), 500
        
        return jsonify({'status': 'received'}), 200
        
    except Exception as e:
        print(f"Erro no webhook: {str(e)}")
        return jsonify({'error': 'Erro interno'}), 500

@payments_bp.route('/pagamentos/status/<payment_id>', methods=['GET'])
def get_payment_status(payment_id):
    """Obter status de um pagamento específico"""
    try:
        payment_info = mp.payment().get(payment_id)
        
        if payment_info["status"] == 200:
            payment_data = payment_info["response"]
            
            return jsonify({
                'id': payment_data['id'],
                'status': payment_data['status'],
                'status_detail': payment_data.get('status_detail'),
                'transaction_amount': payment_data.get('transaction_amount'),
                'currency_id': payment_data.get('currency_id'),
                'date_created': payment_data.get('date_created'),
                'date_approved': payment_data.get('date_approved')
            }), 200
        else:
            return jsonify({'error': 'Pagamento não encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@payments_bp.route('/pagamentos/usuario/<user_id>/historico', methods=['GET'])
def get_user_payment_history(user_id):
    """Obter histórico de pagamentos de um usuário"""
    try:
        db = firestore.client()
        
        # Buscar pagamentos do usuário
        payments_ref = db.collection('payments').where('user_id', '==', user_id)
        payments = payments_ref.stream()
        
        payment_history = []
        for payment in payments:
            payment_data = payment.to_dict()
            payment_data['id'] = payment.id
            payment_history.append(payment_data)
        
        # Ordenar por data (mais recente primeiro)
        payment_history.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return jsonify({
            'payments': payment_history,
            'total': len(payment_history)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

def activate_user_plan(user_id, plan_type, payment_id):
    """Ativar plano para um usuário após pagamento aprovado"""
    try:
        db = firestore.client()
        
        # Atualizar plano do usuário
        user_ref = db.collection('users').document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return False
        
        # Calcular data de expiração
        expiration_date = plano_service._calcular_data_expiracao(plan_type)
        
        # Atualizar dados do usuário
        update_data = {
            'planId': plan_type,
            'planStartDate': datetime.now().isoformat(),
            'planExpirationDate': expiration_date.isoformat() if expiration_date else None,
            'updatedAt': datetime.now().isoformat()
        }
        
        user_ref.update(update_data)
        
        # Registrar pagamento
        payment_data = {
            'user_id': user_id,
            'plan_type': plan_type,
            'payment_id': payment_id,
            'amount': plano_service.PRECOS_PLANOS.get(plan_type, 0),
            'status': 'approved',
            'created_at': datetime.now().isoformat(),
            'expiration_date': expiration_date.isoformat() if expiration_date else None
        }
        
        db.collection('payments').add(payment_data)
        
        return True
        
    except Exception as e:
        print(f"Erro ao ativar plano: {str(e)}")
        return False

@payments_bp.route('/pagamentos/planos', methods=['GET'])
def get_available_plans():
    """Obter lista de planos disponíveis com preços e recursos"""
    try:
        plans = []
        
        for plan_type in plano_service.TIPOS_PLANOS.values():
            plan_info = {
                'id': plan_type,
                'name': plan_type.replace('_', ' ').title(),
                'price': plano_service.PRECOS_PLANOS.get(plan_type, 0),
                'duration_days': plano_service.DURACAO_PLANOS.get(plan_type),
                'renewable': plano_service.RENOVACAO_PLANOS.get(plan_type, False),
                'features': plano_service.RECURSOS_PLANOS.get(plan_type, {})
            }
            plans.append(plan_info)
        
        return jsonify({
            'plans': plans,
            'total': len(plans)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500