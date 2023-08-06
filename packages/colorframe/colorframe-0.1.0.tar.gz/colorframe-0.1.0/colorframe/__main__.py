"""
Created on 2020.07.30
:author: Felix Soubelet

High level object to handle operations.
"""

from colorframe.api import BorderCreator
from colorframe.utils import parse_arguments, set_logger_level


def main() -> None:
    """Run from the 'python -m whiteframe' command."""
    commandline_arguments = parse_arguments()
    set_logger_level(commandline_arguments.log_level)

    border_api = BorderCreator(
        commandline_arguments.path,
        commandline_arguments.vertical_border,
        commandline_arguments.horizontal_border,
        commandline_arguments.color,
    )
    border_api.execute_target()


if __name__ == "__main__":
    main()
