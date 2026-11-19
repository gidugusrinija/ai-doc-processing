import os
import shutil
from pathlib import Path


def get_poppler_path() -> str | None:

    # 1. Check environment variable
    env_path = os.getenv("POPPLER_PATH")

    if env_path:
        path = Path(env_path)

        if (
            (path / "pdfinfo.exe").exists()
            and (path / "pdftoppm.exe").exists()
        ):
            return str(path)

    # 2. Check Windows PATH
    if shutil.which("pdfinfo") and shutil.which("pdftoppm"):
        return None

    # 3. Search common Poppler installation directories
    user_home = Path.home()

    search_directories = [
        Path("C:/poppler"),
        Path("C:/Program Files/poppler"),
        user_home / "poppler",
    ]

    # Include folders such as poppler-26.09.0 under the user directory
    search_directories.extend(
        user_home.glob("poppler*")
    )

    for base_dir in search_directories:

        if not base_dir.exists():
            continue

        # Search for pdfinfo.exe
        for pdfinfo_path in base_dir.rglob("pdfinfo.exe"):

            bin_dir = pdfinfo_path.parent

            pdftoppm_path = bin_dir / "pdftoppm.exe"

            if pdftoppm_path.exists():

                print(f"Poppler found: {bin_dir}")

                return str(bin_dir)

    raise FileNotFoundError(
        "Poppler not found. Please install Poppler "
        "or configure POPPLER_PATH."
    )