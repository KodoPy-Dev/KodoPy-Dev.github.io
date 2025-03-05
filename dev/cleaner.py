########################•########################
"""                   KodoPy                  """
########################•########################

def clean():
    import os
    import shutil
    from pathlib import Path
    root_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent
    for file_path in root_dir.iterdir():
        if file_path.is_file() and file_path.suffix == ".html":
            file_path.unlink()

if __name__ == "__main__":
    clean()
