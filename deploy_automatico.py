#!/usr/bin/env python3
"""
Script de Deploy Automático - Gabarita-AI
Coloque sua plataforma no ar em minutos!
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_header():
    """Imprime o cabeçalho do script"""
    print("\n" + "=" * 60)
    print("🚀 DEPLOY AUTOMÁTICO - GABARITA-AI")
    print("💰 Coloque sua plataforma no ar e comece a faturar!")
    print("=" * 60)

def check_prerequisites():
    """Verifica se os pré-requisitos estão atendidos"""
    print("\n🔍 VERIFICANDO PRÉ-REQUISITOS")
    print("-" * 30)
    
    issues = []
    
    # Verificar se o .env existe
    if not Path('.env').exists():
        issues.append("❌ Arquivo .env não encontrado")
        print("❌ Arquivo .env não encontrado")
        print("   💡 Execute: python configurar_credenciais.py")
    else:
        print("✅ Arquivo .env encontrado")
    
    # Verificar se requirements.txt existe
    if not Path('requirements.txt').exists():
        issues.append("❌ Arquivo requirements.txt não encontrado")
        print("❌ Arquivo requirements.txt não encontrado")
    else:
        print("✅ Arquivo requirements.txt encontrado")
    
    # Verificar se o código principal existe
    if not Path('src/main.py').exists():
        issues.append("❌ Arquivo src/main.py não encontrado")
        print("❌ Arquivo src/main.py não encontrado")
    else:
        print("✅ Código principal encontrado")
    
    # Verificar Git
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        print("✅ Git instalado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        issues.append("❌ Git não instalado")
        print("❌ Git não instalado")
        print("   💡 Instale o Git: https://git-scm.com/")
    
    return len(issues) == 0, issues

def setup_git_repo():
    """Configura o repositório Git"""
    print("\n📦 CONFIGURANDO REPOSITÓRIO GIT")
    print("-" * 30)
    
    try:
        # Verificar se já é um repositório Git
        result = subprocess.run(['git', 'status'], capture_output=True)
        if result.returncode != 0:
            # Inicializar repositório
            subprocess.run(['git', 'init'], check=True)
            print("✅ Repositório Git inicializado")
        else:
            print("✅ Repositório Git já existe")
        
        # Criar .gitignore se não existir
        gitignore_path = Path('.gitignore')
        if not gitignore_path.exists():
            gitignore_content = """# Arquivos de ambiente
.env
.env.local
.env.production

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3

# OS
.DS_Store
Thumbs.db

# Firebase
firebase-debug.log
.firebase/

