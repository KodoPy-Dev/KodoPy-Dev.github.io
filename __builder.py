########################•########################
"""                   KodoPy                  """
########################•########################

import os
import shutil
from pathlib import Path


CUR_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PAGES_NAMES = 'pages'
PAGES_DIR = CUR_DIR.joinpath(PAGES_NAMES)


get_local_folders = lambda directory : [path.resolve() for path in Path(directory).iterdir() if path.is_dir()]
get_local_files = lambda directory : [path.resolve() for path in Path(directory).iterdir() if path.is_file()]
get_all_folders = lambda directory : [path.resolve() for path in Path(directory).rglob("*") if path.is_dir()]
get_all_files = lambda directory : [path.resolve() for path in Path(directory).rglob("*") if path.is_file()]


class Page:
    def __init__(self):
        # Order
        self.index = 0
        self.nesting_level = 0
        # Page
        self.page_title = None
        self.page_path = None
        self.page_content = None
        # Write
        self.write_name = None
        self.write_path = None
        # Sub
        self.sub_pages = []
        self.parent_names = []


def gen_page(folder=None):

    # Error
    if not isinstance(folder, Path):
        print("Error : Improper Call")
        return None

    # Error
    if not folder.is_dir():
        print("Error : Wrong Type")
        return None

    # Error
    if not folder.exists():
        print("Error : Invalid Directory")
        return None

    def get_splits(name=""):
        # Index and Name
        splits = name.split(' ')
        # Error
        if len(splits) != 2:
            print("Error : Invalid Folder Structure")
            return None
        # Order
        index = splits[0]
        # Error
        if not index.isdigit():
            print("Error : Invalid Folder Structure")
            return None
        # Used for file name and display name
        name = splits[1]
        # Error
        if not name:
            print("Error : Invalid Folder Structure")
            return None
        # Valid
        return index, name

    # Index and Name
    splits = get_splits(name=folder.name)

    # Error
    if splits is None:
        print("Error : Splits Failed")
        return None

    # Valid
    index, name = splits

    # Container
    page = Page()

    # Order
    page.index = int(index)

    # Nave tag name
    page.page_title = name.replace('_', ' ').title()

    # Page content path
    page.page_path = folder.joinpath('page.html')

    # Error
    if not page.page_path.exists():
        print("Error : Invalid Folder Structure")
        return None

    # Error
    if not page.page_path.is_file():
        print("Error : Invalid Folder Structure")
        return None

    # Capture page content
    with open(page.page_path, 'r', encoding='utf-8') as reader:
        page.page_content = reader.read()

    # Error
    if not page.page_content:
        print("Error : No Page Content")
        return None

    # Sub Category
    parents = []
    if folder.parent != PAGES_DIR:
        parent_names = [parent.name for parent in folder.parents]

        # Error
        if PAGES_NAMES not in parent_names:
            print("Error : Not in correct directory")
            return None

        # Iter Parents : Extracting the name from the orderings
        for parent_name in parent_names:
            # Stop at root level
            if parent_name == PAGES_NAMES:
                break
            # Index and Name
            parent_splits = get_splits(name=parent_name)

            # Error
            if parent_splits is None:
                print("Error : Splits Failed")
                return None

            # Valid
            parents.append(parent_splits[1])

    # Home > Convert to Index
    if name == 'home':
        name = 'index'

    # Write with Parents
    if parents:
        page.write_name = f"{'_'.join(parents)}_{name}.html"
        page.nesting_level = len(parents)
    # Write without Parents
    else:
        page.write_name = f'{name}.html'
    page.write_path = Path(CUR_DIR).joinpath(page.write_name)

    # Remove previous
    if page.write_path.exists():
        page.write_path.unlink()

    # Make new file
    page.write_path.touch()

    # Error
    if not page.write_path.exists():
        print("Error : Page write path failed")
        return None

    return page


def gen_pages():
    pages = []

    root_folders = get_local_folders(PAGES_DIR)
    for root_folder in root_folders:
        root_page = gen_page(folder=root_folder)
        # Error
        if root_page is None:
            print("Error : Failed to create root page")
            continue
        # Add
        pages.append(root_page)

        # Sub Pages
        sub_folders = get_local_folders(root_folder)
        for sub_folder in sub_folders:
            sub_page = gen_page(folder=sub_folder)
            # Error
            if sub_page is None:
                print("Error : Failed to create sub page")
                continue
            # Parent
            sub_page.parent_names.append(root_page.page_title)
            # Add
            root_page.sub_pages.append(sub_page)

    return pages


def build():
    pages = gen_pages()

    # Error
    if not pages:
        print("Error : No pages created")
        return

    # Sort
    pages.sort(key=lambda page: page.index)

    # All the pages to generate
    all_pages = []

    # Nav
    nav_items = []
    nav_items.append('\t\t<nav class="sidebar">')
    nav_items.append('\t\t\t<a href="https://github.com/KodoPy-Dev" target="_blank"><img src="images/KodoPy.png"></a>')

    for page in pages:
        all_pages.append(page)
        tag = f'\t\t\t<a href="{page.write_name}">{page.page_title}</a>'
        nav_items.append(tag)
        if page.sub_pages:
            nav_items.append('\t\t\t<ul>')
            for sub_page in page.sub_pages:
                all_pages.append(sub_page)
                tag = f'\t\t\t\t<li><a href="{sub_page.write_name}">{sub_page.page_title}</a></li>'
                nav_items.append(tag)
            nav_items.append('\t\t\t</ul>')
    nav_items.append('\t\t</nav>')

    # Write
    for page in all_pages:

        header = ""
        if page.parent_names:
            header = f'<h1>{" » ".join(page.parent_names)} » {page.page_title}</h1>'
        else:
            header = f'<h1>{page.page_title}</h1>'

        content = [
            '<!DOCTYPE html>',
            '<html lang="en">',
            '\t<head>',
            '\t\t<meta charset="UTF-8">',
            '\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            '\t\t<title>KodoPy Docs</title>',
            '\t\t<link rel="icon" href="images/favicon.ico" type="image/x-icon">',
            '\t\t<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">',
            '\t\t<link href="styles/prism.css" rel="stylesheet">',
            '\t\t<link href="styles/theme.css" rel="stylesheet">',
            '\t</head>',
            '\t<body>',
            '\n<!--------------------------------------------- NAV --------------------------------------------->',
            *nav_items,
            '\t\t<div class="content">',
            '\n<!--------------------------------------------- PAGE --------------------------------------------->',
            header,
            page.page_content,
            '\n<!--------------------------------------------- FOOTER --------------------------------------------->',
            '\t\t</div>',
            '\t\t<script src="scripts/prism.js"></script>',
            '\t\t<script>Prism.highlightAll();</script>',
            '\t\t<script src="scripts/logic.js"></script>',
            '\t</body>',
            '</html>',
        ]
        page.write_path.write_text("\n".join(content), encoding="utf-8")


if __name__ == "__main__":
    build()
