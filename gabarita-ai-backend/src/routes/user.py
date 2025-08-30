from flask import Blueprint, jsonify, request
from src.models.user import User, db
from datetime import datetime
import uuid

user_bp = Blueprint('user', __name__)

@user_bp.route('/usuarios', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/usuarios', methods=['POST'])
def create_user():
    
    data = request.json
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route('/usuarios/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@user_bp.route('/usuarios/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/usuarios/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

@user_bp.route('/usuarios/perfil', methods=['GET'])
def get_profile():
    """Obtém perfil do usuário autenticado"""
    try:
        # Para desenvolvimento, retornar um usuário simulado
        # Em produção, isso deveria# Verificar se há token de autorização
        auth_header = request.headers.get('Authorization')
        print(f"DEBUG - Authorization header: {auth_header}")
        # Para desenvolvimento, aceitar qualquer token ou permitir sem token
        # if not auth_header:
        #     return jsonify({'error': 'Authorization token is required'}), 401
            
        # Usuário simulado para desenvolvimento
        usuario_simulado = {
            'id': str(uuid.uuid4()),
            'name': 'Usuário Teste',
            'email': 'usuario@teste.com',
            'cpf': '123.456.789-00',
            'cargo': 'Enfermeiro',
            'bloco': 'Bloco 5 - Educação, Saúde, Desenvolvimento Social e Direitos Humanos',
            'nivel_escolaridade': 'Superior',
            'vida': 85,
            'pontuacao': 1250,
            'status': 'ativo',
            'data_criacao': datetime.now().isoformat(),
            'ultimo_acesso': datetime.now().isoformat()
        }
        
        return jsonify(usuario_simulado)
        
    except Exception as e:
        print(f"Erro ao buscar perfil: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/usuarios/perfil', methods=['PUT'])
def update_profile():
    """Atualiza perfil do usuário autenticado"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authorization token is required'}), 401
            
        data = request.get_json()
        
        # Para desenvolvimento, retornar os dados atualizados
        usuario_atualizado = {
            'id': str(uuid.uuid4()),
            'name': data.get('name', 'Usuário Teste'),
            'email': data.get('email', 'usuario@teste.com'),
            'cpf': data.get('cpf', '123.456.789-00'),
            'cargo': data.get('cargo', 'Enfermeiro'),
            'bloco': data.get('bloco', 'Bloco 5 - Educação, Saúde, Desenvolvimento Social e Direitos Humanos'),
            'nivel_escolaridade': data.get('nivel_escolaridade', 'Superior'),
            'vida': 85,
            'pontuacao': 1250,
            'status': 'ativo',
            'data_criacao': datetime.now().isoformat(),
            'ultimo_acesso': datetime.now().isoformat()
        }
        
        return jsonify(usuario_atualizado)
        
    except Exception as e:
        print(f"Erro ao atualizar perfil: {e}")
        return jsonify({'error': 'Internal server error'}), 500
