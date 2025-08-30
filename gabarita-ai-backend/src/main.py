from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
from .services.chatgpt_service import chatgpt_service
from .routes.questoes import CONTEUDOS_EDITAL
from .routes.signup import signup_bp
from .routes.auth import auth_bp
from .routes.user import user_bp
from .routes.questoes import questoes_bp
from .routes.planos import planos_bp
from .routes.jogos import jogos_bp
from .routes.news import news_bp
from .routes.opcoes import opcoes_bp
from .routes.ranking import ranking_bp
from .routes.simulados import simulados_bp
from .routes.payments import payments_bp
from .routes.performance import performance_bp

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configuração CORS global usando variáveis de ambiente
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, 
     origins=cors_origins,
     allow_headers=['Content-Type', 'Authorization', 'Accept', 'X-Requested-With'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
     supports_credentials=True)

# Registrar blueprints
app.register_blueprint(signup_bp, url_prefix='/api/auth')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(questoes_bp, url_prefix='/api/questoes')
app.register_blueprint(planos_bp, url_prefix='/api')
app.register_blueprint(jogos_bp, url_prefix='/api/jogos')
app.register_blueprint(news_bp, url_prefix='/api')
app.register_blueprint(opcoes_bp, url_prefix='/api')
app.register_blueprint(ranking_bp, url_prefix='/api')
app.register_blueprint(simulados_bp, url_prefix='/api')
app.register_blueprint(payments_bp, url_prefix='/api')
app.register_blueprint(performance_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def root():
    """Rota raiz da API"""
    return jsonify({
        'message': 'Gabarita.AI Backend API',
        'version': '1.0.0',
        'status': 'online',
        'endpoints': {
            'health': '/health',
            'auth': '/api/auth/*',
            'usuarios': '/api/usuarios',
            'questoes': '/api/questoes/*',
            'planos': '/api/planos',
            'jogos': '/api/jogos/*',
            'noticias': '/api/noticias',
            'opcoes': '/api/opcoes/*',
            'ranking': '/api/ranking',
            'simulados': '/api/simulados',
            'pagamentos': '/api/pagamentos/*'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'message': 'API funcionando corretamente',
        'timestamp': str(datetime.now())
    })

@app.route('/api/test', methods=['GET', 'OPTIONS'])
def test_endpoint():
    """Endpoint de teste público para verificar conectividade"""
    if request.method == 'OPTIONS':
        # Resposta para preflight CORS
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response
    
    return jsonify({
        'status': 'success',
        'message': 'Endpoint de teste funcionando',
        'timestamp': str(datetime.now()),
        'cors_enabled': True
    })

@app.route('/api/opcoes/test', methods=['GET', 'OPTIONS'])
def test_opcoes():
    """Endpoint de teste específico para opções"""
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        return response
    
    try:
        from .routes.questoes import CONTEUDOS_EDITAL
        total_cargos = len(CONTEUDOS_EDITAL) if CONTEUDOS_EDITAL else 0
        
        return jsonify({
            'status': 'success',
            'message': 'Teste de opções funcionando',
            'total_cargos': total_cargos,
            'conteudos_carregados': bool(CONTEUDOS_EDITAL),
            'timestamp': str(datetime.now())
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro no teste: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@app.route('/api/health', methods=['GET'])
def api_health():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

# Endpoint de login removido - agora usando o blueprint auth_bp
# O login real com JWT está implementado em src/routes/auth.py

# Rota removida - agora usando a rota do blueprint questoes_bp

@app.route('/api/questoes/<questao_id>/responder', methods=['POST'])
def responder_questao(questao_id):
    data = request.get_json()
    resposta = data.get('resposta')
    
    return jsonify({
        'success': True,
        'correto': resposta == 'C',
        'gabarito': 'C',
        'explicacao': 'Explicação detalhada da resposta'
    })

@app.route('/api/perplexity/explicacao', methods=['POST'])
def obter_explicacao_perplexity():
    import sys
    print("🔍 Requisição recebida para explicação do Perplexity")
    sys.stdout.flush()
    
    data = request.get_json()
    questao = data.get('questao', '')
    alternativa_correta = data.get('alternativa_correta', '')
    alternativa_escolhida = data.get('alternativa_escolhida', '')
    materia = data.get('materia', '')
    tema = data.get('tema', '')
    
    print(f"📝 Questão: {questao[:100]}...")
    print(f"✅ Alternativa correta: {alternativa_correta}")
    print(f"❌ Alternativa escolhida: {alternativa_escolhida}")
    print(f"📚 Matéria: {materia}")
    print(f"🎯 Tema: {tema}")
    sys.stdout.flush()
    
    try:
        # Criar prompt para explicação detalhada
        prompt_explicacao = f"""
        Explique detalhadamente por que a alternativa {alternativa_correta} é a correta para esta questão de concurso público:
        
        Questão: {questao}
        
        O candidato escolheu a alternativa {alternativa_escolhida}, mas a correta é {alternativa_correta}.
        
        Forneça:
        1. Explicação clara do conceito
        2. Por que a alternativa {alternativa_correta} está correta
        3. Por que a alternativa {alternativa_escolhida} está incorreta
        4. Fontes de estudo recomendadas sobre {tema} em {materia}
        
        Seja didático e inclua referências normativas quando aplicável.
        """
        
        print("🤖 Enviando prompt para o Perplexity...")
        sys.stdout.flush()
        
        # Usar o serviço ChatGPT/Perplexity para gerar explicação
        explicacao_detalhada = chatgpt_service.gerar_explicacao(prompt_explicacao)
        
        if explicacao_detalhada:
            print(f"✅ Explicação gerada com sucesso: {explicacao_detalhada[:100]}...")
            return jsonify({
                'success': True,
                'explicacao': explicacao_detalhada,
                'fontes': [
                    'Constituição Federal de 1988',
                    'Lei 8.080/90 - Lei Orgânica da Saúde',
                    'Lei 8.142/90 - Participação e Financiamento do SUS'
                ]
            })
        else:
            raise Exception("Não foi possível gerar explicação")
            
    except Exception as e:
        print(f"❌ Erro ao gerar explicação: {e}")
        sys.stdout.flush()
        
        # Fallback com explicação genérica
        explicacao_fallback = f"""
        A alternativa {alternativa_correta} é a correta para esta questão sobre {tema}.
        
        Para entender melhor este conceito, recomendo revisar:
        - Legislação específica sobre {materia}
        - Conceitos fundamentais de {tema}
        - Jurisprudência relacionada ao assunto
        
        Continue estudando e pratique mais questões sobre este tema!
        """
        
        return jsonify({
            'success': True,
            'explicacao': explicacao_fallback,
            'fontes': [
                'Material de estudo recomendado',
                'Legislação pertinente',
                'Doutrina especializada'
            ]
        })




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

