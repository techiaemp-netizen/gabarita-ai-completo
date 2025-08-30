from flask import Blueprint, jsonify, request
from datetime import datetime

simulados_bp = Blueprint('simulados', __name__)

@simulados_bp.route('/simulados', methods=['GET'])
def get_simulados():
    """Endpoint para obter lista de simulados disponíveis"""
    try:
        simulados_data = [
            {
                'id': 1,
                'titulo': 'Simulado de Enfermagem - Básico',
                'descricao': 'Simulado com questões básicas de enfermagem',
                'total_questoes': 20,
                'tempo_limite': 60,  # em minutos
                'categoria': 'Enfermagem',
                'nivel': 'Básico',
                'ativo': True
            },
            {
                'id': 2,
                'titulo': 'Simulado de Medicina - Avançado',
                'descricao': 'Simulado com questões avançadas de medicina',
                'total_questoes': 30,
                'tempo_limite': 90,
                'categoria': 'Medicina',
                'nivel': 'Avançado',
                'ativo': True
            },
            {
                'id': 3,
                'titulo': 'Simulado Geral - Conhecimentos Básicos',
                'descricao': 'Simulado com questões gerais de conhecimentos básicos',
                'total_questoes': 25,
                'tempo_limite': 75,
                'categoria': 'Geral',
                'nivel': 'Intermediário',
                'ativo': True
            }
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'simulados': simulados_data,
                'total': len(simulados_data)
            },
            'timestamp': str(datetime.now())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting simulados: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@simulados_bp.route('/simulados/<int:simulado_id>', methods=['GET'])
def get_simulado(simulado_id):
    """Endpoint para obter um simulado específico"""
    try:
        # Simulação de dados do simulado específico
        simulado = {
            'id': simulado_id,
            'titulo': f'Simulado #{simulado_id}',
            'descricao': f'Descrição do simulado {simulado_id}',
            'questoes': [
                {
                    'id': 1,
                    'pergunta': 'Qual é a principal função do sistema cardiovascular?',
                    'alternativas': [
                        'Digestão de alimentos',
                        'Transporte de nutrientes e oxigênio',
                        'Produção de hormônios',
                        'Filtração de toxinas'
                    ],
                    'resposta_correta': 1
                },
                {
                    'id': 2,
                    'pergunta': 'O que significa a sigla SUS?',
                    'alternativas': [
                        'Sistema Único de Saúde',
                        'Serviço Universal de Saúde',
                        'Sistema Unificado de Saúde',
                        'Serviço Único de Saúde'
                    ],
                    'resposta_correta': 0
                }
            ],
            'tempo_limite': 60,
            'total_questoes': 2
        }
        
        return jsonify({
            'success': True,
            'data': simulado,
            'timestamp': str(datetime.now())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error getting simulado: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@simulados_bp.route('/simulados/<int:simulado_id>/resultado', methods=['POST'])
def submit_simulado_resultado(simulado_id):
    """Endpoint para submeter resultado de um simulado"""
    try:
        data = request.get_json()
        respostas = data.get('respostas', [])
        tempo_gasto = data.get('tempo_gasto', 0)
        
        # Simulação de correção
        acertos = 0
        total_questoes = len(respostas)
        
        for resposta in respostas:
            # Simulação simples - considerar que 70% das respostas estão corretas
            if resposta.get('resposta_usuario', -1) == resposta.get('resposta_correta', -1):
                acertos += 1
        
        percentual = (acertos / total_questoes * 100) if total_questoes > 0 else 0
        
        resultado = {
            'simulado_id': simulado_id,
            'acertos': acertos,
            'total_questoes': total_questoes,
            'percentual': round(percentual, 2),
            'tempo_gasto': tempo_gasto,
            'aprovado': percentual >= 70,
            'timestamp': str(datetime.now())
        }
        
        return jsonify({
            'success': True,
            'data': resultado,
            'timestamp': str(datetime.now())
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error processing result: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@simulados_bp.route('/simulados/submit', methods=['POST'])
def submit_simulado():
    """Submete um simulado e calcula o score"""
    try:
        data = request.get_json()
        usuario_id = data.get('usuario_id')
        respostas = data.get('respostas', [])
        
        if not usuario_id or not respostas:
            return jsonify({'success': False, 'error': 'Required data not provided'}), 400
        
        # Calcular estatísticas
        total_questoes = len(respostas)
        acertos = sum(1 for r in respostas if r.get('resposta_usuario') == r.get('gabarito'))
        erros = total_questoes - acertos
        taxa_acerto = (acertos / total_questoes * 100) if total_questoes > 0 else 0
        tempo_total = sum(r.get('tempo_resposta', 0) for r in respostas)
        tempo_medio = tempo_total / total_questoes if total_questoes > 0 else 0
        
        # Calcular score (0-1000 pontos)
        score = int((acertos / total_questoes * 1000)) if total_questoes > 0 else 0
        
        # Resultado do simulado
        resultado = {
            'simulado_id': f'sim-{usuario_id}-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'usuario_id': usuario_id,
            'data_realizacao': datetime.now().isoformat(),
            'total_questoes': total_questoes,
            'acertos': acertos,
            'erros': erros,
            'taxa_acerto': round(taxa_acerto, 2),
            'tempo_total': tempo_total,
            'tempo_medio': round(tempo_medio, 2),
            'score': score,
            'status': 'concluido'
        }
        
        return jsonify({
            'success': True,
            'data': resultado,
            'message': f'Simulado concluído! Você acertou {acertos} de {total_questoes} questões ({taxa_acerto:.1f}%)',
            'timestamp': str(datetime.now())
        })
        
    except Exception as e:
        print(f"Erro ao processar simulado: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'timestamp': str(datetime.now())
        }), 500