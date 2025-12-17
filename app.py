import streamlit as st
import matplotlib.pyplot as plt

# --- Configuração da Página ---
st.set_page_config(page_title="Primos e Padrões", layout="wide")

st.title("Análise de Padrões em Números Primos")
st.markdown("""
Esta aplicação gera números primos baseados na sequência **6n ± 1** e analisa as diferenças entre eles 
(Primos Gémeos, Primos com diferença de 4, 6, etc.).
""")

# --- Entrada de Dados (Substitui o input) ---
st.sidebar.header("Parâmetros")
end = st.sidebar.number_input("Ordem final da sequência (n):", min_value=10, max_value=5000, value=100, step=10)

if st.sidebar.button("Calcular"):
    
    with st.spinner('A processar números primos...'):
        # --- A TUA LÓGICA DE CÁLCULO (Mantida igual) ---
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

        # Encontrar pares (Tua lógica)
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

        # --- APRESENTAÇÃO DOS RESULTADOS ---

        # 1. Métricas (Visual bonito para as contagens)
        st.subheader("Estatísticas Encontradas")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        col1.metric("Gémeos (2)", len(twins))
        col2.metric("Dif. 4", len(fours))
        col3.metric("Dif. 6", len(sixes))
        col4.metric("Dif. 8", len(eights))
        col5.metric("Dif. 10", len(tens))

        st.info(f"Total de números primos encontrados: **{len(primelstlst)}**")

        # 2. Listas Detalhadas (Dentro de expansores para não encher o ecrã)
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

      # 3. O Gráfico (Pontos com Eixos Identificados)
        st.write("---")
        st.subheader("📈 Visualização dos Intervalos (Gaps)")
        
        if len(primelstlst) > 2:
            # Preparar dados
            x_values = primelstlst[:-1] 
            y_values = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
            
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Desenhar apenas os pontos (Pretos, tamanho 15)
            ax.scatter(x_values, y_values, s=15, c='black', marker='o', alpha=0.6)
            
            # --- IDENTIFICAÇÃO DOS EIXOS ---
            
            # Eixo X: Os números primos
            ax.set_xlabel("Número Primo ($p_n$)", fontsize=12, fontweight='bold')
            
            # Eixo Y: O tamanho do intervalo (Gap)
            ax.set_ylabel("Tamanho do Intervalo ($p_{n+1} - p_n$)", fontsize=12, fontweight='bold')
            
            # Título do Gráfico
            ax.set_title(f"Distribuição dos Gaps (até n={end})", fontsize=14)
            
            # --- AJUSTE DA ESCALA DO EIXO Y ---
            # Força o eixo Y a mostrar apenas números pares (2, 4, 6, 8...)
            max_gap = max(y_values) if len(y_values) > 0 else 10
            ax.set_yticks(range(0, max_gap + 4, 2))
            
            # Adiciona uma grelha horizontal fina para ajudar a ler o valor do eixo Y
            ax.grid(True, axis='y', linestyle='--', alpha=0.5)

            st.pyplot(fig)
            
        else:
            st.warning("Aumente o valor de n para gerar o gráfico.")
            
            # Comando do Streamlit para mostrar o gráfico
            st.pyplot(fig)
        else:
            st.warning("Não há dados suficientes de primos gémeos para gerar o gráfico. Aumente o valor de n.")

else:

    st.write("Ajuste o valor de **n** na barra lateral e clique em calcular.")
