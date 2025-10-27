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
        body {
            background: radial-gradient(circle at 0% 0%, rgba(67,97,238,0.08), transparent 55%),
                        radial-gradient(circle at 100% 0%, rgba(114,9,183,0.06), transparent 45%),
                        #f5f7fb;
        }
        main .block-container {
            padding: 2.5rem 3rem 3.5rem;
            max-width: 1200px;
        }
        .hero-card {
            background: linear-gradient(135deg, rgba(67,97,238,0.16), rgba(114,9,183,0.12));
            border: 1px solid rgba(67, 97, 238, 0.18);
            border-radius: 22px;
            padding: 2.8rem 3rem;
            margin-bottom: 2.8rem;
            box-shadow: 0 18px 45px rgba(67, 97, 238, 0.12);
        }
        .hero-card h1 {
            margin-bottom: 0.5rem;
            font-size: 2.8rem;
        }
        .hero-card p {
            font-size: 1.08rem;
            color: rgba(38, 39, 48, 0.78);
            max-width: 760px;
        }
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            background: rgba(67, 97, 238, 0.16);
            color: #1f2a56;
            padding: 0.4rem 1rem;
            border-radius: 999px;
            font-weight: 600;
            font-size: 0.86rem;
            letter-spacing: 0.02em;
        }
        .stats-row {
            margin-bottom: 2.2rem;
        }
        .stats-row div[data-testid="stMetric"] {
            background: #ffffff;
            border-radius: 18px;
            border: 1px solid rgba(67, 97, 238, 0.08);
            box-shadow: 0 12px 36px rgba(15, 23, 42, 0.08);
            padding: 1.4rem 1.6rem;
            height: 100%;
        }
        .stats-row div[data-testid="stMetric"] label {
            color: #1f2937;
            font-weight: 600;
        }
        .stats-row div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
            color: #111827;
            font-size: 2rem;
        }
        .stats-row div[data-testid="stMetric"] div[data-testid="stMetricDelta"] span {
            background: rgba(16, 185, 129, 0.12);
            border-radius: 12px;
            padding: 0.2rem 0.55rem;
            color: #047857;
        }
        .quick-card {
            background: #ffffff;
            border-radius: 18px;
            padding: 1.35rem 1.5rem;
            border: 1px solid rgba(15, 23, 42, 0.08);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
            height: 100%;
        }
        .quick-card .stLinkButton button,
        .quick-card div[data-testid="stPageLink"] a {
            width: 100%;
            border-radius: 999px;
            padding: 0.55rem 1rem;
            font-weight: 600;
            background: linear-gradient(135deg, rgba(67,97,238,0.16), rgba(114,9,183,0.2));
            border: none;
            color: #1f1f3d;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .quick-card .stLinkButton button:hover,
        .quick-card div[data-testid="stPageLink"] a:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 28px rgba(67, 97, 238, 0.28);
        }
        .quick-card span.helper {
            font-size: 0.85rem;
            color: rgba(15, 23, 42, 0.66);
        }
        .card-highlight {
            border-radius: 18px;
            border: 1px solid rgba(142, 150, 175, 0.18);
            background-color: rgba(255, 255, 255, 0.85);
            padding: 1.65rem;
            height: 100%;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
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
            margin-bottom: 1.5rem;
            padding-left: 0.3rem;
        }
        .timeline-step::before {
            content: "";
            position: absolute;
            left: -1.62rem;
            top: 0.4rem;
            width: 0.75rem;
            height: 0.75rem;
            background: linear-gradient(135deg, #4361ee, #7209b7);
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
        @media (max-width: 992px) {
            main .block-container {
                padding: 1.8rem 1.5rem 2.5rem;
            }
            .hero-card {
                padding: 2.2rem 2.4rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

page_link = getattr(st, "page_link", None)

with st.sidebar:
    if page_link:
        page_link("app.py", label="Home", icon="🏠")
        page_link("pages/1_analise_de_curriculos.py", label="Análise de Currículos", icon="🧠")
        page_link("pages/2_audio_studio.py", label="Estúdio de Áudio", icon="🎧")
    else:
        st.markdown("[🏠 Home](app.py)")
        st.markdown("[🧠 Análise de Currículos](pages/1_analise_de_curriculos.py)")
        st.markdown("[🎧 Estúdio de Áudio](pages/2_audio_studio.py)")

st.markdown(
    """<div class="hero-card">
    <span class="pill">Nova experiência unificada</span>
    <h1>Recruitment AI</h1>
    <p>Centralize a avaliação de talentos com fluxos inteligentes, colaboração entre agentes e monitoramento multimídia em um só lugar.</p>
    </div>""",
    unsafe_allow_html=True,
)

stat_columns = st.columns(3)
for column, metric_args, description in zip(
    stat_columns,
    (
        ("Automação ativa", "2 fluxos", "+4 planejados"),
        ("Tempo médio", "12 min", "-35% vs. processo manual"),
        ("Qualidade de matching", "92%", "\u2191 8 p.p"),
    ),
    (
        "Empodere agentes para analisar currículos com scoring consistente e transparente.",
        "Reduza o tempo de triagem com pipelines padronizados e geração automática de relatórios.",
        "Melhore a assertividade das recomendações com insights contextualizados e critérios flexíveis.",
    ),
):
    with column:
        st.markdown("<div class='stats-row'>", unsafe_allow_html=True)
        st.metric(*metric_args)
        st.caption(description)
        st.markdown("</div>", unsafe_allow_html=True)

st.subheader("Comece em segundos")
quick_cols = st.columns(3)
quick_descriptions = (
    "Acompanhe a triagem inteligente com agentes configurados para currículos complexos.",
    "Controle dispositivos, registre entrevistas e organize áudios com clareza.",
    "Converse com o time para adaptar a plataforma ao seu processo de recrutamento.",
)

with quick_cols[0]:
    st.markdown("<div class='quick-card'>", unsafe_allow_html=True)
    if page_link:
        page_link("pages/1_analise_de_curriculos.py", label="🚀 Abrir análise de currículos")
    else:
        st.markdown("[🚀 Abrir análise de currículos](pages/1_analise_de_curriculos.py)")
    st.markdown(f"<span class='helper'>{quick_descriptions[0]}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with quick_cols[1]:
    st.markdown("<div class='quick-card'>", unsafe_allow_html=True)
    if page_link:
        page_link("pages/2_audio_studio.py", label="🎙️ Entrar no estúdio de áudio")
    else:
        st.markdown("[🎙️ Entrar no estúdio de áudio](pages/2_audio_studio.py)")
    st.markdown(f"<span class='helper'>{quick_descriptions[1]}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
with quick_cols[2]:
    st.markdown("<div class='quick-card'>", unsafe_allow_html=True)
    st.link_button("Falar com nossa equipe", "mailto:suporte@recruitment.ai")
    st.markdown(f"<span class='helper'>{quick_descriptions[2]}</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

st.subheader("Como funciona")
st.markdown(
    """<div class="timeline">
    <div class="timeline-step">
        <h4>1. Configure seus agentes inteligentes</h4>
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
