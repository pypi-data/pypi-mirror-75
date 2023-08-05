# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fitzutils', 'pdftocgen', 'pdftocio', 'pdfxmeta']

package_data = \
{'': ['*']}

install_requires = \
['PyMuPDF>=1.17.4,<2.0.0', 'toml>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['pdftocgen = pdftocgen.app:main',
                     'pdftocio = pdftocio.app:main',
                     'pdfxmeta = pdfxmeta.app:main']}

setup_kwargs = {
    'name': 'pdf.tocgen',
    'version': '0.9.9',
    'description': 'Automatically generate table of contents for pdf files',
    'long_description': 'pdf.tocgen\n==========\n\n```\n                          in.pdf\n                            |\n                            |\n     +----------------------+--------------------+\n     |                      |                    |\n     V                      V                    V\n+----------+          +-----------+         +----------+\n|          |  recipe  |           |   ToC   |          |\n| pdfxmeta +--------->| pdftocgen +-------->| pdftocio +---> out.pdf\n|          |          |           |         |          |\n+----------+          +-----------+         +----------+\n```\n\n[pdf.tocgen][tocgen] is a set of command-line tools for automatically\nextracting and generating the table of contents (ToC) of a PDF file. It uses\nthe embedded font attributes and position of headings to deduce the basic\noutline of a PDF file.\n\nIt works best for PDF files produces from a TeX document using `pdftex` (and\nits friends `pdflatex`, `pdfxetex`, etc.), but it\'s designed to work with any\n**software-generated** PDF files (i.e. you shouldn\'t expect it to work with\nscanned PDFs). Some examples include `troff`/`groff`, Adobe InDesign, Microsoft\nWord, and probably more.\n\nPlease see the [**homepage**][tocgen] for a detailed introduction.\n\nInstallation\n------------\n\n`pdf.tocgen` written in Python 3. It is known to work with Python 3.8 under\nLinux, but Python 3.7 should be the minimum. Use\n\n```sh\n$ pip install -U pdf.tocgen\n```\nto install the latest version systemwide, or use\n\n```sh\n$ pip install -U --user pdf.tocgen\n```\nto install it for the current user. I would recommend the latter approach to\navoid messing up the package managers on your system.\n\nWorkflow\n--------\n\nThe design of pdf.tocgen is influenced by the [Unix philosophy][unix]. I\nintentionally separated pdf.tocgen to 3 separate programs. They work together,\nbut each of them is useful on their own.\n\n1. `pdfxmeta`: extract the metadata (font attributes, positions) of headings to\n    build a **recipe** file.\n2. `pdftocgen`: generate a table of contents from the recipe.\n3. `pdftocio`: import the table of contents to the PDF document.\n\nYou should read [the example][ex] on the homepage for a proper introduction,\nbut the basic workflow follows like this.\n\nFirst, use `pdfxmeta` to search for metadata of headings\n\n```sh\n$ pdfxmeta -p page in.pdf pattern >> recipe.toml\n$ pdfxmeta -p page in.pdf pattern2 >> recipe.toml\n```\n\nEdit the `recipe.toml` file to pick out the attributes you need and specify the\nheading levels.\n\n```sh\n$ vim recipe.toml # edit\n```\n\nAn example recipe would look like this:\n\n```toml\n[[filter]]\nlevel = 1\nfont.name = "Times-Bold"\nfont.size = 19.92530059814453\n\n[[filter]]\nlevel = 2\nfont.name = "Times-Bold"\nfont.size = 11.9552001953125\n```\n\nThen pass the recipe to `pdftocgen` to generate a table of contents,\n\n```console\n$ pdftocgen in.pdf < recipe.toml\n"Preface" 5\n    "Bottom-up Design" 5\n    "Plan of the Book" 7\n    "Examples" 9\n    "Acknowledgements" 9\n"Contents" 11\n"The Extensible Language" 14\n    "1.1 Design by Evolution" 14\n    "1.2 Programming Bottom-Up" 16\n    "1.3 Extensible Software" 18\n    "1.4 Extending Lisp" 19\n    "1.5 Why Lisp (or When)" 21\n"Functions" 22\n    "2.1 Functions as Data" 22\n    "2.2 Defining Functions" 23\n    "2.3 Functional Arguments" 26\n    "2.4 Functions as Properties" 28\n    "2.5 Scope" 29\n    "2.6 Closures" 30\n    "2.7 Local Functions" 34\n    "2.8 Tail-Recursion" 35\n    "2.9 Compilation" 37\n    "2.10 Functions from Lists" 40\n"Functional Programming" 41\n    "3.1 Functional Design" 41\n    "3.2 Imperative Outside-In" 46\n    "3.3 Functional Interfaces" 48\n    "3.4 Interactive Programming" 50\n[--snip--]\n```\nwhich can be directly imported to the PDF file using `pdftocio`,\n\n```sh\n$ pdftocgen in.pdf < recipe.toml | pdftocio -o out.pdf in.pdf\n```\n\nOr if you want to edit the table of contents before importing it,\n\n```sh\n$ pdftocgen in.pdf < recipe.toml > toc\n$ vim toc # edit\n$ pdftocio in.pdf < toc\n```\n\nEach of the three programs has some extra functionalities. Use the `-h` option\nto see all the options you could pass in.\n\nDevelopment\n-----------\n\nIf you want to modify the source code or contribute anything, first install\n[`poetry`][poetry], which is a dependency and package manager for Python used\nby pdf.tocgen. Then run\n\n```sh\n$ poetry install\n```\nin the root directory of this repository to set up development dependencies.\n\nIf you want to test the development version of pdf.tocgen, use the `poetry run` command:\n\n```sh\n$ poetry run pdfxmeta in.pdf "pattern"\n```\nAlternatively, you could also use the\n\n```sh\n$ poetry shell\n```\ncommand to open up a virtual environment and run the development version\ndirectly:\n\n```sh\n(pdf.tocgen) $ pdfxmeta in.pdf "pattern"\n```\n\nBefore you send a patch or pull request, make sure the unit test passes by\nrunning:\n\n```sh\n$ make test\n```\n\nLicense\n-------\n\npdf.tocgen is free software. The source code of pdf.tocgen is licensed under\nthe GNU GPLv3 license.\n\npdf.tocgen is based on [PyMuPDF][pymupdf], licensed under the GNU GPLv3\nlicense, which is again based on [MuPDF][mupdf], licensed under the GNU AGPLv3\nlicense. A copy of the AGPLv3 license is included in the repository.\n\nIf you want to make any derivatives based on this project, please follow the\nterms of the GNU GPLv3 license.\n\n[tocgen]: https://krasjet.com/voice/pdf.tocgen/\n[unix]: https://en.wikipedia.org/wiki/Unix_philosophy\n[ex]: https://krasjet.com/voice/pdf.tocgen/#a-worked-example\n[poetry]: https://python-poetry.org/\n[pymupdf]: https://github.com/pymupdf/PyMuPDF\n[mupdf]: https://mupdf.com/docs/index.html\n',
    'author': 'krasjet',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://krasjet.com/voice/pdf.tocgen/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
