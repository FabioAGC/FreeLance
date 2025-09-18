import sqlite3
import os
import sys

if getattr(sys, 'frozen', False):
    PROJECT_ROOT = os.path.dirname(sys.executable)
else:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'db.sqlite3')

def conectar():
    return sqlite3.connect(DB_PATH)

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT,
        telefone TEXT,
        endereco TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS servicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT NOT NULL,
        servico TEXT NOT NULL,
        custo REAL NOT NULL,
        desconto REAL DEFAULT 0.0,
        status TEXT NOT NULL,
        data_inicio TEXT,
        data_conclusao TEXT,
        descricao TEXT
    )''')
    conn.commit()
    conn.close()

def inserir_cliente(nome, email, telefone, endereco):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clientes (nome, email, telefone, endereco) VALUES (?, ?, ?, ?)',
                   (nome, email, telefone, endereco))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes')
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def inserir_servico(cliente, servico, custo, desconto, status, data_inicio, data_conclusao=None):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO servicos (cliente, servico, custo, desconto, status, data_inicio, data_conclusao) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (cliente, servico, custo, desconto, status, data_inicio, data_conclusao))
    conn.commit()
    conn.close()

def listar_servicos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT id, cliente, servico, custo, desconto, status, data_inicio, data_conclusao FROM servicos')
    servicos = cursor.fetchall()
    conn.close()
    return servicos

def atualizar_status_servico(id_servico, novo_status):
    conn = conectar()
    cursor = conn.cursor()
    if novo_status.lower() == 'concluido':
        import datetime
        data_conclusao = datetime.datetime.now().strftime('%d/%m/%Y')
        cursor.execute('UPDATE servicos SET status=?, data_conclusao=? WHERE id=?', (novo_status, data_conclusao, id_servico))
    else:
        cursor.execute('UPDATE servicos SET status=? WHERE id=?', (novo_status, id_servico))
    conn.commit()
    conn.close()
