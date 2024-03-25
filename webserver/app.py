import streamlit as st
from businessLogic import transcribeVideoOrchestrator


def main():
    st.title("VideoQuest")
 

    # User input: YouTube URL
    url = st.text_input("Enter YouTube URL:")

    # User input: model
    models = ["tiny", "base", "small", "medium", "large"]
    model = st.selectbox("Select Model:", models)
    #print(model)
    st.write(
        "If you take a smaller model it is faster but not as accurate, whereas a larger model is slower but more accurate.")
    if st.button("Transcribe"):
        if url:
            transcript = transcribeVideoOrchestrator(url, model)

            if transcript:
                st.subheader("Transcription:")
                st.write(transcript)
            else:
                st.error("Error occurred while transcribing.")
                st.write("Please try again.")

    st.markdown('<div style="margin-top: 450px;"</div>',
                unsafe_allow_html=True)

if __name__ == "__main__":
    main()
