from datetime import datetime
from typing import Optional

import streamlit as st

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

    st.caption(
        "Para capturar áudio diretamente do navegador, considere integrar bibliotecas como "
        "`streamlit-webrtc` ou Web Audio API em uma versão futura."
    )
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
