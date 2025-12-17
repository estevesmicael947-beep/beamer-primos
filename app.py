import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Configuração da Página ---
st.set_page_config(page_title="Primos e Padrões", layout="wide")

st.title("🔍 Análise de Padrões em Números Primos")
st.markdown("""
Esta aplicação gera números primos baseados na sequência **6n ± 1**, analisa as diferenças e permite **zoom interativo**.
""")

# --- 1. MEMÓRIA (Session State) ---
if 'primelstlst' not in st.session_state:
    st.session_state['primelstlst'] = []
if 'calculou' not in st.session_state:
    st.session_state['calculou'] = False

# --- 2. INPUTS ---
st.sidebar.header("Parâmetros")
end = st.sidebar.number_input("Ordem final da sequência (n):", min_value=10, max_value=10000, value=100, step=10)

# --- 3. LÓGICA DE CÁLCULO ---
if st.sidebar.button("Calcular 🚀"):
    
    with st.spinner('A processar números primos...'):
        primelst = set({2, 3})
        
        # Sequência 6n - 1
        n = 1
        while n <= end:
            num = 6 * n - 1
            y = 2
            while y < num:
                if num % y == 0:
                    break
                else:
                    y += 1
            if y == num:
                primelst.add(num)
            n += 1

        # Sequência 6n + 1
        n = 1    
        while n <= end:
            num = 6 * n + 1
            y = 2
            while y < num:
                if num % y == 0:
                    break
                else:
                    y += 1
            if y == num:
                primelst.add(num)
            n += 1
        
        # Guarda o resultado na memória
        st.session_state['primelstlst'] = sorted(list(primelst))
        st.session_state['calculou'] = True

# --- 4. VISUALIZAÇÃO ---
if st.session_state['calculou']:
    
    primelstlst = st.session_state['primelstlst']
    
    # --- NOVA LÓGICA: Dicionário de Intervalos ---
    # Isto vai guardar TODOS os intervalos encontrados (2, 4, 6, 8, 10, 12, 14...)
    # Chave = Tamanho do intervalo (Gap)
    # Valor = Lista de pares
    todos_intervalos = {}

    for x in range(len(primelstlst)-1):
        diff = primelstlst[x+1] - primelstlst[x]
        pair = (primelstlst[x], primelstlst[x+1])
        
        if diff not in todos_intervalos:
            todos_intervalos[diff] = []
        
        todos_intervalos[diff].append(pair)

    # Listas clássicas para as métricas (apenas para manter o visual bonito lá em cima)
    twins = todos_intervalos.get(2, [])
    fours = todos_intervalos.get(4, [])
    sixes = todos_intervalos.get(6, [])
    eights = todos_intervalos.get(8, [])
    tens = todos_intervalos.get(10, [])

    # --- PARTE 1: MÉTRICAS ---
    st.subheader("📊 Estatísticas Encontradas")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.metric("Gémeos (2)", len(twins))
    col2.metric("Dif. 4", len(fours))
    col3.metric("Dif. 6", len(sixes))
    col4.metric("Dif. 8", len(eights))
    col5.metric("Dif. 10", len(tens))

    st.info(f"Total de números primos encontrados: **{len(primelstlst)}**")

    st.write("---")

    # --- PARTE 2: O GRÁFICO ---
    if len(primelstlst) > 2:
        st.subheader("📈 Distribuição dos Intervalos (Gaps)")

        st.info("""
        **O que significam os pontos?** Os pontos marcam os primos que têm esse intervalo.  
        * **Eixo Horizontal:** Indica qual é o número primo.
        * **Eixo Vertical:** Indica qual é a distância para o primo seguinte.
        """)
        
        # Preparação dos dados
        x_values = primelstlst[:-1] 
        y_values = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
        
        # Slider de Zoom
        max_y_zoom = st.slider("Altura Máxima do Eixo Y (Zoom):", min_value=6, max_value=100, value=20, step=2)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Pontinhos pretos
        ax.scatter(x_values, y_values, s=15, c='black', marker='.', alpha=0.5)
        
        # Configuração do Eixo Y
        ticks_y = np.arange(2, max_y_zoom + 2, 2)
        ax.set_yticks(ticks_y)
        ax.set_ylim(0, max_y_zoom + 1)
        
        # Estilização
        ax.grid(True, axis='y', linestyle='-', linewidth=0.5, alpha=0.3, color='gray')
        ax.set_xlabel("Número Primo ($p$)", fontsize=11)
        ax.set_ylabel("Tamanho do Intervalo (Gap)", fontsize=11)
        ax.set_title(f"Padrão dos Intervalos (Focando nos gaps até {max_y_zoom})", fontsize=13)
        ax.set_xlim(0, max(x_values))

        st.pyplot(fig)

    # --- PARTE 3: EXPLORADOR DE INTERVALOS (NOVO) ---
    st.write("---")
    st.subheader("📂 Explorador de Intervalos")
    st.markdown("Aqui podes selecionar **qualquer intervalo** que apareça no gráfico para ver os números primos correspondentes.")

    # Criar lista ordenada dos intervalos disponíveis (chaves do dicionário)
    gaps_disponiveis = sorted(todos_intervalos.keys())

    if not gaps_disponiveis:
        st.warning("Ainda não há dados suficientes.")
    else:
        # Colunas para organizar o layout
        col_sel, col_res = st.columns([1, 2])
        
        with col_sel:
            # Caixa de seleção
            gap_escolhido = st.selectbox(
                "Escolhe o tamanho do intervalo (Gap):", 
                options=gaps_disponiveis
            )
            
            # Mostra a quantidade encontrada
            qtd_encontrada = len(todos_intervalos[gap_escolhido])
            st.success(f"Foram encontrados **{qtd_encontrada}** pares com intervalo de **{gap_escolhido}**.")

        with col_res:
            # Mostra a lista dentro de um expander para não ocupar muito espaço se for grande
            with st.expander(f"Ver lista de pares com intervalo {gap_escolhido}", expanded=True):
                st.write(todos_intervalos[gap_escolhido])

else:
    st.write("👈 Ajuste o valor de **n** na barra lateral e clique em calcular.")
