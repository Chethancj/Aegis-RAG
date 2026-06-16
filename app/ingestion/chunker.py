def chunk_pages(
    pages,
    chunk_size: int = 500
):
    chunks = []

    for page in pages:

        page_num = page["page"]
        text = page["text"]

        for i in range(
            0,
            len(text),
            chunk_size
        ):

            chunks.append(
                {
                    "text": text[i:i + chunk_size],
                    "page": page_num
                }
            )

    return chunks