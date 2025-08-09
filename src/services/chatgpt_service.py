"""
Serviço de integração com ChatGPT para geração de questões
"""
import os
import openai
import json
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class ChatGPTService:
    """Serviço para integração com ChatGPT"""
    
    def __init__(self):
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1')
        )
        self.model = "gpt-4o-mini"  # Modelo otimizado para código e questões
        self.temperature = 0.7
        self.max_tokens = 1500
    
    def _get_prompt_estatico(self) -> str:
        """Retorna o prompt estático para geração de questões FGV"""
        return """Você é um elaborador de questões da banca FGV. Seu papel é criar uma única questão objetiva, com base no edital do cargo abaixo. Siga as instruções com rigor:

- Formato da questão: pode ser de múltipla escolha (com 5 alternativas, apenas uma correta), verdadeiro ou falso, completar lacuna, ou ordenação lógica.
- A questão deve ser inédita, clara, com linguagem técnica adequada.
- A alternativa correta deve ser coerente e as erradas plausíveis, mas incorretas.
- No final, inclua o gabarito e uma explicação técnica da resposta.
- NÃO invente temas fora do edital. Utilize apenas o conteúdo que está listado no edital fornecido.

Retorne a resposta no seguinte formato JSON:
{
  "questao": "texto da questão",
  "tipo": "multipla_escolha|verdadeiro_falso|completar_lacuna|ordenacao",
  "alternativas": ["A) ...", "B) ...", "C) ...", "D) ...", "E) ..."],
  "gabarito": "A",
  "explicacao": "explicação detalhada da resposta correta",
  "tema": "tema principal da questão",
  "dificuldade": "facil|medio|dificil"
}"""
    
    def _get_prompt_dinamico(self, cargo: str, conteudo_edital: str, tipo_questao: str = "múltipla escolha") -> str:
        """Gera o prompt dinâmico baseado no perfil do usuário"""
        return f"""
Cargo do aluno: {cargo}
Conteúdo do edital a ser cobrado: {conteudo_edital}
Tipo de questão desejada: {tipo_questao}
"""
    
    def gerar_questao(self, cargo: str, conteudo_edital: str, tipo_questao: str = "múltipla escolha") -> Optional[Dict[str, Any]]:
        """
        Gera uma questão personalizada usando ChatGPT
        
        Args:
            cargo: Cargo pretendido pelo usuário
            conteudo_edital: Conteúdo específico do edital
            tipo_questao: Tipo de questão desejada
            
        Returns:
            Dict com a questão gerada ou None em caso de erro
        """
        try:
            # Verificar se a API key está configurada
            if not os.getenv('OPENAI_API_KEY'):
                print("⚠️ OPENAI_API_KEY não configurada, usando fallback")
                return self._gerar_questao_fallback(cargo, conteudo_edital)
            
            # Combinar prompts estático e dinâmico
            prompt_completo = self._get_prompt_estatico() + self._get_prompt_dinamico(cargo, conteudo_edital, tipo_questao)
            
            # Fazer chamada para ChatGPT com modelo otimizado
            response = self.client.chat.completions.create(
                model=self.model,  # gpt-4o-mini é melhor para código e questões estruturadas
                messages=[
                    {"role": "system", "content": "Você é um especialista em elaboração de questões para concursos públicos da banca FGV. Use sua expertise para criar questões precisas e bem estruturadas."},
                    {"role": "user", "content": prompt_completo}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            # Extrair resposta
            resposta = response.choices[0].message.content.strip()
            
            # Tentar extrair JSON da resposta
            questao_data = self._extrair_json_resposta(resposta)
            
            if questao_data:
                # Adicionar metadados
                questao_data['cargo'] = cargo
                questao_data['conteudo_edital'] = conteudo_edital
                questao_data['modelo_usado'] = self.model
                questao_data['prompt_usado'] = prompt_completo[:200] + "..."
                
                return questao_data
            else:
                print(f"❌ Erro ao extrair JSON da resposta: {resposta[:200]}...")
                return self._gerar_questao_fallback(cargo, conteudo_edital)
                
        except Exception as e:
            print(f"❌ Erro ao gerar questão: {e}")
            return self._gerar_questao_fallback(cargo, conteudo_edital)
    
    def _gerar_questao_fallback(self, cargo: str, conteudo_edital: str) -> Dict[str, Any]:
        """Gera uma questão de fallback quando a API falha"""
        return {
            "questao": f"Questão sobre {conteudo_edital} para o cargo de {cargo}",
            "tipo": "multipla_escolha",
            "alternativas": [
                {"id": "A", "texto": "Alternativa A"},
                {"id": "B", "texto": "Alternativa B"},
                {"id": "C", "texto": "Alternativa C"},
                {"id": "D", "texto": "Alternativa D"},
                {"id": "E", "texto": "Alternativa E"}
            ],
            "gabarito": "C",
            "explicacao": "Explicação da resposta correta",
            "tema": conteudo_edital,
            "dificuldade": "medio",
            "modelo_usado": "fallback"
        }
    
    def _extrair_json_resposta(self, resposta: str) -> Optional[Dict[str, Any]]:
        """Extrai JSON da resposta do ChatGPT"""
        try:
            # Tentar encontrar JSON na resposta
            json_match = re.search(r'\{.*\}', resposta, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            
            # Se não encontrar JSON, tentar parsear a resposta inteira
            return json.loads(resposta)
            
        except json.JSONDecodeError:
            # Se falhar, tentar extrair manualmente
            return self._extrair_manual_resposta(resposta)
    
    def _extrair_manual_resposta(self, resposta: str) -> Optional[Dict[str, Any]]:
        """Extrai dados manualmente se JSON falhar"""
        try:
            # Implementar extração manual básica
            questao_data = {
                "questao": "",
                "tipo": "multipla_escolha",
                "alternativas": [],
                "gabarito": "",
                "explicacao": "",
                "tema": "",
                "dificuldade": "medio"
            }
            
            # Extrair questão (primeira linha ou parágrafo)
            linhas = resposta.split('\n')
            for linha in linhas:
                if linha.strip() and not linha.startswith(('A)', 'B)', 'C)', 'D)', 'E)')):
                    questao_data["questao"] = linha.strip()
                    break
            
            # Extrair alternativas
            alternativas = []
            for linha in linhas:
                if re.match(r'^[A-E]\)', linha.strip()):
                    alternativas.append(linha.strip())
            
            questao_data["alternativas"] = alternativas
            
            # Extrair gabarito (procurar por "Gabarito:" ou similar)
            for linha in linhas:
                if "gabarito" in linha.lower() or "resposta" in linha.lower():
                    match = re.search(r'[A-E]', linha)
                    if match:
                        questao_data["gabarito"] = match.group()
                        break
            
            # Extrair explicação
            explicacao_iniciou = False
            explicacao_linhas = []
            for linha in linhas:
                if "explicação" in linha.lower() or "justificativa" in linha.lower():
                    explicacao_iniciou = True
                    continue
                if explicacao_iniciou and linha.strip():
                    explicacao_linhas.append(linha.strip())
            
            questao_data["explicacao"] = " ".join(explicacao_linhas)
            
            return questao_data if questao_data["questao"] else None
            
        except Exception as e:
            print(f"❌ Erro na extração manual: {e}")
            return None
    
    def validar_questao(self, questao_data: Dict[str, Any]) -> bool:
        """Valida se a questão gerada está completa"""
        campos_obrigatorios = ["questao", "alternativas", "gabarito", "explicacao"]
        
        for campo in campos_obrigatorios:
            if not questao_data.get(campo):
                return False
        
        # Validar alternativas (deve ter pelo menos 2)
        if len(questao_data.get("alternativas", [])) < 2:
            return False
        
        # Validar gabarito
        gabarito = questao_data.get("gabarito", "")
        if not gabarito or gabarito not in "ABCDE":
            return False
        
        return True
    
    def gerar_explicacao(self, prompt_explicacao: str) -> Optional[str]:
        """Gera explicação detalhada usando o ChatGPT"""
        try:
            # Verificar se a API key está configurada
            if not os.getenv('OPENAI_API_KEY'):
                print("⚠️ OPENAI_API_KEY não configurada, usando explicação fallback")
                return "Explicação detalhada não disponível. Configure a API key do OpenAI para obter explicações personalizadas."
            
            print("🤖 Enviando prompt para gerar explicação...")
            
            response = self.client.chat.completions.create(
                model=self.model,  # Usando gpt-4o-mini para explicações também
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um professor especialista em concursos públicos. Forneça explicações claras, didáticas e fundamentadas em legislação quando aplicável. Use linguagem técnica mas acessível."
                    },
                    {
                        "role": "user",
                        "content": prompt_explicacao
                    }
                ],
                temperature=0.3,  # Menor temperatura para respostas mais precisas
                max_tokens=800
            )
            
            explicacao = response.choices[0].message.content.strip()
            print(f"✅ Explicação gerada com gpt-4o-mini: {explicacao[:100]}...")
            return explicacao
            
        except Exception as e:
            print(f"❌ Erro ao gerar explicação: {e}")
            return "Não foi possível gerar uma explicação detalhada no momento. Tente novamente mais tarde."

# Instância global do serviço
chatgpt_service = ChatGPTService()
