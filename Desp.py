import tkinter as tk
from tkinter import messagebox
import sqlite3

def adicionar_despesa():
    nome = entry_nome.get()
    valor = float(entry_valor.get())
    descricao = entry_descricao.get()
    pago = check_pago.get()

    # Inserir despesa no banco de dados
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO despesas (nome, valor, descricao, pago) VALUES (?, ?, ?, ?)",
                   (nome, valor, descricao, pago))
    conn.commit()
    conn.close()

    # Limpar os campos de entrada
    entry_nome.delete(0, tk.END)
    entry_valor.delete(0, tk.END)
    entry_descricao.delete(0, tk.END)
    check_pago.set(0)

    atualizar_soma_despesas()

def atualizar_soma_despesas():
    # Calcular a soma das despesas pendentes no banco de dados
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor) FROM despesas WHERE pago = 0")
    resultado = cursor.fetchone()[0]
    conn.close()

    # Atualizar o rótulo com a soma das despesas
    label_soma_despesas.config(text="Total de Despesas: R$ {:.2f}".format(resultado or 0))

def visualizar_despesas():
    # Obter todas as despesas do banco de dados
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT nome, valor, descricao, pago FROM despesas")
    despesas = cursor.fetchall()
    conn.close()

    # Criar uma nova janela para exibir as despesas
    janela_despesas = tk.Toplevel()
    janela_despesas.title("Despesas")

    for i, despesa in enumerate(despesas):
        nome, valor, descricao, pago = despesa
        status = "Pago" if pago else "Pendente"
        label_despesa = tk.Label(janela_despesas, text="{} - R$ {:.2f} - {} ({})".format(nome, valor, descricao, status))
        label_despesa.pack()

def simular_sobra():
    # Obter a soma das despesas pendentes
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor) FROM despesas WHERE pago = 0")
    total_despesas = cursor.fetchone()[0]
    conn.close()
    
def retirar_despesasa():
    # Obter o nome da despesa a ser retirada
    nome_despesa = entry_retirar.get()
    
    # Verificar se a despesa existe no banco de dados
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM despesas WHERE nome=?", (nome_despesa,))
    despesa = cursor.fetchone()
    
    if despesa is None:
        messagebox.showerror("Despesa não encontrada", "A despesa informada não foi encontrada no banco de dados!")
    else:
        # Excluir a despesa do banco de dados
        cursor.execute("DELETE FROM despesas WHERE nome=?", (nome_despesa,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Despesa removida", "A despesa foi removida com sucesso!")
        
        # Atualizar a soma das despesas após a remoção
        atualizar_soma_despesas()
        
        # Limpar o campo de entrada
        entry_retirar.delete(0, tk.END)
        

    # Obter o valor informado para a simulação
    valor_simulado = float(entry_simulacao.get())

    # Calcular a sobra de dinheiro
    sobra = valor_simulado - (total_despesas or 0)

    # Exibir a sobra de dinheiro em uma mensagem de diálogo
    tk.messagebox.showinfo("Simulação de Sobra", "Sobra de dinheiro: R$ {:.2f}".format(sobra))

# Criar a tabela no banco de dados, se não existir
conn = sqlite3.connect('despesas.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS despesas 
               ( id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT,
               valor REAL,
               descricao TEXT,
               pago INTEGER)''')
conn.commit()
conn.close()

# Criar a janela principal
janela= tk.Tk()
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

# Criar campo de entrada para retirar despesa
label_retirar = tk.Label(janela, text="Retirar Despesa:")
label_retirar.pack()
entry_retirar = tk.Entry(janela)
entry_retirar.pack()

# Criar Botão para retirar despesa
botao_retirar = tk.Button(janela, text="Retirar Despesa", command=retirar_despesasa)
botao_retirar.pack()

# Criar checkbox para indicar se a despesa foi paga
check_pago = tk.IntVar()
check_pago.set(0)
checkbox_pago = tk.Checkbutton(janela, text="Pago", variable=check_pago)
checkbox_pago.pack()

# Criar botão para adicionar despesa
botao_adicionar = tk.Button(janela, text="Adicionar Despesa", command=adicionar_despesa)
botao_adicionar.pack()

# Criar botão para visualizar despesas
botao_visualizar = tk.Button(janela, text="Visualizar Despesas", command=visualizar_despesas)
botao_visualizar.pack()

# Criar rótulo para exibir a soma das despesas
label_soma_despesas = tk.Label(janela, text="Total de Despesas: R$ 0.00")
label_soma_despesas.pack()

# Criar entrada para simular sobra
label_simulacao = tk.Label(janela, text="Simulação de Sobra:")
label_simulacao.pack()
entry_simulacao = tk.Entry(janela)
entry_simulacao.pack()

# Criar botão para simular sobra
botao_simular_sobra = tk.Button(janela, text="Simular Sobra", command=simular_sobra)
botao_simular_sobra.pack()

# Atualizar a soma das despesas ao iniciar a aplicação
atualizar_soma_despesas()

# Iniciar a aplicação
janela.mainloop()
