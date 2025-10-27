import base64
import importlib.util
from pathlib import Path
from typing import Iterable, List

import streamlit as st

st.set_page_config(page_title="Análise de Currículos", page_icon="🧠", layout="wide")

CREW_AVAILABLE = importlib.util.find_spec("crewai") is not None

if CREW_AVAILABLE:
    from crewai import Agent, Crew, Process, Task  # type: ignore

DEFAULT_PROMPT = (
    "Resuma as principais competências, experiências relevantes e o nível de senioridade "
    "do candidato. Gere também um score de aderência à vaga de 0 a 100 e recomende "
    "próximos passos para a pessoa recrutadora."
)
DEFAULT_TEMPERATURE = 0.2
DEFAULT_PROCESS = "sequential"

st.markdown(
    """
    <style>
        :root {
            --crew-page-background: linear-gradient(120deg, rgba(91,141,239,0.08), rgba(37,99,235,0.04));
            --crew-card-surface: #ffffff;
            --crew-card-border: #d6dcf5;
            --crew-card-shadow: rgba(15, 23, 42, 0.08);
            --crew-step-border: #e3e8f0;
            --crew-step-shadow: rgba(15, 23, 42, 0.08);
            --crew-hero-background: linear-gradient(135deg, #1f3b65, #5b8def);
            --crew-hero-shadow: rgba(31, 59, 101, 0.35);
            --crew-text-strong: #1e293b;
            --crew-text-muted: #475569;
            --crew-file-list-bg: #f8fafc;
            --crew-file-list-border: #e2e8f0;
        }
        html[data-theme="dark"] {
            --crew-page-background: linear-gradient(135deg, rgba(15,23,42,0.92), rgba(30,64,175,0.35));
            --crew-card-surface: rgba(15, 23, 42, 0.72);
            --crew-card-border: rgba(148, 163, 184, 0.28);
            --crew-card-shadow: rgba(2, 6, 23, 0.6);
            --crew-step-border: rgba(148, 163, 184, 0.25);
            --crew-step-shadow: rgba(8, 12, 34, 0.65);
            --crew-hero-background: linear-gradient(135deg, rgba(37,99,235,0.75), rgba(15,23,42,0.85));
            --crew-hero-shadow: rgba(8, 12, 34, 0.7);
            --crew-text-strong: #e2e8f0;
            --crew-text-muted: rgba(226, 232, 240, 0.75);
            --crew-file-list-bg: rgba(30, 41, 59, 0.65);
            --crew-file-list-border: rgba(148, 163, 184, 0.35);
        }
        body {
            background: var(--crew-page-background);
        }
        main .block-container {
            padding: 2.4rem 3rem 3rem;
            max-width: 1180px;
        }
        .crew-hero {
            background: var(--crew-hero-background);
            padding: 2.8rem;
            border-radius: 1.5rem;
            color: #ffffff;
            margin-bottom: 2rem;
            box-shadow: 0 18px 45px var(--crew-hero-shadow);
        }
        .crew-hero h1 {
            font-size: 2.2rem;
            margin-bottom: 0.6rem;
        }
        .crew-hero p {
            font-size: 1.05rem;
            opacity: 0.85;
        }
        .crew-form {
            background: var(--crew-card-surface);
            border-radius: 1.2rem;
            padding: 1.6rem;
            border: 1px solid var(--crew-card-border);
            box-shadow: 0 16px 40px var(--crew-card-shadow);
            margin-bottom: 2rem;
        }
        .crew-form, .crew-step-card, .result-card, .file-list {
            color: var(--crew-text-strong);
        }
        .crew-step-card {
            background-color: var(--crew-card-surface);
            border-radius: 1rem;
            padding: 1.2rem;
            border: 1px solid var(--crew-step-border);
            box-shadow: 0 8px 22px var(--crew-step-shadow);
            height: 100%;
        }
        .crew-step-card h3 {
            font-size: 1.1rem;
            margin-top: 0.75rem;
            margin-bottom: 0.4rem;
            color: var(--crew-text-strong);
        }
        .crew-step-card p {
            font-size: 0.95rem;
            color: var(--crew-text-muted);
        }
        .crew-step-icon {
            font-size: 1.7rem;
        }
        .crew-section-title {
            font-size: 1.4rem;
            margin-bottom: 0.6rem;
            color: var(--crew-text-strong);
        }
        .crew-action-row {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }
        .crew-action-row .stButton button {
            width: 100%;
            border-radius: 999px;
            padding: 0.65rem 1.2rem;
            font-weight: 600;
            background: linear-gradient(135deg, rgba(37,99,235,0.88), rgba(30,64,175,0.92));
            border: none;
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.25);
        }
        html[data-theme="dark"] .crew-action-row .stButton button {
            box-shadow: 0 12px 24px rgba(37, 99, 235, 0.35);
        }
        .crew-action-row .stButton button:hover {
            transform: translateY(-1px);
        }
        .crew-action-row .stButton:nth-child(2) button {
            background: transparent;
            border: 1px solid rgba(37,99,235,0.4);
            color: #1d4ed8;
            box-shadow: none;
        }
        html[data-theme="dark"] .crew-action-row .stButton:nth-child(2) button {
            color: rgba(191, 219, 254, 0.9);
            border-color: rgba(96, 165, 250, 0.55);
        }
        .result-card {
            background-color: var(--crew-card-surface);
            border-radius: 1.1rem;
            padding: 1.6rem;
            border: 1px solid var(--crew-card-border);
            box-shadow: 0 12px 24px var(--crew-card-shadow);
            margin-bottom: 1.3rem;
        }
        .result-card h4 {
            margin-top: 0;
            margin-bottom: 0.8rem;
            color: var(--crew-text-strong);
        }
        .result-card pre {
            white-space: pre-wrap;
        }
        .file-list {
            background-color: var(--crew-file-list-bg);
            border-radius: 1rem;
            padding: 1.2rem;
            border: 1px solid var(--crew-file-list-border);
        }
        .file-list li {
            margin-bottom: 0.35rem;
        }
        .file-list strong {
            color: var(--crew-text-strong);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="crew-hero">
        <h1>📄 Análise de Currículos com CrewAI</h1>
        <p>
            Centralize a triagem de currículos em uma experiência moderna. Faça upload dos arquivos,
            deixe que a CrewAI cuide da inteligência por trás das análises e receba respostas claras
            para priorizar candidatos.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='crew-section-title'>Como funciona</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        """
        <div class="crew-step-card">
            <div class="crew-step-icon">🗂️</div>
            <h3>Organize os arquivos</h3>
            <p>Envie currículos em PDF, DOCX ou TXT. A aplicação cuida da leitura e pré-processamento.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class="crew-step-card">
            <div class="crew-step-icon">🤖</div>
            <h3>Execução inteligente</h3>
            <p>A CrewAI infere automaticamente prompts, agentes e parâmetros para cada análise.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col3:
    st.markdown(
        """
        <div class="crew-step-card">
            <div class="crew-step-icon">📊</div>
            <h3>Resultados acionáveis</h3>
            <p>Receba resumos estruturados, competências-chave e um score de aderência à vaga.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='crew-section-title'>Envie os currículos para análise</div>", unsafe_allow_html=True)
st.caption("Aceitamos múltiplos arquivos de uma só vez. Limite máximo: 10 MB por arquivo.")

st.markdown("<div class='crew-form'>", unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "Arraste e solte ou clique para selecionar currículos",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    key="curriculos",
)

st.markdown("<div class='crew-action-row'>", unsafe_allow_html=True)
col_run, col_reset = st.columns([2, 1])
run_analysis = col_run.button("🚀 Analisar com CrewAI", use_container_width=True)
if col_reset.button("Limpar envios", use_container_width=True):
    st.session_state.pop("curriculos", None)
    st.session_state.pop("analysis_results", None)
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

if "analysis_results" not in st.session_state:
    st.session_state["analysis_results"] = []

if not CREW_AVAILABLE:
    st.info(
        "O pacote `crewai` não foi encontrado no ambiente. Instale-o com `pip install crewai` "
        "para habilitar a orquestração real com agentes. Enquanto isso, mostramos uma simulação "
        "para ilustrar o fluxo de trabalho.",
    )


def _fake_analysis(file_name: str, preview: str) -> str:
    """Retorna um texto de exemplo quando CrewAI não está disponível."""
    return (
        f"**Arquivo:** {file_name}\n\n"
        f"Resumo simulado: {preview[:400]}...\n\n"
        f"Pontuação estimada: 75/100 (temperatura {DEFAULT_TEMPERATURE:.2f})\n"
        "Próximo passo sugerido: convidar o candidato para uma entrevista inicial."
    )


def _read_file_preview(file) -> str:
    data = file.getvalue()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return base64.b64encode(data).decode("ascii")


def _build_tasks(files: Iterable) -> List["Task"]:
    tasks: List["Task"] = []
    for file in files:
        preview = _read_file_preview(file)
        tasks.append(
            Task(
                description=f"Analise o currículo `{file.name}` e produza um resumo estruturado.",
                expected_output="Resumo, principais competências, score de aderência e próximos passos",
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
                    "prompt": DEFAULT_PROMPT,
                    "temperature": DEFAULT_TEMPERATURE,
                },
            )
        )
    return tasks


analysis_ran = False
if run_analysis and uploaded_files:
    with st.spinner("Executando CrewAI..."):
        results_payload = []
        if CREW_AVAILABLE:
            tasks = _build_tasks(uploaded_files)
            crew = Crew(
                agents=[task.agent for task in tasks],
                tasks=tasks,
                process=Process.sequential if DEFAULT_PROCESS == "sequential" else Process.hierarchical,
                verbose=True,
            )
            raw_results = crew.kickoff()

            if isinstance(raw_results, list):
                for file, result in zip(uploaded_files, raw_results):
                    results_payload.append({"title": file.name, "content": str(result)})
            else:
                results_payload.append({"title": "Resultado da análise", "content": str(raw_results)})
        else:
            for file in uploaded_files:
                preview = _read_file_preview(file)
                results_payload.append(
                    {"title": file.name, "content": _fake_analysis(file.name, preview)}
                )
        st.session_state["analysis_results"] = results_payload
        analysis_ran = True
elif run_analysis and not uploaded_files:
    st.warning("Envie pelo menos um currículo antes de iniciar a análise.")

if analysis_ran:
    st.success("Análises concluídas! Confira os resultados abaixo.")

analysis_results = st.session_state.get("analysis_results", [])
if analysis_results:
    st.markdown("---")
    st.markdown("<div class='crew-section-title'>Resultados gerados</div>", unsafe_allow_html=True)
    for result in analysis_results:
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.markdown(f"#### {result['title']}")
        st.markdown(result["content"])
        st.markdown("</div>", unsafe_allow_html=True)
elif uploaded_files:
    st.caption("Tudo pronto! Clique em \"Analisar com CrewAI\" para começar.")
else:
    st.caption("Nenhum arquivo enviado até o momento.")

if uploaded_files:
    st.markdown("---")
    st.markdown("<div class='crew-section-title'>Arquivos enviados</div>", unsafe_allow_html=True)
    st.markdown("<ul class='file-list'>", unsafe_allow_html=True)
    for file in uploaded_files:
        file_path = Path(file.name)
        st.markdown(
            f"<li><strong>{file_path.name}</strong> — {file.size / 1024:.1f} KB</li>",
            unsafe_allow_html=True,
        )
    st.markdown("</ul>", unsafe_allow_html=True)
