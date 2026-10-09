from io import BytesIO
from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile

from PIL import Image, ImageOps, ImageFilter


def _tesseract_command() -> str:
    configured = os.getenv("TESSERACT_CMD")
    if configured and Path(configured).exists():
        return configured

    command = shutil.which("tesseract")
    if command:
        return command

    common = [
        Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe"),
        Path(r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"),
    ]
    for path in common:
        if path.exists():
            return str(path)

    raise RuntimeError(
        "Tesseract OCR is not available. Set TESSERACT_CMD or add Tesseract to PATH."
    )


def clean_ocr_text(text: str) -> str:
    """Clean layout noise while preserving the text that feeds detection."""
    value = text.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+", " ", value)

    # OCR often places URL components on separate lines in screenshots.
    value = re.sub(
        r"(https?://[^\s]+)\s*\n\s*(/[^\s]+)", r"\1\2", value, flags=re.I
    )
    value = re.sub(
        r"(https?://[^\s]+)\s*\n\s*(\?[^\s]+)", r"\1\2", value, flags=re.I
    )
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def extract_text(image_bytes: bytes) -> str:
    command = _tesseract_command()

    try:
        image = Image.open(BytesIO(image_bytes)).convert("L")
        image = ImageOps.autocontrast(image)
        image = image.resize((image.width * 2, image.height * 2))
        image = image.filter(ImageFilter.SHARPEN)
    except Exception as exc:
        raise RuntimeError(f"invalid or unreadable image: {exc}") from exc

    with tempfile.TemporaryDirectory(prefix="scamguard_ocr_") as temp_dir:
        image_path = Path(temp_dir) / "input.png"
        image.save(image_path, format="PNG")

        try:
            result = subprocess.run(
                [command, str(image_path), "stdout", "--psm", "6", "-l", "eng"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("OCR timed out after 30 seconds") from exc
        except OSError as exc:
            raise RuntimeError(f"could not start Tesseract: {exc}") from exc

        if result.returncode != 0:
            detail = result.stderr.strip() or "Tesseract returned a non-zero exit code."
            raise RuntimeError(detail)

        return clean_ocr_text(result.stdout)
