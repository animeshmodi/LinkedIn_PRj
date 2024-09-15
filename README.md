# LinkedIn PDF to HTML Resume Generator & AI Assistant

This web application converts a LinkedIn PDF resume into an HTML format and provides an AI assistant to answer questions about the resume.

## Live Demo

[Access the application here](https://verfablo-linkedintohtml.streamlit.app/)

## Features

- Convert LinkedIn PDF resume to HTML format
- Generate a styled and structured HTML resume
- Download the generated HTML resume
- AI assistant to answer questions about the resume content

## Technology Stack

- Python
- Streamlit for the web interface
- PDFMinerPDFasHTMLLoader for PDF processing
- BeautifulSoup for HTML parsing
- Groq API for AI-powered question answering

## Why Groq API?

We chose to use the Groq API instead of OpenAI for this project because:
1. Groq offers a free tier, making it more accessible for development and testing.
2. It provides similar capabilities to OpenAI for our use case of answering questions about resume content.

## Deployment Choice

The application is deployed on Streamlit Share because:
1. Streamlit offers easy deployment for Python-based web applications.
2. It integrates well with machine learning models and data processing pipelines.
3. Streamlit Share provides a free hosting option for open-source projects.

## How to Use

1. Visit the [application URL](https://verfablo-linkedintohtml.streamlit.app/).
2. Enter your Groq API key when prompted.
3. Upload your LinkedIn PDF resume.
4. Click "Generate HTML Resume" to convert and display the resume.
5. Use the "Download HTML Resume" button to save the generated HTML file.
6. Ask questions about your resume using the AI assistant feature.

## Local Development

To run this project locally:

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Future Improvements

- Add support for multiple resume formats
- Enhance the AI assistant's capabilities
- Improve the HTML styling options

## Contributing

Contributions to improve the application are welcome. Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
