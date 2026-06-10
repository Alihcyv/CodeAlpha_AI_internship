%%writefile translator.py
import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import os

st.set_page_config(page_title="AI Translation Tool", page_icon="🌐")

if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""  
if 'detected_lang' not in st.session_state:
    st.session_state.detected_lang = ""  

@st.cache_data(show_spinner=False)
def translate_text_func(text, src_lang, dest_lang):
    try:
        translator = Translator()
        result = translator.translate(text, src=src_lang, dest=dest_lang)
        return result.text, result.src
    except Exception as e:
        return None, str(e)

st.title("🌐 AI Language Translator")
st.markdown("Enter the text you want to translate and select the languages.")

lang_list = list(LANGUAGES.values())
col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Select the source language:", ["auto"] + lang_list)
    src_code = 'auto' if source_lang == "auto" else [k for k, v in LANGUAGES.items() if v == source_lang][0]

with col2:
    target_lang = st.selectbox("Select target language:", lang_list)
    target_code = [k for k, v in LANGUAGES.items() if v == target_lang][0]

text_to_translate = st.text_area("Type the text here:", placeholder="Salam, necəsən?")

if st.button("Translate ✨"):
    if text_to_translate.strip() == "":
        st.warning("Please enter some text!")
    elif len(text_to_translate) > 5000:
        st.error('❌ The text is too long. Please enter up to 5000 characters.')
    else:
        res_text, res_lang = translate_text_func(text_to_translate, src_lang=src_code, dest_lang=target_code)
        
        if res_text:
            st.session_state.translated_text = res_text
            st.session_state.detected_lang = res_lang
            st.success("Translation completed!")
        else:
            st.error(f"Error: {res_lang}")

if st.session_state.translated_text:
    st.markdown("---")
    st.subheader("Result:")
    
    if src_code == 'auto':
        detected_name = LANGUAGES.get(st.session_state.detected_lang, "Unknown")
        st.info(f"🔍 Detected language: **{detected_name.capitalize()}**")
    
    st.write(st.session_state.translated_text)

    if st.button("Listen to Audio 🔊"):
        try:
            tts = gTTS(text=st.session_state.translated_text, lang=target_code)
            tts.save("result.mp3")
            st.audio("result.mp3")
        except Exception as e:
            st.error(f"Audio error: {e}")

st.markdown("---")
st.caption("AI Engineering Internship Project - Language Translation Tool")
