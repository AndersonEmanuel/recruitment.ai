import streamlit as st

st.set_page_config(
    page_title="Recruitment AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Recruitment AI")
st.caption("Uma suíte integrada para avaliação inteligente de talentos.")

st.markdown(
    """
    ## 👋 Bem-vindo
    Explore as páginas na barra lateral para acessar os fluxos principais da plataforma:

    - **Análise de Currículos** com orquestração via [CrewAI](https://www.crewai.com/).
    - **Estúdio de Áudio** para monitorar e reproduzir fontes de entrada e saída.

    Cada página oferece instruções detalhadas para que você possa começar rapidamente.
    """
)

st.markdown("---")

st.subheader("Como funciona")
st.markdown(
    """
    1. **Configure seus agentes CrewAI** na página de análise para definir o fluxo de avaliação.
    2. **Envie os currículos ou áudios** conforme a necessidade do processo seletivo.
    3. **Acompanhe os resultados** em tempo real e exporte os insights para o seu ATS favorito.
    """
)

st.info(
    "Dica: você pode personalizar prompts e agentes diretamente nas páginas especializadas "
    "para adaptar os resultados ao seu processo seletivo."
)
