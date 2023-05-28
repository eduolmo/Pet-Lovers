from tkinter import *
from tkinter import ttk
import psycopg2
import pandas as pd

#Banco de Dados
def conexao():
	try:
		conn = psycopg2.connect(
		host="kesavan.db.elephantsql.com",
		database="harhjaol",
		user="harhjaol",
		password="SchSpkrLpwPHPVYHHEagEU36dWYdZSPO"
		)
	except(Exception,psycopg2.DatabaseError) as error:
		print(error)
	return conn



def tabela(conn):
	global c
	c = conn.cursor()
	c.execute('''
		CREATE TABLE IF NOT EXISTS VETERINARIO (
			salario FLOAT,
			turno VARCHAR,
			nome VARCHAR,
			cpf VARCHAR PRIMARY KEY
		);
		
		CREATE TABLE IF NOT EXISTS CLIENTE (
			telefone INTEGER,
			cpf VARCHAR PRIMARY KEY,
			nome VARCHAR,
			email VARCHAR,
			senha VARCHAR
		);

		CREATE TABLE IF NOT EXISTS PET (
			nome VARCHAR,
			especie VARCHAR,
			raca VARCHAR,
			cod_pet SERIAL PRIMARY KEY,
			FK_CLIENTE_cpf VARCHAR,
			FOREIGN KEY (FK_CLIENTE_cpf) REFERENCES CLIENTE (cpf)
		);

		CREATE TABLE IF NOT EXISTS Consulta (
			fk_VETERINARIO_cpf VARCHAR,
			fk_PET_cod_pet SERIAL,
			cod_consulta SERIAL PRIMARY KEY,
			descricao VARCHAR,
			data_hora TIMESTAMP,
			preco FLOAT,
			FOREIGN KEY (fk_VETERINARIO_cpf) REFERENCES VETERINARIO (cpf),
			FOREIGN KEY (fk_PET_cod_pet) REFERENCES PET (cod_pet)
		);
		 
	''',conn)

global conn
conn = conexao()
tabela(conn)
conn.commit()

