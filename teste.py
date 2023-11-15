#banco de dados com python
#sqlalchemy
#se a tabela existe so faz o mapeamento da class existente no banco

# EXEMPLO UTILIZANDO SQLALCHEMY VERSÃO 2.0

# INSTALAR O MÓDULO SQLALCHEMY
# Executar no terminal o comando
# pip install sqlalchemy

# IMPORTAR MÓDULOS
from sqlalchemy import create_engine, text, Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Session

# CONFIGURAR CONEXÃO COM BANCO DE DADOS SQLITE
# caso o arquivo de banco não exista, ele será criado
engine = create_engine("sqlite:///server.db")

with engine.connect() as connection:
    result = connection.execute(text('''CREATE TABLE IF NOT EXISTS FUNCIONARIO(
                      ID INTEGER PRIMARY KEY,
                      NOME VARCHAR(255) NOT NULL,
                      IDADE INT NOT NULL,
                      SALARIO FLOAT NOT NULL)''')
             )
    
# INICIAR SESSÃO COM BANCO DE DADOS
session = Session(engine)

# CLASSE BASE DO SQLALCHEMY
class Base(DeclarativeBase):
    pass


# DEFINIÇÃO DE CLASSE QUE MAPEIA UMA TABELA
class Funcionario(Base):
    __tablename__ = 'FUNCIONARIO'
    id = Column('ID', Integer, primary_key=True)
    nome = Column('NOME', String(255))
    idade = Column('IDADE', Integer)
    salario = Column('SALARIO', Float)

    def __init__(self, nome, idade, salario):   # Método construtor da classe
        self.nome = nome
        self.idade = idade
        self.salario = salario


# -----------------------------------------------------------------------------
# INSERINDO DADOS NA TABELA

# Inserir uma lista de objetos
func1 = Funcionario('Luizinho', 22, 1250)
func2 = Funcionario('Huguinho', 22, 2200)
lista = [func1, func2]                  # lista de objetos
session.add_all(lista)                  # insere os dados de todos os objetos
session.commit()

# Inserir objetos cadastrados pelo usuário
lista = []
while True:
    nome = input('Informe o nome (Digite SAIR para finalizar): ')
    if nome == 'SAIR':
        break
    idade = int(input('Informe a idade: '))
    salario = float(input('Informe o salario: '))
    func = Funcionario(nome, idade, salario)
    lista.append(func)
session.add_all(lista)
session.commit()

# -----------------------------------------------------------------------------
# CONSULTANDO OS DADOS DA TABELA

# Consultar todos os dados
print('-'*30)
resultado = session.query(Funcionario)          # Retorna uma lista de objetos
for obj in resultado:
    print(obj.id, obj.nome, obj.idade, obj.salario)


# Consultar pela chave primária
print('-'*30)
obj = session.get(Funcionario, 1)        # Busca um objeto pela chave primária
if obj is not None:                            # Se não existir, retorna None
    print(obj.id, obj.nome, obj.idade, obj.salario)
else:
    print('Chave Primária Inexistente')

# Consultar utilizando filtros (salario maior que 1500)
print('-'*30)
resultado = session.query(Funcionario).filter(Funcionario.salario > 1500)
for obj in resultado:
    print(obj.id, obj.nome, obj.idade, obj.salario)


# Consultar utilizando filtros (salário maior que 1500 e idade igual a 22)
print('-'*30)
resultado = session.query(Funcionario).filter(Funcionario.salario > 1500, Funcionario.idade == 22)
for obj in resultado:
    print(obj.id, obj.nome, obj.idade, obj.salario)


# Consultar utilizando filtros e ordenação
print('-'*30)
resultado = session.query(Funcionario).filter(Funcionario.salario > 1500, Funcionario.idade == 22).order_by(Funcionario.nome)
for obj in resultado:
    print(obj.id, obj.nome, obj.idade, obj.salario)


# -----------------------------------------------------------------------------
# ALTERANDO DADOS


# Alterar um objeto
func = session.get(Funcionario, 1)        # Busca um funcionário pelo id
if func is not None:
    func.nome = 'Zezinho da Silva'              # Altera os atributos do objeto
    func.idade = 25
    session.commit()

# -----------------------------------------------------------------------------
# EXCLUINDO DADOS
# Excluir um objeto
func = session.get(Funcionario, 2)        # busca um funcionário pelo id
if func is not None:
    session.delete(func)
    session.commit()

# -----------------------------------------------------------------------------
# CONSULTANDO TODOS OS DADOS
print('-'*30)
resultado = session.query(Funcionario)             # retorna lista de objetos
for obj in resultado:
    print(obj.id, obj.nome, obj.idade, obj.salario)

# -----------------------------------------------------------------------------
# FECHANDO CONEXÃO COM BANCO DE DADOS
connection.close()