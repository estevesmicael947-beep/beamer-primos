import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

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
        st.markdown("<h1 style='text-align: center;'>🌌 Primos e Padrões</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Uma jornada visual pela matemática</h3>", unsafe_allow_html=True)
        st.write("---")
        st.markdown("""
        <div style='text-align: center; font-size: 18px;'>
        Esta aplicação foi desenhada para explorar a beleza oculta dos números primos.
        <br><br>
        <b>O que vais encontrar:</b><br>
        ✨ Geração de sequências <b>6n ± 1</b><br>
        📊 Estatísticas detalhadas de intervalos<br>
        🔭 Gráficos interativos com <b>coloração dinâmica</b><br>
        📂 Explorador de dados
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
    # Valor default bom para ver o efeito das cores
    end = st.sidebar.number_input("Ordem final da sequência (n):", min_value=10, max_value=10000, value=500, step=50)

    # --- CÁLCULO ---
    if st.sidebar.button("Calcular 🚀"):
        with st.spinner('A processar números primos...'):
            primelst = set({2, 3})
            # Sequência 6n - 1
            n = 1
            while n <= end:
                num = 6 * n - 1
                y = 2
                while y < num:
                    if num % y == 0: break
                    else: y += 1
                if y == num: primelst.add(num)
                n += 1
            # Sequência 6n + 1
            n = 1    
            while n <= end:
                num = 6 * n + 1
                y = 2
                while y < num:
                    if num % y == 0: break
                    else: y += 1
                if y == num: primelst.add(num)
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

        twins = todos_intervalos.get(2, [])
        fours = todos_intervalos.get(4, [])
        sixes = todos_intervalos.get(6, [])
        eights = todos_intervalos.get(8, [])
        tens = todos_intervalos.get(10, [])

        # --- PARTE 1: ESTATÍSTICAS ---
        st.subheader("📊 Estatísticas Gerais")
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

        # --- PARTE 2: O GRÁFICO COM COLORAÇÃO DINÂMICA ---
        if len(primelstlst) > 2:
            st.subheader("📈 Distribuição e Intensidade dos Intervalos")

            st.info("""
            **Como ler este gráfico:**
            * **Eixo X (Horizontal):** O número primo onde estás.
            * **Eixo Y (Vertical) e Cor:** Indicam o tamanho do salto para o próximo primo.
            * 🔵 **Azul/Roxo:** Intervalos pequenos e comuns (ex: 2, 4, 6).
            * 🔴 **Vermelho/Laranja:** Intervalos grandes e raros ("desertos" de primos).
            """)
            
            x_values = primelstlst[:-1] 
            y_values = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
            
            max_y_zoom = st.slider("Altura Máxima do Eixo Y (Zoom):", min_value=6, max_value=max(y_values) if y_values else 100, value=30, step=2)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # --- CORREÇÃO DE VISIBILIDADE AQUI ---
            scatter_plot = ax.scatter(
                x_values, 
                y_values, 
                s=30,                 # Aumentei ligeiramente o tamanho
                c=y_values,
                cmap='Spectral_r',
                marker='o', 
                alpha=0.9,            # Menos transparente (cores mais sólidas)
                edgecolors='black',   # Contorno preto em todos os pontos
                linewidth=0.4         # Espessura fina do contorno
            )
            
            # Barra de cor lateral
            cbar = plt.colorbar(scatter_plot, ax=ax)
            cbar.set_label('Tamanho do Intervalo (Gap)')
            
            # Ajustes finais do gráfico
            ticks_y = np.arange(2, max_y_zoom + 4, 2)
            ax.set_yticks(ticks_y)
            ax.set_ylim(0, max_y_zoom + 2)
            ax.grid(True, axis='y', linestyle='-', linewidth=0.5, alpha=0.3, color='gray')
            ax.set_xlabel("Número Primo ($p$)", fontsize=11)
            ax.set_ylabel("Tamanho do Intervalo (Gap)", fontsize=11)
            ax.set_title(f"Padrão dos Intervalos (Focando nos gaps até {max_y_zoom})", fontsize=13)
            ax.set_xlim(0, max(x_values))

            st.pyplot(fig)

        # --- PARTE 3: EXPLORADOR ---
        st.write("---")
        st.subheader("📂 Explorador de Intervalos")
        st.markdown("Aqui podes selecionar **qualquer intervalo** que apareça no gráfico para ver os números primos correspondentes.")
        gaps_disponiveis = sorted(todos_intervalos.keys())
        if not gaps_disponiveis:
            st.warning("Ainda não há dados suficientes.")
        else:
            col_sel, col_res = st.columns([1, 2])
            with col_sel:
                gap_escolhido = st.selectbox("Escolhe o tamanho do intervalo (Gap):", options=gaps_disponiveis)
                qtd_encontrada = len(todos_intervalos[gap_escolhido])
                st.success(f"Foram encontrados **{qtd_encontrada}** pares com intervalo de **{gap_escolhido}**.")
            with col_res:
                with st.expander(f"Ver lista de pares com intervalo {gap_escolhido}", expanded=True):
                    st.write(todos_intervalos[gap_escolhido])
    else:
        st.info("👈 Para começar, define o valor de **n** na barra lateral e clica em **Calcular**.")

# --- CONTROLADOR PRINCIPAL ---
if st.session_state['iniciar']:
    mostrar_app_principal()
else:
    mostrar_tela_inicial()
