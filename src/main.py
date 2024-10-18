import os
from src.file_handler import copy_files
from src.page_generator import generate_web


def main():
    copy_files()
    generate_web()


if __name__ == "__main__":
    main()
