import streamlit as st

st.set_page_config(
    page_title="Recruitment AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .hero-card {
            background: linear-gradient(135deg, rgba(67,97,238,0.12), rgba(114,9,183,0.08));
            border: 1px solid rgba(67, 97, 238, 0.18);
            border-radius: 18px;
            padding: 2.5rem 2.8rem;
            margin-bottom: 2.5rem;
        }
        .hero-card h1 {
            margin-bottom: 0.5rem;
            font-size: 2.7rem;
        }
        .hero-card p {
            font-size: 1.1rem;
            color: rgba(38, 39, 48, 0.8);
        }
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(67, 97, 238, 0.16);
            color: #2b2c34;
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.85rem;
        }
        .card-highlight {
            border-radius: 16px;
            border: 1px solid rgba(142, 150, 175, 0.18);
            background-color: rgba(255, 255, 255, 0.7);
            padding: 1.5rem;
            height: 100%;
        }
        .card-highlight h4 {
            margin-bottom: 0.75rem;
        }
        .timeline {
            border-left: 2px solid rgba(67, 97, 238, 0.2);
            margin-top: 1.4rem;
            padding-left: 1.2rem;
        }
        .timeline-step {
            position: relative;
            margin-bottom: 1.4rem;
        }
        .timeline-step::before {
            content: "";
            position: absolute;
            left: -1.55rem;
            top: 0.3rem;
            width: 0.75rem;
            height: 0.75rem;
            background: #4361ee;
            border-radius: 50%;
            box-shadow: 0 0 0 4px rgba(67, 97, 238, 0.18);
        }
        .sidebar-box {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 1.2rem;
            margin-bottom: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

page_link = getattr(st, "page_link", None)

with st.sidebar:
    st.markdown("""<div class="sidebar-box"><h3>🚀 Fluxos principais</h3></div>""", unsafe_allow_html=True)
    if page_link:
        page_link("pages/1_analise_de_curriculos.py", label="Análise de Currículos", icon="🧠")
        page_link("pages/2_audio_studio.py", label="Estúdio de Áudio", icon="🎧")
    else:
        st.markdown("[🧠 Análise de Currículos](pages/1_analise_de_curriculos.py)")
        st.markdown("[🎧 Estúdio de Áudio](pages/2_audio_studio.py)")
    st.markdown("""<div class="sidebar-box">
        <h4>Guia rápido</h4>
        <ul>
            <li>Defina seus agentes CrewAI.</li>
            <li>Carregue currículos e áudios.</li>
            <li>Monitore insights em tempo real.</li>
        </ul>
        </div>""", unsafe_allow_html=True)
    st.markdown("""<div class="sidebar-box">
        <strong>Dica:</strong> personalize prompts e habilidades para adaptar a jornada ao seu processo.
        </div>""", unsafe_allow_html=True)

st.markdown(
    """<div class="hero-card">
    <span class="pill">Nova experiência unificada</span>
    <h1>Recruitment AI</h1>
    <p>Centralize a avaliação de talentos com fluxos inteligentes, colaboração entre agentes e monitoramento multimídia em um só lugar.</p>
    </div>""",
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Automação ativa", "2 fluxos", "+4 planejados")
    st.markdown("Empodere agentes para analisar currículos com scoring consistente e transparente.")
with col2:
    st.metric("Tempo médio", "12 min", "-35% vs. processo manual")
    st.markdown("Reduza o tempo de triagem com pipelines padronizados e geração automática de relatórios.")
with col3:
    st.metric("Qualidade de matching", "92%", "\u2191 8 p.p")
    st.markdown("Melhore a assertividade das recomendações com insights contextualizados e critérios flexíveis.")

st.subheader("Comece em segundos")
quick_cols = st.columns(3)
with quick_cols[0]:
    if page_link:
        page_link("pages/1_analise_de_curriculos.py", label="🚀 Abrir análise de currículos")
    else:
        st.markdown("[🚀 Abrir análise de currículos](pages/1_analise_de_curriculos.py)")
with quick_cols[1]:
    if page_link:
        page_link("pages/2_audio_studio.py", label="🎙️ Entrar no estúdio de áudio")
    else:
        st.markdown("[🎙️ Entrar no estúdio de áudio](pages/2_audio_studio.py)")
with quick_cols[2]:
    st.link_button("Ver documentação do CrewAI", "https://docs.crewai.com/")

st.markdown("---")

st.subheader("Como funciona")
st.markdown(
    """<div class="timeline">
    <div class="timeline-step">
        <h4>1. Configure seus agentes CrewAI</h4>
        <p>Personalize personas, ferramentas e prompts diretamente no fluxo de análise para se adequar às competências que deseja mapear.</p>
    </div>
    <div class="timeline-step">
        <h4>2. Centralize currículos e áudios</h4>
        <p>Suba arquivos, acompanhe a transcrição de entrevistas e mantenha todo o histórico de decisões do time.</p>
    </div>
    <div class="timeline-step">
        <h4>3. Gere insights acionáveis</h4>
        <p>Exporte relatórios e compartilhe recomendações com o seu ATS e gestores com apenas um clique.</p>
    </div>
    </div>""",
    unsafe_allow_html=True,
)

st.subheader("Por que equipes escolhem o Recruitment AI")
info_col1, info_col2 = st.columns(2)
with info_col1:
    st.markdown(
        """<div class="card-highlight">
        <h4>Operações conectadas</h4>
        <p>Integre facilmente com seu stack atual e acompanhe KPIs de contratação em dashboards prontos para uso.</p>
        </div>""",
        unsafe_allow_html=True,
    )
with info_col2:
    st.markdown(
        """<div class="card-highlight">
        <h4>Experiência centrada no candidato</h4>
        <p>Utilize áudios, resumos e insights personalizados para oferecer feedback rápido e consistente.</p>
        </div>""",
        unsafe_allow_html=True,
    )

st.info(
    "Pronto para expandir? Adicione novas páginas à barra lateral para testar fluxos como entrevistas automáticas, feedback de gestores e muito mais.",
)
