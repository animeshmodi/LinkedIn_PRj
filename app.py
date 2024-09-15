import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import PDFMinerPDFasHTMLLoader
from bs4 import BeautifulSoup
import tempfile
import re
import transformers
from groq import Groq

# Streamlit App Configuration
st.set_page_config(page_title="LinkedIn PDF to HTML Resume & AI Assistant", page_icon="📄")
st.title("📄 LinkedIn PDF to HTML Resume Generator & AI Assistant")
st.subheader("Generate an HTML Resume from your LinkedIn PDF and ask questions!")

# User input for API key
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

st.session_state.api_key = st.text_input("Enter your Groq API Key", value=st.session_state.api_key, type="password")

# Ensure that the user has entered an API key
if not st.session_state.api_key:
    st.warning("Please enter your Groq API key to continue.")
else:
    # Initialize the Groq client with the provided API key
    client = Groq(api_key=st.session_state.api_key)

    # PDF file uploader
    uploaded_pdf = st.file_uploader("Upload your LinkedIn PDF file:", type="pdf")

    def save_uploaded_file(uploaded_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.read())
            return temp_file.name

    def convert_pdf_to_html(pdf_file_path):
        loader = PDFMinerPDFasHTMLLoader(file_path=pdf_file_path)
        documents = loader.load()
        return documents[0].page_content if documents else ""

    def clean_html_content(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text

    def structure_resume(text):
        sections = ["Summary", "Education", "Skills", "Experience"]
        structured_html = ""
        section_order = []
        section_texts = {}
        
        for section in sections:
            if section in text:
                section_order.append(section)
                section_texts[section] = ""
        
        for section in section_order:
            section_text = ""
            lines = text.splitlines()
            section_found = False
            section_start = 0
            
            for i, line in enumerate(lines):
                if section in line and not section_found:
                    section_found = True
                    section_start = i + 1
                    continue
            
            for i, line in enumerate(lines[section_start:]):
                if line.strip() == "":
                    break
                if any(other_section in line for other_section in sections if other_section != section):
                    break
                section_text += line + "\n"
            
            section_texts[section] = section_text
        
        for section, text in section_texts.items():
            if text:
                structured_html += f"<div class='section'><h2>{section}</h2><p>{text}</p></div>"
        
        return structured_html

    def add_css_styling(html_content):
        css = """
        <style>
            .resume {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
            }
            .section {
                margin-bottom: 20px;
            }
            h2 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 5px;
            }
            p {
                margin-bottom: 10px;
            }
        </style>
        """
        return f"{css}\n<div class='resume'>{html_content}</div>"

    def generate_response(prompt, resume_content):
        full_prompt = f"""Based on the following resume content:

    {resume_content}

    Please answer the following question:
    {prompt}

    Provide a concise and relevant answer based solely on the information present in the resume. If the information is not available in the resume, please state that clearly."""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an AI assistant that helps answer questions about resumes. Provide concise and accurate responses based solely on the information given in the resume."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content

    # Main app logic
    if uploaded_pdf is not None:
        if 'resume_processed' not in st.session_state:
            st.session_state.resume_processed = False
        
        if not st.session_state.resume_processed and st.button("Generate HTML Resume"):
            try:
                with st.spinner("Converting PDF to HTML..."):
                    temp_file_path = save_uploaded_file(uploaded_pdf)
                    html_output = convert_pdf_to_html(temp_file_path)
                    cleaned_text = clean_html_content(html_output)
                    structured_html = structure_resume(cleaned_text)
                    final_html = add_css_styling(structured_html)
                
                st.success("HTML Resume generated successfully!")
                st.markdown("### Generated Resume:")
                st.markdown(final_html, unsafe_allow_html=True)
                
                # Store the cleaned text and final HTML in session state for later use
                st.session_state.cleaned_text = cleaned_text
                st.session_state.final_html = final_html
                st.session_state.resume_processed = True
                
                # Clean up the temporary file
                os.unlink(temp_file_path)
            except Exception as e:
                st.error(f"Error: {str(e)}")

        # Download option
        if st.session_state.resume_processed:
            st.download_button(
                label="Download HTML Resume",
                data=st.session_state.final_html,
                file_name="linkedin_resume.html",
                mime="text/html"
            )

        # AI Assistant Section
        if st.session_state.resume_processed:
            st.subheader("Ask Questions About Your Resume")
            user_input = st.text_input("Ask a question about your resume:")
            
            if st.button("Submit Question"):
                if user_input:
                    try:
                        response = generate_response(user_input, st.session_state.cleaned_text)
                        st.write(response)
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
                else:
                    st.warning("Please enter a question before submitting.")
        else:
            st.info("Please generate the HTML resume first before asking questions.")
    else:
        st.info("Please upload a PDF file to get started.")
