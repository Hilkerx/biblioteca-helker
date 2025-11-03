import sqlite3
import os
import datetime
from flask import (
    Flask, request, session, g, redirect, url_for, 
    flash, get_flashed_messages
)
from werkzeug.security import generate_password_hash, check_password_hash

# --- 1. Configuração do App ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'minha_chave_secreta_para_o_app_da_biblioteca'
DB_FILE = 'biblioteca.db'
app.config['DATABASE'] = os.path.join(app.root_path, DB_FILE)


# --- 2. Estilos CSS (Embutidos e Atualizados) ---
CSS_STYLE = """
<style>
    :root {
        --cor-primaria: #007bff; --cor-secundaria: #6c757d;
        --cor-sucesso: #28a745; --cor-perigo: #dc3545; --cor-aviso: #ffc107;
        --cor-fundo-sidebar: #343a40; --cor-texto-sidebar: #f8f9fa;
        --cor-fundo-main: #f4f6f9; --cor-borda: #dee2e6;
        --cor-texto: #333;
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        background-color: var(--cor-fundo-main);
        color: var(--cor-texto);
        line-height: 1.6;
    }
    
    /* --- Layout Principal (Logado) --- */
    .wrapper { display: flex; min-height: 100vh; }
    .sidebar {
        width: 250px; background-color: var(--cor-fundo-sidebar);
        color: var(--cor-texto-sidebar); flex-shrink: 0;
        display: flex; flex-direction: column;
    }
    .sidebar-header {
        padding: 1.5rem; text-align: center; font-size: 1.5rem;
        font-weight: bold; border-bottom: 1px solid #495057;
    }
    .sidebar-nav { flex-grow: 1; list-style-type: none; }
    .sidebar-nav li a {
        display: block; padding: 1rem 1.5rem; color: var(--cor-texto-sidebar);
        text-decoration: none; border-bottom: 1px solid #495057;
        transition: background-color 0.3s;
    }
    .sidebar-nav li a:hover { background-color: #495057; }
    .sidebar-footer { padding: 1.5rem; text-align: center; border-top: 1px solid #495057;}
    .sidebar-footer p { margin-bottom: 0.5rem; font-size: 0.9rem; }

    .main-content { flex-grow: 1; padding: 2rem; overflow-y: auto; }

    /* --- Layout (Deslogado) --- */
    .container-deslogado {
        display: flex; align-items: center; justify-content: center;
        min-height: 100vh; padding: 1rem;
    }

    /* --- Formulários (Login, Registro, CRUD) --- */
    .form-container {
        background-color: #fff; padding: 2rem; border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08); width: 100%;
        max-width: 500px; margin: 0 auto;
    }
    .form-container-full {
        background-color: #fff; padding: 2rem; border-radius: 8px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08); width: 100%;
    }
    .form-container h2, .form-container-full h2 {
        text-align: center; margin-bottom: 1.5rem; color: var(--cor-primaria);
    }
    .form-group { margin-bottom: 1rem; }
    .form-group label { display: block; margin-bottom: 5px; font-weight: 600; }
    .form-group input, .form-group select {
        width: 100%; padding: 10px; border: 1px solid var(--cor-borda);
        border-radius: 5px; font-size: 1rem;
    }

    /* --- Botões --- */
    .btn {
        padding: 10px 15px; border: none; border-radius: 5px;
        text-decoration: none; cursor: pointer; font-weight: 600;
        transition: opacity 0.3s; display: inline-block; margin: 5px 2px;
    }
    .btn:hover { opacity: 0.85; }
    .btn-primary { background-color: var(--cor-primaria); color: #fff; }
    .btn-success { background-color: var(--cor-sucesso); color: #fff; }
    .btn-warning { background-color: var(--cor-aviso); color: #000; }
    .btn-danger { background-color: var(--cor-perigo); color: #fff; }
    .btn-secondary { background-color: var(--cor-secundaria); color: #fff; }
    .btn-full { width: 100%; }

    /* --- Tabelas de Gerenciamento --- */
    .page-header {
        display: flex; justify-content: space-between;
        align-items: center; margin-bottom: 1.5rem;
    }
    .data-table {
        width: 100%; border-collapse: collapse; background-color: #fff;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); border-radius: 8px; overflow: hidden;
    }
    .data-table th, .data-table td {
        padding: 1rem; border-bottom: 1px solid var(--cor-borda);
        text-align: left;
    }
    .data-table th { background-color: #f1f1f1; }
    .data-table td.actions { white-space: nowrap; }
    .data-table td.actions .btn { padding: 5px 10px; font-size: 0.9rem; margin: 0 2px; }
    .data-table td.actions form { display: inline-block; }

    /* --- Mensagens Flash --- */
    .alert { padding: 1rem; border-radius: 5px; margin-bottom: 1rem; border: 1px solid transparent; }
    .alert-success { background-color: #d4edda; color: #155724; border-color: #c3e6cb; }
    .alert-danger { background-color: #f8d7da; color: #721c24; border-color: #f5c6cb; }
    .alert-info { background-color: #d1ecf1; color: #0c5460; border-color: #bee5eb; }
    .status-emprestado { color: var(--cor-perigo); font-weight: bold; }
    .status-devolvido { color: var(--cor-sucesso); }
    
    footer { text-align: center; padding: 1.5rem 0; margin-top: auto; background: #343a40; color: #f8f9fa; }
</style>
"""

