from flask import Flask, render_template, request, redirect, url_for
import random
import string
import sqlite3
from datetime import datetime

# ====================================================================
# CONFIGURAÇÃO INICIAL
# ====================================================================

# Nome do arquivo de banco de dados SQLite
DATABASE = 'senhas_geradas.db'

# Inicializa o aplicativo Flask
app = Flask(__name__)

# -----------------------------------------------------------
# FUNÇÕES DE BANCO DE DADOS (SQLite)
# -----------------------------------------------------------

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DATABASE)
    # Permite acessar colunas por nome (ex: senha['servico'])
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    """Inicializa o banco de dados e cria a tabela 'senhas' se não existir."""
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS senhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            senha TEXT NOT NULL,
            forca TEXT NOT NULL,
            data_criacao TEXT NOT NULL,
            servico TEXT
        );
        """
    )
    conn.commit()
    conn.close()

# -----------------------------------------------------------
# FUNÇÕES DE LÓGICA DO NEGÓCIO
# -----------------------------------------------------------

def gerar_senha(tamanho, usar_maiusculas, usar_numeros, usar_simbolos):
    """Gera uma senha aleatória baseada nos parâmetros do usuário."""
    caracteres_base = string.ascii_lowercase
    
    if usar_maiusculas:
        caracteres_base += string.ascii_uppercase
    if usar_numeros:
        caracteres_base += string.digits
    if usar_simbolos:
        # Removendo aspas para evitar problemas de sintaxe em strings de banco de dados/JS
        caracteres_base += string.punctuation.replace('"', '').replace("'", '')
        
    if not caracteres_base:
        return "Erro: Nenhuma opção de caractere selecionada!"

    senha_gerada = ''.join(random.choice(caracteres_base) for _ in range(tamanho))
    
    return senha_gerada

def analisar_forca(senha):
    """Analisa a força da senha para fornecer feedback visual (cores)."""
    score = 0
    # Lógica de pontuação baseada em comprimento e diversidade
    if len(senha) >= 8: score += 2
    if len(senha) >= 12: score += 3
    if any(c.islower() for c in senha): score += 1
    if any(c.isupper() for c in senha): score += 2
    if any(c.isdigit() for c in senha): score += 2
    if any(c in string.punctuation for c in senha): score += 3
        
    if score >= 10:
        return "Muito Forte"
    elif score >= 7:
        return "Forte"
    elif score >= 4:
        return "Média"
    else:
        return "Fraca"

# -----------------------------------------------------------
# ROTAS FLASK (Endpoints)
# -----------------------------------------------------------

# Rota principal: Gerador de Senhas
@app.route('/', methods=['GET', 'POST'])
def index():
    # Definição de estados iniciais
    senha_final = None
    forca_senha = None
    estado_maiusculas = True
    estado_numeros = True
    estado_simbolos = True
    tamanho_desejado = 12
    servico_nome = '' 
    # NOVO: Estado inicial do checkbox de salvar senha
    estado_salvar = True 
    
    if request.method == 'POST':
        # 1. Coleta de dados do formulário
        try:
            tamanho_desejado = int(request.form.get('tamanho', 12))
        except ValueError:
            tamanho_desejado = 12 
            
        servico_nome = request.form.get('servico', 'Não Informado')
            
        maiusculas_selecionada = 'maiusculas' in request.form
        numeros_selecionada = 'numeros' in request.form
        simbolos_selecionada = 'simbolos' in request.form
        # NOVO: Coleta se o usuário quer salvar a senha
        salvar_selecionado = 'salvar_senha' in request.form 
        
        # 2. Persistência de estado para reexibir no formulário
        estado_maiusculas = maiusculas_selecionada
        estado_numeros = numeros_selecionada
        estado_simbolos = simbolos_selecionada
        estado_salvar = salvar_selecionado # Persiste o estado do novo checkbox
        
        # 3. Geração e Análise
        senha_final = gerar_senha(
            tamanho_desejado, 
            maiusculas_selecionada, 
            numeros_selecionada, 
            simbolos_selecionada
        )
        forca_senha = analisar_forca(senha_final)
        
        # 4. Salvamento Condicional no Banco de Dados
        if salvar_selecionado:
            conn = get_db_connection()
            conn.execute(
                "INSERT INTO senhas (senha, forca, data_criacao, servico) VALUES (?, ?, ?, ?)",
                (senha_final, forca_senha, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), servico_nome)
            )
            conn.commit()
            conn.close()
        
    # Renderiza o template, passando todas as variáveis de estado
    return render_template('index.html', 
                           senha=senha_final, 
                           forca=forca_senha,
                           maiusculas_checked=estado_maiusculas,
                           numeros_checked=estado_numeros,
                           simbolos_checked=estado_simbolos,
                           tamanho_atual=tamanho_desejado,
                           servico_nome=servico_nome,
                           salvar_checked=estado_salvar) # NOVO: Passa o estado de salvar

# Rota de Histórico: Lista todas as senhas salvas, com filtro opcional
@app.route('/historico', methods=['GET'])
def historico():
    # 1. Coleta o termo de pesquisa (se existir na URL, ex: /historico?search=Google)
    termo_pesquisa = request.args.get('search')
    
    conn = get_db_connection()
    
    if termo_pesquisa:
        # Se houver termo, executa a consulta com a cláusula WHERE
        # O operador LIKE e os curingas (%) permitem buscar por parte do nome.
        # Utilizamos o placeholder (?) para segurança contra SQL Injection.
        consulta_sql = "SELECT * FROM senhas WHERE servico LIKE ? ORDER BY id DESC"
        parametro = ('%' + termo_pesquisa + '%',)
        senhas = conn.execute(consulta_sql, parametro).fetchall()
    else:
        # Se não houver termo, executa a consulta normal
        senhas = conn.execute('SELECT * FROM senhas ORDER BY id DESC').fetchall()
    
    conn.close()
    
    # Passamos o termo de pesquisa de volta para o HTML, para manter o campo preenchido
    return render_template('historico.html', senhas=senhas, termo_pesquisa=termo_pesquisa)

# Rota de Exclusão: Deleta um registro específico
@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):
    """Deleta um registro do banco de dados com base no ID (operação DELETE no CRUD)."""
    conn = get_db_connection()
    conn.execute('DELETE FROM senhas WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    # Redireciona de volta para a lista de histórico
    return redirect(url_for('historico'))


if __name__ == '__main__':
    # Inicializa o DB antes de rodar o app para garantir que a tabela exista
    with app.app_context():
        init_db()
        
    # Roda o servidor Flask em modo de desenvolvimento
    app.run(debug=True)