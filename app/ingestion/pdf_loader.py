from pypdf import PdfReader

def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text
if __name__ == "__main__":
    text = load_pdf("docs/sample.pdf")
    print(text)