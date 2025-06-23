import pathlib
import zipfile

import httpx

REFERENCE_FMUS_URL = "https://github.com/modelica/Reference-FMUs/releases/download/v0.0.38/Reference-FMUs-0.0.38.zip"


def download_reference_fmus(
    tmpdir: pathlib.Path, subdirs: list[str] | None = None
) -> list[pathlib.Path]:
    """
    Download all reference FMUs to the specified temporary directory.

    Args:
        tmpdir: Path to the temporary directory where FMUs will be downloaded.

    Returns:
        List of paths to the downloaded FMU files.
    """
    response = httpx.get(REFERENCE_FMUS_URL, follow_redirects=True)
    response.raise_for_status()  # Ensure the request was successful

    zip_path = tmpdir / "Reference-FMUs.zip"
    with open(zip_path, "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(tmpdir)

    if subdirs is not None:
        # Filter FMUs by subdirectories if specified
        paths = []
        for subdir in subdirs:
            paths.extend(pathlib.Path(tmpdir).glob(f"{subdir}/**/*.fmu"))
        return list(map(lambda p: p.absolute(), paths))
    else:
        # Return all FMU files in the temporary directory
        return list(map(lambda p: p.absolute(), pathlib.Path(tmpdir).glob("**/*.fmu")))


def download_reference_fmu(name: str, tmpdir: pathlib.Path) -> pathlib.Path:
    # Download the reference FMU zip file to a temporary directory
    response = httpx.get(REFERENCE_FMUS_URL, follow_redirects=True)
    response.raise_for_status()  # Ensure the request was successful

    zip_path = tmpdir / "Reference-FMUs.zip"
    with open(zip_path, "wb") as f:
        f.write(response.content)

    # Extract the zip file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(tmpdir)

    # Return the path to the extracted FMU files
    return (tmpdir / name).absolute()
