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

  # 3. O Gráfico (Estilo "Pontinhos" / Scatter Plot)
        st.write("---")
        st.subheader("📈 Distribuição dos Intervalos (Scatter Plot)")
        
        if len(primelstlst) > 2:
            import numpy as np
            
            # Dados
            x_values = primelstlst[:-1] 
            y_values = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
            max_gap = max(y_values) if len(y_values) > 0 else 10
            
            # Criar a figura
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # --- OS PONTINHOS ---
            # s=10: Tamanho pequeno para parecerem "pontinhos"
            # c='black': Cor preta para alto contraste
            # alpha=0.5: Transparência (se muitos pontos ficarem uns em cima dos outros, fica mais escuro)
            # marker='o': Formato de bolinha
            ax.scatter(x_values, y_values, s=10, c='black', marker='o', alpha=0.5)
            
            # --- EIXO Y (Intervalos: 2, 4, 6...) ---
            # Cria a escala apenas com números pares
            ticks_y = np.arange(2, max_gap + 2, 2)
            ax.set_yticks(ticks_y)
            ax.set_ylim(0, max_gap + 2) # Margem ligeira
            
            # --- VISUALIZAÇÃO ---
            # Grelha horizontal fina para guiar o olhar nas linhas 2, 4, 6...
            ax.grid(True, axis='y', linestyle='-', linewidth=0.5, alpha=0.3, color='gray')
            
            # Labels (Títulos dos Eixos)
            ax.set_xlabel("Número Primo ($p$)", fontsize=11)
            ax.set_ylabel("Tamanho do Intervalo (Gap)", fontsize=11)
            ax.set_title(f"Padrão dos Intervalos entre Primos (até {end})", fontsize=13)
            
            # Ajustar limite X para coincidir com o input do utilizador
            ax.set_xlim(0, end)

            # Mostrar gráfico
            st.pyplot(fig)
            
            st.caption("Cada ponto preto representa um intervalo entre dois primos consecutivos.")
            
        else:
            st.warning("Aumente o valor de n para gerar o gráfico.")

else:
    st.write(" Ajuste o valor de **n** na barra lateral e clique em calcular.")






