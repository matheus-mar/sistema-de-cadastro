import tkinter
from tkinter import ttk
from tkcalendar import DateEntry
from funcoes_com_sql import JanelaCadastro, JanelaGerenciar, CadastrarCliente, Filtrar, EditarCadastro


root = tkinter.Tk()
root.title("Sistema de Controle de Pacientes")
root.geometry("1100x400")

opcoes_label = tkinter.LabelFrame(root)
opcoes_label.place(x=10, y=10)

opcao_cadastrar = ttk.Button(opcoes_label, text="Cadastrar Paciente",
                             command=lambda: JanelaCadastro(cadastro_label, listagem_label))
opcao_cadastrar.pack(side=tkinter.LEFT)

opcao_gerenciar = ttk.Button(opcoes_label, text="Gerenciar Pacientes",
                             command=lambda: JanelaGerenciar(cadastro_label, listagem_label, listagem_treeView))
opcao_gerenciar.pack(side=tkinter.LEFT)

opcao_buscativa = ttk.Button(opcoes_label, text="Realizar Buscativa")
opcao_buscativa.pack(side=tkinter.RIGHT)

for widget in opcoes_label.winfo_children():
    widget.pack_configure(padx=91, ipadx=30)


# -----------vvv----------------------JANELA CADASTRO----------------vvv----------------------- #

def PadronizarCPF(event):
    cpf_paciente = cpf_entry.get()

    cpf_paciente = ''.join(filter(str.isdigit, cpf_paciente))

    if len(cpf_paciente) == 3 and len(cpf_paciente) < 6:
        cpf_paciente = f'{cpf_paciente[:3]}.'
    elif 6 <= len(cpf_paciente) < 9:
        cpf_paciente = f'{cpf_paciente[:3]}.{cpf_paciente[3:6]}.{cpf_paciente[6:]}'
    elif len(cpf_paciente) >= 9:
        cpf_paciente = f'{cpf_paciente[:3]}.{cpf_paciente[3:6]}.{cpf_paciente[6:9]}-{cpf_paciente[9:11]}'
    elif len(cpf_paciente) > 3:
        cpf_paciente = f'{cpf_paciente[:3]}.{cpf_paciente[3:]}'

    cpf_entry.delete(0, 'end')
    cpf_entry.insert(0, cpf_paciente)


cadastro_label = tkinter.LabelFrame(root, text='Cadastrar Paciente')

nome_label = tkinter.Label(cadastro_label, text="Nome Completo:")
nome_entry = tkinter.Entry(cadastro_label)
nome_label.grid(row=0, column=0)
nome_entry.grid(row=1, column=0)

nascimento_label = tkinter.Label(cadastro_label, text="Data de nascimento:")
nascimento_entry = DateEntry(cadastro_label, locale='pt_BR', date_pattern='dd/mm/yyyy')
nascimento_label.grid(row=0, column=1)
nascimento_entry.grid(row=1, column=1)

sexo_label = tkinter.Label(cadastro_label, text="Sexo:")
sexo_entry = ttk.Combobox(cadastro_label, values=["Feminino", "Masculino"], state='readonly')
sexo_label.grid(row=0, column=2)
sexo_entry.grid(row=1, column=2)

numeroFamilia_label = tkinter.Label(cadastro_label, text="Número da Família:")
numeroFamilia_entry = tkinter.Spinbox(cadastro_label, from_=1, to=200, justify='center', wrap=True)
numeroFamilia_label.grid(row=0, column=3)
numeroFamilia_entry.grid(row=1, column=3)

cpf_label = tkinter.Label(cadastro_label, text="CPF:")
cpf_entry = tkinter.Entry(cadastro_label)
cpf_entry.bind('<KeyRelease>', PadronizarCPF)
cpf_label.grid(row=0, column=4)
cpf_entry.grid(row=1, column=4)