#Aplicacao do Pet Lovers
class Application:
	#tela incial do login
	def __init__(self,master=None):
		#criando titulo
		self.master = master
		master.title('LOGIN')
		self.l1 = Label(master,text='PET LOVERS',font='times 15',bg='#C56AFF',fg='#5E0498',pady=20)
		self.l1.pack()

		#sessao do login
		self.l2 = Label(master,text='Login',font='times 12',bg='#C56AFF')
		self.l2.pack()

		#criando containers
		self.c1 = Frame(master,pady=10,bg='#C56AFF')
		self.c1.pack()

		self.c2 = Frame(master,pady=10,bg='#C56AFF')
		self.c2.pack()

		#widgets do login
		self.l3 = Label(self.c1,text='Email:',bg='#C56AFF')
		self.l3.pack(side=LEFT)

		self.e1 = Entry(self.c1,width=30)
		self.e1.pack()

		self.l4 = Label(self.c2,text='Senha:',bg='#C56AFF')
		self.l4.pack(side=LEFT)

		self.e2 = Entry(self.c2,width=30)
		self.e2.pack()

		self.b1 = Button(master,text='Logar')
		self.b1['command'] = self.logar
		self.b1.pack()

		self.c3 = Frame(master,bg='#C56AFF',pady=60)
		self.c3.pack()

		self.b2 = Button(self.c3,text='Não tenho Cadastro')
		self.b2['command'] = self.cadastro
		self.b2.pack()
	
	def logar(self):
		global email
		email = self.e1.get()
		
		tabela = pd.read_sql_query(f"""select senha from cliente where email = '{email}'""",conn)		
		senha = tabela.senha.item()
		
		if(senha == self.e2.get()):
			self.menu()
		
		self.master.destroy()		
		
		
	def cadastro(self):
		#criando tela
		self.tk = Tk()
		self.tk.title('CADASTRO')
		self.tk['bg'] = '#C56AFF'
		self.tk.geometry('400x450')

		#criando titulo
		self.l1 = Label(self.tk,text='PET LOVERS',font='times 15',bg='#C56AFF',fg='#5E0498',pady=20)
		self.l1.pack()

		#sessao do cadastro
		self.l2 = Label(self.tk,text='Cadastro',font='times 12',bg='#C56AFF')
		self.l2.pack()

		#criando containers
		self.c8 = Frame(self.tk,pady=10,bg='#C56AFF')
		self.c8.pack()
		
		self.c9 = Frame(self.tk,pady=10,bg='#C56AFF')
		self.c9.pack()
		
		self.c1 = Frame(self.tk,pady=10,bg='#C56AFF')
		self.c1.pack()

		self.c2 = Frame(self.tk,pady=10,bg='#C56AFF')
		self.c2.pack()

		self.c3 = Frame(self.tk,pady=10,bg='#C56AFF')
		self.c3.pack()
		
		#widgets do cadastro
		self.l11 = Label(self.c8,text='Email:',bg='#C56AFF')
		self.l11.pack(side=LEFT)
		
		self.e8 = Entry(self.c8,width=30)
		self.e8.pack()
		
		self.l12 = Label(self.c9,text='Senha:',bg='#C56AFF')
		self.l12.pack(side=LEFT)
		
		self.e9 = Entry(self.c9,width=30)
		#self.e9['show'] = '*'
		self.e9.pack()
		
		self.l3 = Label(self.c1,text='CPF:',bg='#C56AFF')
		self.l3.pack(side=LEFT)

		self.e1 = Entry(self.c1,width=30)
		self.e1.pack()

		self.l4 = Label(self.c2,text='Nome:',bg='#C56AFF')
		self.l4.pack(side=LEFT)

		self.e2 = Entry(self.c2,width=30)
		self.e2.pack()

		self.l5 = Label(self.c3,text='Telefone:',bg='#C56AFF')
		self.l5.pack(side=LEFT)

		self.e3 = Entry(self.c3,width=30)
		self.e3.pack()
		
		#criando botao
		self.b1 = Button(self.tk,text='Cadastrar')
		self.b1['command'] = self.cadastrar
		self.b1.pack(pady=40)
		
	def cadastrar(self):
		email = self.e8.get()
		senha = self.e9.get()
		cpf = self.e1.get()
		nome = self.e2.get()
		tel = self.e3.get()
		
		c.execute(f'''
		insert into cliente values({tel},'{cpf}','{nome}','{email}','{senha}')
		''',conn)
		conn.commit()
		
		self.tk.destroy()

	def menu(self):
		#criando janela
		self.tk = Tk()
		self.tk.title('MENU')
		self.tk['bg'] = '#FF932F'
		self.tk.geometry("250x250")

		#adicionando o titulo
		self.l = Label(self.tk, text='PET LOVERS')
		self.l['font'] = 'times 15'
		self.l['fg'] = 'brown'
		self.l['bg'] = '#FF932F'
		self.l['pady'] = 20
		self.l.pack()

		#criando containers
		self.c1 = Frame(self.tk)
		self.c1["bg"] = "#FF932F"
		self.c1['pady'] = 10
		self.c1.pack()

		self.c2 = Frame(self.tk)
		self.c2['bg'] = '#FF932F'
		self.c2['pady'] = 10
		self.c2.pack()

		self.c3 = Frame(self.tk)
		self.c3["bg"] = "#FF932F"
		self.c3['pady'] = 10
		self.c3.pack()

		self.c4 = Frame(self.tk)
		self.c4["bg"] = "#FF932F"
		self.c4['pady'] = 10
		self.c4.pack()

		#criando botoes
		self.b1 = Button(self.c1)
		self.b1['text'] = 'Cadastrar Pet'
		self.b1['activebackground'] = '#FF812F'
		self.b1['command'] = self.pet
		self.b1.pack()

		self.b2 = Button(self.c2)
		self.b2['text'] = 'Agendamento'
		self.b2['activebackground'] = '#FF812F'
		self.b2['command'] = self.agendamento
		self.b2.pack()

		self.b3 = Button(self.c3)
		self.b3['text'] = 'Visualizar Agendamentos'
		self.b3['activebackground'] = '#FF812F'
		self.b3['command'] = self.visualizar
		self.b3.pack()
		
	def pet(self):
		#criando a janela(interface grafica)
		self.tk = Tk()
		self.tk.title('CADASTRAR PET')
		self.tk.geometry('400x350')
		self.tk['bg'] = '#FF5E6E'

		#adicionando o titulo
		self.l1 = Label(self.tk,text='Cadastrar Pet',font='times 15',bg='#FF5E6E',fg='white',pady=15)
		self.l1.pack()

		#adicionando o titulo da sessao do pet
		self.l2 = Label(self.tk,text='Pet',font='times 12',bg='#FF5E6E')
		self.l2.pack()

		#widgets do nome
		self.c5 = Frame(self.tk)
		self.c5['bg'] = '#FF5E6E'
		self.c5['pady'] = 10
		self.c5.pack()

		self.l3 = Label(self.c5,text='Nome:',bg='#FF5E6E')
		self.l3.pack(side=LEFT)

		self.e1 = Entry(self.c5)
		self.e1['width'] = 30
		self.e1.pack()

		#widgets da raca
		self.c6 = Frame(self.tk)
		self.c6['bg'] = '#FF5E6E'
		self.c6['pady'] = 10
		self.c6.pack()

		self.l4 = Label(self.c6,text='Raça:',bg='#FF5E6E')
		self.l4.pack(side=LEFT)

		self.e2 = Entry(self.c6)
		self.e2['width'] = 30
		self.e2.pack()

		#widgets da especie
		self.c7 = Frame(self.tk)
		self.c7['bg'] = '#FF5E6E'
		self.c7['pady'] = 10
		self.c7.pack()

		self.l5 = Label(self.c7,text='Espécie:',bg='#FF5E6E')
		self.l5.pack(side=LEFT)

		self.e3 = Entry(self.c7)
		self.e3['width'] = 30
		self.e3.pack()
		
		#adicionando botao
		self.c10 = Frame(self.tk)
		self.c10['bg'] = '#FF5E6E'
		self.c10['pady'] = 30
		self.c10.pack()

		self.b5 = Button(self.c10,text='Cadastrar Pet')
		self.b5['command'] = self.cadastrarPet
		self.b5.pack()
		
	def cadastrarPet(self):
		nome = self.e1.get()
		raca = self.e2.get()
		especie = self.e3.get()
		
		minitabela = pd.read_sql_query(f"select cpf from cliente where email = '{email}'",conn)
		cpf = minitabela.cpf.item()		
		
		c.execute(f"insert into pet(nome,especie,raca,fk_cliente_cpf) values('{nome}','{especie}','{raca}','{cpf}')",conn)
		conn.commit()
		
		self.tk.destroy()
		
	def agendamento(self):
		#criando janela
		self.tk = Tk()
		self.tk['bg'] = '#FF5E6E'
		self.tk.title('AGENDAMENTO')
		self.tk.geometry('500x550')

		#criando titulo
		self.l7 = Label(self.tk,text='Agendamento',font='times 15',bg='#FF5E6E',fg='white',pady=20)
		self.l7.pack()
		
		#criando tabela
		colunas = ['cod_pet','nome','raca','especie']
		self.t = ttk.Treeview(self.tk,columns=colunas,show='headings')
		self.t.heading('cod_pet',text='Codigo do Pet')
		self.t.heading('nome',text='Nome')
		self.t.heading('raca',text='Raca')
		self.t.heading('especie',text='Especie')
		self.t.column('cod_pet',width=100)
		self.t.column('nome',width=100)
		self.t.column('raca',width=100)	
		self.t.column('especie',width=100)	
		self.t.pack()		
				
		#adicionando o titulo da sessao do consulta
		self.l13 = Label(self.tk,text='Dados da Consulta',font='times 15',fg='white',bg='#FF5E6E')
		self.l13.pack(pady=10)
		
		#widget do codigo do 
		self.c16 = Frame(self.tk,bg='#FF5E6E')
		self.c16.pack(pady=10)
		
		self.l16 = Label(self.c16,text='Codigo do pet:',bg='#FF5E6E')
		self.l16.pack(side=LEFT)
		
		self.e10 = Entry(self.c16,width=30)
		self.e10.pack()
		
		#widgets da data
		self.c14 = Frame(self.tk)
		self.c14['bg'] = '#FF5E6E'
		self.c14['pady'] = 10
		self.c14.pack()
	
		self.l14 = Label(self.c14,text='Data/Hora:',bg='#FF5E6E')
		self.l14.pack(side=LEFT)

		self.e9 = Entry(self.c14)
		self.e9['width'] = 30
		self.e9.pack()
		
		#adicionando botao
		self.c15 = Frame(self.tk)
		self.c15['bg'] = '#FF5E6E'
		self.c15['pady'] = 30
		self.c15.pack()

		self.b6 = Button(self.c15,text='Agendar Consulta')
		self.b6['command'] = self.agendar
		self.b6.pack()
		
		#preenchendo a tabela
		pets = pd.read_sql_query("select * from pet",conn)
		
		tabelinha = pd.read_sql_query(f"select cpf from cliente where email = '{email}'",conn)
		cpf = tabelinha.cpf.item()
		
		for i in range(len(pets)):
			if(cpf == pets['fk_cliente_cpf'][i]):
				self.t.insert('',END,values=[pets['cod_pet'][i],pets['nome'][i],pets['raca'][i],pets['especie'][i]])
					

	def agendar(self):
		cod_pet = self.e10.get()
		data_hora = self.e9.get()
		
		tabelinha = pd.read_sql_query(f"select cpf from cliente where email = '{email}'",conn)
		cpf = tabelinha.cpf.item()
		c.execute(f"insert into consulta(fk_veterinario_cpf,fk_pet_cod_pet,descricao,data_hora,preco) values('123',{cod_pet},null,'{data_hora}',null)",conn)
		conn.commit()
		
		self.tk.destroy()
		
	def visualizar(self):
		#criando janela
		self.tk = Tk()
		self.tk.title('VISUALIZAR AGENDAMENTOS')
		self.tk.geometry('700x500')
		self.tk['bg'] = '#FF5E6E'
		
		#criando titulo
		self.l1 = Label(self.tk,text='Visualizar Agendamentos',font='times 15',bg='#FF5E6E',fg='white',pady=20)
		self.l1.pack()
		
		#criando tabela
		colunas = ['codigo','cpf_cliente','data']
		self.t = ttk.Treeview(self.tk,columns=colunas,show='headings')
		self.t.heading('codigo',text='Codigo da Consulta')
		self.t.heading('cpf_cliente',text='CPF do Dono')
		self.t.heading('data',text='Data da Consulta')
		self.t.column('codigo',width=150)
		self.t.column('cpf_cliente',width=150)
		self.t.column('data',width=150)		
		self.t.pack()
		
		#criando sessao para desmarcar
		self.l1 = Label(self.tk,text='Desmarcar Consulta',font='times 15',bg='#FF5E6E',fg='white',pady=20)
		self.l1.pack()
		
		self.l2 = Label(self.tk,text='Digite o código da cosulta que deseja desmarcar:',bg='#FF5E6E',fg='white')
		self.l2.pack()
		
		self.e1 = Entry(self.tk,width=30)
		self.e1.pack()
		
		self.b1 = Button(self.tk,text='Desmarcar')
		self.b1['command'] = self.desmarcar
		self.b1.pack(pady=20)
		
		#preenchendo a tabela
		consultas = pd.read_sql_query("select * from consulta",conn)
		
		tabelinha = pd.read_sql_query(f"select cpf from cliente where email = '{email}'",conn)
		cpf = tabelinha.cpf.item()
		
		for i in range(len(consultas)):
			if(cpf == consultas['fk_pet_cpf_cliente'][i]):
				self.t.insert('',END,values=[consultas['cod_consulta'][i],consultas['fk_pet_cpf_cliente'][i],consultas['data_hora'][i]])
					
		
	def desmarcar(self):
		codigo = self.e1.get()
		c.execute(f"delete from consulta where cod_consulta = {codigo}",conn)
		conn.commit()

root = Tk()
root['bg'] = '#C56AFF'
Application(root)
root.geometry("300x350")
root.mainloop()

conn.close()

