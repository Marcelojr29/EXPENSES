import tkinter as tk
from tkinter import messagebox
import sqlite3

# Criar a tabela no banco de dados, se não existir
conn = sqlite3.connect('despesas.db')
cursor = conn.cursor()

# Criação da tabela despesas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS despesas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        valor REAL,
        descricao TEXT
    )
''')
conn.commit()
conn.close()

def adicionar_despesa():
    nome = entry_nome.get()
    valor = float(entry_valor.get())
    descricao = entry_descricao.get()

    # Inserir despesa no banco de dados
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO despesas (nome, valor, descricao) VALUES (?, ?, ?)", (nome, valor, descricao))
    conn.commit()
    conn.close()

    # Limpar os campos de entrada
    entry_nome.delete(0, tk.END)
    entry_valor.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)

    atualizar_soma_despesas()

def atualizar_soma_despesas():
    # Calcular a soma das despesas no banco de dados
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor) FROM despesas")
    resultado = cursor.fetchone()[0]
    conn.close()

    # Atualizar o rótulo com a soma das despesas
    label_soma_despesas.config(text="Total de Despesas: R$ {:.2f}".format(resultado or 0))
    
def visualizar_despesas():
    # Obter todas as despesas do banco de dados
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, valor, descricao FROM despesas")
    despesas = cursor.fetchall()
    conn.close()

    # Criar uma nova janela para exibir as despesas
    janela_despesas = tk.Toplevel()
    janela_despesas.title("Despesas")
    
    for i, despesa in enumerate(despesas):
        nome, valor, descricao = despesa
        label_despesa = tk.Label(janela_despesas, text="{} - R$ {:.2f} - {}".format(nome, valor, descricao))
        label_despesa.pack() 

def simular_sobra():
    # Obter a soma das despesas
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor) FROM despesas")
    total_despesas = cursor.fetchone()[0]
    conn.close()
    
    # Obter o valor informado para a simulacao
    valor_simulado = float(entry_simulacao.get())
    
    # Calcular a sobra do dinheiro
    sobra = valor_simulado - (total_despesas or 0)
    
    # Exibir a sobra de dinheiro em uma mensagem de dialogo
    tk.messagebox.showinfo("Simulação de Sobra", "Sobra de Dinheiro: R$ {:.2f}".format(sobra))

# Criar a janela principal
janela = tk.Tk()
janela.title("Aplicação de Despesas")

# Criar rótulo e campos de entrada
label_nome = tk.Label(janela, text="Nome:")
label_nome.pack()
entry_nome = tk.Entry(janela)
entry_nome.pack()

label_valor = tk.Label(janela, text="Valor:")
label_valor.pack()
entry_valor = tk.Entry(janela)
entry_valor.pack()

label_descricao = tk.Label(janela, text="Descrição:")
label_descricao.pack()
entry_descricao = tk.Entry(janela)
entry_descricao.pack()

# Criar botão para adicionar despesa
botao_adicionar = tk.Button(janela, text="Adicionar Despesa", command=adicionar_despesa)
botao_adicionar.pack()

# Criar rótulo para exibir a soma das despesas
label_soma_despesas = tk.Label(janela, text="Total de Despesas: R$ 0.00")
label_soma_despesas.pack()

# Atualizar a soma das despesas ao iniciar a aplicação
atualizar_soma_despesas()

# Iniciar a aplicação
janela.mainloop()