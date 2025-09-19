import streamlit as st
import pandas as pd
import numpy as np
import base64
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from deep_translator import GoogleTranslator
import time
import speech_recognition as sr

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="🌍 Language Detector & Translator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Background -----------------
def set_bg(img_path):
    try:
        with open(img_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_b64}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: The background image file '{img_path}' was not found.")
    except Exception as e:
        st.error(f"An error occurred while loading the background image: {e}")

set_bg("Project.jpg")

# ----------------- CSS Styling -----------------
st.markdown("""
<style>
.title-box {
    background: linear-gradient(90deg, #4b6cb7, #182848);
    padding: 18px 30px;
    border-radius: 25px;
    color: white;
    font-size: 30px;
    font-weight: 700;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 5px 20px rgba(0,0,0,0.4);
}
.card {
    background-color: rgba(255,255,255,0.95);
    border-radius: 20px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 6px 25px rgba(0,0,0,0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
    transform: scale(1.02);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
div[data-testid="stButton"] > button {
    border-radius: 15px;
    padding: 0.8em 1.6em;
    font-weight: bold;
    font-size: 16px;
    color: white;
    margin: 5px;
    border: none;
    transition: transform 0.2s, box-shadow 0.2s;
}
div[data-testid="stButton"] > button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 15px rgba(0,0,0,0.4);
}

/* Specific button styling using a custom data attribute */
[data-testid="stButton"] button {
    background-color: #007BFF;
}

[data-testid="stButton-translate"] button {
    background-color: green;
}

[data-testid="stButton-clear"] button {
    background-color: red;
}

[data-testid="stButton-download"] button {
    background-color: #FFAA00;
}

.output-box {
    background-color: rgba(250,250,250,0.95);
    border-radius: 20px;
    padding: 20px;
    font-size: 18px;
    line-height: 1.6;
    color: #000;
    box-shadow: 0 5px 20px rgba(0,0,0,0.25);
}
.lang-detected {
    color: #007BFF;
    font-weight: bold;
    font-size: 20px;
}
textarea {
    font-size: 17px !important;
}
.css-1n76uvr, .stSelectbox>div>div>div>div {
    font-size: 17px !important;
    padding: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ----------------- Languages -----------------
LANGUAGES = GoogleTranslator().get_supported_languages(as_dict=True)
LANGUAGES = dict(sorted(LANGUAGES.items()))  # sort alphabetically

# ----------------- Load Dataset -----------------
try:
    df = pd.read_csv("language.csv", encoding="utf-8")
except FileNotFoundError:
    st.error("⚠ Could not load dataset. Make sure 'language.csv' exists in the same directory.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the dataset: {e}")
    st.stop()

df = df.dropna(subset=["Text", "language"])
texts = np.array(df["Text"])
langs = np.array(df["language"])

# ----------------- Train Model -----------------
@st.cache_resource
def train_model():
    """Trains and caches the language detection model."""
    vec = CountVectorizer()
    X = vec.fit_transform(texts)
    X_train, X_test, y_train, y_test = train_test_split(X, langs, test_size=0.3, random_state=42)
    nb = MultinomialNB()
    nb.fit(X_train, y_train)
    return nb, vec

model, vectorizer = train_model()

# ----------------- Translator -----------------
def translate_text(text, target_lang="en"):
    """Translates text to the target language using GoogleTranslator."""
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        return f"⚠ Translation failed: {e}"

# ----------------- Session State -----------------
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
if "predicted" not in st.session_state:
    st.session_state.predicted = ""
if "translated" not in st.session_state:
    st.session_state.translated = ""

# ----------------- Sidebar -----------------
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🌍 Language App</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.info(
        """
        *Features:*
        - Detect language instantly
        - Translate to 100+ languages
        - Download translated text
        - Modern interactive UI
        """
    )
    st.markdown("---")
    # Color pickers for mic UI
    listen_color = st.color_picker("🎨 Pick Listening Box Color", "#FFEB99")
    recorded_color = st.color_picker("🎨 Pick Recorded Text Box Color", "#D4EDDA")

# ----------------- Main Layout -----------------
st.markdown('<div class="title-box">🌐 Language Detector & Translator</div>', unsafe_allow_html=True)

# Two-column layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="title-box">🔍 Language Detector</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: black; font-size: 30px;'>✍ Enter text here:</p>", unsafe_allow_html=True)
    
    # ----------------- Mic Input -----------------
    st.markdown("<p style='color: black; font-size: 30px;'>🎤 Or speak your text:</p>", unsafe_allow_html=True)
    if st.button("🎙 Start Recording", key="mic_button"):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.markdown(
                f"""
                <div style="
                    background-color: {listen_color};
                    padding: 15px;
                    border-radius: 12px;
                    font-size: 18px;
                    font-weight: bold;
                    color: black;
                    text-align: center;
                    border: 1px solid #555;">
                    🎤 Listening... Speak now
                </div>
                """,
                unsafe_allow_html=True
            )
            audio = r.listen(source, timeout=5)
        try:
            text_from_mic = r.recognize_google(audio)
            st.session_state.text_input = text_from_mic
            st.markdown(
                f"""
                <div style="
                    background-color: {recorded_color};
                    padding: 15px;
                    border-radius: 12px;
                    font-size: 18px;
                    font-weight: bold;
                    color: black;
                    text-align: center;
                    border: 1px solid #555;">
                    ✅ Recorded text added to input
                </div>
                """,
                unsafe_allow_html=True
            )
        except sr.UnknownValueError:
            st.warning("Could not understand audio. Please try again.")
        except sr.RequestError as e:
            st.error(f"Speech recognition service error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred during recording: {e}")

    # Text area
    st.session_state.text_input = st.text_area("", st.session_state.text_input, height=150, key="text_area")

    # Live detection
    if st.session_state.text_input.strip():
        vec_txt = vectorizer.transform([st.session_state.text_input.strip()])
        pred = model.predict(vec_txt)
        st.session_state.predicted = pred[0]
        st.markdown(
            f"<div class='output-box'>🌐 Detected Language: <span class='lang-detected'>{st.session_state.predicted}</span></div>",
            unsafe_allow_html=True
        )

with col2:
    st.markdown('<div class="title-box">🌐 Translator</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: black; font-size: 30px;'>Choose target language:</p>", unsafe_allow_html=True)
    target_language_name = st.selectbox("", list(LANGUAGES.keys()), index=0, key="target_lang_select")
    target_language = LANGUAGES[target_language_name]

    if st.button("Translate", key="translate"):
        if st.session_state.text_input.strip():
            with st.spinner("Translating... ⏳"):
                st.session_state.translated = translate_text(st.session_state.text_input, target_language)
            
            st.markdown(
                f"<div class='output-box'>✅ Translation ({st.session_state.predicted} ➝ {target_language_name})<br><br>{st.session_state.translated}</div>",
                unsafe_allow_html=True
            )
            
            st.download_button(
                label="📥 Download Translation",
                data=st.session_state.translated,
                file_name="translation.txt",
                mime="text/plain",
                key="download"
            )
        else:
            st.warning("Please enter some text to translate.")
            
# ----------------- Clear Button -----------------
if st.button("🧹 Clear All", key="clear"):
    st.session_state.text_input = ""
    st.session_state.predicted = ""
    st.session_state.translated = ""
    st.rerun()
