import streamlit as st
import numpy as np
import pandas as pd
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go

# --- Configuração da Página ---
st.set_page_config(page_title="Primos e Padrões Ultimate", layout="wide", page_icon="🧮")

# ==========================================
# ⚡ MOTOR DE CÁLCULO (CRIVO DE ERATÓSTENES)
# ==========================================
# Usamos st.cache_data para que o cálculo seja super rápido após a primeira vez
@st.cache_data(show_spinner=False)
def crivo_eratostenes(limite):
    """Gera todos os primos até ao limite usando o método mais rápido conhecido."""
    if limite < 2: return []
    # Cria uma lista de booleanos (True/False)
    e_primo = [True] * (limite + 1)
    e_primo[0] = e_primo[1] = False
    
    # O algoritmo do Crivo
    for p in range(2, int(limite**0.5) + 1):
        if e_primo[p]:
            # Marca todos os múltiplos de p como não primos
            for i in range(p * p, limite + 1, p):
                e_primo[i] = False
                
    # Retorna a lista de números que sobreviveram (True)
    return [p for p in range(limite + 1) if e_primo[p]]

# ==========================================
# 🌀 FUNÇÃO AUXILIAR: ESPIRAL DE ULAM
# ==========================================
@st.cache_data(show_spinner=False)
def gerar_coordenadas_ulam(n_pontos):
    """Gera as coordenadas (x,y) para uma espiral quadrada."""
    x, y = 0, 0
    dx, dy = 0, -1
    coords = [(0,0)] # Começa no centro (o número 1)
    
    for i in range(2, n_pontos + 1):
        if -x/2 < y <= x/2 and -y < x <= y: # Verifica se deve virar
            dx, dy = -dy, dx # Vira 90 graus à direita
        x, y = x + dx, y + dy
        coords.append((x, y))
    return np.array(coords)

# --- LÓGICA DE NAVEGAÇÃO ---
if 'iniciar' not in st.session_state: st.session_state['iniciar'] = False
if 'calculou' not in st.session_state: st.session_state['calculou'] = False
if 'dados_primos' not in st.session_state: st.session_state['dados_primos'] = {}

