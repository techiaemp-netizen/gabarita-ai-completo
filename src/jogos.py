from flask import Blueprint, jsonify, request
import random
import openai
import os
from dotenv import load_dotenv
from prompts_jogos import PROMPTS_JOGOS

load_dotenv()

jogos_bp = Blueprint('jogos', __name__)

# Configurar OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# Sistema de gamificação
class GamificationSystem:
    def __init__(self):
        self.levels = {
            1: {"xp_required": 0, "title": "Iniciante"},
            2: {"xp_required": 100, "title": "Estudante"},
            3: {"xp_required": 300, "title": "Dedicado"},
            4: {"xp_required": 600, "title": "Focado"},
            5: {"xp_required": 1000, "title": "Expert"},
            6: {"xp_required": 1500, "title": "Mestre"},
            7: {"xp_required": 2100, "title": "Campeão"},
            8: {"xp_required": 2800, "title": "Lenda"}
        }
    
    def calculate_level(self, xp):
        level = 1
        for lvl, data in self.levels.items():
            if xp >= data["xp_required"]:
                level = lvl
        return level
    
    def get_xp_for_next_level(self, current_xp):
        current_level = self.calculate_level(current_xp)
        if current_level < max(self.levels.keys()):
            next_level = current_level + 1
            return self.levels[next_level]["xp_required"] - current_xp
        return 0
    
    def calculate_rewards(self, correct_answers, total_questions, time_bonus=0):
        base_xp = correct_answers * 10
        accuracy_bonus = (correct_answers / total_questions) * 20 if total_questions > 0 else 0
        total_xp = int(base_xp + accuracy_bonus + time_bonus)
        
        # Energia baseada no desempenho
        accuracy = correct_answers / total_questions if total_questions > 0 else 0
        if accuracy >= 0.8:
            energy_change = 5
        elif accuracy >= 0.6:
            energy_change = 2
        elif accuracy >= 0.4:
            energy_change = 0
        else:
            energy_change = -3
        
        return {
            "xp_gained": total_xp,
            "energy_change": energy_change,
            "accuracy": accuracy * 100
        }

gamification = GamificationSystem()

@jogos_bp.route('/jogos/status', methods=['GET'])
def get_game_status():
    """Retorna o status atual do jogador"""
    # Em uma implementação real, isso viria do banco de dados do usuário
    default_status = {
        "xp": 0,
        "level": 1,
        "energy": 100,
        "life": 100,
        "coins": 0,
        "streak": 0,
        "achievements": [],
        "power_ups": []
    }
    return jsonify(default_status)

