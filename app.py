import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# --- Configuração da Página ---
st.set_page_config(page_title="Primos e Padrões", layout="wide")

st.title("🔍 Análise de Padrões em Números Primos")

# --- 1. MEMÓRIA (Session State) ---
# Isto impede que o programa "feche" quando mexes no zoom
if 'primelstlst' not in st.session_state:
    st.session_state['primelstlst'] = []
if 'calculou' not in st.session_state:
    st.session_state['calculou'] = False

# --- 2. INPUTS ---
st.sidebar.header("Parâmetros")
end = st.sidebar.number_input("Ordem final da sequência (n):", min_value=10, max_value=10000, value=100, step=10)

# --- 3. CÁLCULO (Só corre se clicares no botão) ---
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
        
        # GUARDA NA MEMÓRIA
        st.session_state['primelstlst'] = sorted(list(primelst))
        st.session_state['calculou'] = True

# --- 4. VISUALIZAÇÃO (Corre sempre que houver dados na memória) ---
if st.session_state['calculou']:
    
    # Recupera os dados da memória
    primelstlst = st.session_state['primelstlst']
    
    # Prepara os dados estatísticos
    twins, fours, sixes, eights, tens = [], [], [], [], []
    
    for x in range(len(primelstlst)-1):
        diff = primelstlst[x+1] - primelstlst[x]
        pair = (primelstlst[x], primelstlst[x+1])
        if diff == 2: twins.append(pair)
        elif diff == 4: fours.append(pair)
        elif diff == 6: sixes.append(pair)
        elif diff == 8: eights.append(pair)
        elif diff == 10: tens.append(pair)

    # Métricas
    st.subheader("📊 Estatísticas Encontradas")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Gémeos (2)", len(twins))
    col2.metric("Dif. 4", len(fours))
    col3.metric("Dif. 6", len(sixes))
    col4.metric("Dif. 8", len(eights))
    col5.metric("Dif. 10", len(tens))
    
    st.info(f"Total de números primos encontrados: **{len(primelstlst)}**")

    # Listas (Expansores)
    st.write("---")
    with st.expander("Ver Listas Detalhadas"):
        c1, c2 = st.columns(2)
        c1.write(f"Gémeos: {twins}")
        c2.write(f"Todos: {primelstlst}")

    # --- O GRÁFICO (Com Zoom Estável) ---
    st.write("---")
    st.subheader("📈 Distribuição dos Intervalos (Gaps)")
    
    if len(primelstlst) > 2:
        # Dados do gráfico
        x_values = primelstlst[:-1] 
        y_values = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
        
        # --- O SLIDER AGORA FUNCIONA ---
        # Como está fora do "if button", ele não reseta os dados
        max_y_zoom = st.slider("Altura Máxima do Eixo Y (Zoom):", min_value=6, max_value=100, value=20, step=2)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Pontinhos pretos
        ax.scatter(x_values, y_values, s=15, c='black', marker='.', alpha=0.5)
        
        # Eixo Y controlado pelo slider
        ticks_y = np.arange(2, max_y_zoom + 2, 2)
        ax.set_yticks(ticks_y)
        ax.set_ylim(0, max_y_zoom + 1)
        
        # Estilo
        ax.grid(True, axis='y', linestyle='-', linewidth=0.5, alpha=0.3, color='gray')
        ax.set_xlabel("Número Primo ($p$)", fontsize=11)
        ax.set_ylabel("Tamanho do Intervalo (Gap)", fontsize=11)
        ax.set_title(f"Padrão dos Intervalos (Focando nos gaps até {max_y_zoom})", fontsize=13)
        ax.set_xlim(0, max(x_values)) # Usa o valor real do cálculo

        st.pyplot(fig)
        st.caption("Usa o slider acima para fazer zoom no eixo Y.")

else:
    st.write("👈 Ajuste o valor de **n** na barra lateral e clique em calcular.")
