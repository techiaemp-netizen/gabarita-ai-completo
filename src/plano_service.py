import sqlite3
import json
from datetime import datetime
import os

class PlanoService:
    def __init__(self, db_path="planos.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializa o banco de dados SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Criar tabela de planos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descricao TEXT,
                conteudo TEXT,
                cargo TEXT,
                nivel TEXT,
                tempo_disponivel TEXT,
                areas_foco TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Criar tabela de progresso
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progresso_planos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plano_id INTEGER,
                user_id TEXT,
                progresso REAL DEFAULT 0.0,
                status TEXT DEFAULT 'iniciado',
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plano_id) REFERENCES planos (id)
            )
        """)
        
        conn.commit()
        conn.close()
        
        # Inserir planos padrão se não existirem
        self.insert_default_planos()
    
    def insert_default_planos(self):
        """Insere planos padrão no banco de dados"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar se já existem planos
        cursor.execute("SELECT COUNT(*) FROM planos")
        count = cursor.fetchone()[0]
        
        if count == 0:
            planos_default = [
                {
                    "titulo": "Plano Intensivo - Técnico em Enfermagem",
                    "descricao": "Plano completo para concursos de Técnico em Enfermagem",
                    "conteudo": json.dumps({
                        "duracao": "3 meses",
                        "cronograma": {
                            "semana_1_4": "Fundamentos de Enfermagem e Anatomia",
                            "semana_5_8": "Procedimentos e Técnicas",
                            "semana_9_12": "SUS e Saúde Pública"
                        },
                        "materias": [
                            "Fundamentos de Enfermagem",
                            "Anatomia e Fisiologia",
                            "Farmacologia",
                            "SUS",
                            "Ética Profissional"
                        ],
                        "metas_semanais": [
                            "Estudar 20 horas por semana",
                            "Resolver 50 questões",
                            "Fazer 1 simulado"
                        ]
                    }),
                    "cargo": "Técnico em Enfermagem",
                    "nivel": "intermediario",
                    "tempo_disponivel": "20 horas/semana",
                    "areas_foco": json.dumps(["Enfermagem", "SUS", "Ética"])
                },
                {
                    "titulo": "Plano Básico - Agente Comunitário de Saúde",
                    "descricao": "Preparação focada para ACS",
                    "conteudo": json.dumps({
                        "duracao": "2 meses",
                        "cronograma": {
                            "semana_1_3": "SUS e Políticas de Saúde",
                            "semana_4_6": "Saúde da Família e Comunidade",
                            "semana_7_8": "Revisão e Simulados"
                        },
                        "materias": [
                            "SUS",
                            "Saúde da Família",
                            "Epidemiologia Básica",
                            "Saúde Pública",
                            "Português",
                            "Matemática"
                        ],
                        "metas_semanais": [
                            "Estudar 15 horas por semana",
                            "Resolver 30 questões",
                            "Ler 1 artigo sobre saúde pública"
                        ]
                    }),
                    "cargo": "Agente Comunitário de Saúde",
                    "nivel": "iniciante",
                    "tempo_disponivel": "15 horas/semana",
                    "areas_foco": json.dumps(["SUS", "Saúde da Família", "Epidemiologia"])
                },
                {
                    "titulo": "Plano Avançado - Enfermeiro",
                    "descricao": "Preparação completa para concursos de Enfermeiro",
                    "conteudo": json.dumps({
                        "duracao": "4 meses",
                        "cronograma": {
                            "mes_1": "Fundamentos e Processo de Enfermagem",
                            "mes_2": "Enfermagem Clínica e Cirúrgica",
                            "mes_3": "Saúde Pública e Gestão",
                            "mes_4": "Revisão e Simulados Intensivos"
                        },
                        "materias": [
                            "Processo de Enfermagem",
                            "Enfermagem Clínica",
                            "Enfermagem Cirúrgica",
                            "Saúde da Mulher",
                            "Saúde da Criança",
                            "Saúde Mental",
                            "Gestão em Enfermagem",
                            "SUS",
                            "Epidemiologia"
                        ],
                        "metas_semanais": [
                            "Estudar 25 horas por semana",
                            "Resolver 70 questões",
                            "Fazer 2 simulados",
                            "Revisar 1 protocolo clínico"
                        ]
                    }),
                    "cargo": "Enfermeiro",
                    "nivel": "avancado",
                    "tempo_disponivel": "25 horas/semana",
                    "areas_foco": json.dumps(["Enfermagem Clínica", "Gestão", "SUS"])
                }
            ]
            
            for plano in planos_default:
                cursor.execute("""
                    INSERT INTO planos (titulo, descricao, conteudo, cargo, nivel, tempo_disponivel, areas_foco)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    plano['titulo'],
                    plano['descricao'],
                    plano['conteudo'],
                    plano['cargo'],
                    plano['nivel'],
                    plano['tempo_disponivel'],
                    plano['areas_foco']
                ))
        
        conn.commit()
        conn.close()
    
    def get_all_planos(self):
        """Retorna todos os planos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, titulo, descricao, cargo, nivel, tempo_disponivel, areas_foco, created_at
            FROM planos
            ORDER BY created_at DESC
        """)
        
        planos = []
        for row in cursor.fetchall():
            plano = {
                "id": row[0],
                "titulo": row[1],
                "descricao": row[2],
                "cargo": row[3],
                "nivel": row[4],
                "tempo_disponivel": row[5],
                "areas_foco": json.loads(row[6]) if row[6] else [],
                "created_at": row[7]
            }
            planos.append(plano)
        
        conn.close()
        return planos
    
    def get_plano_by_id(self, plano_id):
        """Retorna um plano específico"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, titulo, descricao, conteudo, cargo, nivel, tempo_disponivel, areas_foco, created_at
            FROM planos
            WHERE id = ?
        """, (plano_id,))
        
        row = cursor.fetchone()
        if row:
            plano = {
                "id": row[0],
                "titulo": row[1],
                "descricao": row[2],
                "conteudo": json.loads(row[3]) if row[3] else {},
                "cargo": row[4],
                "nivel": row[5],
                "tempo_disponivel": row[6],
                "areas_foco": json.loads(row[7]) if row[7] else [],
                "created_at": row[8]
            }
            conn.close()
            return plano
        
        conn.close()
        return None
    
    def create_plano(self, plano_data):
        """Cria um novo plano"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO planos (titulo, descricao, conteudo, cargo, nivel, tempo_disponivel, areas_foco)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            plano_data.get('titulo', ''),
            plano_data.get('descricao', ''),
            json.dumps(plano_data.get('conteudo', {})),
            plano_data.get('cargo', ''),
            plano_data.get('nivel', ''),
            plano_data.get('tempo_disponivel', ''),
            json.dumps(plano_data.get('areas_foco', []))
        ))
        
        plano_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return plano_id
    
    def update_progresso(self, plano_id, user_id, progresso, status='em_andamento'):
        """Atualiza o progresso de um plano"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Verificar se já existe registro de progresso
        cursor.execute("""
            SELECT id FROM progresso_planos
            WHERE plano_id = ? AND user_id = ?
        """, (plano_id, user_id))
        
        existing = cursor.fetchone()
        
        if existing:
            # Atualizar registro existente
            cursor.execute("""
                UPDATE progresso_planos
                SET progresso = ?, status = ?, last_activity = CURRENT_TIMESTAMP
                WHERE plano_id = ? AND user_id = ?
            """, (progresso, status, plano_id, user_id))
        else:
            # Criar novo registro
            cursor.execute("""
                INSERT INTO progresso_planos (plano_id, user_id, progresso, status)
                VALUES (?, ?, ?, ?)
            """, (plano_id, user_id, progresso, status))
        
        conn.commit()
        conn.close()
    
    def get_progresso(self, plano_id, user_id):
        """Retorna o progresso de um plano para um usuário"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT progresso, status, last_activity
            FROM progresso_planos
            WHERE plano_id = ? AND user_id = ?
        """, (plano_id, user_id))
        
        row = cursor.fetchone()
        if row:
            progresso = {
                "progresso": row[0],
                "status": row[1],
                "last_activity": row[2]
            }
            conn.close()
            return progresso
        
        conn.close()
        return {"progresso": 0.0, "status": "nao_iniciado", "last_activity": None}
    
    def get_current_timestamp(self):
        """Retorna timestamp atual"""
        return datetime.now().isoformat()