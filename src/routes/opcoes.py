from flask import Blueprint, jsonify
from routes.questoes import CONTEUDOS_EDITAL

opcoes_bp = Blueprint('opcoes', __name__)

@opcoes_bp.route('/blocos-cargos', methods=['GET'])
def get_blocos_cargos():
    """
    Retorna todos os blocos e cargos disponíveis no sistema
    """
    try:
        # Extrair todos os blocos únicos
        todos_blocos = set()
        todos_cargos = list(CONTEUDOS_EDITAL.keys())
        
        # Iterar sobre todos os cargos para extrair blocos
        for cargo, blocos_dict in CONTEUDOS_EDITAL.items():
            if isinstance(blocos_dict, dict):
                for bloco in blocos_dict.keys():
                    todos_blocos.add(bloco)
        
        # Converter set para lista ordenada
        todos_blocos = sorted(list(todos_blocos))
        todos_cargos = sorted(todos_cargos)
        
        return jsonify({
            'success': True,
            'data': {
                'todos_blocos': todos_blocos,
                'todos_cargos': todos_cargos,
                'total_blocos': len(todos_blocos),
                'total_cargos': len(todos_cargos)
            },
            'timestamp': '2024-01-01T00:00:00Z'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao carregar blocos e cargos: {str(e)}',
            'timestamp': '2024-01-01T00:00:00Z'
        }), 500

@opcoes_bp.route('/cargos/<path:bloco>', methods=['GET'])
def get_cargos_por_bloco(bloco):
    """
    Retorna os cargos disponíveis para um bloco específico
    """
    try:
        # Decodificar o nome do bloco (URL decode)
        import urllib.parse
        bloco_decodificado = urllib.parse.unquote(bloco)
        
        cargos_disponiveis = []
        
        # Iterar sobre todos os cargos para encontrar quais têm o bloco especificado
        for cargo, blocos_dict in CONTEUDOS_EDITAL.items():
            if isinstance(blocos_dict, dict):
                if bloco_decodificado in blocos_dict:
                    cargos_disponiveis.append(cargo)
        
        if not cargos_disponiveis:
            return jsonify({
                'success': False,
                'error': f'Nenhum cargo encontrado para o bloco "{bloco_decodificado}"',
                'timestamp': '2024-01-01T00:00:00Z'
            }), 404
        
        # Ordenar cargos alfabeticamente
        cargos_disponiveis = sorted(cargos_disponiveis)
        
        return jsonify({
            'success': True,
            'data': {
                'bloco': bloco_decodificado,
                'cargos': cargos_disponiveis,
                'total_cargos': len(cargos_disponiveis)
            },
            'timestamp': '2024-01-01T00:00:00Z'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao carregar cargos para o bloco {bloco}: {str(e)}',
            'timestamp': '2024-01-01T00:00:00Z'
        }), 500

@opcoes_bp.route('/blocos-por-cargo/<cargo>', methods=['GET'])
def get_blocos_por_cargo(cargo):
    """
    Retorna os blocos disponíveis para um cargo específico
    """
    try:
        if cargo not in CONTEUDOS_EDITAL:
            return jsonify({
                'success': False,
                'error': f'Cargo "{cargo}" não encontrado',
                'timestamp': '2024-01-01T00:00:00Z'
            }), 404
        
        blocos_cargo = CONTEUDOS_EDITAL[cargo]
        
        if isinstance(blocos_cargo, dict):
            blocos_disponiveis = list(blocos_cargo.keys())
        else:
            # Se for uma lista, significa que há apenas um bloco padrão
            blocos_disponiveis = ['Bloco Único']
        
        return jsonify({
            'success': True,
            'data': {
                'cargo': cargo,
                'blocos': blocos_disponiveis,
                'total_blocos': len(blocos_disponiveis)
            },
            'timestamp': '2024-01-01T00:00:00Z'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro ao carregar blocos para o cargo {cargo}: {str(e)}',
            'timestamp': '2024-01-01T00:00:00Z'
        }), 500