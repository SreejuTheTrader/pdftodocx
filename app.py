import streamlit as st
import fitz
from docx import Document
import tempfile

st.title("📄 PDF → Clean Structured DOCX")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

def extract_column_text(page, side="left"):
    rect = page.rect

    if side == "left":
        clip = fitz.Rect(0, 0, rect.width/2, rect.height)
    else:
        clip = fitz.Rect(rect.width/2, 0, rect.width, rect.height)

    return page.get_text("text", clip=clip)

if uploaded_file:
    st.write("Processing...")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    pdf = fitz.open(pdf_path)
    doc = Document()

    q_no = 1

    for page in pdf:
        # LEFT → English
        left_text = extract_column_text(page, "left")

        # RIGHT → Tamil
        right_text = extract_column_text(page, "right")

        left_lines = [l.strip() for l in left_text.split("\n") if l.strip()]
        right_lines = [l.strip() for l in right_text.split("\n") if l.strip()]

        # Simple grouping logic
        for i in range(min(len(left_lines), len(right_lines))):
            
            tamil = right_lines[i]
            english = left_lines[i]

            # Tamil first
            doc.add_paragraph(f"{q_no}. {tamil}")

            # English next
            doc.add_paragraph(english)

            doc.add_paragraph("")

            q_no += 1

    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".docx").name
    doc.save(output_path)

    with open(output_path, "rb") as f:
        st.download_button(
            "Download DOCX",
            f.read(),
            file_name="clean_output.docx"
        )

    st.success("✅ Done")
