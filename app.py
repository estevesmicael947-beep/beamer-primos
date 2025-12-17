import streamlit as st
import matplotlib.pyplot as plt

# --- Configuração da Página ---
st.set_page_config(page_title="Primos e Padrões", layout="wide")

st.title("🔍 Análise de Padrões em Números Primos")
st.markdown("""
Esta aplicação gera números primos baseados na sequência **6n ± 1** e analisa as diferenças entre eles.
""")

# --- Entrada de Dados ---
st.sidebar.header("Parâmetros")
end = st.sidebar.number_input("Ordem final da sequência (n):", min_value=10, max_value=5000, value=100, step=10)

if st.sidebar.button("Calcular 🚀"):
    
    with st.spinner('A processar números primos...'):
        # --- LÓGICA DE CÁLCULO ORIGINAL ---
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
        
        # Organizar listas
        primelstlst = sorted(list(primelst))
        
        twins = []
        fours = []
        sixes = []
        eights = []
        tens = []

        # Encontrar pares
        for x in range(len(primelstlst)-1):
            diff = primelstlst[x+1] - primelstlst[x]
            pair = (primelstlst[x], primelstlst[x+1])
            
            if diff == 2:
                twins.append(pair)
            elif diff == 4:
                fours.append(pair)
            elif diff == 6:
                sixes.append(pair)
            elif diff == 8:
                eights.append(pair)
            elif diff == 10:
                tens.append(pair)

        # --- PARTE 1: APRESENTAÇÃO DOS RESULTADOS (Métricas e Listas) ---

        # 1. Métricas
        st.subheader("📊 Estatísticas Encontradas")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        col1.metric("Gémeos (2)", len(twins))
        col2.metric("Dif. 4", len(fours))
        col3.metric("Dif. 6", len(sixes))
        col4.metric("Dif. 8", len(eights))
        col5.metric("Dif. 10", len(tens))

        st.info(f"Total de números primos encontrados: **{len(primelstlst)}**")

        # 2. Listas Detalhadas
        st.write("---")
        col_left, col_right = st.columns(2)
        
        with col_left:
            with st.expander("Ver lista de Primos Gémeos"):
                st.write(twins)
            with st.expander("Ver lista Dif. 4"):
                st.write(fours)
            with st.expander("Ver lista Dif. 6"):
                st.write(sixes)

        with col_right:
            with st.expander("Ver lista completa de Primos"):
                st.write(primelstlst)

        # --- PARTE 2: O GRÁFICO (Versão Apenas Pontos) ---
        if len(twins) > 1:
            st.write("---")
            st.subheader("📈 Distância entre pares de Primos Gémeos (Dispersão)")
            
            # Cálculo original do gráfico
            twingap = [twins[x+1][0] - twins[x][0] for x in range(len(twins)-1)]
            x_axis = [x[0] for x in twins[:-1]]
            
            fig, ax = plt.subplots(figsize=(10, 4))
            
            # --- ALTERAÇÃO AQUI ---
            # Mudei linestyle='-' para linestyle='None'
            # Aumentei markersize para 5 para os pontos ficarem mais visíveis
            ax.plot(x_axis, twingap, marker='o', linestyle='None', color='b', markersize=5, alpha=0.6)
            
            ax.set_title("Variação da distância entre primos gémeos consecutivos")
            ax.set_xlabel("Valor do Primo")
            ax.set_ylabel("Distância (Gap)")
            # Adicionei grid também no eixo X para facilitar a leitura dos pontos
            ax.grid(True, which='both', linestyle='--', alpha=0.5)
            
            st.pyplot(fig)
        else:
            st.warning("Não há dados suficientes de primos gémeos para gerar o gráfico. Aumente o valor de n.")

else:
    st.write("👈 Ajuste o valor de **n** na barra lateral e clique em calcular.")
