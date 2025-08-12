from flask import Blueprint, jsonify, request
import openai
import os
from dotenv import load_dotenv
from plano_service import PlanoService

load_dotenv()

planos_bp = Blueprint('planos', __name__)
plano_service = PlanoService()

# Configurar OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

@planos_bp.route('/planos', methods=['GET'])
def get_planos():
    """Retorna todos os planos disponíveis"""
    try:
        planos = plano_service.get_all_planos()
        return jsonify(planos)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@planos_bp.route('/planos/<int:plano_id>', methods=['GET'])
def get_plano(plano_id):
    """Retorna um plano específico"""
    try:
        plano = plano_service.get_plano_by_id(plano_id)
        if plano:
            return jsonify(plano)
        return jsonify({"error": "Plano não encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@planos_bp.route('/planos/gerar', methods=['POST'])
def gerar_plano_ia():
    """Gera um plano de estudos personalizado usando IA"""
    try:
        data = request.json
        cargo = data.get('cargo', '')
        tempo_disponivel = data.get('tempo_disponivel', '')
        nivel = data.get('nivel', 'iniciante')
        areas_foco = data.get('areas_foco', [])
        
        # Prompt para o ChatGPT
        prompt = f"""
        Crie um plano de estudos detalhado para concurso público na área da saúde.
        
        Informações:
        - Cargo: {cargo}
        - Tempo disponível: {tempo_disponivel}
        - Nível: {nivel}
        - Áreas de foco: {', '.join(areas_foco)}
        
        O plano deve incluir:
        1. Cronograma semanal
        2. Distribuição de matérias
        3. Metas semanais
        4. Dicas de estudo
        5. Recursos recomendados
        
        Formato: JSON com estrutura clara e organizada.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um especialista em concursos públicos da área da saúde. Crie planos de estudo personalizados e eficazes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        plano_gerado = response.choices[0].message.content
        
        # Salvar o plano gerado
        novo_plano = {
            "titulo": f"Plano para {cargo}",
            "descricao": f"Plano personalizado para {cargo} - {nivel}",
            "conteudo": plano_gerado,
            "cargo": cargo,
            "nivel": nivel,
            "tempo_disponivel": tempo_disponivel,
            "areas_foco": areas_foco
        }
        
        plano_id = plano_service.create_plano(novo_plano)
        novo_plano['id'] = plano_id
        
        return jsonify(novo_plano)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@planos_bp.route('/planos/sugestoes', methods=['POST'])
def get_sugestoes():
    """Retorna sugestões de estudo baseadas no desempenho"""
    try:
        data = request.json
        desempenho = data.get('desempenho', {})
        areas_dificuldade = data.get('areas_dificuldade', [])
        
        prompt = f"""
        Baseado no desempenho do usuário, forneça sugestões de estudo:
        
        Desempenho atual: {desempenho}
        Áreas de dificuldade: {', '.join(areas_dificuldade)}
        
        Forneça:
        1. 3 sugestões específicas de estudo
        2. Recursos recomendados
        3. Cronograma de revisão
        4. Técnicas de memorização
        
        Resposta em formato JSON.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um tutor especializado em concursos da área da saúde. Forneça sugestões personalizadas de estudo."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        sugestoes = response.choices[0].message.content
        
        return jsonify({
            "sugestoes": sugestoes,
            "timestamp": plano_service.get_current_timestamp()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500