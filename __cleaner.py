########################•########################
"""                   KodoPy                  """
########################•########################

import os
import shutil
from pathlib import Path

CUR_DIR_ = Path(os.path.dirname(os.path.abspath(__file__)))


def clean():
    global CUR_DIR_
    for file_path in CUR_DIR_.iterdir():
        if file_path.is_file() and file_path.suffix == ".html":
            file_path.unlink()


if __name__ == "__main__":
    clean()
