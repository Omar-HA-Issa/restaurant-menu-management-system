import os
from typing import Optional
import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_file_path: str) -> Optional[str]:
    """
    Extract text from a PDF file using PyMuPDF only.
    Returns a single string with page texts separated by blank lines, or None on error/empty.
    """
    try:
        if not os.path.exists(pdf_file_path):
            print(f"[PDF] File not found: {pdf_file_path}")
            return None

        print(f"[PDF] Opening: {pdf_file_path}")
        doc = fitz.open(pdf_file_path)
        try:
            pages = []
            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                page_text = page.get_text("text").strip()
                if page_text:
                    pages.append(page_text)

            combined = "\n\n".join(pages).strip()
            if not combined:
                print("[PDF] No extractable text found (might be scanned images).")
                return None

            # Debug slice
            print(f"[PDF] Extracted length: {len(combined)}")
            print(f"[PDF] Preview: {combined[:200]!r}")
            return combined
        finally:
            doc.close()

    except fitz.FileDataError as e:
        print(f"[PDF] Invalid/corrupted PDF: {e}")
        return None
    except Exception as e:
        print(f"[PDF] Unexpected error: {type(e).__name__}: {e}")
        return None


def extract_text_from_image(image_path: str) -> Optional[str]:
    """
    Placeholder for image OCR. Google Vision removed to keep the project light.
    - Returns None, but never raises due to missing OCR libs.
    - If you later add OCR (e.g., Tesseract or Google Vision), implement here.
    """
    if not os.path.exists(image_path):
        print(f"[IMG] File not found: {image_path}")
        return None

    print("[IMG] OCR disabled in this build (no external OCR dependency).")
    return None


def save_text_to_file(text: Optional[str], output_file_path: str) -> bool:
    """
    Save extracted text to a file. Returns True on success, False otherwise.
    """
    try:
        if not text:
            print("[SAVE] No text to save.")
            return False

        os.makedirs(os.path.dirname(output_file_path) or ".", exist_ok=True)
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[SAVE] Wrote text to: {output_file_path}")
        return True
    except Exception as e:
        print(f"[SAVE] Error: {type(e).__name__}: {e}")
        return False
