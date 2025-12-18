import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter
from matplotlib.ticker import MaxNLocator

# --- Configuração da Página (Modo Desktop / Wide) ---
st.set_page_config(page_title="Primos e Padrões", layout="wide", page_icon="🧮")

# --- LÓGICA DE NAVEGAÇÃO ---
if 'iniciar' not in st.session_state:
    st.session_state['iniciar'] = False

def mostrar_tela_inicial():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("")
        st.write("")
        
        try:
            st.image("logo_ua.png", width=150)
        except:
            st.write("### 🏛️ Universidade de Aveiro")
            st.caption("(Imagem 'logo_ua.png' não encontrada)")

        st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>🧮 Primos e Padrões</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: gray; font-weight: normal;'>A beleza matemática da sequência 6n ± 1</h4>", unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        st.write("")

        c1, c2, c3 = st.columns([1, 2, 1]) 
        with c2:
            if st.button("Iniciar Investigação ⚡", type="primary", use_container_width=True):
                st.session_state['iniciar'] = True
                st.rerun()

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

    st.sidebar.markdown("### ⚙️ Configuração da Pesquisa")
    if st.sidebar.button("🏠 Voltar à Capa"):
        st.session_state['iniciar'] = False
        st.rerun()
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("**Definição do Intervalo:**")
    
    end = st.sidebar.number_input(
        "Valor da variável 'n':", 
        min_value=10, 
        max_value=20000, 
        value=500, 
        step=50,
        help="Aumente este valor para encontrar primos maiores."
    )
    
    limite_real = end * 6
    st.sidebar.info(f"""
    ℹ️ **O que isto significa?**
    A app vai gerar candidatos usando a fórmula $6n \\pm 1$.
    Ao escolher **n = {end}**, estamos a investigar números até aprox. **{limite_real}**.
    """)

    if st.sidebar.button("Gerar Padrões ⚡", type="primary"):
        with st.spinner(f'A calcular primos até {limite_real}...'):
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
            
    st.sidebar.markdown("---")
    st.sidebar.caption("Projeto **TMFC** | Universidade de Aveiro")
    st.sidebar.caption("Autores: Catarina, Diogo, Mateus, Micael")

    st.title("🧮 Análise de Padrões em Números Primos")
    
    if 'primelstlst' not in st.session_state:
        st.session_state['primelstlst'] = []
    if 'calculou' not in st.session_state:
        st.session_state['calculou'] = False

    if st.session_state['calculou']:
        primelstlst = st.session_state['primelstlst']
        
        todos_intervalos = {}
        for x in range(len(primelstlst)-1):
            diff = primelstlst[x+1] - primelstlst[x]
            pair = (primelstlst[x], primelstlst[x+1])
            if diff not in todos_intervalos: todos_intervalos[diff] = []
            todos_intervalos[diff].append(pair)

        # Contagens
        counts = {k: len(todos_intervalos.get(k, [])) for k in [2, 4, 6, 8, 10]}
        y_values = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
        x_values = primelstlst[:-1]
        dominio_do_6 = (counts[6] > counts[2]) and (counts[6] > counts[4])

        tab_dash, tab_expl, tab_sobre = st.tabs(["📉 Análise Visual", "🔬 Laboratório de Dados", "🎓 Teoria Matemática"])

        # === TAB 1: PAINEL DE ANÁLISE ===
        with tab_dash:
            st.markdown("### 📊 Indicadores Globais")
            kpi1, kpi2, kpi3 = st.columns(3)
            with kpi1: st.metric("🔢 Primos Identificados", len(primelstlst), border=True)
            with kpi2: st.metric("🔝 Maior Primo (Max)", max(primelstlst) if primelstlst else 0, border=True)
            with kpi3: st.metric("📏 Total de Intervalos", len(primelstlst)-1 if len(primelstlst) > 1 else 0, border=True)

            st.write("---")

            if len(primelstlst) > 2:
                st.subheader("📍 Dispersão dos Intervalos")
                
                st.info("""
                **Legenda do Gráfico:**
                * **Eixo X:** Posição do primo. | **Eixo Y:** Distância ao próximo.
                * 🟣 **Ponto Magenta:** O único intervalo de 1 (entre 2 e 3).
                * 🔵 **Azul:** Intervalos mais frequentes.
                """)
                
                max_y_zoom = st.slider("Zoom Vertical (Eixo Y):", min_value=6, max_value=max(y_values) if y_values else 100, value=30, step=2)
                
                # Tamanho Panorâmico (Desktop)
                fig, ax = plt.subplots(figsize=(12, 6))
                
                x_arr = np.array(x_values)
                y_arr = np.array(y_values)
                mask_1 = (y_arr == 1)
                
                # Pontos normais
                scatter_plot = ax.scatter(
                    x_arr[~mask_1], y_arr[~mask_1], s=30, c=y_arr[~mask_1], 
                    cmap='Spectral_r', marker='o', alpha=0.9, 
                    edgecolors='black', linewidth=0.4
                )
                
                # Ponto único (Gap 1)
                if np.any(mask_1):
                    ax.scatter(
                        x_arr[mask_1], y_arr[mask_1], s=80, c='#D500F9', 
                        marker='o', edgecolors='black', linewidth=1.0, 
                        label='Gap Único (1)'
                    )
                
                cbar = plt.colorbar(scatter_plot, ax=ax)
                cbar.set_label('Tamanho do Intervalo')
                
                ticks_y = np.arange(2, max_y_zoom + 4, 2)
                ax.set_yticks(ticks_y)
                ax.set_ylim(0, max_y_zoom + 2)
                ax.grid(True, axis='y', linestyle='-', linewidth=0.5, alpha=0.3, color='gray')
                ax.set_xlabel("Número Primo ($p$)", fontsize=11)
                ax.set_ylabel("Distância ao próximo primo (Intervalo)", fontsize=11)
                ax.set_title(f"Dispersão dos Intervalos entre Primos (Zoom até {max_y_zoom})", fontsize=13)
                ax.set_xlim(0, max(x_values))
                st.pyplot(fig)

                st.write("---")
                st.subheader("📊 Histograma de Frequências")
                
                gap_counts = Counter(y_values)
                sorted_gaps = sorted(gap_counts.keys())
                filtered_gaps = [g for g in sorted_gaps if g <= max_y_zoom]
                filtered_counts = [gap_counts[g] for g in filtered_gaps]
                x_labels = [str(g) for g in filtered_gaps]

                # Tamanho Panorâmico (Desktop)
                fig2, ax2 = plt.subplots(figsize=(12, 4))
                bars = ax2.bar(x_labels, filtered_counts, color='#4e79a7', edgecolor='black', alpha=0.8, width=0.6)
                
                ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
                ax2.set_xlabel("Tipo de Intervalo")
                ax2.set_ylabel("Frequência")
                ax2.set_title("Dominância dos Intervalos")
                ax2.grid(axis='y', linestyle='--', alpha=0.5)
                
                for bar in bars:
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                            ha='center', va='bottom', fontsize=9)
                st.pyplot(fig2)

                if dominio_do_6:
                    with st.container(border=True):
                        st.markdown("""
                        ### 💡 Observação Matemática Detetada
                        **O intervalo 6 é o mais frequente.**
                        Isto confirma a tendência de que múltiplos de 6 são privilegiados, mesmo quando comparados com intervalos menores como 4.
                        """)

        # === TAB 2: EXPLORADOR (Laboratório de Dados) ===
        with tab_expl:
            st.header("🔬 Laboratório de Dados")
            
            # Duas colunas: Lista Geral (Esquerda) e Análise Detalhada (Direita)
            # No Desktop damos mais espaço à análise (proporção 1 para 2)
            col_list, col_analise = st.columns([1, 2])
            
            # --- 1. LADO ESQUERDO: LISTA DE TODOS OS PRIMOS ---
            with col_list:
                st.markdown("### 🔢 Lista Geral")
                st.caption(f"Total encontrados: {len(primelstlst)}")
                
                # Cria Tabela Simples
                df_todos = pd.DataFrame(primelstlst, columns=["Primos"])
                st.dataframe(df_todos, height=500, use_container_width=True)
                
                # Botão Download Lista Simples
                csv_todos = df_todos.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 Baixar Lista Simples (CSV)",
                    data=csv_todos,
                    file_name='todos_os_primos.csv',
                    mime='text/csv',
                    use_container_width=True
                )

            # --- 2. LADO DIREITO: ANÁLISE DE INTERVALOS ---
            with col_analise:
                st.markdown("### 📏 Análise de Intervalos")
                
                gaps_disponiveis = sorted(todos_intervalos.keys())
                
                if not gaps_disponiveis:
                    st.warning("Sem dados para analisar.")
                else:
                    # Seletor de Gap
                    gap_escolhido = st.selectbox("Escolha o Intervalo para ver os pares:", options=gaps_disponiveis)
                    st.success(f"Foram isolados **{len(todos_intervalos[gap_escolhido])}** pares com Intervalo **{gap_escolhido}**.")
                    
                    # Tabela de Pares
                    dados_pares = todos_intervalos[gap_escolhido]
                    df_pares = pd.DataFrame(dados_pares, columns=["Primo A", "Primo B"])
                    
                    # Formatar visualmente para (A, B) na tabela
                    df_visual = df_pares.copy()
                    df_visual['Par'] = df_visual.apply(lambda x: f"({x['Primo A']}, {x['Primo B']})", axis=1)
                    st.dataframe(df_visual[['Par']], height=350, use_container_width=True)
                    
                    st.markdown("---")
                    
                    # --- EXPORTAÇÃO COMPLETA ---
                    export_dict = {}
                    for gap in gaps_disponiveis:
                        col_name = f"Intervalo {gap}"
                        # Usamos (p1, p2) para o Excel
                        pares_formatados = [f"({p[0]}, {p[1]})" for p in todos_intervalos[gap]]
                        export_dict[col_name] = pares_formatados
                    
                    df_export = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in export_dict.items()]))
                    df_export = df_export.fillna("")
                    
                    csv_data = df_export.to_csv(index=False, sep=';').encode('utf-8-sig')
                    
                    st.download_button(
                        label="💾 Baixar Tabela Organizada por Intervalos (Excel)", 
                        data=csv_data, 
                        file_name='primos_por_intervalo.csv', 
                        mime='text/csv', 
                        type='primary',
                        use_container_width=True
                    )

        # === TAB 3: SOBRE ===
        with tab_sobre:
            st.header("🎓 Contexto Teórico")
            st.markdown("""
            Projeto desenvolvido para a unidade curricular **TMFC (Tópicos Matemáticos e Ferramentas Computacionais)** na Universidade de Aveiro.
            """)
            
            # --- NOVA SECÇÃO DE EXPLICAÇÃO ---
            with st.container(border=True):
                st.subheader("🌟 Porque o intervalo 6 é mais frequente")
                
                st.markdown("""
                Todo primo maior que 3 não é múltiplo de 2 nem de 3, logo pertence às formas:
                
                $$
                6n - 1 \\quad \\text{ou} \\quad 6n + 1
                $$
                
                O intervalo 6 é o **menor deslocamento** que mantém essas duas condições ao mesmo tempo, criando mais pares candidatos a primos do que outros intervalos.
                
                > *Por isso, observa-se experimentalmente uma maior frequência de pares de primos separados por 6.*
                """)

            st.markdown("""
            ### 📚 Glossário de Intervalos
            * **Primos Gémeos:** $p, p+2$ (ex: 11, 13).
            * **Primos Primos:** $p, p+4$ (ex: 7, 11).
            * **Primos Sexy:** $p, p+6$ (ex: 5, 11).
            """)
            
            st.write("---")
            st.caption("Investigação realizada por: Catarina Mendes, Diogo Maria, Mateus Carmo e Micael Esteves.")

    else:
        st.info("👈 Defina o valor de **n** na barra lateral e clique em **Gerar Padrões** para iniciar.")

if st.session_state['iniciar']:
    mostrar_app_principal()
else:
    mostrar_tela_inicial()
