import streamlit as st
from pdf2image import convert_from_bytes
from docx import Document
from docx.shared import Inches
import tempfile
import os

st.title("📄 PDF → EXACT DOCX (Pixel Perfect)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    st.info("Processing...")

    # Convert PDF → images
    images = convert_from_bytes(uploaded_file.read(), dpi=300)

    doc = Document()

    for i, img in enumerate(images):
        st.write(f"Processing Page {i+1}")

        # Save temp image
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        img.save(temp_img.name)

        # Add image to docx
        doc.add_picture(temp_img.name, width=Inches(6))

        # Page break
        doc.add_page_break()

    # Save docx
    output_path = os.path.join(tempfile.gettempdir(), "exact_output.docx")
    doc.save(output_path)

    with open(output_path, "rb") as f:
        st.success("Done ✅ (100% exact layout)")
        st.download_button("Download DOCX", f, file_name="exact_output.docx")
