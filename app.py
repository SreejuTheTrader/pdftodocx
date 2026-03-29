import streamlit as st
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Inches
import tempfile
import os

st.title("📄 PDF → DOCX (Exact Layout)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    try:
        st.write("Processing...")

        # Save PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        pdf = fitz.open(pdf_path)
        doc = Document()

        for i, page in enumerate(pdf):
            pix = page.get_pixmap()

            img_path = os.path.join(tempfile.gettempdir(), f"page_{i}.png")
            pix.save(img_path)

            doc.add_picture(img_path, width=Inches(6))

        output_path = os.path.join(tempfile.gettempdir(), "output.docx")
        doc.save(output_path)

        with open(output_path, "rb") as f:
            st.download_button("Download DOCX", f, file_name="output.docx")

        with open(output_path, "rb") as f:
            file_bytes = f.read()

        st.download_button(
            label="Download DOCX",
            data=file_bytes,
            file_name="output.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

    except Exception as e:
        st.error("Error occurred:")
        st.code(str(e))
