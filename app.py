import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter

# --- Configuração da Página ---
st.set_page_config(page_title="Primos e Padrões", layout="wide")

# --- LÓGICA DE NAVEGAÇÃO (TELA INICIAL vs APP) ---
if 'iniciar' not in st.session_state:
    st.session_state['iniciar'] = False

def mostrar_tela_inicial():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("")
        st.write("")
        
        # --- LOGO LOCAL ---
        try:
            st.image("logo_ua.png", width=200)
        except:
            st.write("### 🏛️ Universidade de Aveiro")
            st.caption("(Imagem 'logo_ua.png' não encontrada)")
        
        st.markdown("<h1 style='text-align: center;'>🌌 Primos e Padrões</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Uma jornada visual pela matemática</h3>", unsafe_allow_html=True)
        st.write("---")
        st.markdown("""
        <div style='text-align: center; font-size: 18px;'>
        Esta aplicação foi desenhada para explorar a beleza oculta dos números primos.
        <br><br>
        <b>Funcionalidades:</b><br>
        ✨ Geração de sequências <b>6n ± 1</b><br>
        📊 Histograma de Frequências (Novo)<br>
        🔭 Gráficos com coloração dinâmica<br>
        💾 Exportação de Dados
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        
        cols_btn = st.columns([1, 1, 1])
        if cols_btn[1].button("Começar a Explorar 🚀", type="primary", use_container_width=True):
            st.session_state['iniciar'] = True
            st.rerun()

        # --- CRÉDITOS ---
        st.write("")
        st.write("")
        st.markdown("""
        <div style='text-align: center; color: grey; font-size: 14px; margin-top: 30px;'>
        <b>Universidade de Aveiro</b><br>
        App desenvolvida no âmbito de <b>TMFC</b> por:<br>
        <b>Catarina Mendes, Diogo Maria, Mateus Carmo e Micael Esteves</b><br>
        <i>com ajuda do Gemini</i>
        </div>
        """, unsafe_allow_html=True)

def mostrar_app_principal():
    # --- SIDEBAR ---
    try:
        st.sidebar.image("logo_ua.png", use_container_width=True)
    except:
        st.sidebar.markdown("### 🏛️ Universidade de Aveiro")

    st.sidebar.markdown("### ⚙️ Configurações")
    if st.sidebar.button("🏠 Voltar ao Início"):
        st.session_state['iniciar'] = False
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.caption("**Universidade de Aveiro**")
    st.sidebar.caption("No âmbito de **TMFC**")
    st.sidebar.caption("Por: Catarina Mendes, Diogo Maria, Mateus Carmo e Micael Esteves")

    st.title("🔍 Análise de Padrões em Números Primos")
    
    # --- MEMÓRIA ---
    if 'primelstlst' not in st.session_state:
        st.session_state['primelstlst'] = []
    if 'calculou' not in st.session_state:
        st.session_state['calculou'] = False

    # --- INPUTS ---
    st.sidebar.header("Parâmetros")
    end = st.sidebar.number_input("Ordem final da sequência (n):", min_value=10, max_value=20000, value=500, step=50)

    # --- CÁLCULO ---
    if st.sidebar.button("Calcular 🚀"):
        with st.spinner('A processar números primos e a gerar estatísticas...'):
            primelst = set({2, 3})
            
            # Função de verificação otimizada
            def is_prime(num):
                if num < 2: return False
                for i in range(2, int(num**0.5) + 1):
                    if num % i == 0:
                        return False
                return True

            # Sequência 6n - 1
            n = 1
            while n <= end:
                num = 6 * n - 1
                if is_prime(num): primelst.add(num)
                n += 1

            # Sequência 6n + 1
            n = 1    
            while n <= end:
                num = 6 * n + 1
                if is_prime(num): primelst.add(num)
                n += 1
            
            st.session_state['primelstlst'] = sorted(list(primelst))
            st.session_state['calculou'] = True

    # --- VISUALIZAÇÃO ---
    if st.session_state['calculou']:
        primelstlst = st.session_state['primelstlst']
        
        # Dicionário de Intervalos
        todos_intervalos = {}
        for x in range(len(primelstlst)-1):
            diff = primelstlst[x+1] - primelstlst[x]
            pair = (primelstlst[x], primelstlst[x+1])
            if diff not in todos_intervalos: todos_intervalos[diff] = []
            todos_intervalos[diff].append(pair)

        # Dados para as métricas
        twins = todos_intervalos.get(2, [])
        fours = todos_intervalos.get(4, [])
        sixes = todos_intervalos.get(6, [])
        eights = todos_intervalos.get(8, [])
        tens = todos_intervalos.get(10, [])

        # Preparar dados do gráfico (Gaps)
        y_values = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
        x_values = primelstlst[:-1]

        # --- CRIAÇÃO DOS TABS ---
        tab_dash, tab_expl, tab_sobre = st.tabs(["📊 Dashboard", "📂 Explorador", "ℹ️ Sobre o Projeto"])

        # === TAB 1: DASHBOARD ===
        with tab_dash:
            # 1. Métricas Principais
            st.subheader("Estatísticas Gerais")
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1: st.metric("🔢 Total de Primos", len(primelstlst), border=True)
            with kpi2: st.metric("🔝 Maior Primo Encontrado", max(primelstlst) if primelstlst else 0, border=True)
            with kpi3: st.metric("📏 Total de Intervalos", len(primelstlst)-1 if len(primelstlst) > 1 else 0, border=True)

            st.markdown("#### Contagem por Tipo de Intervalo (Gap):")
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Gémeos (Gap 2)", len(twins))
            col2.metric("Primos (Gap 4)", len(fours))
            col3.metric("Sexy (Gap 6)", len(sixes))
            col4.metric("Gap 8", len(eights))
            col5.metric("Gap 10", len(tens))

            st.write("---")

            if len(primelstlst) > 2:
                # 2. Gráfico de Dispersão (Scatter Plot)
                st.subheader("📈 Distribuição e Intensidade dos Intervalos")
                st.info("""
                **Como ler este gráfico:**
                * **Eixo X:** Número primo atual.
                * **Eixo Y e Cor:** Tamanho do salto para o próximo primo.
                * 🔵 **Azul/Roxo:** Intervalos pequenos (comuns).
                * 🔴 **Vermelho:** Intervalos grandes (raros).
                """)
                
                max_y_zoom = st.slider("Altura Máxima do Eixo Y (Zoom):", min_value=6, max_value=max(y_values) if y_values else 100, value=30, step=2)
                
                fig, ax = plt.subplots(figsize=(12, 6))
                
                scatter_plot = ax.scatter(
                    x_values, 
                    y_values, 
                    s=30, 
                    c=y_values, 
                    cmap='Spectral_r', 
                    marker='o', 
                    alpha=0.9, 
                    edgecolors='black', 
                    linewidth=0.4
                )
                
                cbar = plt.colorbar(scatter_plot, ax=ax)
                cbar.set_label('Tamanho do Intervalo (Gap)')
                
                ticks_y = np.arange(2, max_y_zoom + 4, 2)
                ax.set_yticks(ticks_y)
                ax.set_ylim(0, max_y_zoom + 2)
                ax.grid(True, axis='y', linestyle='-', linewidth=0.5, alpha=0.3, color='gray')
                ax.set_xlabel("Número Primo ($p$)", fontsize=11)
                ax.set_ylabel("Tamanho do Intervalo (Gap)", fontsize=11)
                ax.set_title(f"Padrão dos Intervalos (Focando nos gaps até {max_y_zoom})", fontsize=13)
                ax.set_xlim(0, max(x_values))
                st.pyplot(fig)

                # 3. Histograma de Frequências
                st.write("---")
                st.subheader("📊 Frequência dos Intervalos")
                st.markdown("Este gráfico mostra **quais intervalos aparecem mais vezes**. Nota como os múltiplos de 6 são dominantes.")
                
                gap_counts = Counter(y_values)
                sorted_gaps = sorted(gap_counts.keys())
                
                filtered_gaps = [g for g in sorted_gaps if g <= max_y_zoom]
                filtered_counts = [gap_counts[g] for g in filtered_gaps]

                fig2, ax2 = plt.subplots(figsize=(12, 4))
                bars = ax2.bar(filtered_gaps, filtered_counts, color='#4e79a7', edgecolor='black', alpha=0.7, width=1.5)
                
                ax2.set_xlabel("Tamanho do Intervalo (Gap)")
                ax2.set_ylabel("Quantidade Encontrada")
                ax2.set_title("Histograma de Frequência dos Intervalos")
                ax2.set_xticks(filtered_gaps)
                ax2.grid(axis='y', linestyle='--', alpha=0.5)
                
                for bar in bars:
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}',
                            ha='center', va='bottom', fontsize=9)
                
                st.pyplot(fig2)


        # === TAB 2: EXPLORADOR ===
        with tab_expl:
            st.header("📂 Explorador de Dados")
            
            col_left, col_right = st.columns([1, 2])
            
            with col_left:
                st.markdown("### 1. Filtrar")
                gaps_disponiveis = sorted(todos_intervalos.keys())
                if not gaps_disponiveis:
                    st.warning("Sem dados.")
                else:
                    gap_escolhido = st.selectbox("Escolhe o tamanho do intervalo (Gap):", options=gaps_disponiveis)
                    qtd_encontrada = len(todos_intervalos[gap_escolhido])
                    st.success(f"Encontrados **{qtd_encontrada}** pares com Gap **{gap_escolhido}**.")
                    
                    st.markdown("---")
                    st.markdown("### 2. Exportar")
                    csv_data = pd.DataFrame(primelstlst, columns=["Números Primos"]).to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="💾 Baixar Lista de Primos (CSV)",
                        data=csv_data,
                        file_name='numeros_primos.csv',
                        mime='text/csv',
                        type='primary'
                    )

            with col_right:
                st.markdown("### Visualização")
                st.write(f"**Tabela de pares com diferença {gap_escolhido}:**")
                dados_pares = todos_intervalos[gap_escolhido]
                df_pares = pd.DataFrame(dados_pares, columns=["Primo 1", "Primo 2"])
                df_pares.index = df_pares.index + 1
                st.dataframe(df_pares, height=500, use_container_width=True)

        # === TAB 3: SOBRE ===
        with tab_sobre:
            st.header("ℹ️ Sobre este Projeto")
            st.markdown("""
            Este projeto foi desenvolvido no âmbito da unidade curricular **TMFC** na **Universidade de Aveiro**.
            
            ### O Fundamento Matemático: 6n ± 1
            Todos os números primos maiores que 3 podem ser escritos na forma $6n - 1$ ou $6n + 1$.
            Isto acontece porque qualquer número inteiro pode ser escrito como $6n + k$, onde $k \in \{0, 1, 2, 3, 4, 5\}$.
            * Se $k = 0, 2, 4$, o número é par (divisível por 2).
            * Se $k = 3$, o número é divisível por 3.
            * Logo, restam apenas as opções **$k=1$** e **$k=5$** (que equivale a $-1$).
            
            ---
            ### 🌟 Porquê tantos primos com intervalo de 6?
            Observamos no histograma que o intervalo **6** é extremamente comum (mais que 2 ou 4). Isto é explicado matematicamente:
            
            1.  **Divisibilidade:** O número 6 é o produto dos dois primeiros primos ($2 \\times 3$).
            2.  **O "Filtro" dos Primos:** Para um número ser primo, não pode ser divisível por 2 nem por 3.
            3.  **A vantagem do 6:** * Se tivermos um primo $p$ (que não é divisível por 2 nem por 3), então $p+6$ mantém as mesmas propriedades de resto. 
                * Ou seja, somar 6 **não altera a paridade nem a divisibilidade por 3**.
                * Somar 2 ou 4 pode facilmente fazer cair num múltiplo de 3, eliminando a possibilidade de ser primo.
            
            Por isso, é "mais fácil" encontrar pares separados por 6 (Primos Sexy) do que por outros números pequenos.
            
            ---
            ### Glossário de Intervalos
            * **Primos Gémeos:** Diferença de 2 (ex: 11, 13).
            * **Primos Primos:** Diferença de 4 (ex: 7, 11).
            * **Primos Sexy:** Diferença de 6 (ex: 5, 11). O nome vem do latim *sex* (seis).
            """)
            st.write("---")
            st.caption("Autores: Catarina Mendes, Diogo Maria, Mateus Carmo e Micael Esteves.")

    else:
        st.info("👈 Para começar, define o valor de **n** na barra lateral e clica em **Calcular**.")

# --- CONTROLADOR PRINCIPAL ---
if st.session_state['iniciar']:
    mostrar_app_principal()
else:
    mostrar_tela_inicial()
