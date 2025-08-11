from config.firebase_config import firebase_config
from datetime import datetime, timedelta
import uuid

class PlanoService:
    def __init__(self):
        self.db = firebase_config.get_firestore()
    
    def listar_planos(self):
        """Lista todos os planos disponíveis"""
        try:
            planos_ref = self.db.collection('planos')
            planos = []
            
            for doc in planos_ref.stream():
                plano_data = doc.to_dict()
                plano_data['id'] = doc.id
                planos.append(plano_data)
            
            return planos
        except Exception as e:
            raise Exception(f"Erro ao listar planos: {str(e)}")
    
    def obter_plano_usuario(self, user_id):
        """Obtém o plano atual do usuário"""
        try:
            user_ref = self.db.collection('usuarios').document(user_id)
            user_doc = user_ref.get()
            
            if not user_doc.exists:
                return {'plano': 'free', 'ativo': False}
            
            user_data = user_doc.to_dict()
            plano_atual = user_data.get('plano_atual', {})
            
            # Verifica se o plano ainda está ativo
            if plano_atual.get('data_expiracao'):
                data_expiracao = plano_atual['data_expiracao']
                if isinstance(data_expiracao, str):
                    data_expiracao = datetime.fromisoformat(data_expiracao)
                
                if datetime.now() > data_expiracao:
                    # Plano expirado, atualiza para free
                    user_ref.update({
                        'plano_atual': {
                            'plano_id': 'free',
                            'nome': 'Gratuito',
                            'ativo': False,
                            'data_ativacao': datetime.now().isoformat(),
                            'data_expiracao': None
                        }
                    })
                    return {'plano': 'free', 'ativo': False}
            
            return plano_atual
        except Exception as e:
            raise Exception(f"Erro ao obter plano do usuário: {str(e)}")
    
    def ativar_plano(self, user_id, plano_id):
        """Ativa um plano para o usuário"""
        try:
            # Busca informações do plano
            plano_ref = self.db.collection('planos').document(plano_id)
            plano_doc = plano_ref.get()
            
            if not plano_doc.exists:
                raise Exception("Plano não encontrado")
            
            plano_data = plano_doc.to_dict()
            
            # Calcula data de expiração
            data_ativacao = datetime.now()
            duracao_dias = plano_data.get('duracao_dias', 30)
            data_expiracao = data_ativacao + timedelta(days=duracao_dias)
            
            # Atualiza o usuário com o novo plano
            user_ref = self.db.collection('usuarios').document(user_id)
            user_ref.update({
                'plano_atual': {
                    'plano_id': plano_id,
                    'nome': plano_data.get('nome'),
                    'ativo': True,
                    'data_ativacao': data_ativacao.isoformat(),
                    'data_expiracao': data_expiracao.isoformat()
                }
            })
            
            # Registra no histórico
            historico_ref = self.db.collection('historico_planos')
            historico_ref.add({
                'user_id': user_id,
                'plano_id': plano_id,
                'nome_plano': plano_data.get('nome'),
                'acao': 'ativacao',
                'data': data_ativacao.isoformat(),
                'valor': plano_data.get('preco', 0)
            })
            
            return {
                'message': 'Plano ativado com sucesso',
                'plano': {
                    'id': plano_id,
                    'nome': plano_data.get('nome'),
                    'data_expiracao': data_expiracao.isoformat()
                }
            }
        except Exception as e:
            raise Exception(f"Erro ao ativar plano: {str(e)}")
    
    def verificar_acesso(self, user_id, funcionalidade):
        """Verifica se o usuário tem acesso a uma funcionalidade"""
        try:
            plano_usuario = self.obter_plano_usuario(user_id)
            
            if not plano_usuario.get('ativo', False):
                return False
            
            plano_id = plano_usuario.get('plano_id', 'free')
            
            # Busca as permissões do plano
            plano_ref = self.db.collection('planos').document(plano_id)
            plano_doc = plano_ref.get()
            
            if not plano_doc.exists:
                return False
            
            plano_data = plano_doc.to_dict()
            funcionalidades = plano_data.get('funcionalidades', [])
            
            return funcionalidade in funcionalidades
        except Exception as e:
            raise Exception(f"Erro ao verificar acesso: {str(e)}")
    
    def obter_limite_questoes(self, user_id):
        """Obtém o limite de questões do usuário"""
        try:
            plano_usuario = self.obter_plano_usuario(user_id)
            plano_id = plano_usuario.get('plano_id', 'free')
            
            # Busca o limite do plano
            plano_ref = self.db.collection('planos').document(plano_id)
            plano_doc = plano_ref.get()
            
            if not plano_doc.exists:
                return 3  # Limite padrão para plano free
            
            plano_data = plano_doc.to_dict()
            return plano_data.get('limite_questoes', 3)
        except Exception as e:
            raise Exception(f"Erro ao obter limite de questões: {str(e)}")
    
    def processar_pagamento(self, user_id, plano_id, metodo_pagamento):
        """Processa o pagamento de um plano"""
        try:
            # Aqui você integraria com um gateway de pagamento
            # Por enquanto, vamos simular um pagamento aprovado
            
            # Busca informações do plano
            plano_ref = self.db.collection('planos').document(plano_id)
            plano_doc = plano_ref.get()
            
            if not plano_doc.exists:
                raise Exception("Plano não encontrado")
            
            plano_data = plano_doc.to_dict()
            
            # Simula processamento do pagamento
            pagamento_id = str(uuid.uuid4())
            
            # Registra o pagamento
            pagamento_ref = self.db.collection('pagamentos')
            pagamento_ref.add({
                'id': pagamento_id,
                'user_id': user_id,
                'plano_id': plano_id,
                'valor': plano_data.get('preco', 0),
                'metodo_pagamento': metodo_pagamento,
                'status': 'aprovado',
                'data': datetime.now().isoformat()
            })
            
            # Ativa o plano
            resultado_ativacao = self.ativar_plano(user_id, plano_id)
            
            return {
                'message': 'Pagamento processado com sucesso',
                'pagamento_id': pagamento_id,
                'status': 'aprovado',
                'plano': resultado_ativacao['plano']
            }
        except Exception as e:
            raise Exception(f"Erro ao processar pagamento: {str(e)}")
    
    def obter_historico_planos(self, user_id):
        """Obtém o histórico de planos do usuário"""
        try:
            historico_ref = self.db.collection('historico_planos').where('user_id', '==', user_id)
            historico = []
            
            for doc in historico_ref.stream():
                historico_data = doc.to_dict()
                historico_data['id'] = doc.id
                historico.append(historico_data)
            
            # Ordena por data (mais recente primeiro)
            historico.sort(key=lambda x: x.get('data', ''), reverse=True)
            
            return historico
        except Exception as e:
            raise Exception(f"Erro ao obter histórico de planos: {str(e)}")

# Instância global do serviço
plano_service = PlanoService()
