#!/usr/bin/env python3

from pathlib import Path
import sys


def print_shortened_path(
    directory_path: Path,
    *,
    max_len: int = 60,
    first_directories: int = 2,
    last_directories: int = 1,
) -> None:
    """Function that takes sys.argv Path argument and shorten it accordingly.

    It should replace ${HOME} with ~.
    If after replacing lenght of arg is lower than `max_len`, then it just prints it.

    If it exceeds maximum limit, path should be limited to the amount of directories that
    are specified as the arguments.

    >>> print_shortened_path(Path("~/git/some/long/path/to/process"), last_directories=2)
    ~/git/some/long/path/to/process

    >>> print_shortened_path(Path("~/git/some/long/path/to/process/that/should/be/shortened/to/this"), last_directories=2)
    ~/git/some/../to/this

    >>> print_shortened_path(Path("/git/some/long/path/to/process/that/should/be/shortened/to/this"), last_directories=2)
    /git/some/../to/this

    >>> print_shortened_path(Path("/git/some_long_path_to_with_more_elements/process/that/should_be_shortened_to/this"), last_directories=2)
    /git/some_long_path_to_with_more_elements/../should_be_shortened_to/this

    >>> print_shortened_path(Path("/git/some_long_path_to_with_more_elements_process_should_be/this"))
    /git/some_long_path_to_with_more_elements_process_should_be/this

    >>> print_shortened_path(Path("~/git/some/long/path/to/process"), last_directories=1)
    ~/git/some/long/path/to/process

    >>> print_shortened_path(Path("~/git/some/long/path/to/process/that/should/be/shortened/to/this"), last_directories=1)
    ~/git/some/../this

    >>> print_shortened_path(Path("/git/some/long/path/to/process/that/should/be/shortened/to/this"), last_directories=1)
    /git/some/../this

    >>> print_shortened_path(Path("/git/some_long_path_to_with_more_elements/process/that/should_be_shortened_to/this"), last_directories=1)
    /git/some_long_path_to_with_more_elements/../this

    >>> print_shortened_path(Path("/git/some_long_path_to_with_more_elements_process_should_be/this"))
    /git/some_long_path_to_with_more_elements_process_should_be/this
    """
    home_path = Path.home()
    if directory_path.is_relative_to(home_path):
        directory_path = Path("~", directory_path.relative_to(home_path))

    stringified_directory = str(directory_path)
    if len(stringified_directory) > max_len:
        path_element = Path(directory_path)
        path_elements = [path_element.name]
        while path_element := path_element.parent:
            if path_element.name == "":
                break
            path_elements.append(path_element.name)
        path_elements = list(reversed(path_elements))
        number_of_path_elements = len(path_elements)

        if first_directories + last_directories < number_of_path_elements:
            directories_to_leave_in_front = number_of_path_elements - last_directories
            if directories_to_leave_in_front < 0:
                directories_to_leave_in_front = 0
            else:
                directories_to_leave_in_front = min(
                    first_directories, directories_to_leave_in_front
                )
            prefix = "/" if directory_path.is_absolute() else ""
            if not directory_path.is_absolute():
                directories_to_leave_in_front += 1
            rebuilt_path = Path(
                prefix,
                *path_elements[:directories_to_leave_in_front],
                "..",
                *path_elements[-last_directories:],
            )

            print(rebuilt_path)
            return

    print(stringified_directory)


if __name__ == "__main__":
    assert (
        len(sys.argv) == 2
    ), "Wrong number of arguments, usage: shorten_path.py <path>"
    directory_path = Path(sys.argv[1])
    print_shortened_path(directory_path)
