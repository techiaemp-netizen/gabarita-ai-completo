from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
from services.chatgpt_service import chatgpt_service
from routes.questoes import CONTEUDOS_EDITAL
from routes.auth import auth_bp
from routes.questoes import questoes_bp
from routes.payments import payments_bp
from routes.opcoes import opcoes_bp
from routes.planos import planos_bp

app = Flask(__name__)
CORS(app)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(questoes_bp, url_prefix='/api/questoes')
app.register_blueprint(payments_bp)
app.register_blueprint(opcoes_bp, url_prefix='/api/opcoes')
app.register_blueprint(planos_bp, url_prefix='/api')

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Gabarita.AI Backend API',
        'status': 'online',
        'version': '1.0.1',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'health': '/health',
            'auth': '/api/auth/*',
            'questoes': '/api/questoes/*',
            'payments': '/api/payments/*'
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    # Simulação de login simples
    return jsonify({
        'success': True,
        'user': {
            'id': '1',
            'nome': data.get('email', 'Usuário'),
            'email': data.get('email'),
            'cargo': 'Enfermeiro',
            'bloco': 'Saúde'
        },
        'token': 'demo_token_123'
    })

# Rota removida - usando apenas a rota do blueprint questoes.py

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

@app.route('/api/usuarios/perfil', methods=['GET'])
def get_user_profile():
    """Endpoint para obter perfil do usuário"""
    try:
        # Dados simulados de perfil para desenvolvimento
        user_profile = {
            'id': 'user-123',
            'nome': 'Usuário Teste',
            'email': 'usuario@teste.com',
            'cargo': 'Enfermeiro',
            'bloco': 'Saúde',
            'nivel_escolaridade': 'Superior',
            'vida': 80,
            'pontuacao': 2847,
            'status': 'ativo',
            'plano': 'gratuito',
            'data_criacao': datetime.now().isoformat(),
            'ultimo_acesso': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'data': user_profile
        })
        
    except Exception as e:
        print(f"Erro ao buscar perfil: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao carregar perfil do usuário'
        }), 500

@app.route('/api/performance', methods=['GET'])
def get_performance():
    """Endpoint para obter dados de performance do usuário"""
    try:
        # Dados simulados de performance para desenvolvimento
        performance_data = {
            'questoes_respondidas': 1247,
            'questoes_corretas': 1059,
            'taxa_acerto': 85.0,
            'tempo_total_estudo': 18420,
            'dias_consecutivos': 12,
            'melhor_sequencia': 28,
            'nivel_atual': 23,
            'xp_atual': 2847,
            'xp_proximo_nivel': 3000,
            'ranking_posicao': 156,
            'ranking_total': 2847,
            'percentil': 94.5,
            'favoritas': 23,
            'listas_revisao': 8,
            'simulados_completos': 15,
            'media_tempo_questao': 45,
            'questoes_hoje': 15,
            'meta_diaria': 20,
            'progresso_semanal': 78,
            'meta_semanal': 140
        }
        
        return jsonify({
            'success': True,
            'data': performance_data
        })
        
    except Exception as e:
        print(f"Erro ao buscar performance: {e}")
        return jsonify({
            'success': False,
            'error': 'Erro ao carregar dados de performance'
        }), 500

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

