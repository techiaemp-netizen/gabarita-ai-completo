"""
Rotas de autenticação para o Gabarita.AI
"""
from flask import Blueprint, request, jsonify
from firebase_admin import auth, firestore
from config.firebase_config import firebase_config
import uuid
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint para login de usuários"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        # Aceitar tanto 'senha' quanto 'password'
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
                    return jsonify({
                        'success': True,
                        'data': {
                            'user': usuario_data,
                            'token': user.uid  # Em produção, usar token JWT
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
        
        # Autenticação simulada para desenvolvimento
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
        
        return jsonify({
            'success': True,
            'data': {
                'user': usuario_simulado,
                'token': usuario_simulado['id']
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
        
        # Validar dados obrigatórios - aceitar nome/name e senha/password
        nome = data.get('nome') or data.get('name')
        email = data.get('email')
        senha = data.get('senha') or data.get('password')
        cargo = data.get('cargo')
        bloco = data.get('bloco')
        
        campos_obrigatorios = {
            'nome': nome,
            'email': email,
            'senha': senha,
            'cargo': cargo,
            'bloco': bloco
        }
        
        for campo, valor in campos_obrigatorios.items():
            if not valor:
                return jsonify({'success': False, 'error': f'Campo {campo} é obrigatório'}), 400
        
        # Validar confirmação de senha
        confirmar_senha = data.get('confirmarSenha') or data.get('confirmPassword')
        if confirmar_senha and senha != confirmar_senha:
            return jsonify({'success': False, 'error': 'Senhas não coincidem'}), 400
        
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
                if db is not None:
                    db.collection('usuarios').document(user.uid).set(usuario_data)
                
                return jsonify({
                    'success': True,
                    'data': {
                        'user': usuario_data,
                        'token': user.uid
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
        
        return jsonify({
            'success': True,
            'data': {
                'user': usuario_data,
                'token': usuario_id
            }
        })
        
    except Exception as e:
        print(f"Erro no cadastro: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/verificar-token', methods=['POST'])
def verificar_token():
    """Endpoint para verificar validade do token"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'success': False, 'error': 'Token is required'}), 400
        
        if firebase_config.is_connected():
            try:
                # Verificar token com Firebase Auth
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token['uid']
                
                # Buscar dados do usuário
                usuario_data = _get_usuario_firestore(uid)
                
                if usuario_data:
                    # Atualizar último acesso
                    _atualizar_ultimo_acesso(uid)
                    
                    return jsonify({
                        'success': True,
                        'data': {
                            'user': usuario_data
                        }
                    })
                else:
                    return jsonify({'success': False, 'error': 'Usuário não encontrado'}), 404
                    
            except auth.InvalidIdTokenError:
                return jsonify({'success': False, 'error': 'Token inválido'}), 401
            except Exception as e:
                print(f"Erro na verificação do token: {e}")
                # Fallback para verificação simulada
                pass
        
        # Verificação simulada para desenvolvimento
        # Em desenvolvimento, qualquer token é válido
        usuario_simulado = {
            'id': token,
            'nome': 'Usuário Teste',
            'email': 'teste@gabarita.ai',
            'cargo': 'Enfermeiro na Atenção Primária',
            'bloco': 'Bloco 5',
            'vida': 85,
            'pontuacao': 1250
        }
        
        return jsonify({
            'success': True,
            'data': {
                'user': usuario_simulado
            }
        })
        
    except Exception as e:
        print(f"Erro na verificação do token: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/google-auth', methods=['POST'])
def google_auth():
    """Endpoint para autenticação/cadastro com Google"""
    try:
        data = request.get_json()
        id_token = data.get('idToken')
        
        if not id_token:
            return jsonify({'success': False, 'error': 'Token do Google é obrigatório'}), 400
        
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
                        'success': True,
                        'data': {
                            'user': usuario_existente,
                            'token': uid,
                            'isNewUser': False
                        }
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
                        'success': True,
                        'data': {
                            'user': usuario_data,
                            'token': uid,
                            'isNewUser': True
                        }
                    })
                    
            except auth.InvalidIdTokenError:
                return jsonify({'success': False, 'error': 'Token do Google inválido'}), 401
            except Exception as e:
                print(f"Erro na autenticação Google: {e}")
                return jsonify({'success': False, 'error': 'Erro na autenticação com Google'}), 500
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
                'success': True,
                'data': {
                    'user': usuario_simulado,
                    'token': 'google-test-token',
                    'isNewUser': True
                }
            })
            
    except Exception as e:
        print(f"Erro no Google Auth: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/complete-profile', methods=['POST'])
def complete_profile():
    """Endpoint para completar perfil de usuários Google"""
    try:
        data = request.get_json()
        nickname = data.get('nickname')
        
        # Obter token do header Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'Token de autorização é obrigatório'}), 401
            
        token = auth_header.split(' ')[1]
        
        if not nickname:
            return jsonify({'success': False, 'error': 'Nickname é obrigatório'}), 400
            
        if len(nickname) < 3 or len(nickname) > 20:
            return jsonify({'success': False, 'error': 'Nickname deve ter entre 3 e 20 caracteres'}), 400
        
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
                    'success': True,
                    'data': {
                        'user': usuario_atualizado
                    },
                    'message': 'Perfil completado com sucesso'
                })
                
            except auth.InvalidIdTokenError:
                return jsonify({'success': False, 'error': 'Token inválido'}), 401
            except Exception as e:
                print(f"Erro ao completar perfil: {e}")
                return jsonify({'success': False, 'error': 'Erro ao atualizar perfil'}), 500
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
                'success': True,
                'data': {
                    'user': usuario_simulado
                },
                'message': 'Perfil completado com sucesso'
            })
            
    except Exception as e:
        print(f"Erro ao completar perfil: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Endpoint para logout de usuários"""
    try:
        # Em uma implementação real, invalidar o token
        # Para desenvolvimento, apenas retornar sucesso
        return jsonify({
            'success': True, 
            'message': 'Logout realizado com sucesso'
        })
        
    except Exception as e:
        print(f"Erro no logout: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

@auth_bp.route('/update-profile', methods=['PUT'])
def update_profile():
    """Endpoint para atualizar perfil do usuário"""
    try:
        data = request.get_json()
        
        # Obter token do header Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'Token de autorização é obrigatório'}), 401
            
        token = auth_header.split(' ')[1]
        
        if firebase_config.is_connected():
            try:
                # Verificar se o token é válido
                decoded_token = auth.verify_id_token(token)
                uid = decoded_token['uid']
                
                # Preparar dados para atualização
                update_data = {}
                if data.get('cargo'):
                    update_data['cargo'] = data['cargo']
                if data.get('bloco'):
                    update_data['bloco'] = data['bloco']
                if data.get('nome') or data.get('name'):
                    update_data['nome'] = data.get('nome') or data.get('name')
                if data.get('nickname'):
                    update_data['nickname'] = data['nickname']
                    
                update_data['updatedAt'] = datetime.now().isoformat()
                
                # Atualizar perfil no Firestore
                db = firebase_config.get_db()
                db.collection('usuarios').document(uid).update(update_data)
                
                # Buscar dados atualizados
                usuario_atualizado = _get_usuario_firestore(uid)
                
                return jsonify({
                    'success': True,
                    'data': {
                        'user': usuario_atualizado
                    },
                    'message': 'Perfil atualizado com sucesso'
                })
                
            except auth.InvalidIdTokenError:
                print(f"Token Firebase inválido, usando modo desenvolvimento: {token}")
                # Fallback para modo desenvolvimento
                pass
            except Exception as e:
                print(f"Erro ao atualizar perfil Firebase: {e}")
                # Fallback para modo desenvolvimento
                pass
        
        # Modo desenvolvimento - simular atualização (usado como fallback também)
        usuario_simulado = {
            'id': token,
            'nome': data.get('nome') or data.get('name', 'user'),
            'email': 'raf@el.com',
            'cargo': data.get('cargo', 'Analista Judiciario'),
            'bloco': data.get('bloco', 'Bloco 6 - Controle e Fiscalizacao'),
            'vida': 80,
            'pontuacao': 0,
            'status': 'ativo',
            'updatedAt': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': {
                'user': usuario_simulado
            },
            'message': 'Perfil atualizado com sucesso'
        })
            
    except Exception as e:
        print(f"Erro ao atualizar perfil: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500

def _get_usuario_firestore(uid):
    """Busca dados do usuário no Firestore"""
    try:
        db = firebase_config.get_db()
        if db is None:
            print("⚠️ Firebase não configurado, não é possível buscar usuário")
            return None
            
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
        if db is None:
            print("⚠️ Firebase não configurado, não é possível atualizar último acesso")
            return
            
        db.collection('usuarios').document(uid).update({
            'ultimo_acesso': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Erro ao atualizar último acesso: {e}")
        pass

