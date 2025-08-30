from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from firebase_admin import firestore
import re

signup_bp = Blueprint('signup', __name__)
db = firestore.client()

def validate_email(email):
    """Valida formato do email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Valida se a senha atende aos criterios minimos"""
    if len(password) < 6:
        return False, "Password must have at least 6 characters"
    return True, ""

def validate_nickname(nickname):
    """Valida se o apelido atende aos criterios"""
    if len(nickname) < 4:
        return False, "Nickname must have at least 4 characters"
    return True, ""

@signup_bp.route('/signup', methods=['POST'])
@signup_bp.route('/cadastro', methods=['POST'])  # Alias para compatibilidade com frontend
def signup():
    """Endpoint para cadastro de usuario com hash de senha"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatorios - aceitar 'nome', 'nomeCompleto' ou 'name'
        nome_completo = data.get('nome') or data.get('nomeCompleto') or data.get('name')
        if not nome_completo:
            return jsonify({
                'success': False,
                'error': 'Name field is required'
            }), 400
            
        required_fields = ['cpf', 'email', 'senha', 'cargo', 'bloco']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Field {field} is required'
                }), 400
        
        nome_completo = nome_completo.strip()
        cpf = data['cpf'].strip()
        email = data['email'].strip().lower()
        senha = data['senha']
        cargo = data['cargo'].strip()
        bloco = data['bloco'].strip()
        
        # Validacoes
        if not validate_email(email):
            return jsonify({
                'success': False,
                'error': 'Invalid email'
            }), 400
        
        # Validar CPF (implementação básica)
        if not cpf or len(cpf.replace('.', '').replace('-', '')) != 11:
            return jsonify({
                'success': False,
                'error': 'Invalid CPF'
            }), 400
        
        is_valid_password, password_error = validate_password(senha)
        if not is_valid_password:
            return jsonify({
                'success': False,
                'error': password_error
            }), 400
        
        # Verificar se email ja existe
        users_ref = db.collection('users')
        existing_user = users_ref.where('email', '==', email).limit(1).get()
        
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Email already registered'
            }), 409
        
        # Verificar se CPF ja existe
        existing_cpf = users_ref.where('cpf', '==', cpf).limit(1).get()
        
        if existing_cpf:
            return jsonify({
                'success': False,
                'error': 'CPF already registered'
            }), 409
        
        # Gerar hash da senha
        password_hash = generate_password_hash(senha)
        
        # Criar usuario no Firestore
        user_data = {
            'nomeCompleto': nome_completo,
            'cpf': cpf,
            'email': email,
            'password_hash': password_hash,
            'cargo': cargo,
            'bloco': bloco,
            'freeQuestionsRemaining': 3,
            'createdAt': firestore.SERVER_TIMESTAMP,
            'totalAnswered': 0,
            'correctAnswers': 0,
            'planId': 'free',
            'profileComplete': True
        }
        
        # Adicionar usuario
        doc_ref = users_ref.add(user_data)
        user_id = doc_ref[1].id
        
        # Gerar token simples para desenvolvimento local
        import jwt
        import datetime
        
        token_payload = {
            'user_id': user_id,
            'email': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }
        token = jwt.encode(token_payload, 'dev-secret-key', algorithm='HS256')
        
        # Retornar dados no formato esperado pelo frontend
        usuario_response = {
            'id': user_id,
            'nome': nome_completo,
            'email': email,
            'cpf': cpf,
            'cargo': cargo,
            'bloco': bloco,
            'firebaseUid': data.get('firebaseUid')
        }
        
        return jsonify({
            'success': True,
            'data': {
                'token': token,
                'user': usuario_response
            },
            'message': 'User registered successfully'
        }), 201
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

# Endpoint de login removido - agora usando o blueprint auth_bp
# O login real com JWT está implementado em src/routes/auth.py
# @signup_bp.route('/login', methods=['POST'])
# def login():
#     """Endpoint para login com verificacao de hash"""
#     try:
#         data = request.get_json()
#         
#         email = data.get('email', '').strip().lower()
#         senha = data.get('senha', '')
#         
#         if not email or not senha:
#             return jsonify({
#                 'sucesso': False,
#                 'erro': 'Email e senha sao obrigatorios'
#             }), 400
#         
#         # Buscar usuario por email
#         users_ref = db.collection('users')
#         user_query = users_ref.where('email', '==', email).limit(1).get()
#         
#         if not user_query:
#             return jsonify({
#                 'sucesso': False,
#                 'erro': 'Usuario nao encontrado'
#             }), 404
#         
#         user_doc = user_query[0]
#         user_data = user_doc.to_dict()
#         
#         # Verificar senha
#         if not check_password_hash(user_data.get('password_hash', ''), senha):
#             return jsonify({
#                 'sucesso': False,
#                 'erro': 'Senha incorreta'
#             }), 401
#         
#         # Remover hash da senha dos dados retornados
#         user_data.pop('password_hash', None)
#         user_data['id'] = user_doc.id
#         
#         return jsonify({
#             'sucesso': True,
#             'mensagem': 'Login realizado com sucesso',
#             'usuario': user_data
#         }), 200
#         
#     except Exception as e:
#         print(f"Erro no login: {str(e)}")
#         return jsonify({
#             'sucesso': False,
#             'erro': 'Erro interno do servidor'
#         }), 500