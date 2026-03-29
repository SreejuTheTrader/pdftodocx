import streamlit as st
from pdf2docx import Converter
import tempfile
import os

st.title("📄 PDF → Editable DOCX (Web App)")

uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])

if uploaded_file:
    st.info("Processing... please wait ⏳")

    # Save uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        tmp_pdf.write(uploaded_file.read())
        pdf_path = tmp_pdf.name

    # Output DOCX path
    output_path = pdf_path.replace(".pdf", ".docx")

    try:
        cv = Converter(pdf_path)
        cv.convert(output_path, start=0, end=None)
        cv.close()

        with open(output_path, "rb") as f:
            st.success("Conversion Complete ✅")
            st.download_button(
                "Download DOCX",
                f,
                file_name="output.docx"
            )

    except Exception as e:
        st.error(f"Error: {str(e)}")
