"""
Utilities related to file paths
"""
import os


def find_file(file_name: str, start_path: str = './') -> str:
    """
    Find a file recursively from the star_path and return if found
    :param file_name:
    :param start_path:
    :return:
    """
    for root, dirs, files in os.walk(start_path):
        if file_name in files:
            return os.path.join(root, file_name)
