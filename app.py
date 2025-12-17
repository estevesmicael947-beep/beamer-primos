import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(page_title="Primos e Padrões", layout="wide")

st.title("🔍 Análise de Padrões em Números Primos")

# --- 1. MEMÓRIA (Session State) ---
# Impede que o programa reinicie ao mexer no zoom
if 'primelstlst' not in st.session_state:
    st.session_state['primelstlst'] = []
if 'calculou' not in st.session_state:
    st.session_state['calculou'] = False

# --- 2. INPUTS ---
st.sidebar.header("Parâmetros")
end = st.sidebar.number_input("Ordem final da sequência (n):", min_value=10, max_value=10000, value=100, step=10)

# --- 3. CÁLCULO ---
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

# --- 4. VISUALIZAÇÃO ---
if st.session_state['calculou']:
    
    # Recupera dados
    primelstlst = st.session_state['primelstlst']
    
    # Prepara listas de diferenças
    # (Gap do primo i é a distância até i+1)
    gaps_list = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
    
    # Estatísticas simples para visualização rápida
    twins = [p for i, p in enumerate(primelstlst[:-1]) if gaps_list[i] == 2]
    sixes = [p for i, p in enumerate(primelstlst[:-1]) if gaps_list[i] == 6]

    # --- MÉTRICAS ---
    st.subheader("📊 Resumo Estatístico")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Primos", len(primelstlst))
    c2.metric("Primos Gémeos (Gap 2)", len(twins))
    c3.metric("Primos Sexy (Gap 6)", len(sixes))
    
    st.write("---")

    # --- LISTAGEM DOS DADOS (O QUE PEDISTE) ---
    st.subheader("📋 Dados Brutos")
    
    # Opção A: Tabela Lado a Lado (Listas completas)
    col_primos, col_gaps = st.columns(2)
    
    with col_primos:
        st.write("**Lista de Primos Encontrados:**")
        # Mostra como uma caixa de texto rolável para não ocupar a página toda
        st.text_area("Primos", value=str(primelstlst), height=150, label_visibility="collapsed")
        
    with col_gaps:
        st.write("**Lista de Intervalos (Gaps):**")
        st.text_area("Intervalos", value=str(gaps_list), height=150, label_visibility="collapsed")

    # Opção B: Tabela Relacional (Mais fácil de ler)
    with st.expander("Ver Tabela Detalhada (Primo -> Intervalo)"):
        df = pd.DataFrame({
            "Número Primo": primelstlst[:-1],
            "Distância para o próximo": gaps_list
        })
        st.dataframe(df, use_container_width=True)

    # --- O GRÁFICO ---
    st.write("---")
    st.subheader("📈 Distribuição Visual dos Intervalos")
    
    if len(primelstlst) > 2:
        x_values = primelstlst[:-1] 
        y_values = gaps_list
        
        # Slider de Zoom
        max_y_zoom = st.slider("Altura Máxima do Eixo Y (Zoom):", min_value=6, max_value=100, value=20, step=2)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Pontinhos
        ax.scatter(x_values, y_values, s=15, c='black', marker='.', alpha=0.5)
        
        # Eixo Y
        ticks_y = np.arange(2, max_y_zoom + 2, 2)
        ax.set_yticks(ticks_y)
        ax.set_ylim(0, max_y_zoom + 1)
        
        # Estilo
        ax.grid(True, axis='y', linestyle='-', linewidth=0.5, alpha=0.3, color='gray')
        ax.set_xlabel("Número Primo ($p$)", fontsize=11)
        ax.set_ylabel("Tamanho do Intervalo ($p_{next} - p$)", fontsize=11)
        ax.set_title(f"Padrão dos Intervalos (Focando nos gaps até {max_y_zoom})", fontsize=13)
        ax.set_xlim(0, max(x_values))

        st.pyplot(fig)
        st.caption("Usa o slider acima para cortar os 'gaps' muito grandes e focar nas linhas de baixo.")

else:
    st.write("👈 Ajuste o valor de **n** na barra lateral e clique em calcular.")
