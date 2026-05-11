# Smart Wardrobe Optimizer

Projeto Full Stack focado em **FashionTech** e **Produtividade Intencional**, desenvolvido como parte da especialização em IA e Ciência de Dados.

## Tecnologias Utilizadas

- **Backend:** FastAPI (Python) para criação de API REST.
- **Frontend:** Streamlit para interface de usuário e dashboards.
- **Banco de Dados:** SQLite para persistência de dados.
- **Data Viz:** Plotly e Pandas para análise do inventário.

## Metodologia Ágil (Scrum)

O projeto foi dividido em Sprints focadas em entregas de valor:

- **Sprint 0:** Setup de ambiente virtual com `uv`.
- **Sprint 1:** Arquitetura do Banco de Dados e API.
- **Sprint 2:** Integração com Frontend Minimalista.
- **Sprint 3:** Dashboard Analítico e Motor de IA.

## Como Executar:

1. Instalar dependências: `uv pip install -r requirements.txt`
2. Rodar Backend: `uvicorn backend.main:app --reload`
3. Rodar Frontend: `streamlit run frontend/app.py`
