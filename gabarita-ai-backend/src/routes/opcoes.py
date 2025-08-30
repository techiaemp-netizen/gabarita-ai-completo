from flask import Blueprint, jsonify
from datetime import datetime
from src.routes.questoes import CONTEUDOS_EDITAL

opcoes_bp = Blueprint('opcoes', __name__)

@opcoes_bp.route('/opcoes/cargos-blocos', methods=['GET'])
def get_cargos_blocos():
    """Endpoint para obter lista de cargos e blocos disponíveis"""
    try:
        # Extrair cargos e seus blocos do mapeamento CONTEUDOS_EDITAL
        opcoes = {}
        
        for cargo, blocos_data in CONTEUDOS_EDITAL.items():
            opcoes[cargo] = list(blocos_data.keys())
        
        # Criar lista única de blocos para facilitar a busca
        todos_blocos = set()
        for blocos in opcoes.values():
            todos_blocos.update(blocos)
        
        return jsonify({
            'success': True,
            'data': {
                'cargos_blocos': opcoes,
                'todos_cargos': list(opcoes.keys()),
                'todos_blocos': sorted(list(todos_blocos))
            }
        }), 200
        
    except Exception as e:
        print(f"Error getting options: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@opcoes_bp.route('/opcoes/diagnostico', methods=['GET'])
def diagnostico_opcoes():
    """Endpoint de diagnóstico para verificar o status das opções"""
    try:
        # Verificar se CONTEUDOS_EDITAL está carregado
        if not CONTEUDOS_EDITAL:
            return jsonify({
                'success': False,
                'error': 'CONTEUDOS_EDITAL not loaded',
                'diagnostico': {
                    'conteudos_carregados': False,
                    'total_cargos': 0,
                    'total_blocos': 0
                }
            }), 500
        
        # Contar cargos e blocos
        total_cargos = len(CONTEUDOS_EDITAL)
        todos_blocos = set()
        
        for cargo, blocos_data in CONTEUDOS_EDITAL.items():
            if isinstance(blocos_data, dict):
                todos_blocos.update(blocos_data.keys())
        
        total_blocos = len(todos_blocos)
        
        # Testar endpoints principais
        try:
            # Simular chamada para blocos-cargos
            blocos_cargos = {}
            for cargo, blocos_data in CONTEUDOS_EDITAL.items():
                if isinstance(blocos_data, dict):
                    for bloco in blocos_data.keys():
                        if bloco not in blocos_cargos:
                            blocos_cargos[bloco] = []
                        blocos_cargos[bloco].append(cargo)
            
            endpoint_blocos_cargos_ok = True
        except Exception as e:
            endpoint_blocos_cargos_ok = False
        
        return jsonify({
            'success': True,
            'diagnostico': {
                'conteudos_carregados': True,
                'total_cargos': total_cargos,
                'total_blocos': total_blocos,
                'endpoint_blocos_cargos_ok': endpoint_blocos_cargos_ok,
                'primeiros_cargos': list(CONTEUDOS_EDITAL.keys())[:5],
                'primeiros_blocos': sorted(list(todos_blocos))[:5],
                'timestamp': str(datetime.now())
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Diagnostic error: {str(e)}',
            'diagnostico': {
                'conteudos_carregados': False,
                'erro_detalhado': str(e)
            }
        }), 500

@opcoes_bp.route('/opcoes/blocos-cargos', methods=['GET'])
def get_blocos_cargos():
    """Endpoint para obter lista de blocos e cargos disponíveis (formato esperado pelo frontend)"""
    try:
        # Extrair cargos e seus blocos do mapeamento CONTEUDOS_EDITAL
        blocos_cargos = {}
        
        # Inverter a estrutura: bloco -> [cargos]
        for cargo, blocos_data in CONTEUDOS_EDITAL.items():
            # Verificar se blocos_data é um dicionário ou lista
            if isinstance(blocos_data, dict):
                # Estrutura nova: cargo -> {bloco: {conhecimentos_especificos: [...]}}
                for bloco in blocos_data.keys():
                    if bloco not in blocos_cargos:
                        blocos_cargos[bloco] = []
                    blocos_cargos[bloco].append(cargo)
            else:
                # Estrutura antiga: cargo -> [conhecimentos] - assumir bloco padrão
                print(f"Aviso: Cargo {cargo} tem estrutura antiga (lista), ignorando...")
                continue
        
        # Criar listas únicas
        todos_blocos = list(blocos_cargos.keys())
        todos_cargos = list(CONTEUDOS_EDITAL.keys())
        
        print(f"Debug: Encontrados {len(todos_blocos)} blocos e {len(todos_cargos)} cargos")
        print(f"Debug: Blocos: {todos_blocos[:3]}...")  # Primeiros 3 blocos
        print(f"Debug: Cargos: {todos_cargos[:3]}...")   # Primeiros 3 cargos
        
        return jsonify({
            'success': True,
            'data': {
                'cargos_blocos': blocos_cargos,  # Frontend espera cargos_blocos
                'blocos_cargos': blocos_cargos,  # Manter compatibilidade
                'todos_blocos': sorted(todos_blocos),
                'todos_cargos': sorted(todos_cargos)
            }
        }), 200
        
    except Exception as e:
        print(f"Error getting blocks-positions options: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@opcoes_bp.route('/opcoes/cargos/<bloco>', methods=['GET'])
def get_cargos_por_bloco(bloco):
    """Endpoint para obter cargos disponíveis para um bloco específico"""
    try:
        cargos = []
        for cargo, blocos_data in CONTEUDOS_EDITAL.items():
            if bloco in blocos_data:
                cargos.append(cargo)
        
        if not cargos:
            return jsonify({
                'success': False,
                'error': 'Block not found'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'bloco': bloco,
                'cargos': cargos
            }
        }), 200
        
    except Exception as e:
        print(f"Error getting positions for block {bloco}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@opcoes_bp.route('/opcoes/blocos/<cargo>', methods=['GET'])
def get_blocos_por_cargo(cargo):
    """Endpoint para obter blocos disponíveis para um cargo específico"""
    try:
        blocos = list(CONTEUDOS_EDITAL.get(cargo, {}).keys())
        
        if not blocos:
            return jsonify({
                'success': False,
                'error': 'Position not found'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'cargo': cargo,
                'blocos': blocos
            }
        }), 200
        
    except Exception as e:
        print(f"Error getting blocks for position {cargo}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500