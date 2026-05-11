from fastapi import FastAPI
import sqlite3
import random

app = FastAPI()

# Criar banco de dados ao iniciar o servidor
def init_db():
    conn = sqlite3.connect('wardrobe.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roupas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            cor TEXT NOT NULL,
            categoria TEXT NOT NULL,
            estilo TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Chamamos a função para garantir que o banco exista
init_db()

@app.get("/", tags=["Health Check"])
def home():
    """Verifica se a API está online."""
    return {"status": "Smart Wardrobe API Ativa"}

@app.post("/adicionar-roupa", tags=["Inventário"])
def add_item(item: str, cor: str, categoria: str, estilo: str):
    """Cadastra uma peça incluindo a nova coluna de estilo."""
    conn = sqlite3.connect('wardrobe.db')
    cursor = conn.cursor()
    # Adicionado 'estilo' no INSERT para bater com a estrutura da tabela
    cursor.execute(
        "INSERT INTO roupas (item, cor, categoria, estilo) VALUES (?, ?, ?, ?)", 
        (item, cor, categoria, estilo)
    )
    conn.commit()
    conn.close()
    return {"message": "Item adicionado com sucesso!"}

@app.get("/listar-roupas", tags=["Inventário"])
def listar_roupas():
    """Retorna todas as roupas para o Dashboard."""
    conn = sqlite3.connect('wardrobe.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, item, cor, categoria, estilo FROM roupas")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {"id": r[0], "item": r[1], "cor": r[2], "categoria": r[3], "estilo": r[4]} 
        for r in rows
    ]

@app.get("/sugerir-look", tags=["IA"])
def sugerir_look(clima: str, ocasiao: str):
    """Motor de IA que filtra por Estilo/Ocasião e Clima."""
    conn = sqlite3.connect('wardrobe.db')
    cursor = conn.cursor()
    
    # Filtra peças que correspondem à ocasião selecionada
    cursor.execute("SELECT item, cor FROM roupas WHERE estilo = ?", (ocasiao,))
    pecas = cursor.fetchall()
    conn.close()

    if len(pecas) < 2:
        return {"sugestao": f"Você precisa de pelo menos 2 peças de estilo '{ocasiao}' para uma sugestão completa."}

    # Seleção aleatória dentro do filtro de estilo
    look = random.sample(pecas, 2)
    
    conector = "perfeito para o frio" if clima == "Frio" else "ótimo para o dia"
    frase = f"Para um evento {ocasiao} e clima {clima}, que tal combinar seu {look[0][0]} {look[0][1]} com {look[1][0]} {look[1][1]}? É {conector}."
    
    return {"sugestao": frase}