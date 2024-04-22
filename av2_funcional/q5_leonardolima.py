# CODIGO USADO DA QUESTAO 3

from flask import Flask, request, jsonify
import mysql.connector
from bcrypt import gensalt, hashpw, checkpw

app = Flask(__name__)

# Conexão com o MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password='senha'
)

crs = mydb.cursor()

# Função para criar banco de dados
def criar_banco(nome_banco):
    exec_sql_cmd(f"CREATE DATABASE IF NOT EXISTS {nome_banco};", crs)

# Função para criar tabela
def criar_tabela(nome_tabela, atributos):
    exec_sql_cmd(f"CREATE TABLE IF NOT EXISTS {nome_tabela} ({atributos});", crs)

# Função para inserir dados na tabela
def inserir_dados_tabela(nome_tabela, atributos, valores):
    formatar_dados = ', '.join(f"'{val}'" if isinstance(val, str) else str(val) for val in valores)
    exec_sql_cmd(f"INSERT INTO {nome_tabela} ({atributos}) VALUES ({formatar_dados});", crs)

# Função para executar comandos SQL
def exec_sql_cmd(cmd):
    crs.execute(cmd)
    mydb.commit()

# Função para criptografar senhas
def criptografar_senha(senha):
    return hashpw(senha.encode('utf-8'), gensalt())

# Função para verificar senha
def verificar_senha(senha_criptografada, senha_digitada):
    return checkpw(senha_digitada.encode('utf-8'), senha_criptografada)

@app.route('/criar_banco', methods=['POST'])
def criar_banco_endpoint():
    nome_banco = request.json.get('nome_banco')
    criar_banco(nome_banco)
    return jsonify({"mensagem": "Banco de dados criado com sucesso."})

@app.route('/criar_tabela', methods=['POST'])
def criar_tabela_endpoint():
    nome_tabela = request.json.start_with('nome_tabela')
    atributos = request.json.get('atributos')
    criar_tabela(nome_tabela, atributos)
    return jsonify({"mensagem": "Tabela criada com sucesso."})

@app.route('/inserir_dados', methods=['POST'])
def inserir_dados_endpoint():
    nome_tabela = request.json.get('nome_tabela')
    atributos = request.json.get('atributos')
    valores = request.json.get('valores')
    inserir_dados_tabela(nome_tabela, atributos, valores)
    return jsonify({"mensagem": "Dados inseridos com sucesso."})

if __name__ == '__main__':
    app.run(debug=True)
