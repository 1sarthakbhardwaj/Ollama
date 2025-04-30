import re
import base64
import streamlit as st
from ollama import chat

# ——— Page configuration must be first ———
st.set_page_config(page_title="Local Mini DeepSeek with Qwen3 & Ollama", layout="centered")

# ——— Helper functions ———
def format_reasoning_response(thinking_content):
    return (
        thinking_content.replace("<think>\n\n</think>", "")
                         .replace("<think>", "")
                         .replace("</think>", "")
    )

def display_message(message):
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        if role == "assistant":
            display_assistant_message(message["content"])
        else:
            st.markdown(message["content"])

def display_assistant_message(content):
    pattern = r"<think>(.*?)</think>"
    think_match = re.search(pattern, content, re.DOTALL)
    if think_match:
        think_content = think_match.group(0)
        response_content = content.replace(think_content, "")
        think_content = format_reasoning_response(think_content)
        with st.expander("Thinking complete! 🧠"):
            st.markdown(think_content)
        st.markdown(response_content)
    else:
        st.markdown(content)

def process_thinking_phase(stream):
    thinking_content = ""
    with st.status("Thinking...", expanded=True) as status:
        placeholder = st.empty()
        for chunk in stream:
            content = chunk["message"]["content"] or ""
            thinking_content += content
            if "<think>" in content:
                continue
            if "</think>" in content:
                status.update(label="Thinking complete! 🧠", state="complete", expanded=False)
                break
            placeholder.markdown(format_reasoning_response(thinking_content))
    return thinking_content

def process_response_phase(stream):
    response = ""
    placeholder = st.empty()
    for chunk in stream:
        content = chunk["message"]["content"] or ""
        response += content
        placeholder.markdown(response)
    return response

@st.cache_resource
def get_chat_model():
    return lambda messages: chat(
        model="qwen3:4b",
        messages=messages,
        stream=True,
    )

# ——— Initialize session ———
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# ——— Main application ———
# Header with logos and powered-by text
qwen_bytes = open("assets/logo_qwen3.png", "rb").read()
ollama_bytes = open("assets/ollama.jpg", "rb").read()
qwen_b64 = base64.b64encode(qwen_bytes).decode()
ollama_b64 = base64.b64encode(ollama_bytes).decode()
st.markdown(
    f"""
    <div style='text-align: center;'>
        <h1>Local Mini DeepSeek</h1>
        <img src='data:image/png;base64,{qwen_b64}' width='100' alt='Qwen3 logo' style='margin:0 20px;' />
        <img src='data:image/jpeg;base64,{ollama_b64}' width='100' alt='Ollama logo' style='margin:0 20px;' />
        <p style='font-size:14px; color:gray;'>Powered by Qwen3 and Ollama inference</p>
        <h4>Think Deeper, Act Faster Locally</h4>
    </div>
    """, unsafe_allow_html=True
)

# ——— Display chat history ———
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        display_message(msg)

# ——— Bottom input centered ———
st.markdown("---")
# Center toggle above input
col1, col2, col3 = st.columns([1,4,1])
with col2:
    enable_reasoning = st.toggle(
        "        Enable step-by-step reasoning 🧠",
        value=True,
    )
# Spacing
st.write("<br>", unsafe_allow_html=True)
# Full-width chat input at bottom
if user_input := st.chat_input("Type your question and press Enter…"):
    tag = "/think" if enable_reasoning else "/no_think"
    prompt = f"{tag} {user_input}"
    # Save and display user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(user_input)
    # Assistant response
    with st.chat_message("assistant"):
        stream = get_chat_model()(st.session_state["messages"])
        thinking = process_thinking_phase(stream)
        answer = process_response_phase(stream)
        st.session_state["messages"].append({"role": "assistant", "content": thinking + answer})
