import streamlit as st
import fitz  # PyMuPDF
from docx import Document
from docx.shared import Inches
import tempfile
import os

st.set_page_config(page_title="PDF to DOCX", layout="centered")

st.title("📄 PDF → EXACT DOCX (Stable Version)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    try:
        st.info("Processing... ⏳")

        # Save uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        # Open PDF
        pdf = fitz.open(pdf_path)

        doc = Document()

        for i, page in enumerate(pdf):
            st.write(f"Processing page {i+1}")

            pix = page.get_pixmap(dpi=300)

            img_path = os.path.join(tempfile.gettempdir(), f"page_{i}.png")
            pix.save(img_path)

            doc.add_picture(img_path, width=Inches(6))
            doc.add_page_break()

        output_path = os.path.join(tempfile.gettempdir(), "output.docx")
        doc.save(output_path)

        with open(output_path, "rb") as f:
            st.success("✅ Conversion Complete")
            st.download_button(
                "Download DOCX",
                f,
                file_name="output.docx"
            )

    except Exception as e:
        st.error("Something went wrong ❌")
        st.code(str(e))