endereco_label = tkinter.Label(cadastro_label, text='Endereço:')
numerocasa_label = tkinter.Label(cadastro_label, text='Número:')
bairro_label = tkinter.Label(cadastro_label, text='Bairro:')
endereco_entry = tkinter.Entry(cadastro_label)
numerocasa_entry = tkinter.Entry(cadastro_label)
bairro_entry = tkinter.Entry(cadastro_label)

endereco_label.grid(row=2, column=0)
endereco_entry.grid(row=3, column=0)
numerocasa_label.grid(row=2, column=1)
numerocasa_entry.grid(row=3, column=1)
bairro_label.grid(row=2, column=2)
bairro_entry.grid(row=3, column=2)

cadastro_button = ttk.Button(cadastro_label, text='Cadastrar',
                             command=lambda: CadastrarCliente(nome_entry, nascimento_entry, sexo_entry,
                                                              numeroFamilia_entry, cpf_entry, endereco_entry,
                                                              numerocasa_entry, bairro_entry))

for widget in cadastro_label.winfo_children():
    widget.grid_configure(ipadx=20, pady=3, padx=20)

cadastro_button.grid(row=3, column=3, ipadx=50)

# ------------------VVV-------------JANELA GERENCIAR-----------------VVV----------------------#
listagem_label = tkinter.LabelFrame(root)

filtro_frame = tkinter.Frame(listagem_label)
filtro_frame.grid(row=0, column=0)
filtrar_nome_label = tkinter.Label(filtro_frame, text='Nome:')
filtrar_nome_label.grid(row=0, column=0)
filtrar_nome_entry = tkinter.Entry(filtro_frame)
filtrar_nome_entry.grid(row=0, column=1, ipadx=50)
filtrar_button = ttk.Button(filtro_frame, text='Filtrar',
                            command=lambda: Filtrar(filtrar_nome_entry, listagem_treeView))
filtrar_button.grid(row=0, column=3, ipadx=10, padx=20)

editar_button = ttk.Button(filtro_frame, text='Editar Paciente',
                           command=lambda: EditarCadastro(listagem_treeView))
editar_button.grid(row=0, column=4, ipadx=10)

deletar_button = ttk.Button(filtro_frame, text='Deletar Paciente')
deletar_button.grid(row=0, column=5, ipadx=10)

listagem_treeFrame = ttk.Frame(listagem_label)
listagem_treeFrame.grid(row=1, column=0, pady=5)
listagem_scroll = ttk.Scrollbar(listagem_treeFrame)
listagem_scroll.pack(side='right', fill='y')
colunas = ('ID', 'Nome do Paciente', 'Data de Nascimento', 'Sexo', 'Número da Família', 'CPF', 'Endereço', 'Bairro')
listagem_treeView = ttk.Treeview(listagem_treeFrame, show='headings',
                                 yscrollcommand=listagem_scroll.set, columns=colunas, height=13)
listagem_treeView.column('ID', width=50)
listagem_treeView.column('Nome do Paciente', width=200)
listagem_treeView.column('Data de Nascimento', width=150)
listagem_treeView.column('Sexo', width=120)
listagem_treeView.column('Número da Família', width=100)
listagem_treeView.column('CPF', width=130)
listagem_treeView.column('Endereço', width=150)
listagem_treeView.column('Bairro', width=150)
listagem_treeView.pack()
listagem_treeView.heading('ID', text='ID')
listagem_treeView.heading('Nome do Paciente', text='Nome do Paciente')
listagem_treeView.heading('Data de Nascimento', text='Data de Nascimento')
listagem_treeView.heading('Sexo', text='Sexo')
listagem_treeView.heading('Número da Família', text='Nº Família')
listagem_treeView.heading('CPF', text='CPF')
listagem_treeView.heading('Endereço', text='Endereço')
listagem_treeView.heading('Bairro', text='Bairro')
listagem_scroll.config(command=listagem_treeView.yview)

# ----------------------------------------------------------------------------------------------


root.mainloop()
