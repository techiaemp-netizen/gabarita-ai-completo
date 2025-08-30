from flask import Blueprint, jsonify, request
from datetime import datetime
import json

ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/ranking', methods=['GET'])
def get_ranking():
    """Endpoint para obter o ranking de usuários"""
    try:
        # Simulação de dados de ranking
        ranking_data = [
            {
                'id': 1,
                'nome': 'João Silva',
                'pontuacao': 950,
                'posicao': 1,
                'simulados_realizados': 15,
                'media_acertos': 85.5
            },
            {
                'id': 2,
                'nome': 'Maria Santos',
                'pontuacao': 920,
                'posicao': 2,
                'simulados_realizados': 12,
                'media_acertos': 82.3
            },
            {
                'id': 3,
                'nome': 'Pedro Costa',
                'pontuacao': 890,
                'posicao': 3,
                'simulados_realizados': 18,
                'media_acertos': 79.8
            }
        ]
        
        return jsonify({
            'sucesso': True,
            'ranking': ranking_data,
            'total_usuarios': len(ranking_data),
            'timestamp': str(datetime.now())
        })
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao obter ranking: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@ranking_bp.route('/ranking/usuario/<int:user_id>', methods=['GET'])
def get_user_ranking(user_id):
    """Endpoint para obter a posição específica de um usuário no ranking"""
    try:
        # Simulação de dados do usuário específico
        user_ranking = {
            'id': user_id,
            'nome': 'Usuário Exemplo',
            'pontuacao': 750,
            'posicao': 15,
            'simulados_realizados': 8,
            'media_acertos': 72.5,
            'melhor_desempenho': {
                'simulado': 'Simulado de Enfermagem #3',
                'acertos': 18,
                'total': 20,
                'percentual': 90.0
            }
        }
        
        return jsonify({
            'sucesso': True,
            'usuario': user_ranking,
            'timestamp': str(datetime.now())
        })
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': f'Erro ao obter ranking do usuário: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500