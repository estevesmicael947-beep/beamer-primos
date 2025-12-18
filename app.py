import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter
from matplotlib.ticker import MaxNLocator

# --- Configuração da Página ---
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
    st.sidebar.caption("*Com apoio do Gemini*")

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

        twins = todos_intervalos.get(2, [])
        fours = todos_intervalos.get(4, [])
        sixes = todos_intervalos.get(6, [])
        eights = todos_intervalos.get(8, [])
        tens = todos_intervalos.get(10, [])

        y_values = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
        x_values = primelstlst[:-1]

        dominio_do_6 = (len(sixes) > len(twins)) and (len(sixes) > len(fours))

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
                * **Eixo X:** Posição do primo. | **Eixo Y:** Distância ao próximo.
                * 🟣 **Ponto Magenta:** O único intervalo de 1 (entre 2 e 3).
                * 🔵 **Azul:** Intervalos mais frequentes. | 🔴 **Vermelho:** Intervalos de grande dimensão.
                """)
                
                max_y_zoom = st.slider("Zoom Vertical (Eixo Y):", min_value=6, max_value=max(y_values) if y_values else 100, value=30, step=2)
                
                fig, ax = plt.subplots(figsize=(12, 6))
                
                x_arr = np.array(x_values)
                y_arr = np.array(y_values)
                mask_1 = (y_arr == 1)
                
                x_others = x_arr[~mask_1]
                y_others = y_arr[~mask_1]
                x_unique = x_arr[mask_1]
                y_unique = y_arr[mask_1]
                
                scatter_plot = ax.scatter(
                    x_others, y_others, s=30, c=y_others, 
                    cmap='Spectral_r', marker='o', alpha=0.9, 
                    edgecolors='black', linewidth=0.4
                )
                
                if len(x_unique) > 0:
                    ax.scatter(
                        x_unique, y_unique, s=80, c='#D500F9', 
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
                st.markdown("Comparação da quantidade de vezes que cada intervalo ocorre.")
                
                gap_counts = Counter(y_values)
                sorted_gaps = sorted(gap_counts.keys())
                
                filtered_gaps = [g for g in sorted_gaps if g <= max_y_zoom]
                filtered_counts = [gap_counts[g] for g in filtered_gaps]
                x_labels = [str(g) for g in filtered_gaps]

                fig2, ax2 = plt.subplots(figsize=(12, 4))
                
                bars = ax2.bar(x_labels, filtered_counts, color='#4e79a7', edgecolor='black', alpha=0.8, width=0.6)
                
                ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
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
                        Isto confirma a tendência de que múltiplos de 6 são privilegiados, mesmo quando comparados com intervalos menores como 4.
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
                    
                    # --- CORREÇÃO DA DATA: USAR PARÊNTESIS ---
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter
from matplotlib.ticker import MaxNLocator

# --- Configuração da Página (Otimizada para Mobile) ---
st.set_page_config(page_title="Primos e Padrões", layout="centered", page_icon="🧮")

# --- LÓGICA DE NAVEGAÇÃO ---
if 'iniciar' not in st.session_state:
    st.session_state['iniciar'] = False

def mostrar_tela_inicial():
    # Layout ajustado para ecrã de telemóvel
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
    
    with col2:
        st.write("") 
        
        try:
            st.image("logo_ua.png", use_container_width=True)
        except:
            st.write("### 🏛️ Universidade de Aveiro")

        st.markdown("<h1 style='text-align: center; margin-bottom: 0px;'>🧮 Primos e Padrões</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: gray; font-weight: normal; font-size: 16px;'>A beleza matemática da sequência 6n ± 1</h4>", unsafe_allow_html=True)
        
        st.write("")
        st.write("")

        if st.button("Iniciar Investigação ⚡", type="primary", use_container_width=True):
            st.session_state['iniciar'] = True
            st.rerun()

        st.write("")
        st.markdown("""
        <div style='text-align: center; color: #b0b0b0; font-size: 11px;'>
        Projeto <b>TMFC</b> | Universidade de Aveiro<br>
        Catarina M. • Diogo M. • Mateus C. • Micael E.<br>
        </div>
        """, unsafe_allow_html=True)

def mostrar_app_principal():
    # --- SIDEBAR ---
    try:
        st.sidebar.image("logo_ua.png", use_container_width=True)
    except:
        st.sidebar.markdown("### 🏛️ UAveiro")

    st.sidebar.markdown("### ⚙️ Configuração")
    if st.sidebar.button("🏠 Voltar ao Início", use_container_width=True):
        st.session_state['iniciar'] = False
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Input simplificado
    end = st.sidebar.number_input(
        "Valor de 'n':", 
        min_value=10, 
        max_value=20000, 
        value=500, 
        step=50
    )
    
    limite_real = end * 6
    st.sidebar.info(f"🔎 A analisar até ≈ **{limite_real}**")

    if st.sidebar.button("Gerar Padrões ⚡", type="primary", use_container_width=True):
        with st.spinner('A processar...'):
            primelst = set({2, 3})
            
            def is_prime(num):
                if num < 2: return False
                for i in range(2, int(num**0.5) + 1):
                    if num % i == 0:
                        return False
                return True

            # Geração 6n
            for n in range(1, end + 1):
                if is_prime(6 * n - 1): primelst.add(6 * n - 1)
                if is_prime(6 * n + 1): primelst.add(6 * n + 1)
            
            st.session_state['primelstlst'] = sorted(list(primelst))
            st.session_state['calculou'] = True
            
    st.sidebar.markdown("---")
    st.sidebar.caption("Projeto TMFC | UAveiro")

    st.title("🧮 Padrões nos Primos")
    
    if 'primelstlst' not in st.session_state:
        st.session_state['primelstlst'] = []
    if 'calculou' not in st.session_state:
        st.session_state['calculou'] = False

    if st.session_state['calculou']:
        primelstlst = st.session_state['primelstlst']
        
        # Lógica de Intervalos
        todos_intervalos = {}
        for x in range(len(primelstlst)-1):
            diff = primelstlst[x+1] - primelstlst[x]
            pair = (primelstlst[x], primelstlst[x+1])
            if diff not in todos_intervalos: todos_intervalos[diff] = []
            todos_intervalos[diff].append(pair)

        # Contagens para verificar dominância
        counts = {k: len(todos_intervalos.get(k, [])) for k in [2, 4, 6, 8, 10]}
        y_values = [primelstlst[i+1] - primelstlst[i] for i in range(len(primelstlst)-1)]
        x_values = primelstlst[:-1]
        dominio_do_6 = (counts[6] > counts[2]) and (counts[6] > counts[4])

        # Abas
        tab_dash, tab_expl, tab_sobre = st.tabs(["📉 Visual", "🔬 Dados", "🎓 Teoria"])

        # === TAB 1: VISUAL ===
        with tab_dash:
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Primos", len(primelstlst))
            c2.metric("Maior Primo", max(primelstlst))
            c3.metric("Intervalos", len(primelstlst)-1)

            st.write("---")
            st.markdown("##### 📍 Dispersão dos Intervalos")
            
            max_y_zoom = st.slider("Zoom Vertical:", 6, max(y_values) if y_values else 100, 30, 2)
            
            # Gráfico ajustado para mobile (mais alto)
            fig, ax = plt.subplots(figsize=(10, 8)) 
            
            x_arr = np.array(x_values)
            y_arr = np.array(y_values)
            mask_1 = (y_arr == 1)
            
            scatter = ax.scatter(
                x_arr[~mask_1], y_arr[~mask_1], s=40, c=y_arr[~mask_1], 
                cmap='Spectral_r', marker='o', alpha=0.9, edgecolors='black', linewidth=0.5
            )
            
            if np.any(mask_1):
                ax.scatter(
                    x_arr[mask_1], y_arr[mask_1], s=120, c='#D500F9', 
                    marker='o', edgecolors='black', linewidth=1.5, label='Gap 1'
                )
            
            ax.set_xlabel("Número Primo (p)", fontsize=14)
            ax.set_ylabel("Tamanho do Intervalo", fontsize=14)
            ax.set_title("Dispersão dos Intervalos", fontsize=16)
            ax.tick_params(axis='both', which='major', labelsize=12)
            ax.set_ylim(0, max_y_zoom + 2)
            ax.set_xlim(0, max(x_values))
            ax.grid(True, axis='y', alpha=0.3)
            st.pyplot(fig, use_container_width=True)

            st.write("---")
            st.markdown("##### 📊 Histograma")
            
            gap_counts = Counter(y_values)
            sorted_gaps = sorted([g for g in gap_counts.keys() if g <= max_y_zoom])
            counts_list = [gap_counts[g] for g in sorted_gaps]
            labels = [str(g) for g in sorted_gaps]

            fig2, ax2 = plt.subplots(figsize=(10, 6))
            bars = ax2.bar(labels, counts_list, color='#4e79a7', edgecolor='black', alpha=0.8)
            ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax2.set_xlabel("Tipo de Intervalo", fontsize=14)
            ax2.set_ylabel("Frequência", fontsize=14)
            ax2.tick_params(axis='both', labelsize=12)
            ax2.grid(axis='y', alpha=0.5)
            
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                        ha='center', va='bottom', fontsize=11, fontweight='bold')
            st.pyplot(fig2, use_container_width=True)

            if dominio_do_6:
                st.success("💡 **Destaque:** O intervalo **6** é o mais comum!")

        # === TAB 2: DADOS (Com a nova funcionalidade) ===
        with tab_expl:
            st.header("🔬 Laboratório de Dados")
            
            # Divide em colunas para mobile (no telemóvel fica um em cima do outro)
            col_left, col_right = st.columns([1, 1])
            
            # --- PARTE NOVA: VER TODOS OS PRIMOS ---
            with col_left:
                st.markdown("### 1. Lista de Primos")
                st.info("Aqui podes ver todos os números encontrados.")
                
                # Tabela simples
                df_todos = pd.DataFrame(primelstlst, columns=["Todos os Primos"])
                st.dataframe(df_todos, height=250, use_container_width=True)
                
                # Botão para baixar só a lista
                csv_todos = df_todos.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 Baixar Lista (CSV)",
                    data=csv_todos,
                    file_name='lista_completa_primos.csv',
                    mime='text/csv',
                    use_container_width=True
                )
                
                st.markdown("---")

            # --- PARTE ANTIGA: ANALISAR INTERVALOS ---
            with col_right:
                st.markdown("### 2. Análise por Intervalo")
                gaps_disponiveis = sorted(todos_intervalos.keys())
                
                if not gaps_disponiveis:
                    st.warning("Sem dados.")
                else:
                    # Seletor
                    gap_escolhido = st.selectbox("Escolha o Intervalo:", options=gaps_disponiveis)
                    
                    # Tabela do intervalo
                    st.markdown(f"**Pares com diferença de {gap_escolhido}:**")
                    df_pares = pd.DataFrame(todos_intervalos[gap_escolhido], columns=["Primo A", "Primo B"])
                    st.dataframe(df_pares, height=250, use_container_width=True)

                    # Exportação Completa Organizada
                    st.markdown("#### Exportar Tudo")
                    export_dict = {}
                    for gap in gaps_disponiveis:
                        col_name = f"Gap {gap}"
                        # Formato (p1, p2) para o Excel não estragar
                        export_dict[col_name] = [f"({p[0]}, {p[1]})" for p in todos_intervalos[gap]]
                    
                    df_export = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in export_dict.items()])).fillna("")
                    csv_data = df_export.to_csv(index=False, sep=';').encode('utf-8-sig')
                    
                    st.download_button(
                        label="💾 Baixar Tabela de Intervalos", 
                        data=csv_data, 
                        file_name='primos_intervalos_organizados.csv', 
                        mime='text/csv', 
                        type='primary', 
                        use_container_width=True
                    )

        # === TAB 3: TEORIA (Explicação Simples e Visual) ===
        with tab_sobre:
            st.header("🎓 A Lógica do Produto (2 x 3)")
            st.markdown("""
            Para um número sobreviver e ser primo, ele tem de passar pelos dois primeiros "filtros" da matemática:
            
            1.  **Filtro do 2:** Não pode ser par.
            2.  **Filtro do 3:** Não pode ser múltiplo de 3.
            
            ### O Segredo do 6
            O número 6 é o **produto perfeito** destes dois filtros:
            $$6 = 2 \\times 3$$
            
            Isto significa que o 6 é "invisível" para estes filtros.
            
            * **Somar 2 ou 4:** É como atirar uma pedra ao acaso. Muitas vezes bate na rede do filtro do 3 e o número é eliminado (não é primo).
            * **Somar 6:** Como o 6 é feito de $2 \\times 3$, somar 6 **não altera** a divisibilidade por 2 nem por 3.
            
            **Conclusão:**
            Se encontrou um buraco na rede (um número primo), a forma mais segura de encontrar outro buraco é dar um salto do tamanho da malha da rede ($2 \\times 3 = 6$).
            """)
            
            st.info("Nota: A visualização foi otimizada para ecrãs móveis.")
            st.caption("TMFC | UAveiro | Catarina, Diogo, Mateus, Micael")

    else:
        # Mensagem clara para mobile
        st.info("👈 **Toque na seta no topo esquerdo** (Sidebar) para definir 'n' e começar.")

if st.session_state['iniciar']:
    mostrar_app_principal()
else:
    mostrar_tela_inicial()
