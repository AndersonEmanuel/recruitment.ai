import base64
import binascii
import json
from datetime import datetime
from typing import Optional, Tuple

import streamlit as st
import streamlit.components.v1 as components


def _browser_audio_recorder(element_id: str = "browser-recorder") -> Optional[Tuple[bytes, str]]:
    """Renderiza um componente HTML que grava áudio pelo navegador."""

    component_value = components.html(
        f"""
        <div id="{element_id}-container" style="padding:0.75rem;border:1px solid var(--secondary-background-color,#d6d6d6);border-radius:0.5rem;">
            <div style="display:flex;gap:0.5rem;flex-wrap:wrap;align-items:center;">
                <button id="{element_id}-start" style="padding:0.4rem 1rem;border:none;border-radius:999px;background-color:#f63366;color:white;font-weight:600;cursor:pointer;">Iniciar gravação</button>
                <button id="{element_id}-stop" style="padding:0.4rem 1rem;border-radius:999px;border:1px solid #f63366;background-color:white;color:#f63366;font-weight:600;cursor:pointer;" disabled>Parar</button>
                <span id="{element_id}-status" style="font-size:0.9rem;color:#6c757d;">Pronto para gravar.</span>
            </div>
            <audio id="{element_id}-player" controls style="margin-top:0.75rem;width:100%;display:none;"></audio>
        </div>
        <script>
        (function() {{
            const startBtn = document.getElementById("{element_id}-start");
            const stopBtn = document.getElementById("{element_id}-stop");
            const statusLabel = document.getElementById("{element_id}-status");
            const player = document.getElementById("{element_id}-player");
            let mediaStream = null;
            let recorder = null;
            let chunks = [];

            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {{
                statusLabel.textContent = "Seu navegador não suporta captura de áudio.";
                startBtn.disabled = true;
                stopBtn.disabled = true;
                return;
            }}

            function postValue(value) {{
                window.parent.postMessage({{
                    isStreamlitMessage: true,
                    type: "streamlit:setComponentValue",
                    value: value
                }}, "*");
            }}

            async function ensureStream() {{
                if (mediaStream) {{
                    return mediaStream;
                }}
                try {{
                    mediaStream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                    return mediaStream;
                }} catch (err) {{
                    statusLabel.textContent = "Permita o acesso ao microfone para gravar.";
                    console.error(err);
                    return null;
                }}
            }}

            startBtn.addEventListener("click", async () => {{
                const stream = await ensureStream();
                if (!stream) {{
                    return;
                }}

                if (recorder && recorder.state !== "inactive") {{
                    recorder.stop();
                }}

                chunks = [];
                try {{
                    recorder = new MediaRecorder(stream);
                }} catch (err) {{
                    statusLabel.textContent = "Não foi possível iniciar a gravação.";
                    console.error(err);
                    return;
                }}

                recorder.ondataavailable = (event) => {{
                    if (event.data && event.data.size > 0) {{
                        chunks.push(event.data);
                    }}
                }};

                recorder.onstop = () => {{
                    const blob = new Blob(chunks, {{ type: recorder.mimeType }});
                    if (player.src) {{
                        URL.revokeObjectURL(player.src);
                    }}
                    player.src = URL.createObjectURL(blob);
                    player.style.display = "block";

                    const reader = new FileReader();
                    reader.onloadend = () => {{
                        const base64 = reader.result.split(",")[1];
                        const payload = JSON.stringify({{
                            data: base64,
                            mimeType: blob.type
                        }});
                        postValue(payload);
                    }};
                    reader.readAsDataURL(blob);

                    statusLabel.textContent = "Gravação pronta para reprodução.";
                }};

                postValue(null);
                recorder.start();
                statusLabel.textContent = "Gravando... clique em Parar para finalizar.";
                startBtn.disabled = true;
                stopBtn.disabled = false;
            }});

            stopBtn.addEventListener("click", () => {{
                if (recorder && recorder.state !== "inactive") {{
                    recorder.stop();
                }}
                stopBtn.disabled = true;
                startBtn.disabled = false;
            }});
        }})();
        </script>
        """,
        height=240,
    )

    if component_value:
        try:
            payload = json.loads(component_value)
        except json.JSONDecodeError:
            return None

        if not payload or not isinstance(payload, dict):
            return None

        data_b64 = payload.get("data")
        if not data_b64:
            return None

        mime_type = payload.get("mimeType", "audio/webm")
        try:
            audio_bytes = base64.b64decode(data_b64)
        except (binascii.Error, ValueError):
            return None

        return audio_bytes, mime_type

    return None

st.title("🎧 Estúdio de Áudio")
st.write(
    """
    Controle as fontes de áudio do seu computador durante entrevistas remotas. Escolha se
    deseja monitorar o microfone (entrada), os alto-falantes (saída) ou ambos e faça upload
    de arquivos para reprodução ou compartilhamento.
    """
)

