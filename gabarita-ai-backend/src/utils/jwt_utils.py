import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

class JWTManager:
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'gabarita-ai-secret-key-2024')
        self.algorithm = 'HS256'
        self.expiration_hours = 24
    
    def generate_token(self, user_data):
        """Gera um token JWT para o usuário"""
        try:
            payload = {
                'user_id': user_data.get('id'),
                'email': user_data.get('email'),
                'nome': user_data.get('nome'),
                'cargo': user_data.get('cargo'),
                'bloco': user_data.get('bloco'),
                'exp': datetime.utcnow() + timedelta(hours=self.expiration_hours),
                'iat': datetime.utcnow()
            }
            
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return token
        except Exception as e:
            print(f"Erro ao gerar token JWT: {e}")
            return None
    
    def verify_token(self, token):
        """Verifica e decodifica um token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return {'error': 'Token expirado'}
        except jwt.InvalidTokenError:
            return {'error': 'Token inválido'}
        except Exception as e:
            print(f"Erro ao verificar token JWT: {e}")
            return {'error': 'Erro na verificação do token'}
    
    def refresh_token(self, token):
        """Renova um token JWT válido"""
        payload = self.verify_token(token)
        if 'error' in payload:
            return None
        
        # Remove campos de tempo para gerar novo token
        user_data = {
            'id': payload.get('user_id'),
            'email': payload.get('email'),
            'nome': payload.get('nome'),
            'cargo': payload.get('cargo'),
            'bloco': payload.get('bloco')
        }
        
        return self.generate_token(user_data)

# Instância global do gerenciador JWT
jwt_manager = JWTManager()

def token_required(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Verificar se o token está no header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    'success': False,
                    'error': 'Formato de token inválido'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'error': 'Token de acesso necessário'
            }), 401
        
        # Verificar o token
        payload = jwt_manager.verify_token(token)
        if 'error' in payload:
            return jsonify({
                'success': False,
                'error': payload['error']
            }), 401
        
        # Adicionar dados do usuário ao contexto da requisição
        request.current_user = payload
        return f(*args, **kwargs)
    
    return decorated

def get_current_user():
    """Retorna os dados do usuário atual da requisição"""
    return getattr(request, 'current_user', None)