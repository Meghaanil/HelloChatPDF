import streamlit as st
import requests

# Sidebar contents
st.sidebar.title('🤗💬 LLM Chat App')
st.sidebar.markdown('''
## About
This app is an LLM-powered chatbot built using:
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://python.fastapi.com/)
- [OpenAI](https://platform.openai.com/docs/models) LLM model
 
''')
st.sidebar.write('Made with ❤️ by Megha Anil')

def main():
    st.header("Chat with PDF 💬")
 
    # upload a PDF file
    pdf = st.file_uploader("Upload your PDF", type='pdf')

    if pdf is not None:
        files = {"file": pdf}
        response = requests.post("http://localhost:8000/upload/", files=files)
        if response.status_code == 200:
            st.success("PDF uploaded successfully")
        else:
            st.error("Failed to upload PDF")

    # Accept user questions/query
    query = st.text_input("Ask questions about your PDF file:")
    st.write(query)  # To ensure that the text input is displayed (for debugging)

    if st.button("Submit Query"):
        response = requests.post("http://localhost:8000/query/", data={"query": query})
        if response.status_code == 200:
            result = response.json()
            st.write(result)
        else:
            st.error("Failed to process query")

if __name__ == '__main__':
    main()
