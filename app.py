import streamlit as st

st.set_page_config(page_title="Recruitment AI", page_icon="🤖", layout="wide")

st.title("Recruitment AI Dashboard")
st.write(
    """
    Welcome to the Recruitment AI Streamlit app. Use the controls in the sidebar to explore
    candidate profiles, evaluate interview notes, and review automated recommendations.
    """
)

with st.sidebar:
    st.header("Search Filters")
    job_role = st.selectbox(
        "Target role",
        ["Software Engineer", "Data Scientist", "Product Manager", "Designer", "Other"],
    )
    experience = st.slider("Minimum years of experience", min_value=0, max_value=20, value=2)
    include_remote = st.checkbox("Include remote candidates", value=True)

st.subheader("Candidate Overview")
st.info(
    f"Filtering for **{job_role}** candidates with at least **{experience}** years of experience"
)
if include_remote:
    st.success("Remote candidates will be included in the search results.")
else:
    st.warning("Remote candidates are excluded from the search results.")

st.subheader("Interview Summaries")
st.write(
    """
    Upload structured interview notes to get tailored summaries, improvement feedback, and
    hiring recommendations powered by AI.
    """
)
uploaded_file = st.file_uploader("Upload interview notes (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
if uploaded_file is not None:
    st.write("File uploaded successfully! In a production app, the contents would be analyzed here.")
    st.button("Run AI Analysis")
else:
    st.caption("Waiting for a file upload to begin analysis.")

st.subheader("Next Steps")
st.write(
    """
    - Refine the AI evaluation prompts.
    - Integrate with the applicant tracking system.
    - Enable real-time collaboration for hiring teams.
    """
)
