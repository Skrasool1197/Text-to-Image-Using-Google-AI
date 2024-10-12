import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)

st.set_page_config(page_title='Image to Text Generator', layout='wide')
model = genai.GenerativeModel('gemini-1.5-flash')

prompt = '''
    Analyze the image and provide a short, engaging description. Focus on key visual elements such as
    colors, objects, emotions, and the scene. Make the description vivid and imaginative, appealing to a general
    audience. Avoid technical jargon and keep it simple, yet creative.
    '''


css = """
    <style>
        .main {
            background-color: #f0f2f6;
            padding: 2rem;
        }
        h1 {
            color: #0073e6;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }
        .description {
            text-align: center;
            font-size: 1.1rem;
            color: #4a4a4a;
            margin-bottom: 2rem;
        }
        .uploaded-image {
            display: flex;
            justify-content: center;
            margin: 2rem 0;
        }
        .generated-text {
            background-color: #eaf2ff;
            border-radius: 8px;
            padding: 1.5rem;
            margin-top: 2rem;
            font-size: 1.2rem;
            color: #333;
        }
        .file-upload-label {
            font-weight: bold;
            color: #0073e6;
            font-size: 1.1rem;
            margin-top: 1rem;
        }
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

st.title("Image to Text Generator")
st.markdown("<div class='description'>Upload an image to generate a descriptive text summary</div>", unsafe_allow_html=True)

st.markdown("<div class='file-upload-label'>Choose an image (JPG, JPEG, PNG):</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    try:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image', use_column_width=False, width=300)
        
        with st.spinner('Generating text...'):
            res = model.generate_content([prompt, img])

        st.markdown("<div class='generated-text'><b>Generated Text:</b><br>" + res.text + "</div>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Upload an image to start generating text.")
