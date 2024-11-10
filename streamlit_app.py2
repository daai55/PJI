from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///acougue.db'
app.config['JWT_SECRET_KEY'] = 'sua_chave_secreta_aqui'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Modelos
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))
    preco = db.Column(db.Float, nullable=False)
    duracao = db.Column(db.Integer, nullable=False)

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pendente')

# Rotas de exemplo
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['senha']).decode('utf-8')
    novo_cliente = Cliente(nome=data['nome'], email=data['email'], senha=hashed_password)
    db.session.add(novo_cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente registrado com sucesso!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cliente = Cliente.query.filter_by(email=data['email']).first()
    if cliente and bcrypt.check_password_hash(cliente.senha, data['senha']):
        token = create_access_token(identity=cliente.id)
        return jsonify({'token': token})
    return jsonify({'message': 'Login inválido!'}), 401

@app.route('/servicos', methods=['GET'])
def listar_servicos():
    servicos = Servico.query.all()
    output = [{'id': servico.id, 'nome': servico.nome, 'descricao': servico.descricao, 'preco': servico.preco, 'duracao': servico.duracao} for servico in servicos]
    return jsonify({'servicos': output})

@app.route('/agendamentos', methods=['POST'])
def agendar_servico():
    data = request.get_json()
    cliente_id = data['cliente_id']
    servico_id = data['servico_id']
    data_hora = datetime.strptime(data['data_hora'], '%Y-%m-%d %H:%M')
    novo_agendamento = Agendamento(cliente_id=cliente_id, servico_id=servico_id, data_hora=data_hora)
    db.session.add(novo_agendamento)
    db.session.commit()
    return jsonify({'message': 'Agendamento criado com sucesso!'})

if __name__ == '__main__':
    db.create_all()  # Cria o banco de dados e as tabelas
    app.run(debug=True)
