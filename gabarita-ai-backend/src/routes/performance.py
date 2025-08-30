from flask import Blueprint, jsonify

performance_bp = Blueprint('performance', __name__)

@performance_bp.route('/performance', methods=['GET'])
def get_performance():
    """Retorna dados de performance do usuário"""
    try:
        # Dados simulados de performance
        performance_data = {
            'total_questoes': 150,
            'acertos': 120,
            'erros': 30,
            'taxa_acerto': 80.0,
            'tempo_medio': 45.5,
            'sequencia_atual': 5,
            'melhor_sequencia': 12,
            'nivel_atual': 'Intermediário',
            'pontos_totais': 2450,
            'progresso_semanal': [
                {'dia': 'Seg', 'questoes': 15, 'acertos': 12},
                {'dia': 'Ter', 'questoes': 20, 'acertos': 16},
                {'dia': 'Qua', 'questoes': 18, 'acertos': 15},
                {'dia': 'Qui', 'questoes': 22, 'acertos': 18},
                {'dia': 'Sex', 'questoes': 25, 'acertos': 20}
            ],
            'desempenho_por_materia': [
                {'materia': 'SUS', 'total': 50, 'acertos': 42, 'taxa': 84.0},
                {'materia': 'Enfermagem', 'total': 60, 'acertos': 45, 'taxa': 75.0},
                {'materia': 'Saúde Pública', 'total': 40, 'acertos': 33, 'taxa': 82.5}
            ]
        }
        return jsonify({'success': True, 'data': performance_data})
    except Exception as e:
        print(f"Erro ao obter performance: {e}")
        return jsonify({'success': False, 'error': 'Erro interno do servidor'}), 500