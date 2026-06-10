# AI-Powered Language Translation Tool

[Click here to test the application in your browser](https://codealphaaiinternship-dbzbirsg2ommj4edvsjvll.streamlit.app)

## Project Overview
This project was developed as part of the **AI Engineering Internship Program**. The goal was to create a robust, user-friendly translation tool that leverages cloud-based APIs to provide high-quality translations across multiple languages.

The application is built using **Streamlit**, providing a modern web interface, and integrates the **Google Translate API** for core translation logic and **gTTS** for text-to-speech functionality.

## Key Features
- **Multi-Language Support:** Ability to select from a wide range of source and target languages.
- **Automatic Language Detection:** Smart detection of the input language when the "auto" option is selected.
- **Text-to-Speech (TTS):** An optional feature that allows users to listen to the translated text in the target language.
- **Responsive UI:** A clean, professional interface with columns, status indicators, and a user-centric layout.
- **Input Validation:** Built-in checks for empty inputs and character limits (max 5000 characters) to ensure system stability.

## Engineering Decisions & Optimizations

- **Performance Optimization (Caching)**: I implemented `@st.cache_data` to cache translation results. This prevents redundant API calls for the same input, significantly reducing latency and protecting the application from API rate limits.

- **State Management (Session State)**: I used `st.session_state` to handle the application's memory. Since Streamlit reruns the entire script upon every interaction, session state ensures that the translated text remains on the screen when the user clicks the "Listen to Audio" button, providing a seamless User Experience.

- **Robustness & Error Handling**: The core translation logic is wrapped in `try-except` blocks. Network requests are prone to failure. Instead of the app crashing, the user receives a clean, human-readable error message if the API is unavailable.

- **Deployment**: The application is deployed on **Streamlit Cloud**, ensuring a scalable and accessible environment for users to test the tool without any local setup.

## Tech Stack
- **Language:** Python 3.x
- **Frontend Framework:** Streamlit
- **Translation API:** googletrans
- **Speech Synthesis:** gTTS
- **Deployment:** Streamlit Cloud
