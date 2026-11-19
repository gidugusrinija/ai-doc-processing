import os
import shutil
from pathlib import Path


def get_poppler_path() -> str | None:
    """
    Dynamically locate Poppler on Windows.

    Search order:
    1. POPPLER_PATH environment variable
    2. Windows PATH
    3. Common installation directories

    Returns:
        Poppler bin directory, or None if available through PATH.
    """

    # 1. Check environment variable
    env_path = os.getenv("POPPLER_PATH")

    if env_path:
        path = Path(env_path)

        if (path / "pdfinfo.exe").exists() and (path / "pdftoppm.exe").exists():
            return str(path)

    # 2. Check system PATH
    pdfinfo = shutil.which("pdfinfo")
    pdftoppm = shutil.which("pdftoppm")

    if pdfinfo and pdftoppm:
        return None

    # 3. Search common user directories
    user_home = Path.home()

    search_directories = [
        user_home / "poppler",
        Path("C:/poppler"),
        Path("C:/Program Files/poppler"),
    ]

    for base_dir in search_directories:

        if not base_dir.exists():
            continue

        # Search nested directories for the executables
        for pdfinfo_path in base_dir.rglob("pdfinfo.exe"):

            bin_dir = pdfinfo_path.parent

            pdftoppm_path = bin_dir / "pdftoppm.exe"

            if pdftoppm_path.exists():
                print(f"Poppler found: {bin_dir}")
                return str(bin_dir)

    raise FileNotFoundError(
        "Poppler not found. Install Poppler or add it to your system PATH."
    )