# --- 3. Helper de Renderização (Modificado para Sidebar) ---

def render_page(title, content, layout_type='main'):
    """
    Função auxiliar que constrói a página HTML.
    'main' = Layout com sidebar (logado)
    'auth' = Layout centralizado (login/register)
    """
    
    messages = get_flashed_messages(with_categories=True)
    flash_html = '<div class="flash-messages">'
    for category, message in messages:
        flash_html += f'<div class="alert alert-{category}">{message}</div>'
    flash_html += '</div>'

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - Biblioteca</title>
        {CSS_STYLE}
    </head>
    """

    if layout_type == 'auth':
        # Layout para Login e Registro (Centralizado)
        html += f"""
        <body>
            <div class="container-deslogado">
                <main>
                    {flash_html if messages else ''}
                    {content}
                </main>
            </div>
        </body>
        """
    else:
        # Layout Principal com Sidebar (Logado)
        user_name = session.get('user_name', 'Usuário')
        html += f"""
        <body>
            <div class="wrapper">
                <aside class="sidebar">
                    <div class="sidebar-header">Biblioteca</div>
                    <ul class="sidebar-nav">
                        <li><a href="{url_for('dashboard')}">Dashboard</a></li>
                        <li><a href="{url_for('gerenciar_livros')}">Gerenciar Livros</a></li>
                        <li><a href="{url_for('gerenciar_usuarios')}">Gerenciar Usuários</a></li>
                        <li><a href="{url_for('gerenciar_emprestimos')}">Gerenciar Empréstimos</a></li>
                    </ul>
                    <div class="sidebar-footer">
                        <p>Usuário: <strong>{user_name}</strong></p>
                        <a href="{url_for('logout')}" class="btn btn-danger btn-full">Logout</a>
                    </div>
                </aside>

                <main class="main-content">
                    {flash_html if messages else ''}
                    {content}
                </main>
            </div>
        </body>
        """
        
    html += "</html>"
    return html

# --- 4. Funções do Banco de Dados (com ON DELETE CASCADE) ---

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    if os.path.exists(app.config['DATABASE']):
        return # Banco de dados já existe

    print(f"Criando novo banco de dados em: {app.config['DATABASE']}")
    db = get_db()
    
    db.executescript("""
        CREATE TABLE Usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        );
        CREATE TABLE Livros (
            id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER
        );
        CREATE TABLE Emprestimos (
            id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario_fk INTEGER NOT NULL,
            id_livro_fk INTEGER NOT NULL,
            data_emprestimo DATE NOT NULL,
            data_devolucao DATE,
            FOREIGN KEY (id_usuario_fk) REFERENCES Usuarios (id_usuario) ON DELETE CASCADE,
            FOREIGN KEY (id_livro_fk) REFERENCES Livros (id_livro) ON DELETE CASCADE
        );
    """)
    
    db.execute('INSERT INTO Usuarios (nome, email, senha_hash) VALUES (?, ?, ?)',
               ('Ana Silva', 'ana@email.com', generate_password_hash('123456')))
    db.execute('INSERT INTO Usuarios (nome, email, senha_hash) VALUES (?, ?, ?)',
               ('Bruno Costa', 'bruno@email.com', generate_password_hash('senhaforte')))
    db.execute('INSERT INTO Usuarios (nome, email, senha_hash) VALUES (?, ?, ?)',
               ('Admin', 'admin@email.com', generate_password_hash('admin')))
    
    db.executescript("""
        INSERT INTO Livros (titulo, autor, ano_publicacao) VALUES
        ('O Senhor dos Anéis', 'J.R.R. Tolkien', 1954),
        ('1984', 'George Orwell', 1949),
        ('Dom Casmurro', 'Machado de Assis', 1899),
        ('A Arte da Guerra', 'Sun Tzu', -500);

        INSERT INTO Emprestimos (id_usuario_fk, id_livro_fk, data_emprestimo, data_devolucao) VALUES
        (1, 2, '2025-10-15', NULL),          -- Ana pegou '1984'
        (2, 3, '2025-10-10', '2025-10-20'),  -- Bruno pegou 'Dom Casmurro' e devolveu
        (1, 1, '2025-10-25', NULL);          -- Ana pegou 'O Senhor dos Anéis'
    """)
    
    db.commit()
    print("Banco de dados inicializado e populado com sucesso.")


# --- 5. Rotas de Autenticação ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        db = get_db()
        usuario = db.execute('SELECT * FROM Usuarios WHERE email = ?', (email,)).fetchone()
        
        if usuario is None:
            flash('Email não encontrado.', 'danger')
        elif not check_password_hash(usuario['senha_hash'], senha):
            flash('Senha incorreta.', 'danger')
        else:
            session.clear()
            session['user_id'] = usuario['id_usuario']
            session['user_name'] = usuario['nome']
            return redirect(url_for('dashboard'))
            
    login_form_html = """
    <div class="form-container">
        <h2>Login do Sistema</h2>
        <form method="POST" action="">
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" name="email" required>
            </div>
            <div class="form-group">
                <label for="senha">Senha</label>
                <input type="password" id="senha" name="senha" required>
            </div>
            <button type="submit" class="btn btn-primary btn-full">Entrar</button>
        </form>
        <p style="text-align: center; margin-top: 1rem;">
            Não tem uma conta? <a href="/register">Crie uma aqui</a>.
        </p>
    </div>
    """
    return render_page("Login", login_form_html, layout_type='auth')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        db = get_db()
        
        if db.execute('SELECT id_usuario FROM Usuarios WHERE email = ?', (email,)).fetchone():
            flash(f"O email {email} já está cadastrado.", 'danger')
        else:
            db.execute('INSERT INTO Usuarios (nome, email, senha_hash) VALUES (?, ?, ?)',
                       (nome, email, generate_password_hash(senha)))
            db.commit()
            flash('Conta criada com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))
        
    register_form_html = """
    <div class="form-container">
        <h2>Criar Conta</h2>
        <form method="POST" action="">
            <div class="form-group"><label for="nome">Nome Completo</label>
                <input type="text" id="nome" name="nome" required></div>
            <div class="form-group"><label for="email">Email</label>
                <input type="email" id="email" name="email" required></div>
            <div class="form-group"><label for="senha">Senha</label>
                <input type="password" id="senha" name="senha" required></div>
            <button type="submit" class="btn btn-primary btn-full">Registrar</button>
        </form>
        <p style="text-align: center; margin-top: 1rem;">
            Já tem uma conta? <a href="/login">Faça o login</a>.
        </p>
    </div>
    """
    return render_page("Criar Conta", register_form_html, layout_type='auth')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('login'))

# --- 6. Rotas Principais (com CRUD) ---

def login_required():
    """Verifica se o usuário está logado."""
    if 'user_id' not in session:
        flash('Você precisa estar logado para ver esta página.', 'danger')
        return redirect(url_for('login'))
    return None # Usuário está logado

@app.route('/dashboard')
def dashboard():
    redirect_response = login_required()
    if redirect_response: return redirect_response

    db = get_db()
    # Mostra apenas empréstimos ATIVOS do usuário no dashboard
    emprestimos = db.execute(
        '''
        SELECT l.titulo, l.autor, e.data_emprestimo
        FROM Emprestimos e JOIN Livros l ON e.id_livro_fk = l.id_livro
        WHERE e.id_usuario_fk = ? AND e.data_devolucao IS NULL
        ORDER BY e.data_emprestimo DESC
        ''', (session['user_id'],)
    ).fetchall()

    content = f"<h2>Dashboard</h2><p>Bem-vindo ao sistema, {session['user_name']}!</p>"
    content += "<h3>Meus Empréstimos Ativos</h3>"
    
    if not emprestimos:
        content += "<p>Você não possui empréstimos ativos no momento.</p>"
    else:
        content += "<table class='data-table'><thead><tr><th>Título</th><th>Autor</th><th>Data de Empréstimo</th></tr></thead><tbody>"
        for emp in emprestimos:
            content += f"<tr><td>{emp['titulo']}</td><td>{emp['autor']}</td><td>{emp['data_emprestimo']}</td></tr>"
        content += "</tbody></table>"

    return render_page("Dashboard", content)

# --- CRUD de LIVROS ---

@app.route('/livros')
def gerenciar_livros():
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    db = get_db()
    livros = db.execute('SELECT * FROM Livros ORDER BY titulo').fetchall()
    
    content = f"""
    <div class="page-header">
        <h2>Gerenciar Livros</h2>
        <a href="{url_for('add_livro')}" class="btn btn-success">Adicionar Novo Livro</a>
    </div>
    <table class="data-table">
        <thead><tr><th>ID</th><th>Título</th><th>Autor</th><th>Ano</th><th>Ações</th></tr></thead>
        <tbody>
    """
    if not livros:
        content += '<tr><td colspan="5">Nenhum livro cadastrado.</td></tr>'
    else:
        for livro in livros:
            content += f"""
            <tr>
                <td>{livro['id_livro']}</td>
                <td>{livro['titulo']}</td>
                <td>{livro['autor']}</td>
                <td>{livro['ano_publicacao']}</td>
                <td class="actions">
                    <a href="{url_for('edit_livro', id=livro['id_livro'])}" class="btn btn-warning">Editar</a>
                    <form action="{url_for('delete_livro', id=livro['id_livro'])}" method="POST" onsubmit="return confirm('Tem certeza?');">
                        <button type="submit" class="btn btn-danger">Excluir</button>
                    </form>
                </td>
            </tr>
            """
    content += "</tbody></table>"
    return render_page("Gerenciar Livros", content)

@app.route('/livros/add', methods=['GET', 'POST'])
def add_livro():
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano_publicacao']
        
        db = get_db()
        db.execute('INSERT INTO Livros (titulo, autor, ano_publicacao) VALUES (?, ?, ?)', (titulo, autor, ano))
        db.commit()
        
        flash('Livro adicionado com sucesso!', 'success')
        return redirect(url_for('gerenciar_livros'))

    form_html = """
    <div class="form-container-full">
        <h2>Adicionar Novo Livro</h2>
        <form method="POST">
            <div class="form-group"><label for="titulo">Título</label>
                <input type="text" id="titulo" name="titulo" required></div>
            <div class="form-group"><label for="autor">Autor</label>
                <input type="text" id="autor" name="autor" required></div>
            <div class="form-group"><label for="ano_publicacao">Ano de Publicação</label>
                <input type="number" id="ano_publicacao" name="ano_publicacao" required></div>
            <button type="submit" class="btn btn-success">Salvar</button>
            <a href="{0}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
    """.format(url_for('gerenciar_livros'))
    
    return render_page("Adicionar Livro", form_html)

@app.route('/livros/edit/<int:id>', methods=['GET', 'POST'])
def edit_livro(id):
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    db = get_db()
    
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano = request.form['ano_publicacao']
        
        db.execute('UPDATE Livros SET titulo = ?, autor = ?, ano_publicacao = ? WHERE id_livro = ?',
                   (titulo, autor, ano, id))
        db.commit()
        
        flash('Livro atualizado com sucesso!', 'success')
        return redirect(url_for('gerenciar_livros'))
    
    livro = db.execute('SELECT * FROM Livros WHERE id_livro = ?', (id,)).fetchone()
    if not livro:
        flash('Livro não encontrado.', 'danger')
        return redirect(url_for('gerenciar_livros'))

    form_html = f"""
    <div class="form-container-full">
        <h2>Editar Livro</h2>
        <form method="POST">
            <div class="form-group"><label for="titulo">Título</label>
                <input type="text" id="titulo" name="titulo" value="{livro['titulo']}" required></div>
            <div class="form-group"><label for="autor">Autor</label>
                <input type="text" id="autor" name="autor" value="{livro['autor']}" required></div>
            <div class="form-group"><label for="ano_publicacao">Ano de Publicação</label>
                <input type="number" id="ano_publicacao" name="ano_publicacao" value="{livro['ano_publicacao']}" required></div>
            <button type="submit" class="btn btn-success">Salvar Alterações</button>
            <a href="{url_for('gerenciar_livros')}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
    """
    
    return render_page("Editar Livro", form_html)

@app.route('/livros/delete/<int:id>', methods=['POST'])
def delete_livro(id):
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    db = get_db()
    # Graças ao "ON DELETE CASCADE", os empréstimos associados serão removidos juntos.
    db.execute('DELETE FROM Livros WHERE id_livro = ?', (id,))
    db.commit()
    
    flash('Livro excluído com sucesso!', 'success')
    return redirect(url_for('gerenciar_livros'))

# --- CRUD de USUÁRIOS ---

@app.route('/usuarios')
def gerenciar_usuarios():
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    db = get_db()
    usuarios = db.execute('SELECT * FROM Usuarios ORDER BY nome').fetchall()
    
    content = f"""
    <div class="page-header">
        <h2>Gerenciar Usuários</h2>
        <a href="{url_for('add_usuario')}" class="btn btn-success">Adicionar Novo Usuário</a>
    </div>
    <table class="data-table">
        <thead><tr><th>ID</th><th>Nome</th><th>Email</th><th>Ações</th></tr></thead>
        <tbody>
    """
    if not usuarios:
        content += '<tr><td colspan="4">Nenhum usuário cadastrado.</td></tr>'
    else:
        for usuario in usuarios:
            content += f"""
            <tr>
                <td>{usuario['id_usuario']}</td>
                <td>{usuario['nome']}</td>
                <td>{usuario['email']}</td>
                <td class="actions">
                    <a href="{url_for('edit_usuario', id=usuario['id_usuario'])}" class="btn btn-warning">Editar</a>
                    <form action="{url_for('delete_usuario', id=usuario['id_usuario'])}" method="POST" onsubmit="return confirm('Tem certeza?');">
                        <button type="submit" class="btn btn-danger">Excluir</button>
                    </form>
                </td>
            </tr>
            """
    content += "</tbody></table>"
    return render_page("Gerenciar Usuários", content)

@app.route('/usuarios/add', methods=['GET', 'POST'])
def add_usuario():
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        db = get_db()
        if db.execute('SELECT id_usuario FROM Usuarios WHERE email = ?', (email,)).fetchone():
            flash(f"O email {email} já está cadastrado.", 'danger')
            return redirect(url_for('add_usuario'))
            
        db.execute('INSERT INTO Usuarios (nome, email, senha_hash) VALUES (?, ?, ?)',
                   (nome, email, generate_password_hash(senha)))
        db.commit()
        
        flash('Usuário adicionado com sucesso!', 'success')
        return redirect(url_for('gerenciar_usuarios'))

    form_html = f"""
    <div class="form-container-full">
        <h2>Adicionar Novo Usuário</h2>
        <form method="POST">
            <div class="form-group"><label for="nome">Nome</label>
                <input type="text" id="nome" name="nome" required></div>
            <div class="form-group"><label for="email">Email</label>
                <input type="email" id="email" name="email" required></div>
            <div class="form-group"><label for="senha">Senha</label>
                <input type="password" id="senha" name="senha" required></div>
            <button type="submit" class="btn btn-success">Salvar</button>
            <a href="{url_for('gerenciar_usuarios')}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
    """
    return render_page("Adicionar Usuário", form_html)

@app.route('/usuarios/edit/<int:id>', methods=['GET', 'POST'])
def edit_usuario(id):
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    db = get_db()
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if not senha:
            # Se a senha veio vazia, não atualiza
            db.execute('UPDATE Usuarios SET nome = ?, email = ? WHERE id_usuario = ?', (nome, email, id))
        else:
            # Se a senha foi preenchida, atualiza com o novo hash
            db.execute('UPDATE Usuarios SET nome = ?, email = ?, senha_hash = ? WHERE id_usuario = ?',
                       (nome, email, generate_password_hash(senha), id))
        db.commit()
        
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('gerenciar_usuarios'))
    
    usuario = db.execute('SELECT * FROM Usuarios WHERE id_usuario = ?', (id,)).fetchone()
    if not usuario:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('gerenciar_usuarios'))

    form_html = f"""
    <div class="form-container-full">
        <h2>Editar Usuário</h2>
        <form method="POST">
            <div class="form-group"><label for="nome">Nome</label>
                <input type="text" id="nome" name="nome" value="{usuario['nome']}" required></div>
            <div class="form-group"><label for="email">Email</label>
                <input type="email" id="email" name="email" value="{usuario['email']}" required></div>
            <div class="form-group"><label for="senha">Nova Senha</label>
                <input type="password" id="senha" name="senha" placeholder="Deixe em branco para não alterar"></div>
            <button type="submit" class="btn btn-success">Salvar Alterações</button>
            <a href="{url_for('gerenciar_usuarios')}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
    """
    return render_page("Editar Usuário", form_html)

@app.route('/usuarios/delete/<int:id>', methods=['POST'])
def delete_usuario(id):
    redirect_response = login_required()
    if redirect_response: return redirect_response

    if id == session['user_id']:
        flash('Você não pode excluir o seu próprio usuário enquanto está logado.', 'danger')
        return redirect(url_for('gerenciar_usuarios'))

    db = get_db()
    db.execute('DELETE FROM Usuarios WHERE id_usuario = ?', (id,))
    db.commit()
    
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('gerenciar_usuarios'))

# --- CRUD de EMPRÉSTIMOS ("Aluguel") ---

@app.route('/emprestimos')
def gerenciar_emprestimos():
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    db = get_db()
    emprestimos = db.execute("""
        SELECT e.*, u.nome AS nome_usuario, l.titulo AS titulo_livro
        FROM Emprestimos e
        JOIN Usuarios u ON e.id_usuario_fk = u.id_usuario
        JOIN Livros l ON e.id_livro_fk = l.id_livro
        ORDER BY e.data_emprestimo DESC
    """).fetchall()
    
    content = f"""
    <div class="page-header">
        <h2>Gerenciar Empréstimos</h2>
        <a href="{url_for('add_emprestimo')}" class="btn btn-success">Adicionar Empréstimo</a>
    </div>
    <table class="data-table">
        <thead><tr><th>ID</th><th>Usuário</th><th>Livro</th><th>Data Empréstimo</th><th>Status</th><th>Ações</th></tr></thead>
        <tbody>
    """
    if not emprestimos:
        content += '<tr><td colspan="6">Nenhum empréstimo registrado.</td></tr>'
    else:
        for emp in emprestimos:
            status = (f"<span class='status-devolvido'>Devolvido em {emp['data_devolucao']}</span>" 
                      if emp['data_devolucao'] 
                      else "<span class='status-emprestado'>Emprestado</span>")
            
            content += f"""
            <tr>
                <td>{emp['id_emprestimo']}</td>
                <td>{emp['nome_usuario']}</td>
                <td>{emp['titulo_livro']}</td>
                <td>{emp['data_emprestimo']}</td>
                <td>{status}</td>
                <td class="actions">
            """
            if not emp['data_devolucao']:
                # Botão Devolver (simula "editar")
                content += f"""
                    <form action="{url_for('return_emprestimo', id=emp['id_emprestimo'])}" method="POST" style="display:inline;">
                        <button type="submit" class="btn btn-warning">Devolver</button>
                    </form>
                """
            # Botão Excluir (remover)
            content += f"""
                    <form action="{url_for('delete_emprestimo', id=emp['id_emprestimo'])}" method="POST" onsubmit="return confirm('Tem certeza?');">
                        <button type="submit" class="btn btn-danger">Excluir</button>
                    </form>
                </td>
            </tr>
            """
    content += "</tbody></table>"
    return render_page("Gerenciar Empréstimos", content)

@app.route('/emprestimos/add', methods=['GET', 'POST'])
def add_emprestimo():
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    db = get_db()
    
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        id_livro = request.form['id_livro']
        data_emp = request.form['data_emprestimo']
        
        db.execute('INSERT INTO Emprestimos (id_usuario_fk, id_livro_fk, data_emprestimo) VALUES (?, ?, ?)',
                   (id_usuario, id_livro, data_emp))
        db.commit()
        
        flash('Empréstimo registrado com sucesso!', 'success')
        return redirect(url_for('gerenciar_emprestimos'))

    # Busca usuários e livros DISPONÍVEIS para os dropdowns
    usuarios = db.execute('SELECT * FROM Usuarios ORDER BY nome').fetchall()
    livros_disponiveis = db.execute("""
        SELECT * FROM Livros 
        WHERE id_livro NOT IN (SELECT id_livro_fk FROM Emprestimos WHERE data_devolucao IS NULL)
        ORDER BY titulo
    """).fetchall()
    
    hoje = datetime.date.today().isoformat()
    
    form_html = f"""
    <div class="form-container-full">
        <h2>Adicionar Novo Empréstimo</h2>
        <form method="POST">
            <div class="form-group"><label for="id_usuario">Usuário</label>
                <select id="id_usuario" name="id_usuario" required>
                    <option value="">Selecione um usuário</option>
    """
    for u in usuarios:
        form_html += f'<option value="{u["id_usuario"]}">{u["nome"]}</option>'
    
    form_html += """
                </select>
            </div>
            <div class="form-group"><label for="id_livro">Livro (Apenas disponíveis)</label>
                <select id="id_livro" name="id_livro" required>
                    <option value="">Selecione um livro</option>
    """
    for l in livros_disponiveis:
        form_html += f'<option value="{l["id_livro"]}">{l["titulo"]}</option>'
    
    form_html += f"""
                </select>
            </div>
            <div class="form-group"><label for="data_emprestimo">Data de Empréstimo</label>
                <input type="date" id="data_emprestimo" name="data_emprestimo" value="{hoje}" required>
            </div>
            <button type="submit" class="btn btn-success">Salvar</button>
            <a href="{url_for('gerenciar_emprestimos')}" class="btn btn-secondary">Cancelar</a>
        </form>
    </div>
    """
    
    return render_page("Adicionar Empréstimo", form_html)

@app.route('/emprestimos/return/<int:id>', methods=['POST'])
def return_emprestimo(id):
    """ Esta é a nossa função de "editar" o aluguel, marcando-o como devolvido. """
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    db = get_db()
    hoje = datetime.date.today().isoformat()
    
    db.execute('UPDATE Emprestimos SET data_devolucao = ? WHERE id_emprestimo = ?', (hoje, id))
    db.commit()
    
    flash('Livro devolvido com sucesso!', 'success')
    return redirect(url_for('gerenciar_emprestimos'))

@app.route('/emprestimos/delete/<int:id>', methods=['POST'])
def delete_emprestimo(id):
    """ Esta é a função de "remover" o aluguel (o registro do empréstimo). """
    redirect_response = login_required()
    if redirect_response: return redirect_response
    
    db = get_db()
    db.execute('DELETE FROM Emprestimos WHERE id_emprestimo = ?', (id,))
    db.commit()
    
    flash('Registro de empréstimo excluído com sucesso!', 'success')
    return redirect(url_for('gerenciar_emprestimos'))

# --- 7. Execução da Aplicação ---

if __name__ == '__main__':
    with app.app_context():
        init_db()
    
    print(f"Iniciando servidor Flask. Acesse http://127.0.0.1:5000")
    print(f"O banco de dados está salvo em: {app.config['DATABASE']}")
    app.run(debug=True)