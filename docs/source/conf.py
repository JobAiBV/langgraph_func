# docs/source/conf.py
import toml
from pathlib import Path

# -- Path setup --------------------------------------------------------------
# Add your package (src/) to sys.path if needed.

# -- Project metadata -------------------------------------------------------
pyproject = toml.load(Path(__file__).parents[2] / "pyproject.toml")
project = pyproject["tool"]["poetry"]["name"]
raw_authors = pyproject["tool"]["poetry"].get("authors", [])
if raw_authors and isinstance(raw_authors[0], str):
    author = ", ".join(a.split(" <")[0] for a in raw_authors)
else:
    author = ", ".join(a.get("name", str(a)) for a in raw_authors)
release = pyproject["tool"]["poetry"]["version"]

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',
]
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
templates_path = ['_templates']
exclude_patterns = []

# -- HTML output -------------------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
