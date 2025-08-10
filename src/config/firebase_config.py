"""
Configuração do Firebase para o Gabarita.AI
"""
import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv

load_dotenv()

class FirebaseConfig:
    """Classe para gerenciar configurações do Firebase"""
    
    def __init__(self):
        self.db = None
        self.auth = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Inicializa o Firebase com as credenciais"""
        try:
            # Verificar se as credenciais básicas estão presentes
            project_id = os.getenv('FIREBASE_PROJECT_ID')
            client_email = os.getenv('FIREBASE_CLIENT_EMAIL')
            private_key = os.getenv('FIREBASE_PRIVATE_KEY')
            private_key_id = os.getenv('FIREBASE_PRIVATE_KEY_ID')
            
            # Verificar se todas as credenciais necessárias estão presentes
            missing_vars = []
            if not project_id or project_id.strip() == '' or 'your_' in project_id:
                missing_vars.append('FIREBASE_PROJECT_ID')
            if not client_email or client_email.strip() == '' or 'your_' in client_email:
                missing_vars.append('FIREBASE_CLIENT_EMAIL')
            if not private_key or private_key.strip() == '' or 'YOUR_' in private_key:
                missing_vars.append('FIREBASE_PRIVATE_KEY')
            if not private_key_id or private_key_id.strip() == '' or 'your_' in private_key_id:
                missing_vars.append('FIREBASE_PRIVATE_KEY_ID')
            
            if missing_vars:
                print(f"[FIREBASE] ❌ Credenciais não configuradas: {', '.join(missing_vars)}")
                print("[FIREBASE] 📝 Configure as variáveis no arquivo .env seguindo CONFIGURACAO_FIREBASE_MERCADOPAGO.md")
                print("[FIREBASE] 🔧 Modo desenvolvimento ativo - Firebase desabilitado")
                self.db = None
                self.auth = None
                return
            
            if not firebase_admin._apps:
                # Configuração para desenvolvimento usando variáveis de ambiente
                cred_dict = {
                    "type": "service_account",
                    "project_id": project_id,
                    "private_key_id": private_key_id,
                    "private_key": private_key.replace('\\n', '\n'),
                    "client_email": client_email,
                    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                    "auth_uri": os.getenv('FIREBASE_AUTH_URI', 'https://accounts.google.com/o/oauth2/auth'),
                    "token_uri": os.getenv('FIREBASE_TOKEN_URI', 'https://oauth2.googleapis.com/token'),
                }
                
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                print(f"[FIREBASE] ✅ Firebase inicializado com sucesso!")
                print(f"[FIREBASE] 🔥 Projeto: {project_id}")
            
            # Inicializar serviços
            self.db = firestore.client()
            self.auth = auth
            print("[FIREBASE] ✅ Firestore e Auth conectados com sucesso!")
            
        except Exception as e:
            print(f"[FIREBASE] ❌ Erro ao inicializar Firebase: {e}")
            print("[FIREBASE] 💡 Verifique se as credenciais estão corretas no arquivo .env")
            print("[FIREBASE] 📖 Consulte CONFIGURACAO_FIREBASE_MERCADOPAGO.md para ajuda")
            print("[FIREBASE] 🔧 Continuando em modo desenvolvimento...")
            self.db = None
            self.auth = None
    
    def get_db(self):
        """Retorna a instância do Firestore"""
        return self.db
    
    def get_auth(self):
        """Retorna a instância do Auth"""
        return self.auth
    
    def is_connected(self):
        """Verifica se o Firebase está conectado"""
        return self.db is not None

# Instância global do Firebase
firebase_config = FirebaseConfig()

