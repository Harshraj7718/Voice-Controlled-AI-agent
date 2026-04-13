import streamlit as st
from stt import transcribe
from intent import detect_intent
from tools import *
from memory import save, get
from mic import record_audio
import os

#  PAGE CONFIG

st.set_page_config(
    page_title="Voice AI Agent",
    page_icon="🎙",
    layout="centered"
)

# SIDEBAR

st.sidebar.title("⚙️ Navigation")

page = st.sidebar.radio(
    "Go to",
    ["🏠 Dashboard", "🧠 History", "ℹ️ About"]
)

# Ensure output folder exists
os.makedirs("output", exist_ok=True)


# 🏠 DASHBOARD

if page == "🏠 Dashboard":

    st.title("🎙 Voice-Controlled AI Agent")

    history = get()

    #  Metrics
    st.markdown("## 📊 System Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("🎤 Inputs", len(history))
    col2.metric("⚙️ Actions", len(history))
    col3.metric("🧠 Memory", len(history))

    st.divider()

    # Input Section
    st.subheader("🎤 Input Options")

    col1, col2 = st.columns(2)

    if "audio_path" not in st.session_state:
        st.session_state["audio_path"] = None

    with col1:
        audio_file = st.file_uploader("📂 Upload Audio", type=["wav", "mp3"])
        if audio_file:
            with open("temp.wav", "wb") as f:
                f.write(audio_file.read())
            st.session_state["audio_path"] = "temp.wav"

    with col2:
        if st.button("🎙 Record (10 sec)"):
            st.session_state["audio_path"] = record_audio()
            st.success("Recording complete!")

    audio_path = st.session_state["audio_path"]

    
    # PIPELINE

    if audio_path:
        try:
            #  STT
            with st.spinner("🔊 Converting speech to text..."):
                text = transcribe(audio_path)

            st.markdown("### 📝 Transcribed Text")

            # Editable text
            edited_text = st.text_area(
                "✏️ Edit transcription:",
                value=text,
                height=150
            )

            use_edited = st.checkbox("Use edited text", value=True)
            final_text = edited_text if use_edited else text

            st.write("**Final Text Used:**", final_text)

            #  Intent Detection
            with st.spinner("🧠 Understanding your request..."):
                intent_data = detect_intent(final_text)

            # Store in session
            st.session_state["intent_data"] = intent_data
            st.session_state["final_text"] = final_text

            st.markdown("### 🧠 Intent Detection")
            st.json(intent_data)

            
            #  EXECUTION
            
            if st.button("✅ Confirm & Execute"):

                if "intent_data" not in st.session_state:
                    st.error("⚠️ No intent detected yet!")
                else:
                    intent_data = st.session_state["intent_data"]
                    final_text = st.session_state["final_text"]

                    try:
                        st.markdown("### ⚙️ Results")

                        progress = st.progress(0)

                        if isinstance(intent_data, dict):
                            intent_data = [intent_data]

                        for i, item in enumerate(intent_data):
                            intent = item.get("intent", "chat")
                            filename = item.get("filename", "output.txt")

                            if not filename or filename == "none":
                                filename = "output.txt"

                           
                            # ACTIONS
                            
                            if intent == "create_file":
                                result = create_file(filename)
                                st.success(result)

                                        
                                if any(word in final_text.lower() for word in ["code", "function", "program"]):
                                    st.info("Detected code-related request → Generating code...")

                                    code = generate_code(final_text)

                                    st.markdown("### 💻 Generated Code")
                                    st.code(code, language="python")

                                    write_code(filename, code)
                                    st.success(f"✅ Code written to {filename}")

                            elif intent == "write_code":
                                code = generate_code(final_text)

                                if not filename.endswith(".py"):
                                    filename = filename.replace(".txt", ".py")

                               
                                st.markdown("### 💻 Generated Code")
                                st.code(code, language="python")

                                result = write_code(filename, code)
                                st.success(f"✅ Code saved to {filename}")

                            elif intent == "summarize":
                                result = summarize(final_text)
                                st.success(result)

                            else:
                                result = chat_response(final_text)
                                st.success(result)

                            # Save memory
                            save({
                                "text": final_text,
                                "intent": intent,
                                "filename": filename,
                                "result": result
                            })

                            progress.progress((i + 1) / len(intent_data))

                    except Exception as e:
                        st.error(f"Execution Error: {str(e)}")

        except Exception as e:
            st.error(f"Processing Error: {str(e)}")


# HISTORY PAGE

elif page == "🧠 History":

    st.title("🧠 Session History")

    history = get()

    if history:
        for item in history[::-1]:
            st.markdown("### 📝 Input")
            st.write(item["text"])

            st.markdown("### 🧠 Intent")
            st.write(item["intent"])

            st.markdown("### ⚙️ Result")
            st.success(item["result"])

            st.divider()
    else:
        st.info("No history yet.")


#BOUT PAGE

elif page == "ℹ️ About":

    st.title("ℹ️ About This Project")

    st.markdown("""
    ## 🚀 Voice-Controlled AI Agent

    This project processes voice input, detects intent using LLM, and executes tasks locally.

    ### 🎯 Features
    - 🎤 Audio input (upload + mic)
    - 🔊 Hugging Face Whisper STT
    - 🧠 Ollama LLaMA3 intent detection
    - ⚙️ File + code execution
    - 🧠 Memory tracking
    - ✏️ Editable transcription

    ### 🧩 Pipeline
    Audio → Text → Intent → Action → Output

    ### 👨‍💻 Author
    Harsh
    """)