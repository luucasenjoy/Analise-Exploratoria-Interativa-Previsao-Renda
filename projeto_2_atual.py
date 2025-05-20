import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Análise de Renda Interativa",
    page_icon="💰",
    layout="wide",
)

st.title("📊 Análise Exploratória Interativa da Previsão de Renda")

# Carregar dados
renda = pd.read_csv('previsao_de_renda.csv')

# Converter data_ref para datetime
if not pd.api.types.is_datetime64_any_dtype(renda['data_ref']):
    renda['data_ref'] = pd.to_datetime(renda['data_ref'])

# Lista das colunas categóricas que vamos usar para filtro e gráficos
categorical_cols = ['posse_de_imovel', 'posse_de_veiculo', 'qtd_filhos', 
                    'tipo_renda', 'educacao', 'estado_civil', 'tipo_residencia']

# Sidebar - filtros interativos
st.sidebar.header("Filtros")

filtros = {}
for col in categorical_cols:
    opcoes = renda[col].dropna().unique().tolist()
    selecao = st.sidebar.multiselect(f"Selecionar {col.replace('_',' ').title()}:", options=opcoes, default=opcoes)
    filtros[col] = selecao

# Aplicar filtros nos dados
mask = pd.Series(True, index=renda.index)
for col, valores in filtros.items():
    mask &= renda[col].isin(valores)

df_filtrado = renda[mask]

# === Gráficos ao longo do tempo ===
st.header("📈 Renda ao Longo do Tempo por Categorias")

for col in categorical_cols:
    fig = px.line(df_filtrado, x='data_ref', y='renda', color=col,
                  title=f'Renda ao longo do tempo por {col.replace("_", " ").title()}',
                  labels={'data_ref':'Data', 'renda':'Renda', col: col.replace('_', ' ').title()},
                  height=400)
    fig.update_layout(legend_title_text=col.replace('_', ' ').title())
    st.plotly_chart(fig, use_container_width=True)

# === Gráficos Bivariada ===
st.header("📊 Média da Renda por Categoria")

for col in categorical_cols:
    media_renda = df_filtrado.groupby(col)['renda'].mean().reset_index()
    fig = px.bar(media_renda, x=col, y='renda',
                 title=f'Média da Renda por {col.replace("_", " ").title()}',
                 labels={col: col.replace('_', ' ').title(), 'renda': 'Média da Renda'},
                 height=400)
    st.plotly_chart(fig, use_container_width=True)
