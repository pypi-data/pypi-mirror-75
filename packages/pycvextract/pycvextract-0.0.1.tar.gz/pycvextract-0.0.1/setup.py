import setuptools

from os import path


here = path.abspath(path.dirname(__file__))





with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycvextract", # Replace with your own username
    version="0.0.1",
    author="yenatfanta shifferaw",
    author_email="yenatshif@gmail.com",
    description="'A simple resume parser used for extracting information from resumes'",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yenat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    package_data={
   'pycvextract.pycvextract': ['*']     # All files from folder A
     #All text files from folder B
   },


    include_package_data=True,

    install_requires=[
        'attrs>=19.1.0',
        'blis>=0.2.4',
        'certifi>=2019.6.16',
        'chardet>=3.0.4',
        'cymem>=2.0.2',
        'docx2txt>=0.7',
        'idna>=2.8',
        'jsonschema>=3.0.1',
        'nltk>=3.4.3',
        'numpy>=1.16.4',
        'pandas>=0.24.2',
        'pdfminer.six>=20181108',
        'preshed>=2.0.1',
        'pycryptodome>=3.8.2',
        'pyrsistent>=0.15.2',
        'python-dateutil>=2.8.0',
        'pytz>=2019.1',
        'requests>=2.22.0',
        'six>=1.12.0',
        'sortedcontainers>=2.1.0',
        'spacy>=2.1.4',
        'srsly>=0.0.7',
        'textract>=1.6.1',
        'thinc>=7.0.4',
        'tqdm>=4.32.2',
        'urllib3>=1.25.3',
        'wasabi>=0.2.2'
    ],

)
