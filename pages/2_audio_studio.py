from datetime import datetime
from io import BytesIO
from typing import Optional

import numpy as np
import streamlit as st
from streamlit_webrtc import AudioProcessorBase, WebRtcMode, webrtc_streamer


class AudioRecorder(AudioProcessorBase):
    """Captura quadros de áudio do navegador para gerar um arquivo WAV."""

    def __init__(self) -> None:
        self.frames = []

    def recv(self, frame):  # type: ignore[override]
        self.frames.append(frame)
        return frame


def _frames_to_wav(frames) -> Optional[BytesIO]:
    if not frames:
        return None

    sample_rate = frames[0].sample_rate
    channels = frames[0].layout.nb_channels

    audio_chunks = [frame.to_ndarray() for frame in frames]
    audio_concat = np.concatenate(audio_chunks, axis=1)

    # Converte para o formato (num_samples, num_channels) exigido pelo WAV.
    audio_concat = audio_concat.T

    if audio_concat.dtype != np.int16:
        max_int16 = np.iinfo(np.int16).max
        audio_concat = np.clip(audio_concat, -1.0, 1.0)
        audio_concat = (audio_concat * max_int16).astype(np.int16)
    else:
        audio_concat = audio_concat.astype(np.int16)

    wav_buffer = BytesIO()
    wav_buffer.write(b"RIFF")
    # Cálculo manual do cabeçalho WAV para evitar dependências adicionais.
    data_bytes = audio_concat.tobytes()
    file_size = 36 + len(data_bytes)
    wav_buffer.write(file_size.to_bytes(4, "little"))
    wav_buffer.write(b"WAVEfmt ")
    wav_buffer.write((16).to_bytes(4, "little"))  # Subchunk1Size (PCM)
    wav_buffer.write((1).to_bytes(2, "little"))  # AudioFormat PCM
    wav_buffer.write((channels).to_bytes(2, "little"))
    wav_buffer.write((sample_rate).to_bytes(4, "little"))
    byte_rate = sample_rate * channels * 2  # 16 bits = 2 bytes
    wav_buffer.write(byte_rate.to_bytes(4, "little"))
    block_align = channels * 2
    wav_buffer.write(block_align.to_bytes(2, "little"))
    wav_buffer.write((16).to_bytes(2, "little"))  # BitsPerSample
    wav_buffer.write(b"data")
    wav_buffer.write(len(data_bytes).to_bytes(4, "little"))
    wav_buffer.write(data_bytes)
    wav_buffer.seek(0)
    return wav_buffer

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
        "Clique em \"Start\" para iniciar a captura pelo microfone padrão e em \"Stop\" para encerrar."
    )

    if "recorded_audio" not in st.session_state:
        st.session_state.recorded_audio = None
    if "was_streaming" not in st.session_state:
        st.session_state.was_streaming = False

    ctx = webrtc_streamer(
        key="audio-recorder",
        mode=WebRtcMode.SENDONLY,
        media_stream_constraints={"audio": True, "video": False},
        audio_receiver_size=256,
        async_processing=False,
        audio_processor_factory=AudioRecorder,
    )

    if ctx.state.playing:
        st.info("🎙️ Gravando... sua voz está sendo capturada.")
        if not st.session_state.was_streaming and ctx.audio_processor:
            ctx.audio_processor.frames = []
        st.session_state.was_streaming = True
        st.session_state.recorded_audio = None
    elif st.session_state.was_streaming and ctx.audio_processor:
        wav_buffer = _frames_to_wav(ctx.audio_processor.frames)
        ctx.audio_processor.frames = []
        st.session_state.was_streaming = False
        if wav_buffer is None:
            st.warning(
                "Não foi possível gerar o arquivo. Verifique se o microfone está liberado para o navegador."
            )
        st.session_state.recorded_audio = wav_buffer

    if st.session_state.recorded_audio:
        st.success("Gravação finalizada! Ouça ou baixe o arquivo abaixo.")
        st.audio(st.session_state.recorded_audio, format="audio/wav")
        st.download_button(
            "Baixar gravação",
            data=st.session_state.recorded_audio.getvalue(),
            file_name=f"gravacao_{datetime.now().strftime('%H%M%S')}.wav",
            mime="audio/wav",
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
