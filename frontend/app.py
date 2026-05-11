import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 1. Configuração e Estilo 
st.set_page_config(page_title="Smart Wardrobe Analytics", page_icon="👗", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F5F5DC; }
    h1, h2, h3 { color: #5D4037; }
    .stButton>button { background-color: #5D4037; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title(" Smart Wardrobe Analytics")

# 2. Organização 
tab1, tab2 = st.tabs(["✨ Gestão & IA", " Dashboard de Dados"])

with tab1:
    st.header("Gerenciar Guarda-Roupa")
    
    # --- SEÇÃO DE CADASTRO ---
    with st.expander("➕ Adicionar Nova Peça"):
        col1, col2 = st.columns(2)
        with col1:
            item = st.text_input("Peça", placeholder="Ex: Blazer")
            cor = st.text_input("Cor", placeholder="Ex: Bege")
        with col2:
            categoria = st.selectbox("Categoria", ["Blusas", "Calças", "Vestidos", "Sapatos", "Acessórios"])
            # Inclusão do campo Estilo com KEY única para evitar erro de ID duplicado
            estilo_cad = st.selectbox("Estilo", ["Casual", "Formal", "Trabalho", "Noite"], key="cad_estilo")
            
        if st.button("Salvar no Inventário"):
    # Criamos o dicionário de parâmetros
          payload = {"item": item, "cor": cor, "categoria": categoria, "estilo": estilo_cad}
    
    # Passamos o payload para o params
          res = requests.post("http://127.0.0.1:8000/adicionar-roupa", params=payload)
    
          if res.status_code == 200:
             st.success(f"{item} adicionado com sucesso!")
             st.rerun() # Comando para atualizar a página e o dashboard na hora
        else:
         st.error("Erro ao salvar o item.")

    st.divider()

    # --- SEÇÃO DO MOTOR DE IA ---
    st.subheader(" Motor de IA: Sugestão por Estilo")
    st.write("Sua produtividade intencional começa na escolha do look.")
    
    col_ia1, col_ia2 = st.columns(2)
    with col_ia1:
        clima_escolhido = st.selectbox("Como está o tempo?", ["Ensolarado", "Frio", "Chuvoso"], key="clima_ia")
    with col_ia2:
        ocasiao_escolhida = st.selectbox("Qual o evento?", ["Casual", "Formal", "Trabalho", "Noite"], key="ocasiao_ia")

    if st.button("Gerar Look Estratégico"):
        try:
            params = {"clima": clima_escolhido, "ocasiao": ocasiao_escolhida}
            res = requests.get("http://127.0.0.1:8000/sugerir-look", params=params)
            
            if res.status_code == 200:
                st.info(res.json()['sugestao'])
            else:
                st.warning("Nenhuma peça encontrada para essa combinação de estilo e ocasião.")
        except Exception:
            st.error("Erro na conexão: O servidor Backend está desligado.")

with tab2:
    st.header("Análise Estratégica do Inventário")
    
    try:
        response = requests.get("http://127.0.0.1:8000/listar-roupas")
        if response.status_code == 200 and response.json():
            df = pd.DataFrame(response.json())

            # KPIs Rápidos
            st.metric("Total de Peças no Closet", len(df))

            col_graf1, col_graf2 = st.columns(2)

            with col_graf1:
                st.subheader("Distribuição por Categoria")
                cores_minimalistas = ['#5D4037', '#8D6E63', '#D7CCC8', '#BCAAA4', '#EFEBE9']
                fig_rosca = px.pie(df, names='categoria', hole=0.4, 
                                   color_discrete_sequence=cores_minimalistas)
                st.plotly_chart(fig_rosca, use_container_width=True)

            with col_graf2:
                st.subheader("Paleta de Cores Frequentes")
                df_cores = df['cor'].value_counts().reset_index()
                fig_barras = px.bar(df_cores, x='cor', y='count',
                                   labels={'count':'Quantidade', 'cor':'Cores'},
                                   color_discrete_sequence=['#5D4037'])
                fig_barras.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_barras, use_container_width=True)
        else:
            st.warning("Seu inventário está vazio. Adicione peças na aba 'Gestão & IA'.")
    except Exception:
        st.error("Não foi possível carregar os dados. Verifique o servidor.")