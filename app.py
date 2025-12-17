import streamlit as st
import matplotlib.pyplot as plt

# --- Configuração da Página ---
st.set_page_config(page_title="Primos e Padrões", layout="wide")

st.title(" Análise de Padrões em Números Primos")
st.markdown("""
Esta aplicação gera números primos baseados na sequência **6n ± 1** e analisa as diferenças entre eles.
""")

# --- Entrada de Dados ---
st.sidebar.header("Parâmetros")
end = st.sidebar.number_input("Ordem final da sequência (n):", min_value=10, max_value=5000, value=100, step=10)

if st.sidebar.button("Calcular"):
    
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

        # --- APRESENTAÇÃO DOS RESULTADOS ---

        # 1. Métricas
        st.subheader("Estatísticas Encontradas")
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

    # 3. O Gráfico (Gráfico de Barras - Comparação de Quantidades)
        st.write("---")
        st.subheader("📊 Comparação: Qual é o padrão mais comum?")
        
        if len(primelstlst) > 2:
            
            # Preparar os dados para o gráfico de barras
            categorias = ['Gémeos (Diff 2)', 'Diff 4', 'Diff 6', 'Diff 8', 'Diff 10']
            quantidades = [len(twins), len(fours), len(sixes), len(eights), len(tens)]
            
            # Criar o gráfico
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Criar as barras com cores diferentes para cada categoria
            cores = ['#ff4b4b', '#1f77b4', '#2ca02c', '#ff7f0e', '#9467bd']
            barras = ax.bar(categorias, quantidades, color=cores, alpha=0.8)
            
            # Títulos e Eixos
            ax.set_ylabel("Quantidade Encontrada", fontsize=12)
            ax.set_title(f"Frequência dos Diferentes Tipos de Primos (n={end})", fontsize=14)
            
            # Remover linhas desnecessárias para limpar o visual
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis='y', linestyle='--', alpha=0.3)
            
            # --- O TRUQUE PARA SER FÁCIL DE LER ---
            # Escrever o número exato em cima de cada barra
            for barra in barras:
                height = barra.get_height()
                ax.annotate(f'{height}',
                            xy=(barra.get_x() + barra.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom', fontweight='bold')

            st.pyplot(fig)
            
        else:
            st.warning("Aumente o valor de n para gerar o gráfico.")

else:
    st.write(" Ajuste o valor de **n** na barra lateral e clique em calcular.")





