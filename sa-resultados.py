import streamlit as st
import json
import plotly.graph_objects as go

#  Ativa o modo wide
st.set_page_config(layout="wide")

# ===============================
# FUNÇÕES PARA GERAR OS GRÁFICOS
# ===============================

def criar_grafico_horizonte(dados, num_iter, tipo_solucao):
    """
    Cria um gráfico de barras comparando as estratégias 'Aleatória' e 'Localizada'
    para um tipo de solução específico (média ou melhor).

    Args:
        dados (dict): dicionário com os dados carregados do json.
        num_iter (str): o número de iterações selecionado.
        tipo_solucao (str): 'media' para 'solucao media' ou 'melhor' para 'melhor solucao'.
    
    Returns:
        go.Figure: a figura do plotly pronta para ser exibida.
    """
    fig = go.Figure()
    anos = list(range(1, 17))
    
    # Chave do dicionário, títulos e cores
    if tipo_solucao == 'media':
        chave_dados = 'solucao media'
        titulo_grafico = f'Análise da Solução Média ({int(num_iter):,} Iterações)'
        cor_aleatoria = '#2c3e50'
        cor_localizada = "#f0cb13"
    else: # 'melhor'
        chave_dados = 'melhor solucao'
        titulo_grafico = f'Análise da Melhor Solução ({int(num_iter):,} Iterações)'
        cor_aleatoria = '#2c3e50'
        cor_localizada = '#f0cb13'

    # Barra para a Estratégia Aleatória
    fig.add_trace(go.Bar(
        x=anos,
        y=dados['aleatoria'][num_iter][chave_dados],
        name='Aleatória',
        marker_color=cor_aleatoria,
        hovertemplate='<b>Ano: %{x}</b><br>VPL: %{y:,.0f}<extra></extra>'
    ))
    
    # Barra para a Estratégia Localizada
    fig.add_trace(go.Bar(
        x=anos,
        y=dados['localizada'][num_iter][chave_dados],
        name='Localizada',
        marker_color=cor_localizada,
        hovertemplate='<b>Ano: %{x}</b><br>VPL: %{y:,.0f}<extra></extra>'
    ))

    # Linhas de limite
    fig.add_hline(y=140000, line_dash="solid", line_color="#C42B1A", line_width=2)
    fig.add_hline(y=160000, line_dash="solid", line_color="#C42B1A", line_width=2)

    # Layout do gráfico
    fig.update_layout(
        title={'text': titulo_grafico, 'x': 0.5, 'xanchor': 'center'},
        xaxis_title='Ano do Horizonte de Planejamento',
        yaxis_title='Valor Presente Líquido (VPL)',
        xaxis=dict(tickmode='linear', tick0=1, dtick=1, gridcolor='gray'),
        yaxis=dict(range=[120000, 170000], gridcolor='gray', tickformat=',.0f'),
        hovermode='x unified',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        barmode='group',
        margin=dict(t=80)
    )
    return fig

def criar_grafico_convergencia(dados_vpl, tipo_solucao):
    """
    Cria um gráfico de linhas mostrando a evolução do VPL para um tipo de solução.

    Args:
        dados_vpl (dict): dicionário com os dados de VPL.
        tipo_solucao (str): 'media' ou 'melhor'.

    Returns:
        go.Figure: a figura do plotly pronta para ser exibida.
    """
    fig = go.Figure()
    iteracoes = [5000, 10000, 25000, 50000]
    iter_labels = [f'{i:,}' for i in iteracoes]
    
    if tipo_solucao == 'media':
        chave_dados = 'solucao media'
        titulo_grafico = 'Evolução do VPL da Solução Média'
        cor_aleatoria = '#2c3e50'
        cor_localizada = '#f0cb13'
    else: # 'melhor'
        chave_dados = 'melhor solucao'
        titulo_grafico = 'Evolução do VPL da Melhor Solução'
        cor_aleatoria = '#2c3e50'
        cor_localizada = '#f0cb13'

    # Extração de dados
    vpl_aleat = [dados_vpl['aleatoria'][str(i)][chave_dados][0] for i in iteracoes]
    vpl_local = [dados_vpl['localizada'][str(i)][chave_dados][0] for i in iteracoes]

    # Linhas
    fig.add_trace(go.Scatter(x=iter_labels, y=vpl_aleat, mode='lines+markers', name='Aleatória', line=dict(color=cor_aleatoria, width=2.5), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=iter_labels, y=vpl_local, mode='lines+markers', name='Localizada', line=dict(color=cor_localizada, width=2.5), marker=dict(size=8)))
    
    # Layout
    fig.update_layout(
        title={'text': titulo_grafico, 'x': 0.5, 'xanchor': 'center'},
        xaxis_title='Número de Iterações',
        yaxis_title='Valor Presente Líquido (VPL) Total',
        xaxis=dict(gridcolor='gray', tickmode='array', tickvals=iteracoes, ticktext=iter_labels),
        yaxis=dict(gridcolor='gray', tickformat=',.0f'),
        hovermode='x unified',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=80)
    )
    return fig


# =======================
# INTERFACE DO STREAMLIT
# =======================

st.title("Simulated Annealing - Média e Melhor Solução")

# Carregar dados
try:
    with open('sa_resultados.json', 'r') as f:
        dados_resultados = json.load(f)
    with open('sa_vpl.json', 'r') as f:
        dados_vpl = json.load(f)

    # Abas
    tab1, tab2 = st.tabs(["Análise por Horizonte de Planejamento", "Análise por VPL Máximo"])

    with tab1:
        st.header("Comparativo do VPL Anual por Modelo de Análise")
        
        iter_option = st.selectbox(
            'Selecione o número de iterações para visualizar:',
            ('5000', '10000', '25000', '50000'),
            format_func=lambda x: f"{int(x):,} Iterações",
            key='selectbox_horizonte'
        )
        
        st.markdown("---")

        # Solução Média
        fig_media = criar_grafico_horizonte(dados_resultados, iter_option, 'media')
        st.plotly_chart(fig_media, use_container_width=True)

        st.markdown("---")
        
        # Melhor Solução
        fig_melhor = criar_grafico_horizonte(dados_resultados, iter_option, 'melhor')
        st.plotly_chart(fig_melhor, use_container_width=True)

    with tab2:
        st.header("Evolução do VPL Total por Número de Iterações")
        
        st.markdown("---")

        # Evolução da Solução Média
        fig_conv_media = criar_grafico_convergencia(dados_vpl, 'media')
        st.plotly_chart(fig_conv_media, use_container_width=True)
        
        st.markdown("---")

        # Evolução da Melhor Solução
        fig_conv_melhor = criar_grafico_convergencia(dados_vpl, 'melhor')
        st.plotly_chart(fig_conv_melhor, use_container_width=True)

except FileNotFoundError:
    st.error("Erro: Verifique se os arquivos 'sa_resultados.json' e 'sa_vpl.json' estão no mesmo diretório que o script.")
except Exception as e:
    st.error(f"Ocorreu um erro ao processar os arquivos: {e}")