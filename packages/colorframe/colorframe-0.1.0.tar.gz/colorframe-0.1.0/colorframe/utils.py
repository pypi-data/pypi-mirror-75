"""
Created on 2020.07.30
:author: Felix Soubelet

Some utilities for main functionality.
"""
import argparse
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, Iterator

from loguru import logger


@contextmanager
def timeit(function: Callable) -> Iterator[None]:
    """
    Returns the time elapsed when executing code in the context via `function`.
    Original code from @jaimecp89

    Args:
        function: any callable taking one argument. Was conceived with a lambda in mind.

    Returns:
        The elapsed time as an argument for the provided function.

    Usage:
        with timeit(lambda spanned: logger.debug(f'Did some stuff in {spanned} seconds')):
            some_stuff()
            some_other_stuff()
    """
    start_time = time.time()
    try:
        yield
    finally:
        time_used = time.time() - start_time
        function(time_used)


def parse_arguments():
    """
    Simple argument parser to make life easier in the command-line.
    Returns a NameSpace with arguments as attributes.
    """
    parser = argparse.ArgumentParser(description="Adding a colored border to your images.")
    parser.add_argument(
        "-p",
        "--path",
        dest="path",
        type=str,
        default=None,
        required=True,
        help="Path to the file or directory of files to add a colored border to.",
    )
    parser.add_argument(
        "-hv",
        "--vertical_border",
        dest="vertical_border",
        type=int,
        default=150,
        help="Size (width) of the whiteframe to add on the vertical image edges. Defaults to 150.",
    )
    parser.add_argument(
        "-hb",
        "--horizontal_border",
        dest="horizontal_border",
        type=int,
        default=150,
        help="Size (height) of the whiteframe to add on the horizontal image edges. Defaults to "
        "150.",
    )
    parser.add_argument(
        "-c",
        "--color",
        dest="color",
        type=str,
        default="white",
        help="The desired color of the added border. Should be a keyword recognized by Pillow. "
        "Defaults to 'white'.",
    )
    parser.add_argument(
        "-l",
        "--logs",
        dest="log_level",
        type=str,
        default="info",
        help="The logging level. Defaults to 'info'.",
    )
    return parser.parse_args()


def set_logger_level(log_level: str = "info") -> None:
    """
    Sets the logger level to the one provided at the commandline.

    Default loguru handler will have DEBUG level and ID 0.
    We need to first remove this default handler and add ours with the wanted level.

    Args:
        log_level: string, the default logging level to print out.

    Returns:
        Nothing, acts in place.
    """
    logger.remove(0)
    logger.add(sys.stderr, level=log_level.upper())


def create_output_dir() -> None:
    """Create a local directory named 'outputs' to store resulting images into."""
    output_dir = Path("outputs")

    if not output_dir.is_dir():
        logger.info("Creating output directory")
        output_dir.mkdir()
    else:
        logger.warning(
            "The 'outputs' directory is already present. This may lead to unexpected problems, "
            "please remove it before trying again."
        )
        sys.exit()
