import pytest
from app import ocr


def test_ocr_module_does_not_require_pytesseract():
    assert hasattr(ocr, "extract_text")
    assert "pytesseract" not in ocr.__dict__


def test_ocr_command_finds_windows_install(monkeypatch):
    monkeypatch.delenv("TESSERACT_CMD", raising=False)
    # On the target Windows setup the standard path should be discoverable;
    # this assertion is intentionally skipped on non-Windows CI environments.
    import sys
    if sys.platform != "win32":
        pytest.skip("Windows installation-path check")
    from app.ocr import _tesseract_command
    assert _tesseract_command().lower().endswith("tesseract.exe")


def test_clean_ocr_joins_split_urls():
    from app.ocr import clean_ocr_text
    text = "Click https://chat.whatsapp.com\n/ABC123\n?mode=gi_t"
    cleaned = clean_ocr_text(text)
    assert "https://chat.whatsapp.com/ABC123?mode=gi_t" in cleaned