# Temporary files
*.tmp
*.temp
"""
            with open(gitignore_path, 'w', encoding='utf-8') as f:
                f.write(gitignore_content)
            print("✅ Arquivo .gitignore criado")
        
        # Adicionar arquivos
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit inicial
        try:
            subprocess.run(['git', 'commit', '-m', 'Deploy inicial - Gabarita-AI'], check=True)
            print("✅ Commit inicial criado")
        except subprocess.CalledProcessError:
            print("ℹ️ Nenhuma alteração para commit")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao configurar Git: {e}")
        return False

def deploy_to_render():
    """Deploy para Render.com"""
    print("\n🌐 DEPLOY PARA RENDER.COM")
    print("-" * 30)
    
    print("\n📋 INSTRUÇÕES PARA RENDER:")
    print("1. Acesse: https://render.com/")
    print("2. Crie uma conta gratuita")
    print("3. Clique em 'New +' > 'Web Service'")
    print("4. Conecte seu repositório GitHub")
    print("5. Configure as seguintes opções:")
    print("   - Name: gabarita-ai")
    print("   - Environment: Python 3")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: python src/main.py")
    
    print("\n🔧 VARIÁVEIS DE AMBIENTE:")
    print("Adicione estas variáveis na seção 'Environment Variables':")
    
    # Ler variáveis do .env
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Não mostrar valores sensíveis
                    if 'KEY' in key or 'TOKEN' in key or 'SECRET' in key:
                        print(f"   {key} = [SEU_VALOR_AQUI]")
                    else:
                        print(f"   {key} = {value}")
    
    print("\n💡 DICAS:")
    print("- Use o plano gratuito para começar")
    print("- O deploy demora ~5-10 minutos")
    print("- Sua URL será: https://gabarita-ai.onrender.com")
    
    return input("\n✅ Deploy configurado no Render? (s/N): ").strip().lower() in ['s', 'sim', 'y', 'yes']

def deploy_to_vercel():
    """Deploy para Vercel"""
    print("\n⚡ DEPLOY PARA VERCEL")
    print("-" * 30)
    
    print("\n📋 INSTRUÇÕES PARA VERCEL:")
    print("1. Acesse: https://vercel.com/")
    print("2. Crie uma conta gratuita")
    print("3. Clique em 'New Project'")
    print("4. Importe seu repositório GitHub")
    print("5. Configure:")
    print("   - Framework Preset: Other")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Output Directory: .")
    print("   - Install Command: pip install -r requirements.txt")
    
    # Criar vercel.json
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "src/main.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "src/main.py"
            }
        ]
    }
    
    with open('vercel.json', 'w', encoding='utf-8') as f:
        json.dump(vercel_config, f, indent=2)
    
    print("\n✅ Arquivo vercel.json criado")
    
    print("\n🔧 VARIÁVEIS DE AMBIENTE:")
    print("Adicione na seção 'Environment Variables' do Vercel")
    
    return input("\n✅ Deploy configurado no Vercel? (s/N): ").strip().lower() in ['s', 'sim', 'y', 'yes']

def deploy_to_railway():
    """Deploy para Railway"""
    print("\n🚂 DEPLOY PARA RAILWAY")
    print("-" * 30)
    
    print("\n📋 INSTRUÇÕES PARA RAILWAY:")
    print("1. Acesse: https://railway.app/")
    print("2. Crie uma conta gratuita")
    print("3. Clique em 'New Project'")
    print("4. Selecione 'Deploy from GitHub repo'")
    print("5. Escolha seu repositório")
    print("6. Railway detectará automaticamente que é Python")
    
    # Criar Procfile
    with open('Procfile', 'w', encoding='utf-8') as f:
        f.write('web: python src/main.py\n')
    
    print("\n✅ Arquivo Procfile criado")
    
    print("\n💡 VANTAGENS DO RAILWAY:")
    print("- Deploy automático muito rápido")
    print("- $5 de crédito gratuito por mês")
    print("- Ideal para começar")
    
    return input("\n✅ Deploy configurado no Railway? (s/N): ").strip().lower() in ['s', 'sim', 'y', 'yes']

def create_github_repo():
    """Instruções para criar repositório GitHub"""
    print("\n🐙 CRIANDO REPOSITÓRIO GITHUB")
    print("-" * 30)
    
    print("\n📋 INSTRUÇÕES:")
    print("1. Acesse: https://github.com/new")
    print("2. Nome do repositório: gabarita-ai")
    print("3. Descrição: Plataforma de estudos com IA - Gabarita-AI")
    print("4. Deixe como Público (para deploy gratuito)")
    print("5. NÃO marque 'Initialize with README'")
    print("6. Clique em 'Create repository'")
    
    repo_url = input("\n🔗 URL do repositório criado (ex: https://github.com/usuario/gabarita-ai): ").strip()
    
    if repo_url:
        try:
            # Adicionar remote origin
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
            print("✅ Remote origin adicionado")
            
            # Push para GitHub
            subprocess.run(['git', 'branch', '-M', 'main'], check=True)
            subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
            print("✅ Código enviado para GitHub")
            
            return True, repo_url
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao enviar para GitHub: {e}")
            print("💡 Tente fazer o push manualmente")
            return False, repo_url
    
    return False, None

def main():
    """Função principal"""
    print_header()
    
    print("\n🎯 Este script vai ajudar você a:")
    print("   📦 Preparar o código para deploy")
    print("   🐙 Criar repositório no GitHub")
    print("   🌐 Fazer deploy em plataformas gratuitas")
    print("   💰 Colocar sua plataforma no ar para faturar!")
    
    input("\n👆 Pressione Enter para continuar...")
    
    # Verificar pré-requisitos
    prereqs_ok, issues = check_prerequisites()
    if not prereqs_ok:
        print("\n❌ Pré-requisitos não atendidos:")
        for issue in issues:
            print(f"   {issue}")
        print("\n💡 Resolva os problemas acima e execute novamente")
        return
    
    # Configurar Git
    if not setup_git_repo():
        print("\n❌ Erro ao configurar repositório Git")
        return
    
    # Criar repositório GitHub
    print("\n🐙 VAMOS CRIAR O REPOSITÓRIO GITHUB")
    create_github = input("Criar repositório no GitHub? (S/n): ").strip().lower()
    
    github_created = False
    repo_url = None
    
    if create_github not in ['n', 'no', 'não']:
        github_created, repo_url = create_github_repo()
    
    if not github_created:
        print("\n⚠️ Sem repositório GitHub, você precisará criar manualmente")
        print("💡 Acesse: https://github.com/new")
    
    # Escolher plataforma de deploy
    print("\n🚀 ESCOLHA A PLATAFORMA DE DEPLOY")
    print("-" * 40)
    print("1. 🌐 Render.com (Recomendado - Gratuito)")
    print("2. ⚡ Vercel (Rápido - Gratuito)")
    print("3. 🚂 Railway (Fácil - $5 grátis)")
    print("4. 📚 Ver todas as opções")
    
    choice = input("\nEscolha uma opção (1-4): ").strip()
    
    deployed = False
    
    if choice == '1':
        deployed = deploy_to_render()
    elif choice == '2':
        deployed = deploy_to_vercel()
    elif choice == '3':
        deployed = deploy_to_railway()
    elif choice == '4':
        print("\n📚 TODAS AS OPÇÕES DE DEPLOY:")
        deploy_to_render()
        deploy_to_vercel()
        deploy_to_railway()
    
    # Resumo final
    print("\n" + "=" * 60)
    print("🎉 DEPLOY PREPARADO!")
    print("=" * 60)
    
    if github_created:
        print(f"\n✅ Repositório GitHub: {repo_url}")
    
    if deployed:
        print("\n✅ Deploy configurado com sucesso!")
        print("\n⏰ PRÓXIMOS PASSOS:")
        print("   1. Aguarde o deploy finalizar (~5-10 min)")
        print("   2. Teste sua plataforma online")
        print("   3. Configure domínio personalizado (opcional)")
        print("   4. DIVULGUE E COMECE A VENDER! 💰")
    else:
        print("\n⚠️ Deploy não configurado")
        print("\n💡 OPÇÕES MANUAIS:")
        print("   - Render: https://render.com/")
        print("   - Vercel: https://vercel.com/")
        print("   - Railway: https://railway.app/")
        print("   - Heroku: https://heroku.com/")
    
    print("\n💰 ESTRATÉGIAS DE MONETIZAÇÃO:")
    print("   📊 Freemium: 5 questões grátis, depois pago")
    print("   💎 Premium: R$ 29,90/mês - acesso completo")
    print("   🎓 Mentoria: R$ 99,90/mês - acompanhamento")
    print("   🏆 Intensivo: R$ 199,90/mês - preparação completa")
    
    print("\n📈 MARKETING:")
    print("   📱 Redes sociais (Instagram, TikTok, YouTube)")
    print("   📧 Email marketing")
    print("   🤝 Parcerias com influencers")
    print("   🎯 Google Ads / Facebook Ads")
    
    print("\n🎯 BOA SORTE E MUITO SUCESSO!")
    print("💰 Que os lucros estejam com você! 🚀")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Deploy cancelado pelo usuário")
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        print("\n💡 Tente executar novamente ou faça o deploy manualmente")