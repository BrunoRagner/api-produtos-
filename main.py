

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deta import Deta



# Configuração do SDK de base da Deta
deta = Deta("b0aa59j8_suZLrKMJXxSCX4Uoacc2CohBNCyT8Cow")
db = deta.Base('produto')

# Configuração do FastAPI

app = FastAPI()
# Configura o CORS





# Modelo de dados do produto
class Produto(BaseModel):
    nome: str
    preco: float
    quantidade: int
    discriçao: str

#rota index
 



@app.get("/itens")
async def get_itens():
    result = await db.fetch()
    return result["produtos"]


# Rota para listar todos os produtos
@app.get('/produtos')
def listar_produtos():
    produtos = db.fetch()
    return produtos

# Rota para buscar um produto por ID
@app.get('/produtos/{id}')
def buscar_produto(id: int):
    produto = db.get(id)
    if not produto:
        raise HTTPException(status_code=404, detail='Produto não encontrado.')
    return produto

# Rota para criar um novo produto
@app.post('/produtos')
def criar_produto(produto: Produto):
    novo_produto = db.put(produto.dict())
    return novo_produto

# Rota para atualizar um produto
@app.put('/produtos/{id}')
def atualizar_produto(id: int, produto: Produto):
    produto_atualizado = db.update(produto.dict(), id)
    if not produto_atualizado:
        raise HTTPException(status_code=404, detail='Produto não encontrado.')
    return produto_atualizado

# Rota para deletar um produto
@app.delete('/produtos/{id}')
def deletar_produto(id: int):
    produto = db.delete(id)
    if not produto:
        raise HTTPException(status_code=404, detail='Produto não encontrado.')
    return {'mensagem': 'Produto deletado com sucesso.'}

# Inicia o servidor
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
