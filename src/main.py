from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, auth
import json
from planos import planos_bp
from jogos import jogos_bp

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurar Firebase
try:
    # Tentar carregar credenciais do Firebase
    firebase_key = os.getenv('FIREBASE_PRIVATE_KEY')
    if firebase_key:
        # Parse da chave privada (pode estar como string JSON)
        if firebase_key.startswith('{'):
            firebase_config = json.loads(firebase_key)
        else:
            firebase_config = {
                "type": "service_account",
                "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                "private_key": firebase_key.replace('\\n', '\n'),
                "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
            }
        
        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred)
        print("Firebase inicializado com sucesso!")
except Exception as e:
    print(f"Erro ao inicializar Firebase: {e}")
    print("Continuando sem Firebase...")

# Registrar blueprints
app.register_blueprint(planos_bp, url_prefix='/api')
app.register_blueprint(jogos_bp, url_prefix='/api')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Gabarita AI Backend is running!"})

@app.route('/api/auth/verify', methods=['POST'])
def verify_token():
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({"error": "Token não fornecido"}), 400
        
        # Verificar token do Firebase
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        return jsonify({
            "success": True,
            "uid": uid,
            "email": decoded_token.get('email'),
            "name": decoded_token.get('name')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)