@jogos_bp.route('/jogos/questoes/gerar', methods=['POST'])
def gerar_questoes():
    """Gera questões usando IA"""
    try:
        data = request.json
        tema = data.get('tema', 'Saúde Pública')
        dificuldade = data.get('dificuldade', 'medio')
        quantidade = data.get('quantidade', 5)
        tipo = data.get('tipo', 'multipla_escolha')
        
        # Selecionar prompt baseado no tipo
        prompt_template = PROMPTS_JOGOS.get(tipo, PROMPTS_JOGOS['multipla_escolha'])
        
        prompt = prompt_template.format(
            tema=tema,
            dificuldade=dificuldade,
            quantidade=quantidade
        )
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em concursos públicos da área da saúde. Crie questões educativas e desafiadoras."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2500,
            temperature=0.7
        )
        
        questoes_texto = response.choices[0].message.content
        
        return jsonify({
            "questoes": questoes_texto,
            "tema": tema,
            "dificuldade": dificuldade,
            "tipo": tipo,
            "quantidade": quantidade
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jogos_bp.route('/jogos/simulado', methods=['POST'])
def criar_simulado():
    """Cria um simulado personalizado"""
    try:
        data = request.json
        configuracao = {
            "cargo": data.get('cargo', 'Técnico em Saúde'),
            "tempo_limite": data.get('tempo_limite', 60),  # minutos
            "num_questoes": data.get('num_questoes', 20),
            "areas": data.get('areas', ['Saúde Pública', 'SUS', 'Epidemiologia']),
            "dificuldade": data.get('dificuldade', 'medio')
        }
        
        # Gerar questões para o simulado
        questoes_simulado = []
        for area in configuracao['areas']:
            questoes_por_area = configuracao['num_questoes'] // len(configuracao['areas'])
            
            prompt = f"""
            Crie {questoes_por_area} questões de múltipla escolha sobre {area} para concurso de {configuracao['cargo']}.
            Nível de dificuldade: {configuracao['dificuldade']}
            
            Formato para cada questão:
            {{"pergunta": "texto da pergunta", "alternativas": ["a", "b", "c", "d", "e"], "resposta_correta": "letra", "explicacao": "explicação detalhada"}}
            
            Retorne um array JSON com as questões.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um especialista em concursos públicos da área da saúde."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            questoes_area = response.choices[0].message.content
            questoes_simulado.append({
                "area": area,
                "questoes": questoes_area
            })
        
        simulado_id = random.randint(1000, 9999)
        
        return jsonify({
            "simulado_id": simulado_id,
            "configuracao": configuracao,
            "questoes": questoes_simulado,
            "status": "criado"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jogos_bp.route('/jogos/resultado', methods=['POST'])
def processar_resultado():
    """Processa o resultado de um jogo/simulado"""
    try:
        data = request.json
        respostas = data.get('respostas', [])
        tempo_gasto = data.get('tempo_gasto', 0)  # em segundos
        tipo_atividade = data.get('tipo', 'questoes')
        
        # Calcular estatísticas
        total_questoes = len(respostas)
        acertos = sum(1 for r in respostas if r.get('correta', False))
        erros = total_questoes - acertos
        
        # Calcular bônus de tempo (se terminou rápido)
        tempo_bonus = max(0, (3600 - tempo_gasto) // 60) if tempo_gasto < 3600 else 0
        
        # Calcular recompensas
        rewards = gamification.calculate_rewards(acertos, total_questoes, tempo_bonus)
        
        # Análise de desempenho por área
        areas_desempenho = {}
        for resposta in respostas:
            area = resposta.get('area', 'Geral')
            if area not in areas_desempenho:
                areas_desempenho[area] = {'acertos': 0, 'total': 0}
            
            areas_desempenho[area]['total'] += 1
            if resposta.get('correta', False):
                areas_desempenho[area]['acertos'] += 1
        
        # Calcular percentual por área
        for area in areas_desempenho:
            total = areas_desempenho[area]['total']
            acertos_area = areas_desempenho[area]['acertos']
            areas_desempenho[area]['percentual'] = (acertos_area / total * 100) if total > 0 else 0
        
        resultado = {
            "estatisticas": {
                "total_questoes": total_questoes,
                "acertos": acertos,
                "erros": erros,
                "percentual_acerto": (acertos / total_questoes * 100) if total_questoes > 0 else 0,
                "tempo_gasto": tempo_gasto,
                "tempo_medio_por_questao": tempo_gasto / total_questoes if total_questoes > 0 else 0
            },
            "recompensas": rewards,
            "areas_desempenho": areas_desempenho,
            "nivel_atual": gamification.calculate_level(rewards['xp_gained']),
            "xp_proximo_nivel": gamification.get_xp_for_next_level(rewards['xp_gained'])
        }
        
        return jsonify(resultado)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jogos_bp.route('/jogos/ranking', methods=['GET'])
def get_ranking():
    """Retorna o ranking de jogadores"""
    # Em uma implementação real, isso viria do banco de dados
    ranking_mock = [
        {"posicao": 1, "nome": "Ana Silva", "xp": 2500, "level": 7, "cargo": "Enfermeiro"},
        {"posicao": 2, "nome": "João Santos", "xp": 2200, "level": 6, "cargo": "Técnico em Saúde"},
        {"posicao": 3, "nome": "Maria Costa", "xp": 1800, "level": 6, "cargo": "Fisioterapeuta"},
        {"posicao": 4, "nome": "Pedro Lima", "xp": 1500, "level": 5, "cargo": "Nutricionista"},
        {"posicao": 5, "nome": "Carla Oliveira", "xp": 1200, "level": 5, "cargo": "Psicólogo"}
    ]
    
    return jsonify({
        "ranking": ranking_mock,
        "total_jogadores": len(ranking_mock)
    })

@jogos_bp.route('/jogos/conquistas', methods=['GET'])
def get_conquistas():
    """Retorna as conquistas disponíveis"""
    conquistas = [
        {
            "id": 1,
            "nome": "Primeiro Passo",
            "descricao": "Complete seu primeiro simulado",
            "icone": "🎯",
            "xp_reward": 50,
            "desbloqueada": False
        },
        {
            "id": 2,
            "nome": "Sequência de Ouro",
            "descricao": "Acerte 10 questões seguidas",
            "icone": "🏆",
            "xp_reward": 100,
            "desbloqueada": False
        },
        {
            "id": 3,
            "nome": "Maratonista",
            "descricao": "Estude por 7 dias consecutivos",
            "icone": "🏃‍♂️",
            "xp_reward": 200,
            "desbloqueada": False
        },
        {
            "id": 4,
            "nome": "Expert em SUS",
            "descricao": "Acerte 90% das questões sobre SUS",
            "icone": "🏥",
            "xp_reward": 150,
            "desbloqueada": False
        }
    ]
    
    return jsonify({"conquistas": conquistas})