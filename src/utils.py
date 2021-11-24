import os
import pickle

import dvc.api
from loguru import logger


def load_object(
    filename: str,
    local_path: str = "./models",
    cache_path: str = os.path.join(os.path.expanduser("~"), ".cache/deploying-ML"),
    remote: str = "s3",
    rev: str = "main",
):
    """
    Checks to see whether a file exists in a local cache, and if not downloads
    it from dvc.

    Args:
        filename(str): Name of the file (e.g. model.pk)
        cache_path(str): Path to system cache.
        local_path(str): Path to where the file exists in the repository.
        remote(str): Which dvc remote to load the data from.
        rev(str): Which git revision to load the data from.
    """

    cached_object_path = os.path.join(cache_path, filename)
    local_object_path = os.path.join(local_path, filename)

    # Check whether the cache exists, and if not, create it

    if not os.path.exists(cache_path):
        logger.debug("{} does not exist, creating...", cache_path)
        os.makedirs(cache_path)

    # If the file doesn't exist in the cache, then download it from dvc and
    # store it in the cache.

    if not os.path.exists(cached_object_path):

        logger.debug(
            "{} does not exist in cache, loading from dvc and saving to {}",
            filename,
            cached_object_path,
        )

        with dvc.api.open(
            local_object_path, remote=remote, rev=rev, mode="rb"
        ) as remote_file:
            with open(cached_object_path, "wb") as cached_file:
                remote_file_contents = remote_file.read()
                cached_file.write(remote_file_contents)

    else:
        logger.debug(
            "{} exists in cache, loading from {}", filename, cached_object_path
        )

    # Load the file from the cache

    logger.info(cached_object_path)
    with open(cached_object_path, "rb") as cached_file:
        artefact = pickle.load(cached_file)

    # Return the artefact

    return artefact
