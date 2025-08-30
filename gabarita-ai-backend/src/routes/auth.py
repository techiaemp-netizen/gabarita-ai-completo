"""
Rotas de autenticação para o Gabarita.AI
"""
from flask import Blueprint, request, jsonify
from firebase_admin import auth, firestore
from src.config.firebase_config import firebase_config
from src.utils.jwt_utils import jwt_manager, token_required, get_current_user
from datetime import datetime, timedelta
import uuid
import jwt
import os

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para login de usuários"""
    try:
        data = request.get_json()
        email = data.get('email')
        # Aceitar tanto 'senha' quanto 'password' para compatibilidade
        senha = data.get('senha') or data.get('password')
        
        if not email or not senha:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        # Para desenvolvimento, simular autenticação
        # Em produção, usar Firebase Auth
        if firebase_config.is_connected():
            try:
                # Tentar autenticar com Firebase
                user = auth.get_user_by_email(email)
                usuario_data = _get_usuario_firestore(user.uid)
                
                if usuario_data:
                    # Gerar token JWT real
                    # Gerar token JWT real
                    token = jwt_manager.generate_token({
                        'id': user.uid,
                        'email': email,
                        'nome': usuario_data.get('nome', ''),
                        'cargo': usuario_data.get('cargo', ''),
                        'bloco': usuario_data.get('bloco', '')
                    })
                    
                    if not token:
                        return jsonify({'success': False, 'error': 'Erro ao gerar token de autenticação'}), 500
                    
                    return jsonify({
                        'success': True,
                        'data': {
                            'user': usuario_data,
                            'token': token
                        }
                    })
                else:
                    return jsonify({'success': False, 'error': 'Usuário não encontrado'}), 404
                    
            except auth.UserNotFoundError:
                return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
            except Exception as e:
                print(f"Erro na autenticação Firebase: {e}")
                # Fallback para autenticação simulada
                pass
        
        # Fallback: autenticação simulada para desenvolvimento
        usuario_simulado = {
            'id': str(uuid.uuid4()),
            'nome': 'Usuário Teste',
            'email': email,
            'cargo': 'Enfermeiro na Atenção Primária',
            'bloco': 'Bloco 5 - Educação, Saúde, Desenvolvimento Social e Direitos Humanos',
            'vida': 85,
            'pontuacao': 1250,
            'nivel_escolaridade': 'Superior',
            'status': 'ativo',
            'data_criacao': datetime.now().isoformat(),
            'ultimo_acesso': datetime.now().isoformat()
        }
        
        # Gerar token JWT para usuário simulado
        token = jwt_manager.generate_token({
            'id': usuario_simulado['id'],
            'email': email,
            'nome': usuario_simulado['nome'],
            'cargo': usuario_simulado['cargo'],
            'bloco': usuario_simulado['bloco']
        })
        
        if not token:
            return jsonify({'success': False, 'error': 'Erro ao gerar token de autenticação'}), 500

        return jsonify({
            'success': True,
            'data': {
                'user': usuario_simulado,
                'token': token
            }
        })
        
    except Exception as e:
        print(f"Erro no login: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    """Endpoint para cadastro de novos usuários"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        nome = data.get('nome') or data.get('name')  # Aceitar ambos os formatos
        email = data.get('email')
        senha = data.get('senha') or data.get('password')  # Aceitar ambos os formatos
        cargo = data.get('cargo')
        bloco = data.get('bloco')
        
        if not nome or not email or not senha or not cargo or not bloco:
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        # Validar confirmação de senha
        confirmar_senha = data.get('confirmarSenha') or data.get('confirmPassword')
        if confirmar_senha and senha != confirmar_senha:
            return jsonify({'success': False, 'error': 'Passwords do not match'}), 400
        
        nivel_escolaridade = data.get('nivel_escolaridade', 'Superior')
        
        # Verificar se e-mail já existe
        if firebase_config.is_connected():
            try:
                # Tentar criar usuário no Firebase Auth
                user = auth.create_user(
                    email=email,
                    password=senha,
                    display_name=nome
                )
                
                # Criar documento do usuário no Firestore
                usuario_data = {
                    'id': user.uid,
                    'nome': nome,
                    'email': email,
                    'cargo': cargo,
                    'bloco': bloco,
                    'nivel_escolaridade': nivel_escolaridade,
                    'vida': 80,  # Vida inicial
                    'pontuacao': 0,
                    'status': 'ativo',
                    'erros_por_tema': {},
                    'data_criacao': datetime.now().isoformat(),
                    'ultimo_acesso': datetime.now().isoformat()
                }
                
                # Salvar no Firestore
                db = firebase_config.get_db()
                db.collection('usuarios').document(user.uid).set(usuario_data)
                
                # Gerar token JWT real
                token = jwt_manager.generate_token({
                    'id': user.uid,
                    'email': email,
                    'nome': nome,
                    'cargo': cargo,
                    'bloco': bloco
                })
                
                if not token:
                    return jsonify({'success': False, 'error': 'Erro ao gerar token de autenticação'}), 500
                
                return jsonify({
                    'success': True,
                    'data': {
                        'user': usuario_data,
                        'token': token
                    }
                })
                
            except auth.EmailAlreadyExistsError:
                return jsonify({'success': False, 'error': 'E-mail já cadastrado'}), 409
            except Exception as e:
                print(f"Erro no cadastro Firebase: {e}")
                # Fallback para cadastro simulado
                pass
        
        # Cadastro simulado para desenvolvimento
        usuario_id = str(uuid.uuid4())
        usuario_data = {
            'id': usuario_id,
            'nome': nome,
            'email': email,
            'cargo': cargo,
            'bloco': bloco,
            'nivel_escolaridade': nivel_escolaridade,
            'vida': 80,
            'pontuacao': 0,
            'status': 'ativo',
            'erros_por_tema': {},
            'data_criacao': datetime.now().isoformat(),
            'ultimo_acesso': datetime.now().isoformat()
        }
        
        # Gerar token JWT para usuário simulado
        token = jwt_manager.generate_token({
            'id': usuario_id,
            'email': email,
            'nome': nome,
            'cargo': cargo,
            'bloco': bloco
        })
        
        if not token:
            return jsonify({'success': False, 'error': 'Erro ao gerar token de autenticação'}), 500
        
        return jsonify({
            'success': True,
            'data': {
                'user': usuario_data,
                'token': token
            }
        })
        
    except Exception as e:
        print(f"Erro no cadastro: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/verificar-token', methods=['POST'])
@token_required
def verificar_token():
    """Endpoint para verificar validade do token"""
    try:
        # Token já foi validado pelo decorator @token_required
        current_user = get_current_user()
        
        if not current_user:
            return jsonify({'erro': 'Usuário não encontrado'}), 404
        
        # Buscar dados completos do usuário
        if firebase_config.is_connected():
            try:
                usuario_data = _get_usuario_firestore(current_user['id'])
                
                if usuario_data:
                    # Atualizar último acesso
                    _atualizar_ultimo_acesso(current_user['id'])
                    
                    return jsonify({
                        'sucesso': True,
                        'usuario': usuario_data
                    })
                    
            except Exception as e:
                print(f"Erro ao buscar dados do usuário: {e}")
        
        # Retornar dados do token se não conseguir buscar no Firebase
        return jsonify({
            'sucesso': True,
            'usuario': current_user
        })
        
    except Exception as e:
        print(f"Erro na verificação do token: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@auth_bp.route('/google-auth', methods=['POST'])
def google_auth():
    """Endpoint para autenticação/cadastro com Google"""
    try:
        data = request.get_json()
        id_token = data.get('idToken')
        
        if not id_token:
            return jsonify({'error': 'Google token is required'}), 400
        
        if firebase_config.is_connected():
            try:
                # Verificar o token do Google
                decoded_token = auth.verify_id_token(id_token)
                uid = decoded_token['uid']
                email = decoded_token.get('email')
                nome = decoded_token.get('name', '')
                
                # Verificar se o usuário já existe
                usuario_existente = _get_usuario_firestore(uid)
                
                if usuario_existente:
                    # Usuário já existe, fazer login
                    _atualizar_ultimo_acesso(uid)
                    return jsonify({
                        'sucesso': True,
                        'usuario': usuario_existente,
                        'token': uid,
                        'isNewUser': False
                    })
                else:
                    # Novo usuário, criar perfil básico
                    db = firebase_config.get_db()
                    usuario_data = {
                        'nome': nome,
                        'nickname': nome.split(' ')[0] if nome else '',
                        'email': email,
                        'freeQuestionsRemaining': 3,
                        'createdAt': datetime.now().isoformat(),
                        'totalAnswered': 0,
                        'correctAnswers': 0,
                        'isGoogleUser': True,
                        'profileComplete': False
                    }
                    
                    # Salvar no Firestore
                    db.collection('usuarios').document(uid).set(usuario_data)
                    
                    return jsonify({
                        'sucesso': True,
                        'usuario': usuario_data,
                        'token': uid,
                        'isNewUser': True
                    })
                    
            except auth.InvalidIdTokenError:
                return jsonify({'error': 'Invalid Google token'}), 401
            except Exception as e:
                print(f"Erro na autenticação Google: {e}")
                return jsonify({'error': 'Google authentication error'}), 500
        else:
            # Modo desenvolvimento - simular autenticação Google
            usuario_simulado = {
                'id': str(uuid.uuid4()),
                'nome': 'Usuário Google Teste',
                'email': 'google@teste.com',
                'freeQuestionsRemaining': 3,
                'createdAt': datetime.now().isoformat(),
                'totalAnswered': 0,
                'correctAnswers': 0,
                'isGoogleUser': True,
                'profileComplete': False
            }
            
            return jsonify({
                'sucesso': True,
                'usuario': usuario_simulado,
                'token': 'google-test-token',
                'isNewUser': True
            })
            
    except Exception as e:
        print(f"Erro no Google Auth: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@auth_bp.route('/refresh-token', methods=['POST'])
@token_required
def refresh_token():
    """Endpoint para renovar token JWT"""
    try:
        current_user = get_current_user()
        
        # Gerar novo token com os dados atuais do usuário
        user_data = {
            'id': current_user.get('user_id'),
            'email': current_user.get('email'),
            'nome': current_user.get('nome'),
            'cargo': current_user.get('cargo'),
            'bloco': current_user.get('bloco')
        }
        
        new_token = jwt_manager.generate_token(user_data)
        if not new_token:
            return jsonify({
                'success': False,
                'error': 'Erro ao renovar token'
            }), 500
        
        return jsonify({
            'success': True,
            'data': {
                'token': new_token,
                'user': user_data
            }
        })
        
    except Exception as e:
        logging.error(f"Erro ao renovar token: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor'
        }), 500

@auth_bp.route('/complete-profile', methods=['POST'])
@token_required
def complete_profile():
    """Endpoint para completar perfil de usuários Google"""
    try:
        data = request.get_json()
        nickname = data.get('nickname')
        current_user = get_current_user()
        
        if not nickname:
            return jsonify({'error': 'Nickname is required'}), 400
            
        if len(nickname) < 3 or len(nickname) > 20:
            return jsonify({'error': 'Nickname must be between 3 and 20 characters'}), 400
        
        if firebase_config.is_connected():
            try:
                # Verificar se o token é válido
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token['uid']
                
                # Atualizar perfil no Firestore
                db = firebase_config.get_db()
                db.collection('usuarios').document(uid).update({
                    'nickname': nickname,
                    'profileComplete': True,
                    'updatedAt': datetime.now().isoformat()
                })
                
                # Buscar dados atualizados
                usuario_atualizado = _get_usuario_firestore(uid)
                
                return jsonify({
                    'sucesso': True,
                    'usuario': usuario_atualizado,
                    'mensagem': 'Perfil completado com sucesso'
                })
                
            except auth.InvalidIdTokenError:
                return jsonify({'error': 'Invalid token'}), 401
            except Exception as e:
                print(f"Erro ao completar perfil: {e}")
                return jsonify({'error': 'Error updating profile'}), 500
        else:
            # Modo desenvolvimento
            usuario_simulado = {
                'id': token,
                'nome': 'Usuário Google Teste',
                'nickname': nickname,
                'email': 'google@teste.com',
                'freeQuestionsRemaining': 3,
                'createdAt': datetime.now().isoformat(),
                'totalAnswered': 0,
                'correctAnswers': 0,
                'isGoogleUser': True,
                'profileComplete': True
            }
            
            return jsonify({
                'sucesso': True,
                'usuario': usuario_simulado,
                'mensagem': 'Perfil completado com sucesso'
            })
            
    except Exception as e:
        print(f"Erro ao completar perfil: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Endpoint para logout de usuários"""
    try:
        # Em uma implementação real, invalidar o token
        # Para desenvolvimento, apenas retornar sucesso
        return jsonify({'sucesso': True, 'mensagem': 'Logout realizado com sucesso'})
        
    except Exception as e:
        print(f"Erro no logout: {e}")
        return jsonify({'erro': 'Erro interno do servidor'}), 500

def _get_usuario_firestore(uid):
    """Busca dados do usuário no Firestore"""
    try:
        db = firebase_config.get_db()
        doc = db.collection('usuarios').document(uid).get()
        
        if doc.exists:
            return doc.to_dict()
        else:
            return None
            
    except Exception as e:
        print(f"Erro ao buscar usuário no Firestore: {e}")
        return None

def _atualizar_ultimo_acesso(uid):
    """Atualiza o último acesso do usuário"""
    try:
        db = firebase_config.get_db()
        db.collection('usuarios').document(uid).update({
            'ultimo_acesso': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Erro ao atualizar último acesso: {e}")
        pass

