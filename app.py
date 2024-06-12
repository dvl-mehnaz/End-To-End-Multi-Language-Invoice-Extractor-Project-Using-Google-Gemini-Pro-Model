from dotenv import load_dotenv

load_dotenv()
import time as t
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('Google_API_KEY'))

#function to load Gemini Pro
model=genai.GenerativeModel('gemini-pro')

def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()

        image_parts=[
            {
                'mime_type':uploaded_file.type,
                'data':bytes_data
            }
        ]
        return image_parts
    else:
        return FileNotFoundError('No file uploaded')




#initialize the streamlit
st.set_page_config(page_title='Multi-Language Invoice Extractor')
st.header("Multi-Language Invoice Extractor")
#input=st.text_input('input_prompt',key='input')
uploaded_file=st.sidebar.file_uploader("choose an image of invoice...",type=['jpg','jpeg','png'])

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption='uploading',use_column_width=True)


input=st.text_input('input_prompt',key='input')
submit=st.button("Tell me about Invoice")


input_prompt='''
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image

'''
 

if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("This is response")
    st.write(response)
    if response is not None:
        st.balloons()
    else:
        st.markdown(":moon:")