st.sidebar.header("Fontes ativas")
monitor_input = st.sidebar.toggle("Habilitar monitoramento da entrada (microfone)", value=True)
monitor_output = st.sidebar.toggle("Habilitar monitoramento da saída (alto-falantes)", value=False)

audio_mode = st.sidebar.radio(
    "Modo de escuta",
    options=["Tempo real", "Upload de arquivo"],
    help="Selecione se deseja ouvir o áudio do dispositivo ou carregar um arquivo gravado.",
)

st.markdown("---")

col_status, col_timestamp = st.columns([3, 1])
with col_status:
    if monitor_input and monitor_output:
        st.success("Monitorando entrada e saída de áudio.")
    elif monitor_input:
        st.info("Monitorando apenas o microfone.")
    elif monitor_output:
        st.info("Monitorando apenas os alto-falantes.")
    else:
        st.warning("Nenhuma fonte de áudio habilitada.")

with col_timestamp:
    st.caption(f"Última atualização: {datetime.now().strftime('%H:%M:%S')}")

if audio_mode == "Tempo real":
    st.subheader("Escuta em tempo real")
    st.write(
        """
        Utilize seu software preferido (ex.: OBS, VoiceMeeter, Loopback) para direcionar o áudio
        do dispositivo para esta página. Quando habilitado, você poderá visualizar os níveis
        de entrada e saída abaixo.
        """
    )

    volume_input = st.slider("Nível do microfone", 0, 100, 65, help="Ajuste conforme sua mesa de som")
    volume_output = st.slider("Nível dos alto-falantes", 0, 100, 55)

    st.progress(volume_input / 100, text="Nível atual da entrada")
    st.progress(volume_output / 100, text="Nível atual da saída")

    st.markdown("---")

    st.subheader("Gravação rápida pelo navegador")
    st.write(
        "Utilize os botões abaixo para gravar diretamente no navegador e gerar um arquivo para download."
    )

    if "recorded_audio" not in st.session_state:
        st.session_state.recorded_audio = None
    if "recorded_mime" not in st.session_state:
        st.session_state.recorded_mime = "audio/webm"

    recorded_payload = _browser_audio_recorder()
    if recorded_payload:
        audio_bytes, mime_type = recorded_payload
        st.session_state.recorded_audio = audio_bytes
        st.session_state.recorded_mime = mime_type

    if st.session_state.recorded_audio:
        st.success("Gravação finalizada! Ouça ou baixe o arquivo abaixo.")
        st.audio(st.session_state.recorded_audio, format=st.session_state.recorded_mime)

        extension_map = {
            "audio/webm": "webm",
            "audio/ogg": "ogg",
            "audio/wav": "wav",
            "audio/mp3": "mp3",
            "audio/mpeg": "mp3",
            "audio/mp4": "m4a",
        }
        file_extension = extension_map.get(st.session_state.recorded_mime, "webm")

        st.download_button(
            "Baixar gravação",
            data=st.session_state.recorded_audio,
            file_name=f"gravacao_{datetime.now().strftime('%H%M%S')}.{file_extension}",
            mime=st.session_state.recorded_mime,
        )
    else:
        st.caption("Nenhuma gravação disponível ainda.")
else:
    st.subheader("Upload e reprodução")
    uploaded_audio = st.file_uploader(
        "Faça upload de um arquivo de áudio (MP3, WAV, M4A)",
        type=["mp3", "wav", "m4a", "ogg"],
    )

    if uploaded_audio is not None:
        st.audio(uploaded_audio, format=f"audio/{uploaded_audio.type.split('/')[-1]}")

        st.write("Configurações de reprodução")
        playback_speed = st.select_slider(
            "Velocidade",
            options=["0.5x", "0.75x", "1x", "1.25x", "1.5x"],
            value="1x",
        )
        loop_audio = st.checkbox("Repetir áudio em loop", value=False)

        st.success(
            f"Reproduzindo {uploaded_audio.name} na velocidade {playback_speed}"
            + (" com loop ativado." if loop_audio else ".")
        )
    else:
        st.info("Nenhum arquivo de áudio enviado. Faça upload para iniciar a reprodução.")

st.markdown("---")

st.subheader("Preferências avançadas")
latency: Optional[int] = st.number_input(
    "Latência máxima permitida (ms)",
    min_value=10,
    max_value=500,
    value=120,
    step=10,
    help="Ideal para ajustar buffers ao trabalhar com softwares externos.",
)

st.write(
    """
    Ajuste a latência de acordo com a infraestrutura da sua equipe. Valores menores reduzem o
    atraso, mas exigem conexões estáveis. Valores maiores priorizam estabilidade em chamadas.
    """
)

st.button("Salvar preferências", type="primary")
