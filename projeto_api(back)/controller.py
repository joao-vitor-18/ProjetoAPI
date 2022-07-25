from hashlib import sha256
from secrets import token_hex
from fastapi import FastAPI
from models import Pessoa, Tokens, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 


def contecta():
    engine = create_engine("sqlite:///sqlite.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


app = FastAPI()

# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/cadastro")
def cadastro(user: str, email: str, senha: str):
    """
    Descrição:
        Essa função é resposavel pelo cadastro de novos usuários da base de dados.

        Parametros:
            user:
                Espere-se o nome de usuario a ser cadastrado
            email:
                Espare-se o email a ser cadastrado.
            senha:
                Espare-se uma senha com  digitos para ser cadastrada.

        Erros:
            0:
                Cadastro realizado com sucesso.
            1:
                Senha com menos de 6 digitos.
            2:
                Usuario já cadastrado no sistema
            3:
                Erro ao inserir na tabela
    """
    if len(senha) < 6:
        return {'erro': 1 }
    
    senha=sha256(senha.encode()).hexdigest()
    session = contecta()
    usuario = session.query(Pessoa).filter_by(email=email, senha=senha).all()

    if len(usuario) > 0:
        return {'erro':2}
        
    try:
        novo_usuario = Pessoa(usuario=user, email=email, senha=senha)
        session.add(novo_usuario)
        session.commit()
        return{'erro': 0}

    except Exception as e:
        return{'erro': 3}

@app.post('/login')
def login(email: str, senha: str):
    """
        Função que irá verificar o e-mail e senha do usuario e apartir disso gerar um novo token
        de acesso.

            Parametro:
                email: O e-mail cadastrado pelo usuario
                senha: A senha cadastrado pelo usuário.

            Retorno:
                Erro 1: Usuário ou senha inválidos.
                Erro 2: Erro interno do sistema.
                Erro 0: 
    """
    senha = sha256(senha.encode()).hexdigest()
    session = contecta()
    usuario = session.query(Pessoa).filter_by(email=email, senha=senha).all()
    if len(usuario) == 0:
        return {'erro':1} 
    else:
        while True:
            try:
                token = token_hex(50)
                tokensexist = session.query(Tokens).filter_by(token=token).all()
                if len(tokensexist) == 0:
                    pessoaexist = session.query(Tokens).filter_by(id_pessoa=usuario[0].id).all()
                    if len(pessoaexist) > 0:
                        pessoaexist[0].token = token
                        
                    else:
                        novotoken = Tokens(id_pessoa=usuario[0].id, token = token)
                        session.add(novotoken)
                    session.commit()
                    break
            except:
                return{'erro':2}
            
        return{'erro':0}
                
                
                    
            
            


if __name__ == "__main__":
    uvicorn.run('controller:app', port=5000, reload=True, access_log=False)