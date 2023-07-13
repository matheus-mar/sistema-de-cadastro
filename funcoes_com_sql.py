import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector


# Conectar ao banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nopassword",
    database="pacientes"
)

# Criar a tabela de clientes
cursor = db.cursor()
cursor.execute(
    "CREATE TABLE IF NOT EXISTS pacientes (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), nascimento VARCHAR(255), sexo VARCHAR(10), numero_familia INT, cpf VARCHAR(15), endereco VARCHAR(255), bairro VARCHAR(255))")


def JanelaCadastro(cadastro_label, listagem_label):
    listagem_label.place_forget()
    cadastro_label.place(x=10, y=50, height=325)


def JanelaGerenciar(cadastro_label, listagem_label, listagem_treeView):
    cadastro_label.place_forget()
    listagem_label.place(x=10, y=50)
    CarregarDados(listagem_treeView)


def CadastrarCliente(nome_entry, nascimento_entry, sexo_entry, numeroFamilia_entry, cpf_entry,
                     endereco_entry, numerocasa_entry, bairro_entry):
    nome_paciente = nome_entry.get()
    nascimento_paciente = nascimento_entry.get()
    sexo_paciente = sexo_entry.get()
    numero_familia = numeroFamilia_entry.get()
    cpf_paciente = cpf_entry.get()
    rua_paciente = endereco_entry.get()
    numerocasa_paciente = numerocasa_entry.get()
    bairro_paciente = bairro_entry.get()
    endereco_casa = rua_paciente + " Nº" + numerocasa_paciente

    if nome_paciente == "" or nascimento_paciente == "" or sexo_paciente == "" or numero_familia == "" or cpf_paciente == "" or rua_paciente == "" or numerocasa_paciente == "" or bairro_paciente == "":
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    cursor = db.cursor()
    sql = "INSERT INTO pacientes (nome, nascimento, sexo, numero_familia, cpf, endereco, bairro) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (
        nome_paciente, nascimento_paciente, sexo_paciente, numero_familia, cpf_paciente, endereco_casa, bairro_paciente)
    cursor.execute(sql, val)
    db.commit()

    messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso.")

    nome_entry.delete(0, 'end')
    nascimento_entry.delete(0, 'end')
    sexo_entry.delete(0, 'end')
    numeroFamilia_entry.delete(0, 'end')
    cpf_entry.delete(0, 'end')
    endereco_entry.delete(0, 'end')
    numerocasa_entry.delete(0, 'end')
    bairro_entry.delete(0, 'end')


def CarregarDados(listagem_treeView):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()

    for data in listagem_treeView.get_children():
        listagem_treeView.delete(data)
    for ro in pacientes:
        listagem_treeView.insert('', 'end', text='', value=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6], ro[7]))


def Filtrar(filtrar_nome_entry, listagem_treeView):
    nome_filtrar = filtrar_nome_entry.get()

    if nome_filtrar == '':
        CarregarDados(listagem_treeView)

    else:
        for data in listagem_treeView.get_children():
            listagem_treeView.delete(data)

        sql = "SELECT * FROM pacientes WHERE nome REGEXP %s"
        val = (nome_filtrar,)
        cursor.execute(sql, val)
        pacientes = cursor.fetchall()

        for ro in pacientes:
            listagem_treeView.insert('', 'end', text='', value=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6], ro[7]))

def EditarCadastro(listagem_treeView):
    paciente_selecionado = listagem_treeView.focus()
    valores = listagem_treeView.item(paciente_selecionado, 'value')
    print(valores)

    if valores == '':
        messagebox.showerror('Atenção!', 'Selecione um paciente para ser atualizado.')

    else:
        editar_cadastro = tkinter.Tk()
        editar_cadastro.title("Editar Cadastro de Paciente")
        editar_cadastro.geometry("1070x200")

        editar_label = tkinter.LabelFrame(editar_cadastro, text='Editar Cadastro')
        editar_label.place(x=10, height=190)

        editarnome_label = tkinter.Label(editar_label, text="Nome Completo:")
        editarnome_entry = tkinter.Entry(editar_label)
        editarnome_label.grid(row=0, column=0)
        editarnome_entry.grid(row=1, column=0)

        editarnascimento_label = tkinter.Label(editar_label, text="Data de nascimento:")
        editarnascimento_entry = DateEntry(editar_label, locale='pt_BR', date_pattern='dd/mm/yyyy')
        editarnascimento_entry.delete(0, 'end')
        editarnascimento_label.grid(row=0, column=1)
        editarnascimento_entry.grid(row=1, column=1)

        editarsexo_label = tkinter.Label(editar_label, text="Sexo:")
        editarsexo_entry = ttk.Combobox(editar_label, values=["Feminino", "Masculino"])
        editarsexo_label.grid(row=0, column=2)
        editarsexo_entry.grid(row=1, column=2)

        editarnumeroFamilia_label = tkinter.Label(editar_label, text="Número da Família:")
        editarnumeroFamilia_entry = tkinter.Spinbox(editar_label, from_=1, to=200, justify='center', wrap=True)
        editarnumeroFamilia_label.grid(row=0, column=3)
        editarnumeroFamilia_entry.grid(row=1, column=3)

        editarcpf_label = tkinter.Label(editar_label, text="CPF:")
        editarcpf_entry = tkinter.Entry(editar_label)
        '''editarcpf_entry.bind('<KeyRelease>', PadronizarCPF)'''
        editarcpf_label.grid(row=0, column=4)
        editarcpf_entry.grid(row=1, column=4)

        editarendereco_label = tkinter.Label(editar_label, text='Endereço:')
        editarnumerocasa_label = tkinter.Label(editar_label, text='Número:')
        editarbairro_label = tkinter.Label(editar_label, text='Bairro:')
        editarendereco_entry = tkinter.Entry(editar_label)
        editarnumerocasa_entry = tkinter.Entry(editar_label)
        editarbairro_entry = tkinter.Entry(editar_label)

        editarendereco_label.grid(row=2, column=0)
        editarendereco_entry.grid(row=3, column=0)
        editarnumerocasa_label.grid(row=2, column=1)
        editarnumerocasa_entry.grid(row=3, column=1)
        editarbairro_label.grid(row=2, column=2)
        editarbairro_entry.grid(row=3, column=2)

        for widget in editar_label.winfo_children():
            widget.grid_configure(ipadx=20, pady=3, padx=20)

        confirma_button = ttk.Button(editar_label, text='Confirmar')
        confirma_button.grid(row=3, column=3, ipadx=50)
        fechar_button = ttk.Button(editar_label, text='Cancelar', command=lambda: editar_cadastro.destroy())
        fechar_button.grid(row=3, column=4, ipadx=50)

        numerocasa = valores[6]
        enderecosplit = numerocasa.split(' Nº')

        editarnome_entry.insert(0, valores[1])
        editarnascimento_entry.insert(0, valores[2])
        editarsexo_entry.insert(0, valores[3])
        editarnumeroFamilia_entry.insert(0, valores[4])
        editarcpf_entry.insert(0, valores[5])
        editarendereco_entry.insert(0, enderecosplit[0])
        editarnumerocasa_entry.insert(0, enderecosplit[1])
        editarbairro_entry.insert(0, valores[7])
        editarsexo_entry.configure(state='readonly')

        editar_cadastro.mainloop()

