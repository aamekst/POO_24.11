from sqlalchemy import create_engine, text, Column, Integer, String, Float
from sqlalchemy.orm import DeclarativeBase, Session

# CONFIGURAR CONEXÃO COM BANCO DE DADOS SQLITE
# caso o arquivo de banco não exista, ele será criado
engine = create_engine("sqlite:///service.db")

with engine.connect() as connection:
    result = connection.execute(text("""CREATE TABLE IF NOT EXISTS AUTOR(
           ID INTEGER PRIMARY KEY,
           NOME varchar(255))"""))
    
with engine.connect() as connection:
    result = connection.execute(text("""CREATE TABLE IF NOT EXISTS LIVRO(
           ID INTEGER PRIMARY KEY,
           TITULO VARCHAR(255),
           PAGINAS INT,
           AUTOR_ID INT)"""))


    

session = Session(engine)


class Base(DeclarativeBase):
    pass


class Autor(Base):
    __tablename__ = 'AUTOR'
    id = Column('ID', Integer, primary_key=True)
    nome = Column('NOME', String(255))

    def __init__(self, nome):   
        self.nome = nome

class Livro(Base):
    __tablename__ = 'LIVRO'
    id = Column('ID', Integer, primary_key=True)
    titulo = Column('TITULO', String(255))
    paginas = Column('PAGINAS', Integer)
    autor_id = Column('AUTOR_ID', Integer)

    def __init__(self, titulo,paginas, autor_id):
        self.titulo=titulo
        self.paginas=paginas
        self.autor_id=autor_id
     

autor1 = Autor('Paulo coelho')
autor2 = Autor('Machado de assi')
autores = [autor1, autor2]  
session.add_all(autores)                  #
session.commit()

livro1 = Livro('Alquimista', 300, autor1.id)
livro2 = Livro('seleção', 180, autor2.id)
livros = [livro1, livro2]                  
session.add_all(livros)                  #
session.commit()


print('-'*30)
resultado = session.query(Livro, Autor).filter(Livro.id == Autor.id)
print('ID  TITULO     PAGINAS    AUTOR_ID    NM_AUTOR')       
for obj in resultado:
    print(f'{obj.Livro.id}  {obj.Livro.titulo:10} {obj.Livro.paginas:8} {obj.Livro.autor_id:8}        {obj.Autor.nome:8}' )



connection.close()