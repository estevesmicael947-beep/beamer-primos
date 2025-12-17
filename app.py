import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter

# --- Configuração da Página ---
st.set_page_config(page_title="Primos e Padrões", layout="wide", page_icon="🧮")

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
            st.image("logo_ua.png", width=150)
        except:
            st.write("🏛️ **Universidade de Aveiro**")

        st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>🧮 Primos e Padrões</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: gray; font-weight: normal;'>A beleza matemática da sequência 6n ± 1</h4>", unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        st.write("")

        # --- BOTÃO DE AÇÃO ---
        c1, c2, c3 = st.columns([1, 2, 1]) 
        with c2:
            if st.button("Iniciar Investigação ⚡", type="primary", use_container_width=True):
                st.session_state['iniciar'] = True
                st.rerun()

        # --- CRÉDITOS ---
        st.write("")
        st.write("")
        st.write("")
        st.markdown("""
        <div style='text-align: center; color: #b0b0b0; font-size: 12px;'>
        Projeto <b>TMFC</b> | Universidade de Aveiro<br>
        Catarina Mendes • Diogo Maria • Mateus Carmo • Micael Esteves<br>
        <i>Desenvolvido com apoio do Gemini (AI)</i>
        </div>
        """, unsafe_allow_html=True)

def mostrar_app_principal():
    # --- SIDEBAR ---
    try:
        st.sidebar.image("logo_ua.png", use_container_width=True)
    except:
        st.sidebar.markdown("### 🏛️ Universidade de Aveiro")

    st.sidebar.markdown("### ⚙️ Parâmetros do Estudo")
    if st.sidebar.button("🏠 Voltar à Capa"):
        st.session_state['iniciar'] = False
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.caption("**Universidade de Aveiro**")
    st.sidebar.caption("Projeto **TMFC**")
    st.sidebar.caption("Autores: Catarina, Diogo, Mateus, Micael")
    st.sidebar.caption("*Com apoio do Gemini*")

    st.title("🧮 Análise de Padrões em Números Primos")
    
    # --- MEMÓRIA ---
    if 'primelstlst' not in st.session_state:
        st.session_state['primelstlst'] = []
    if 'calculou' not in st.session_state:
        st.session_state['calculou'] = False

    # --- INPUTS ---
    end = st.sidebar.number_input("Limite da sequência (n):", min_value=10, max_value=20000, value=500, step=50, help="Define até onde a sequência 6n é calculada.")

    # --- CÁLCULO ---
    if st.sidebar.button("Gerar Padrões ⚡", type="primary"):
        with st.spinner('A processar cálculos aritméticos...'):
            primelst = set({2, 3})
            
            def is_prime(num):
                if num < 2: return False
                for i in range(2, int(num**0.5) + 1):
                    if num % i == 0:
                        return False
                return True

            n = 1
            while n <= end:
                num = 6 * n - 1
                if is_prime(num): primelst.add(num)
                n += 1

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
        
        todos_intervalos = {}
        for x in range(len(primelstlst)-1):
            diff = primelstlst[x+1] - primelstlst[x]
            pair = (primelstlst[x], primelstlst[x+1])
            if diff not in todos_intervalos: todos_intervalos[diff] = []
            todos_intervalos[diff].append(pair)

        twins = todos_intervalos.get(2, [])
        fours = todos_intervalos.get(4, [])
        sixes = todos_intervalos.get(6, [])
        eights = todos_intervalos.get(8, [])
        tens = todos_intervalos.get(10, [])

        y_values = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
        x_values = primelstlst[:-1]

        dominio_do_6 = (len(sixes) > len(twins)) and (len(sixes) > len(fours))

        # --- ABAS ---
        tab_dash, tab_expl, tab_sobre = st.tabs(["📉 Análise Visual", "🔬 Laboratório de Dados", "🎓 Teoria Matemática"])

        # === TAB 1: PAINEL DE ANÁLISE ===
        with tab_dash:
            st.markdown("### 📊 Indicadores Globais")
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1: st.metric("🔢 Primos Identificados", len(primelstlst), border=True)
            with kpi2: st.metric("🔝 Maior Primo (Max)", max(primelstlst) if primelstlst else 0, border=True)
            with kpi3: st.metric("📏 Total de Intervalos", len(primelstlst)-1 if len(primelstlst) > 1 else 0, border=True)

            st.markdown("#### Distribuição dos Intervalos:")
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Gémeos (Intervalo 2)", len(twins))
            col2.metric("Primos (Intervalo 4)", len(fours))
            col3.metric("Sexy (Intervalo 6)", len(sixes))
            col4.metric("Intervalo 8", len(eights))
            col5.metric("Intervalo 10", len(tens))

            st.write("---")

            if len(primelstlst) > 2:
                st.subheader("📍 Dispersão dos Primos")
                st.info("""
                **Legenda do Gráfico:**
                * **Eixo X ($p$):** A posição na linha dos números.
                * **Eixo Y (Intervalo):** A distância até ao próximo primo.
                * 🎨 **Cor:** Azul (Intervalos comuns) ➝ Vermelho (Intervalos raros).
                """)
                
                max_y_zoom = st.slider("Zoom Vertical (Eixo Y):", min_value=6, max_value=max(y_values) if y_values else 100, value=30, step=2)
                
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
                cbar.set_label('Tamanho do Intervalo')
                
                ticks_y = np.arange(2, max_y_zoom + 4, 2)
                ax.set_yticks(ticks_y)
                ax.set_ylim(0, max_y_zoom + 2)
                ax.grid(True, axis='y', linestyle='-', linewidth=0.5, alpha=0.3, color='gray')
                ax.set_xlabel("Número Primo ($p$)", fontsize=11)
                ax.set_ylabel("Distância ao próximo primo (Intervalo)", fontsize=11)
                ax.set_title(f"Mapa de Calor dos Intervalos (Zoom até {max_y_zoom})", fontsize=13)
                ax.set_xlim(0, max(x_values))
                st.pyplot(fig)

                st.write("---")
                st.subheader("📊 Histograma de Frequências")
                st.markdown("Comparação da quantidade de vezes que cada intervalo ocorre.")
                
                gap_counts = Counter(y_values)
                sorted_gaps = sorted(gap_counts.keys())
                
                filtered_gaps = [g for g in sorted_gaps if g <= max_y_zoom]
                filtered_counts = [gap_counts[g] for g in filtered_gaps]
                x_labels = [str(g) for g in filtered_gaps]

                fig2, ax2 = plt.subplots(figsize=(12, 4))
                bars = ax2.bar(x_labels, filtered_counts, color='#4e79a7', edgecolor='black', alpha=0.7, width=0.6)
                
                ax2.set_xlabel("Tipo de Intervalo")
                ax2.set_ylabel("Frequência")
                ax2.set_title("Dominância dos Intervalos")
                ax2.grid(axis='y', linestyle='--', alpha=0.5)
                
                for bar in bars:
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}',
                            ha='center', va='bottom', fontsize=9)
                
                st.pyplot(fig2)

                if dominio_do_6:
                    with st.container(border=True):
                        st.markdown("""
                        ### 💡 Observação Matemática Detetada
                        **O intervalo 6 é o mais frequente.**
                        Isto não é coincidência. Consulte a aba **'🎓 Teoria Matemática'** para entender por que razão o 6 "vence" o 2 e o 4.
                        """)

        # === TAB 2: EXPLORADOR ===
        with tab_expl:
            st.header("🔬 Laboratório de Dados")
            col_left, col_right = st.columns([1, 2])
            
            with col_left:
                st.markdown("### 1. Filtragem")
                gaps_disponiveis = sorted(todos_intervalos.keys())
                if not gaps_disponiveis:
                    st.warning("Aguardando cálculos.")
                else:
                    gap_escolhido = st.selectbox("Selecione o Intervalo para investigar:", options=gaps_disponiveis)
                    qtd_encontrada = len(todos_intervalos[gap_escolhido])
                    st.success(f"Foram isolados **{qtd_encontrada}** pares com Intervalo **{gap_escolhido}**.")
                    
                    st.markdown("---")
                    st.markdown("### 2. Exportação")
                    csv_data = pd.DataFrame(primelstlst, columns=["Números Primos"]).to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="💾 Exportar Conjunto de Dados (CSV)",
                        data=csv_data,
                        file_name='dataset_primos.csv',
                        mime='text/csv',
                        type='primary'
                    )

            with col_right:
                st.markdown(f"### 📋 Resultados: Intervalo {gap_escolhido}")
                dados_pares = todos_intervalos[gap_escolhido]
                df_pares = pd.DataFrame(dados_pares, columns=["Primo A", "Primo B"])
                df_pares.index = df_pares.index + 1
                st.dataframe(df_pares, height=500, use_container_width=True)

        # === TAB 3: SOBRE ===
        with tab_sobre:
            st.header("🎓 Contexto Teórico")
            st.markdown("""
            Projeto desenvolvido para a unidade curricular **TMFC (Teoria Matemática)** na Universidade de Aveiro.
            
            ### 📐 A Sequência 6n ± 1
            Todos os números primos ($p > 3$) residem na forma $6n - 1$ ou $6n + 1$.
            Isto deve-se à aritmética modular: qualquer inteiro $z$ pode ser escrito como $6n + k$. Ao eliminarmos os múltiplos de 2 e 3, restam apenas os resíduos 1 e 5.
            
            ---
            """)

            if dominio_do_6:
                with st.container(border=True):
                    st.markdown("""
                    ### 🌟 O Fenómeno do Intervalo 6
                    A análise gráfica revelou que o intervalo 6 aparece mais vezes que o 2 ou o 4. Eis a explicação lógica:

                    Para um número ser Primo, ele tem de passar dois "filtros": **não ser divisível por 2** e **não ser divisível por 3**.
                    """)
                    
                    st.markdown("""
                    
                    """)

                    st.markdown("""
                    * **O Número 6:** É o produto perfeito destes filtros ($2 \\times 3 = 6$).
                    * **A "Segurança" do 6:** Ao somarmos 6 a um número primo, **mantemos as propriedades** de resto dele. Se ele já passou nos filtros do 2 e do 3, o novo número também passará (ao contrário de somar 2 ou 4, que pode criar um múltiplo de 3).
                    
                    **Conclusão:** Somar 6 é o caminho estatisticamente "mais limpo" para encontrar o próximo primo.
                    """)
            
            st.markdown("""
            ### 📚 Glossário de Intervalos
            * **Primos Gémeos:** $p, p+2$ (ex: 11, 13).
            * **Primos Primos:** $p, p+4$ (ex: 7, 11).
            * **Primos Sexy:** $p, p+6$ (ex: 5, 11) - o nome vem do latim *sex* (seis).
            """)
            st.write("---")
            st.caption("Investigação realizada por: Catarina Mendes, Diogo Maria, Mateus Carmo e Micael Esteves | Com apoio do Gemini.")

    else:
        st.info("👈 Defina o valor de **n** na barra lateral e clique em **Gerar Padrões** para iniciar.")

# --- CONTROLADOR PRINCIPAL ---
if st.session_state['iniciar']:
    mostrar_app_principal()
else:
    mostrar_tela_inicial()
