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

col1, col2 = st.columns(2)
with col1:
    st.subheader("Comece pela Análise de Currículos")
    st.write(
        """
        Faça upload de vários currículos em PDF, DOCX ou TXT e gere resumos automáticos,
        pontuações e insights sobre os candidatos. Ideal para triagens em lote.
        """
    )
    if st.button("📄 Ir para Análise de Currículos", use_container_width=True):
        st.switch_page("pages/1_analise_de_curriculos.py")

with col2:
    st.subheader("Gerencie os áudios do seu computador")
    st.write(
        """
        Selecione fontes de áudio de entrada ou saída, faça upload de trechos gravados e
        monitore tudo em um painel centralizado para entrevistas ou dinâmicas remotas.
        """
    )
    if st.button("🎧 Ir para Estúdio de Áudio", use_container_width=True):
        st.switch_page("pages/2_audio_studio.py")

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
