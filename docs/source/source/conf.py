# docs/source/conf.py

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'myst_parser',            # ← add this
]

# Tell Sphinx which suffixes to read:
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
