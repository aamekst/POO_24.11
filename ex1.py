from sqlalchemy import create_engine, text, Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Session

# CONFIGURAR CONEXÃO COM BANCO DE DADOS SQLITE
# caso o arquivo de banco não exista, ele será criado
engine = create_engine("sqlite:///server.db")

with engine.connect() as connection:
    result = connection.execute(text('''CREATE TABLE IF NOT EXISTS FUNCIONARIO(
                      ID INTEGER PRIMARY KEY,
                      NOME VARCHAR(255),
                      IDADE INTEGER,
                      SALARIO FLOAT)''')
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
    if nome in ('sair', 'SAIR'):
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



print('-'*30)
print('com filtro')
resultado = session.query(Funcionario).filter(Funcionario.salario > 1500)      # Retorna uma lista de objetos
print('ID  NOME  IDADE  SALARIO')
for obj in resultado:
    print(obj.id, obj.nome, obj.idade, obj.salario)



connection.close()