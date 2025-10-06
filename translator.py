import streamlit as st
from groq import Groq
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY") or "your_api_key_here")

st.set_page_config(page_title="🌍 Smart AI Translator", page_icon="🧠")
st.title("🧠 Smart AI Translator 🌍")

st.write("Automatically detects the input language and translates to any target language you type.")

# Create a form — pressing Enter will submit it
with st.form(key="translation_form"):
    text = st.text_area("✏️ Enter text to translate:")
    target_lang = st.text_input("🌐 Enter target language (e.g., Arabic, Korean, Chinese, French, etc.):")
    submitted = st.form_submit_button("Translate (or press Enter)")

if submitted:
    if text.strip() == "":
        st.warning("⚠️ Please enter some text to translate.")
    elif target_lang.strip() == "":
        st.warning("⚠️ Please enter the target language.")
    else:
        messages = [
            {"role": "system", "content": "You are a multilingual translator that can detect the source language and translate text to any requested target language."},
            {"role": "user", "content": f"Translate the following text into {target_lang}. Only output the translation. Text: {text}"}
        ]

        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        translation = resp.choices[0].message.content

        rtl_languages = ["arabic", "hebrew", "persian", "urdu"]

        st.subheader("📘 Translation:")
        if target_lang.lower() in rtl_languages:
            st.markdown(f"<div dir='rtl' style='font-size:20px; text-align:right;'>{translation}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-size:20px;'>{translation}</div>", unsafe_allow_html=True)
