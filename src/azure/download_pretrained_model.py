import urllib.request
from pathlib import Path


def download_pretrained_model(url: str, file: str) -> None:
    """
    Download a pretrained model to the models folder
    :param url: url of the model to be downloaded
    :param file: name of the downloaded model
    :return: None
    """
    # file = Path("./models/") / file
    if not Path(file).exists():
        urllib.request.urlretrieve(url=url, filename=file)