def mostrar_tela_inicial():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.write("")
        st.write("")
        try: st.image("logo_ua.png", width=150)
        except: st.write("### 🏛️ Universidade de Aveiro")

        st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>🧮 Primos e Padrões</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #D500F9;'>Edição Ultimate: Interativa & Performance</h3>", unsafe_allow_html=True)
        st.write("---")
        st.markdown("""
        <div style='text-align: center; font-size: 16px;'>
        Esta aplicação explora a profundidade matemática dos números primos com ferramentas avançadas.
        <br><br>
        <b>Novas Funcionalidades Premium:</b><br>
        ⚡ <b>Motor de Crivo:</b> Análise de milhões de primos em segundos.<br>
        📊 <b>Gráficos Interativos:</b> Zoom, seleção e detalhes (Plotly).<br>
        🌀 <b>Espiral de Ulam:</b> Visualização do caos ordenado.<br>
        🏁 <b>Viés de Chebyshev:</b> A "corrida" entre 6n-1 e 6n+1.
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.write("")

        c1, c2, c3 = st.columns([1, 2, 1]) 
        with c2:
            if st.button("Iniciar Investigação Avançada 🚀", type="primary", use_container_width=True):
                st.session_state['iniciar'] = True
                st.rerun()

        st.write("")
        st.markdown("""
        <div style='text-align: center; color: #b0b0b0; font-size: 12px;'>
        Projeto <b>TMFC</b> | Universidade de Aveiro<br>
        Catarina Mendes • Diogo Maria • Mateus Carmo • Micael Esteves<br>
        <i>Desenvolvido com apoio de IA</i>
        </div>
        """, unsafe_allow_html=True)

def mostrar_app_principal():
    # --- SIDEBAR ---
    try: st.sidebar.image("logo_ua.png", use_container_width=True)
    except: st.sidebar.markdown("### 🏛️ Universidade de Aveiro")

    st.sidebar.markdown("### ⚙️ Configuração de Alta Performance")
    if st.sidebar.button("🏠 Voltar à Capa"):
        st.session_state['iniciar'] = False
        st.rerun()
    st.sidebar.markdown("---")
    
    # --- INPUTS (Agora com limites muito maiores) ---
    st.sidebar.markdown("**Limite da Investigação:**")
    limite_n = st.sidebar.number_input(
        "Procurar primos até ao número (N):", 
        min_value=1000, 
        max_value=2000000, # Agora podemos ir até 2 MILHÕES!
        value=100000,      # Valor base mais alto
        step=50000,
        help="Graças ao novo Crivo, podemos analisar conjuntos de dados massivos."
    )
    
    st.sidebar.info(f"ℹ️ O motor está pronto para processar até **{limite_n:,}** números.".replace(",", "."))

    # --- CÁLCULO ULTRA-RÁPIDO ---
    if st.sidebar.button("Executar Crivo ⚡", type="primary"):
        with st.spinner(f'A crivar números até {limite_n:,}... Isto vai ser rápido!'):
            # 1. Obter todos os primos
            todos_primos = crivo_eratostenes(limite_n)
            
            # 2. Calcular Intervalos (Gaps)
            gaps = [todos_primos[i+1] - todos_primos[i] for i in range(len(todos_primos)-1)]
            x_gaps = todos_primos[:-1]
            
            # 3. Preparar dados para Chebyshev (Equipa 6n-1 vs 6n+1)
            # Ignoramos 2 e 3 para esta corrida
            primos_corrida = [p for p in todos_primos if p > 3]
            equipa_m1 = np.cumsum([1 if p % 6 == 5 else 0 for p in primos_corrida])
            equipa_p1 = np.cumsum([1 if p % 6 == 1 else 0 for p in primos_corrida])
            diferenca_corrida = equipa_m1 - equipa_p1

            # Guardar tudo na sessão
            st.session_state['dados_primos'] = {
                'lista': todos_primos,
                'gaps': gaps,
                'x_gaps': x_gaps,
                'limite': limite_n,
                'cheby_x': primos_corrida,
                'cheby_diff': diferenca_corrida
            }
            st.session_state['calculou'] = True
            
    st.sidebar.markdown("---")
    st.sidebar.caption("Projeto **TMFC** | UA")
    st.sidebar.caption("Autores: Catarina, Diogo, Mateus, Micael")

    st.title("🧮 Análise Avançada de Primos")
    
    if not st.session_state['calculou']:
        st.info("👈 Defina o limite na barra lateral e clique em **Executar Crivo** para libertar o poder matemático.")
        return

    # Recuperar dados
    dados = st.session_state['dados_primos']
    primelstlst = dados['lista']
    y_values = dados['gaps']
    x_values = dados['x_gaps']
    
    # Contagens rápidas
    gap_counts = Counter(y_values)
    dominio_do_6 = (gap_counts.get(6,0) > gap_counts.get(2,0)) and (gap_counts.get(6,0) > gap_counts.get(4,0))

    # --- NOVAS ABAS ---
    tab_dash, tab_ulam, tab_cheby, tab_expl, tab_sobre = st.tabs([
        "📉 Análise Visual (Plotly)", 
        "🌀 Espiral de Ulam", 
        "🏁 Viés de Chebyshev",
        "🔬 Dados", 
        "🎓 Teoria"
    ])

    # === TAB 1: DASHBOARD INTERATIVO ===
    with tab_dash:
        st.markdown("### 📊 Indicadores Globais (Alta Precisão)")
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1: st.metric("🔢 Primos Encontrados", f"{len(primelstlst):,}".replace(",", "."), border=True)
        with kpi2: st.metric("🔝 Maior Primo", f"{max(primelstlst):,}".replace(",", ".") if primelstlst else 0, border=True)
        with kpi3: st.metric("📏 Total de Intervalos", f"{len(y_values):,}".replace(",", "."), border=True)

        st.write("---")
        st.subheader("📍 Dispersão Interativa dos Primos")
        st.info("💡 **Dica:** Use o rato para fazer zoom, arrastar e passar por cima dos pontos para ver detalhes.")
        
        # Preparar DataFrame para Plotly
        df_scatter = pd.DataFrame({'Primo': x_values, 'Gap': y_values})
        # Criar coluna de cor para destacar o Gap 1
        df_scatter['Tipo'] = df_scatter['Gap'].apply(lambda x: 'Gap Único (1)' if x == 1 else 'Intervalo Normal')
        
        # Gráfico Plotly Scatter
        fig_scatter = px.scatter(
            df_scatter, x='Primo', y='Gap', color='Gap',
            color_continuous_scale='Spectral_r',
            hover_data=['Primo', 'Gap'],
            title="Mapa de Calor Interativo dos Intervalos"
        )
        # Adicionar destaque para o Gap 1 (Ponto Magenta Grande)
        df_gap1 = df_scatter[df_scatter['Gap'] == 1]
        fig_scatter.add_trace(go.Scatter(
            x=df_gap1['Primo'], y=df_gap1['Gap'],
            mode='markers',
            marker=dict(color='#D500F9', size=15, line=dict(width=2, color='black')),
            name='Gap Único (1)', showlegend=True
        ))
        fig_scatter.update_layout(height=500, yaxis_title="Tamanho do Intervalo", xaxis_title="Número Primo (p)")
        st.plotly_chart(fig_scatter, use_container_width=True)

        st.write("---")
        st.subheader("📊 Histograma Interativo")
        
        sorted_gaps = sorted(gap_counts.keys())
        # Filtro inteligente para o histograma não ficar ilegível com muitos dados
        max_gap_hist = st.slider("Filtrar Histograma até Intervalo:", 2, max(sorted_gaps) if sorted_gaps else 10, 50)
        
        filtered_gaps = [g for g in sorted_gaps if g <= max_gap_hist]
        filtered_counts = [gap_counts[g] for g in filtered_gaps]
        x_labels = [str(g) for g in filtered_gaps]
        colors = ['#D500F9' if g == '1' else '#4e79a7' for g in x_labels]

        fig_hist = go.Figure(data=[go.Bar(
            x=x_labels, y=filtered_counts,
            marker_color=colors, text=filtered_counts, textposition='auto'
        )])
        fig_hist.update_layout(title="Frequência dos Intervalos", xaxis_title="Tipo de Intervalo", yaxis_title="Quantidade")
        st.plotly_chart(fig_hist, use_container_width=True)

        if dominio_do_6:
             st.success("💡 **Observação:** O intervalo 6 domina. Veja a aba 'Teoria' para saber porquê.")

    # === TAB 2: ESPIRAL DE ULAM (NOVO!) ===
    with tab_dash:
       pass # Dummy to maintain order

    with tab_ulam:
        st.header("🌀 A Espiral de Ulam")
        st.markdown("""
        Em 1963, o matemático Stanislaw Ulam, aborrecido numa conferência, começou a desenhar números numa espiral. 
        Ao marcar os números primos, descobriu que eles tendem a alinhar-se em diagonais surpreendentes, sugerindo uma ordem oculta.
        """)
        
        # Limitar pontos para a espiral não ficar demasiado lenta
        limite_espiral = min(dados['limite'], 250000) 
        st.info(f"Visualizando a espiral até ao número {limite_espiral:,}. Zonas densas indicam padrões ricos em primos.")

        coords = gerar_coordenadas_ulam(limite_espiral)
        # Filtrar apenas as coordenadas que são números primos
        # O índice i na lista coords corresponde ao número i+1
        indices_primos = [p-1 for p in primelstlst if p <= limite_espiral]
        coords_primos = coords[indices_primos]
        
        df_ulam = pd.DataFrame(coords_primos, columns=['x', 'y'])
        df_ulam['Primo'] = [p for p in primelstlst if p <= limite_espiral]

        fig_ulam = px.scatter(
            df_ulam, x='x', y='y',
            hover_data=['Primo'],
            title=f"Visualização da Espiral de Ulam (N={limite_espiral})",
            color_discrete_sequence=['#D500F9'] # Cor magenta para destaque
        )
        fig_ulam.update_traces(marker=dict(size=3))
        fig_ulam.update_layout(
            height=700, 
            xaxis=dict(showgrid=False, zeroline=False, visible=False),
            yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
            plot_bgcolor='white'
        )
        st.plotly_chart(fig_ulam, use_container_width=True)

    # === TAB 3: VIÉS DE CHEBYSHEV (NOVO!) ===
    with tab_cheby:
        st.header("🏁 O Viés de Chebyshev: Uma Corrida Matemática")
        st.markdown("""
        Embora os primos das formas $6n-1$ e $6n+1$ devam ser igualmente frequentes no infinito, o matemático Pafnuty Chebyshev notou que, na prática, **a equipa $6n-1$ parece estar quase sempre à frente na contagem**.
        
        O gráfico abaixo mostra a diferença acumulada: (Contagem de $6n-1$) - (Contagem de $6n+1$). Se a linha estiver acima de zero, a equipa $6n-1$ está a ganhar.
        """)

        if len(dados['cheby_x']) > 0:
            df_cheby = pd.DataFrame({
                'Primo (p)': dados['cheby_x'],
                'Vantagem da Equipa 6n-1': dados['cheby_diff']
            })

            fig_cheby = px.line(
                df_cheby, x='Primo (p)', y='Vantagem da Equipa 6n-1',
                title="A Corrida dos Primos: (Primos tipo 6n-1) vs (Primos tipo 6n+1)",
                color_discrete_sequence=['#2E86C1']
            )
            # Adicionar uma linha vermelha no zero
            fig_cheby.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Empate")
            fig_cheby.update_layout(height=500, yaxis_title="Diferença Acumulada (Vantagem 6n-1)")
            st.plotly_chart(fig_cheby, use_container_width=True)

            st.info("""
            **Interpretação:** É extremamente raro a linha cruzar para baixo do zero. Isto mostra que os primos "preferem" ligeiramente a forma $6n-1$ nos números iniciais, um fenómeno profundo relacionado com a Hipótese de Riemann.
            """)
        else:
            st.warning("Não há dados suficientes para a corrida (necessário N > 3).")

    # === TAB 4: DADOS ===
    with tab_expl:
        st.header("🔬 Laboratório de Dados")
        # ... (Lógica de explorador similar à anterior, mas adaptada) ...
        # Simplificado para brevidade, focando nas novas features.
        st.write("Explore os dados brutos gerados pelo crivo.")
        col1, col2 = st.columns(2)
        with col1:
             csv_data = pd.DataFrame(primelstlst, columns=["Primos"]).to_csv(index=False).encode('utf-8')
             st.download_button("💾 Exportar Lista Completa (CSV)", csv_data, "primos_completo.csv", "text/csv", type='primary')
        with col2:
            st.dataframe(pd.DataFrame({"Primos Encontrados": primelstlst}), height=400, use_container_width=True)

    # === TAB 5: TEORIA ===
    with tab_sobre:
        st.header("🎓 Contexto Teórico Avançado")
        # ... (A explicação anterior sobre o 6n+/-1 e o intervalo 6 mantém-se aqui) ...
        st.markdown("""
        ### 📐 A Sequência 6n ± 1
        É crucial usar **ambas** as formas ($6n-1$ e $6n+1$) para encontrar todos os primos maiores que 3. Usar apenas uma delas ignoraria metade dos números primos existentes.
        
        ### 🌟 O Fenómeno do Intervalo 6
        O intervalo 6 é o mais comum porque 6 é o produto dos primeiros dois primos ($2 \\times 3$). Somar 6 a um primo é a forma "mais segura" de preservar a não-divisibilidade por 2 e 3, aumentando a probabilidade de encontrar outro primo.
        
        ---
        ### 🧠 Novos Conceitos Adicionados
        
        #### 1. O Crivo de Eratóstenes
        Um algoritmo antigo e eficiente para encontrar primos. Em vez de testar cada número, ele elimina sistematicamente os múltiplos de primos conhecidos (elimina os múltiplos de 2, depois os de 3, os de 5, etc.). O que sobra são os primos.
        
        #### 2. A Espiral de Ulam
        Demonstra visualmente que os números primos não são distribuídos de forma puramente aleatória. As linhas diagonais visíveis correspondem a polinómios quadráticos (como $n^2 - n + 41$) que geram primos com uma frequência invulgarmente alta.
        
        #### 3. O Viés de Chebyshev
        Embora os primos $6n-1$ (ex: 5, 11, 17) e $6n+1$ (ex: 7, 13, 19) devessem estar empatados no infinito, os primos da forma $6n-1$ tendem a ser mais numerosos no início. Isto acontece porque $6n-1$ nunca é um quadrado perfeito de um primo, enquanto $6n+1$ pode ser (ex: $7 \times 7 = 49 = 6 \times 8 + 1$). Essa ligeira "vantagem" estrutural acumula-se.
        """)
        st.write("---")
        st.caption("Investigação TMFC Ultimate | Catarina, Diogo, Mateus, Micael | Apoio Gemini AI")

# --- CONTROLADOR PRINCIPAL ---
if st.session_state['iniciar']: mostrar_app_principal()
else: mostrar_tela_inicial()


