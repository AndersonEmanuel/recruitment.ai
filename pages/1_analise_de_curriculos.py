import base64
import importlib.util
from pathlib import Path
from typing import Iterable, List

import streamlit as st

CREW_AVAILABLE = importlib.util.find_spec("crewai") is not None

if CREW_AVAILABLE:
    from crewai import Agent, Crew, Process, Task  # type: ignore


st.title("📄 Análise de Currículos com CrewAI")
st.write(
    """
    Faça upload de múltiplos currículos para rodar análises em lote com o suporte de agentes
    CrewAI. Personalize prompts, parâmetros e acompanhe os resultados diretamente abaixo.
    """
)

st.sidebar.header("Configurações de Execução")
prompt_base = st.sidebar.text_area(
    "Prompt base para os agentes",
    value=(
        "Resuma as principais competências, experiências relevantes e nível de senioridade "
        "do candidato. Gere também um score de aderência à vaga de 0 a 100."
    ),
    height=160,
)

processo = st.sidebar.selectbox(
    "Orquestração",
    options=["sequential", "hierarchical"],
    help="Determina como as tarefas do Crew serão encadeadas.",
)

temperatura = st.sidebar.slider(
    "Temperatura criativa",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.05,
)

st.markdown("---")

st.subheader("Uploads de Currículos")
uploaded_files = st.file_uploader(
    "Arraste e solte vários arquivos (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    key="curriculos",
)

col_run, col_reset = st.columns([2, 1])
run_analysis = col_run.button("🚀 Rodar análise com CrewAI", use_container_width=True)
if col_reset.button("Limpar uploads", use_container_width=True):
    st.session_state.pop("curriculos", None)
    st.rerun()

if not CREW_AVAILABLE:
    st.info(
        "O pacote `crewai` não foi encontrado no ambiente. Instale-o com `pip install crewai` "
        "para habilitar a orquestração real com agentes. Abaixo exibimos uma simulação." 
    )


def _fake_analysis(file_name: str, preview: str) -> str:
    """Retorna um texto de exemplo quando CrewAI não está disponível."""
    return (
        f"**Arquivo:** {file_name}\n\n"
        f"Resumo simulado: {preview[:400]}...\n\n"
        f"Pontuação estimada: 75/100 (temperatura {temperatura:.2f})\n"
    )


def _read_file_preview(file) -> str:
    data = file.getvalue()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return base64.b64encode(data).decode("ascii")


def _build_tasks(files: Iterable) -> List[Task]:
    tasks: List[Task] = []
    for file in files:
        preview = _read_file_preview(file)
        tasks.append(
            Task(
                description=f"Analise o currículo `{file.name}` e produza um resumo estruturado.",
                expected_output="Resumo, principais competências e score de aderência",
                agent=Agent(
                    role="Analista de Currículos",
                    goal="Classificar rapidamente candidatos em uma triagem inicial.",
                    backstory=(
                        "Especialista em recrutamento técnico com experiência em triagens de alto volume."
                    ),
                    verbose=True,
                    allow_delegation=False,
                ),
                input_data={
                    "file_name": file.name,
                    "preview": preview,
                    "prompt": prompt_base,
                    "temperature": temperatura,
                },
            )
        )
    return tasks


if run_analysis and uploaded_files:
    with st.spinner("Executando CrewAI..."):
        if CREW_AVAILABLE:
            tasks = _build_tasks(uploaded_files)
            crew = Crew(
                agents=[task.agent for task in tasks],
                tasks=tasks,
                process=Process.sequential if processo == "sequential" else Process.hierarchical,
                verbose=True,
            )
            results = crew.kickoff()

            if isinstance(results, list):
                for idx, result in enumerate(results, start=1):
                    st.markdown(f"### Resultado {idx}")
                    st.write(result)
            else:
                st.write(results)
        else:
            for file in uploaded_files:
                preview = _read_file_preview(file)
                st.markdown(f"### Resultado: {file.name}")
                st.markdown(_fake_analysis(file.name, preview))
else:
    if uploaded_files:
        st.write("Pronto para analisar. Clique em \"Rodar análise com CrewAI\" para começar.")
    else:
        st.caption("Nenhum arquivo enviado até o momento.")

if uploaded_files:
    st.markdown("---")
    st.subheader("Arquivos enviados")
    for file in uploaded_files:
        file_path = Path(file.name)
        st.write(f"• {file_path.name} ({file.size / 1024:.1f} KB)")
