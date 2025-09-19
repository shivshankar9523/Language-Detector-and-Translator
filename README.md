# Language-Detector-and-Translator

🔑 Project Description
The application allows users to detect the language of a given text and then translate it into 100+ languages using GoogleTranslator.

It provides multiple input methods (text area + speech-to-text microphone input) and displays results with a modern styled UI.

⚙️ Main Features

🌍 Language Detection

1 Uses a dataset (language.csv) with text–language mappings.

2 Trains a Naive Bayes model (MultinomialNB) with CountVectorizer to classify text language.

3 Detects the input text’s language in real time.

🌐 Language Translation
1 Uses deep_translator.GoogleTranslator for translations.
2 User selects the target language from a dropdown menu.
3 Displays the translated text inside a styled output box.
4 Allows users to download the translated text as a .txt file.

🎤 Speech Recognition

1 Uses speech_recognition to record voice input through the microphone.
2 Converts speech to text with recognize_google.
3 Automatically adds recognized speech into the text input field.

🖼 Custom UI & Styling
1 Custom background image with CSS.
2 Stylish cards, buttons, and output boxes with hover effects.
3 Sidebar for app info + color pickers (to customize mic UI feedback).
4 Buttons with different color themes (Translate = Green, Clear = Red, Download = Yellow).

📥 Clear & Reset
"🧹 Clear All" button resets all session states and clears inputs/outputs.
🛠 Technologies Used
1 Frontend/UI → Streamlit + CSS customization
2 Data Handling → Pandas, NumPy
3 ML Model → Scikit-learn (CountVectorizer, MultinomialNB)
4 Translation → deep-translator (GoogleTranslator)
5 Speech-to-Text → speech_recognition
6 File Export → Streamlit’s download_button

🚀 User Flow
1 Open the app → Background + title UI loads.
2 Enter text manually or click 🎙 Start Recording to use voice input.
3 The app detects the input language automatically.
4 Select a target language from the dropdown.
5 Click Translate → Translation appears in output box.

(Optional) Download the translated text as .txt.

Use Clear All to reset everything.

📬 Contact
Developer:Shivshankar Kumar
Email:    kumarshivshankar2389@gmail.com
Linkedin: https://www.linkedin.com/in/shivshankar-kumar-957166214
