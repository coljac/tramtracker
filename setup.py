from setuptools import setup, find_packages
setup(
    name = "tramtracker",
    version = "0.1",
    packages = find_packages(),
    scripts = ['tramtracker.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = [],

    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author = "Colin Jacobs",
    author_email = "colin@coljac.net",
    description = "Python command line tool to access Yarra Trams TramTracker data",
    license = "Public Domain",
    keywords = "tramtracker command-line",
    url = "https://github.com/coljac/tramtracker",
)
