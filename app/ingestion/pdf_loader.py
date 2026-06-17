from pypdf import PdfReader


def load_pdf(file_path):

    reader = PdfReader(file_path)

    if reader.is_encrypted:
        try:
            reader.decrypt("")
        except Exception:
            raise ValueError(
                "Encrypted PDF is not supported."
            )

    pages = []

    for idx, page in enumerate(reader.pages):

        text = page.extract_text() or ""

        pages.append({
            "page": idx + 1,
            "text": text
        })

    return pages


if __name__ == "__main__":

    pages = load_pdf("docs/sample.pdf")

    print(pages[0])