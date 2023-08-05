#Contains metadata desccribing our libraries


from setuptools import setup

# Reading README.md into a variable & provide into our setup function as a
# long description argument.

with open("README.md", "r") as fh:
    long_description = fh.read()

setup (

    name = 'khatri-pck', #Name of the library (What the user will pip install, How it will be looked up in the PyPy database)
    version = '0.0.1',
    description = 'Apurva Khatri\'s first PyPy package', #Description of what the library does
    py_modules = ["helloworld"],
    package_dir = {'': 'src'},

    url = "https://github.com/apurvakhatri/Khatri-pck/tree/draft1.0",
    author = 'Apurva Khatri',
    author_email = 'apurvakhatri2011@gmail.com',

    long_description = long_description,
    long_description_content_type = "text/markdown",
)
