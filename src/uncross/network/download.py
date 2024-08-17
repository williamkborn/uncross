"""Download helpers."""

from http import HTTPStatus
from pathlib import Path

import requests
from rich.progress import BarColumn, DownloadColumn, Progress, TextColumn


def download_file(url, dest_path):
    """Download url file to path."""
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(),
            DownloadColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
            "•",
            TextColumn("[progress.elapsed]{task.elapsed:>.2f} sec"),
        ) as progress:
            response = requests.get(url, stream=True, timeout=30)

            if response.status_code == HTTPStatus.NOT_FOUND:
                raise FileNotFoundError

            total = int(response.headers.get("content-length", 0))
            task = progress.add_task("Download", filename=dest_path.name, total=total)

            with open(dest_path, "wb") as file:
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    progress.update(task, advance=len(data))
    except requests.exceptions.ConnectionError as exc:
        raise ConnectionError from exc
