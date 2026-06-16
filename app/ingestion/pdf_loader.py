from pypdf import PdfReader


def load_pdf(file_path: str):

    reader = PdfReader(file_path)

    pages = []

    for idx, page in enumerate(reader.pages):

        text = page.extract_text()

        pages.append(
            {
                "page": idx + 1,
                "text": text
            }
        )

    return pages


if __name__ == "__main__":

    pages = load_pdf("docs/sample.pdf")

    print(pages[0])