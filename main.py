from datetime import date, datetime
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from models import db, Usuario, Produto
from werkzeug.security import check_password_hash, generate_password_hash

#inicia aplicativo flask
app = Flask(__name__)

#config banco
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+mysqlconnector://{usuario}:{senha}@{servidor}/{database}'.format(
        usuario = 'root',
        senha = 'xyZ37w49,',
        servidor = 'localhost',
        database = 'estudo_caso'
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evita avisos sobre modificações

app.secret_key = 'minha_chave_secreta'

# Inicialize a instância do SQLAlchemy
# db = SQLAlchemy()

# Vincule o db ao aplicativo Flask
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))
    
#ROTAS
@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('home.html', titulo='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Usuario.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha inválidos!', 'danger')
            return render_template('login.html', error='Usuário ou Senha inválidos!')
        
    return render_template('login.html', titulo='Login')


@app.route('/logout')
def logout():
    logout_user()
    # flash('Você saiu da sua conta!', 'info')
    return redirect(url_for('login'))


@app.route('/lista')
def lista_produtos():
    #busca os dados da tabela
    lista = Produto.query.order_by(Produto.id).all()
    return render_template('lista.html', titulo='Listagem de Produtos', todos_produtos=lista)


@app.route('/cadastrar')
@login_required
def cadastrar_produto():
    return render_template('cadastrar.html', titulo='Novo Produto')

@app.route('/adicionar', methods=['POST'])
def adicionar_produto():
    try:
        #recebe o input do usuario
        descricao_produto = request.form['txtDescricao'].strip()
        qtd_produto = int(request.form['txtQtd'])
        validade_produto = datetime.strptime(request.form['txtValidade'], '%Y-%m-%d').date()

        if not descricao_produto or qtd_produto < 0:
            return "Erro: parametros inválidos ou vazios!", 400
            
        novo_produto = Produto(
            descricao = descricao_produto,
            qtd = qtd_produto,
            validade = validade_produto
        )

        db.session.add(novo_produto)
        db.session.commit()

        flash('Produto adicionado com Sucesso!', 'success')
        return redirect('/lista')
    except Exception as e:
        return f"Erro ao adicionar produto: {str(e)}",500
    

@app.route('/editar/<int:id>')
def editar_produto(id):
    produto = Produto.query.get_or_404(id)  # Busca o produto pelo ID
    return render_template('editar.html', titulo='Editar Produto', produto=produto)


@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar_produto(id):
    produto = Produto.query.get_or_404(id)  # Busca o produto pelo ID

    # Atualiza os dados com base no formulário
    produto.descricao = request.form['txtDescricao']
    produto.qtd = int(request.form['txtQtd'])
    produto.validade = datetime.strptime(request.form['txtValidade'], '%Y-%m-%d').date()

    db.session.commit()  # Salva as alterações no banco

    flash('Produto alterado com Sucesso!', 'success')
    return redirect('/lista')  # Redireciona para a listagem


@app.route('/deletar/<int:id>', methods=['POST'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    flash('Produto excluído com Sucesso!', 'danger')
    return redirect('/lista')  # Redireciona para a lista de produtos após deletar


@app.route('/usuarios')
@login_required
def usuarios():
    if current_user.role != 'admin':
        flash('Acesso negado! Apenas Administradores podem visualizar esta página!', 'danger')
        return redirect(url_for('home'))
    
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=lista_usuarios)

@app.route('/novo_usuario')
@login_required
def novo_usuario():
    if current_user.role != 'admin':
        flash('Acesso Negado! Apenas Administradores podem cadastrar novos Usuários.', 'danger')
        return redirect(url_for('home'))
    return render_template('novo_usuario.html')


@app.route('/cadastrar_usuario', methods=['GET', 'POST'])
@login_required
def cadastrar_usuario():
    if current_user.role != 'admin':
        flash('Acesso negado! Apenas administradores podem cadastrar usuários.', 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if not username or not password or role not in ['admin', 'user']:
            flash('Preencha todos os campos corretamente!', 'warning')
            return redirect(url_for('novo_usuario'))

        # Gerar o hash da senha
        password_hash = generate_password_hash(password)

        # Criar o novo usuário
        novo_user = Usuario(username=username, password_hash=password_hash, role=role)
        db.session.add(novo_user)
        db.session.commit()

        flash('Usuário cadastrado com sucesso!', 'success')
        return redirect(url_for('usuarios'))

    return render_template('novo_usuario.html')

@app.route('/editar_usuario/<int:id>', methods=['GET'])
@login_required
def editar_usuario(id):
    if current_user.role != 'admin':
        flash('Acesso negado!', 'danger')
        return redirect(url_for('usuarios'))
    
    usuario = Usuario.query.get_or_404(id)
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/atualizar_usuario/<int:id>', methods=['POST'])
@login_required
def atualizar_usuario(id):
    if current_user.role != 'admin':
        flash('Acesso Negado!', 'danger')
        return redirect(url_for('usuarios'))

    usuario = Usuario.query.get_or_404(id)

    novo_username = request.form['username']
    nova_role = request.form['role']

    usuario.username = novo_username
    usuario.role = nova_role

    db.session.commit()
    flash('Usuário atualizado com Sucesso!','success')
    return redirect(url_for('usuarios'))


@app.route('/deletar_usuario/<int:id>', methods=['POST'])
@login_required
def deletar_usuario(id):
    if current_user.role != 'admin':
        flash('Acesso Negado!', 'danger')
        return redirect(url_for('usuarios'))
    
    usuario = Usuario.query.get_or_404(id)

    #EVITA EXCLUIR O PROPRIO ADMIN LOGADO
    if usuario.id == current_user.id:
        flash('Voce não pode excluir seu próprio usuário!', 'danger')
        return redirect(url_for('usuarios'))
    
    db.session.delete(usuario)
    db.session.commit()

    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('usuarios'))


if __name__ == '__main__':
    app.run(debug=True)