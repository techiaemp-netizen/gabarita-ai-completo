# Prompts para geração de questões com IA

PROMPTS_JOGOS = {
    'multipla_escolha': """
    Crie {quantidade} questões de múltipla escolha sobre {tema} para concursos públicos da área da saúde.
    Nível de dificuldade: {dificuldade}
    
    Para cada questão, forneça:
    1. Enunciado claro e objetivo
    2. 5 alternativas (A, B, C, D, E)
    3. Resposta correta
    4. Explicação detalhada da resposta
    5. Referências bibliográficas quando aplicável
    
    Formato JSON:
    {{
        "questoes": [
            {{
                "id": 1,
                "enunciado": "Texto da pergunta",
                "alternativas": {{
                    "A": "Alternativa A",
                    "B": "Alternativa B",
                    "C": "Alternativa C",
                    "D": "Alternativa D",
                    "E": "Alternativa E"
                }},
                "resposta_correta": "C",
                "explicacao": "Explicação detalhada",
                "tema": "{tema}",
                "dificuldade": "{dificuldade}",
                "referencias": "Fonte bibliográfica"
            }}
        ]
    }}
    
    Certifique-se de que as questões sejam:
    - Relevantes para concursos da área da saúde
    - Baseadas em conhecimentos atualizados
    - Com alternativas plausíveis
    - Educativas e desafiadoras
    """,
    
    'verdadeiro_falso': """
    Crie {quantidade} questões de Verdadeiro ou Falso sobre {tema} para concursos públicos da área da saúde.
    Nível de dificuldade: {dificuldade}
    
    Para cada questão, forneça:
    1. Afirmação clara e precisa
    2. Resposta (Verdadeiro ou Falso)
    3. Justificativa detalhada
    4. Referências quando aplicável
    
    Formato JSON:
    {{
        "questoes": [
            {{
                "id": 1,
                "afirmacao": "Texto da afirmação",
                "resposta_correta": "Verdadeiro",
                "justificativa": "Explicação detalhada",
                "tema": "{tema}",
                "dificuldade": "{dificuldade}",
                "referencias": "Fonte bibliográfica"
            }}
        ]
    }}
    """,
    
    'associacao': """
    Crie {quantidade} questões de associação/correspondência sobre {tema} para concursos públicos da área da saúde.
    Nível de dificuldade: {dificuldade}
    
    Para cada questão, forneça:
    1. Duas colunas para associar
    2. Instruções claras
    3. Gabarito correto
    4. Explicação das associações
    
    Formato JSON:
    {{
        "questoes": [
            {{
                "id": 1,
                "instrucao": "Associe os itens da coluna A com os da coluna B",
                "coluna_a": ["Item 1", "Item 2", "Item 3"],
                "coluna_b": ["Descrição X", "Descrição Y", "Descrição Z"],
                "gabarito": {{"Item 1": "Descrição Y", "Item 2": "Descrição Z", "Item 3": "Descrição X"}},
                "explicacao": "Explicação das associações corretas",
                "tema": "{tema}",
                "dificuldade": "{dificuldade}"
            }}
        ]
    }}
    """,
    
    'caso_clinico': """
    Crie {quantidade} questões baseadas em casos clínicos sobre {tema} para concursos públicos da área da saúde.
    Nível de dificuldade: {dificuldade}
    
    Para cada questão, forneça:
    1. Caso clínico detalhado
    2. Pergunta específica sobre o caso
    3. 5 alternativas de resposta
    4. Resposta correta
    5. Discussão do caso
    
    Formato JSON:
    {{
        "questoes": [
            {{
                "id": 1,
                "caso_clinico": "Descrição detalhada do caso",
                "pergunta": "Pergunta específica sobre o caso",
                "alternativas": {{
                    "A": "Alternativa A",
                    "B": "Alternativa B",
                    "C": "Alternativa C",
                    "D": "Alternativa D",
                    "E": "Alternativa E"
                }},
                "resposta_correta": "B",
                "discussao": "Análise detalhada do caso e justificativa da resposta",
                "tema": "{tema}",
                "dificuldade": "{dificuldade}"
            }}
        ]
    }}
    
    Os casos devem ser:
    - Realistas e baseados na prática clínica
    - Apropriados para o nível do concurso
    - Educativos e clinicamente relevantes
    """,
    
    'calculo': """
    Crie {quantidade} questões que envolvam cálculos sobre {tema} para concursos públicos da área da saúde.
    Nível de dificuldade: {dificuldade}
    
    Para cada questão, forneça:
    1. Situação que requer cálculo
    2. Dados necessários
    3. 5 alternativas com valores
    4. Resposta correta
    5. Resolução passo a passo
    
    Formato JSON:
    {{
        "questoes": [
            {{
                "id": 1,
                "situacao": "Descrição da situação",
                "dados": "Dados fornecidos para o cálculo",
                "pergunta": "O que deve ser calculado",
                "alternativas": {{
                    "A": "Valor A",
                    "B": "Valor B",
                    "C": "Valor C",
                    "D": "Valor D",
                    "E": "Valor E"
                }},
                "resposta_correta": "C",
                "resolucao": "Passo a passo da resolução",
                "tema": "{tema}",
                "dificuldade": "{dificuldade}"
            }}
        ]
    }}
    
    Os cálculos podem envolver:
    - Dosagens de medicamentos
    - Indicadores epidemiológicos
    - Conversões de unidades
    - Estatísticas de saúde
    """
}

# Prompts específicos por área da saúde
PROMPTS_AREAS = {
    'sus': """
    Foque em questões sobre:
    - Princípios e diretrizes do SUS
    - Lei 8.080/90 e Lei 8.142/90
    - Organização do sistema de saúde
    - Controle social
    - Financiamento
    - Redes de atenção à saúde
    """,
    
    'epidemiologia': """
    Foque em questões sobre:
    - Indicadores epidemiológicos
    - Vigilância em saúde
    - Investigação epidemiológica
    - Medidas de prevenção
    - Doenças transmissíveis
    - Doenças crônicas não transmissíveis
    """,
    
    'saude_publica': """
    Foque em questões sobre:
    - Políticas públicas de saúde
    - Promoção da saúde
    - Prevenção de doenças
    - Educação em saúde
    - Determinantes sociais da saúde
    - Programas de saúde
    """,
    
    'enfermagem': """
    Foque em questões sobre:
    - Processo de enfermagem
    - Técnicas e procedimentos
    - Farmacologia aplicada
    - Ética profissional
    - Segurança do paciente
    - Cuidados específicos por especialidade
    """
}

# Templates para diferentes tipos de simulados
TEMPLATES_SIMULADOS = {
    'concurso_completo': {
        'areas': ['SUS', 'Saúde Pública', 'Epidemiologia', 'Ética', 'Português', 'Matemática'],
        'distribuicao': {
            'SUS': 30,
            'Saúde Pública': 25,
            'Epidemiologia': 20,
            'Ética': 10,
            'Português': 10,
            'Matemática': 5
        },
        'tempo_limite': 180  # 3 horas
    },
    
    'area_especifica': {
        'areas': ['Área Específica'],
        'distribuicao': {
            'Área Específica': 100
        },
        'tempo_limite': 120  # 2 horas
    },
    
    'conhecimentos_basicos': {
        'areas': ['Português', 'Matemática', 'Informática', 'Atualidades'],
        'distribuicao': {
            'Português': 40,
            'Matemática': 30,
            'Informática': 20,
            'Atualidades': 10
        },
        'tempo_limite': 90  # 1.5 horas
    }
}