import streamlit as st

st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍"
)

st.title("🌍 AI Language Translator")
st.write("Simple language translation tool")

LANGUAGES = [
    "English",
    "Hindi",
    "Tamil"
]

translations = {
    ("hello", "English", "Hindi"): "नमस्ते",
    ("hello", "English", "Tamil"): "வணக்கம்",
    ("how are you", "English", "Hindi"): "आप कैसे हैं?",
    ("how are you", "English", "Tamil"): "நீங்கள் எப்படி இருக்கிறீர்கள்?",
    ("good morning", "English", "Hindi"): "सुप्रभात",
    ("good morning", "English", "Tamil"): "காலை வணக்கம்",
    ("thank you", "English", "Hindi"): "धन्यवाद",
    ("thank you", "English", "Tamil"): "நன்றி",
    ("welcome", "English", "Hindi"): "स्वागत है",
    ("welcome", "English", "Tamil"): "வரவேற்கிறோம்"
}

text = st.text_area(
    "Enter text:",
    placeholder="Type Hello here..."
)

source_language = st.selectbox(
    "Source language:",
    LANGUAGES
)

target_language = st.selectbox(
    "Target language:",
    LANGUAGES,
    index=1
)

if st.button("Translate", type="primary"):
    clean_text = text.strip().lower()

    if clean_text == "":
        st.warning("Please enter some text.")

    elif source_language == target_language:
        st.info("Please select different languages.")

    else:
        key = (
            clean_text,
            source_language,
            target_language
        )

        if key in translations:
            result = translations[key]
        else:
            result = (
                "Demo translation available only for: "
                "Hello, How are you, Good morning, Thank you, Welcome"
            )

        st.subheader("Translation Result")
        st.success("Translation completed")
        st.write(result)