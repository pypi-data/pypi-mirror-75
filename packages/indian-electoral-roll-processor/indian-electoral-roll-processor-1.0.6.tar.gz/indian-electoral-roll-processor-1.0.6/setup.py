import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README filinstall_requires e
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="indian-electoral-roll-processor",
    version="1.0.6",
    descp="Extract data from 2020 Indian Electoral Rolls ",
    long_descp=README,
    long_descp_content="text/markdown",
    URL="https://somesite.com",
    author="",
    authoremail="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ier_processor"],
    include_package_data=True,
    package_data={'ier_processor': ['test_data/whole_pdf/Benaulim/Part01.pdf']},
    install_requires=["asgiref==3.2.7",
                      "boto3==1.14.26",
                      "botocore==1.17.27",
                      "chardet==3.0.4",
                      "docutils==0.15.2",
                      "jmespath==0.10.0",
                      "pdf2image==1.13.1",
                      "Pillow==7.1.1",
                      "pyasn1==0.4.8",
                      "pycryptodome==3.9.7",
                      "pytesseract==0.3.3",
                      "python-dateutil==2.8.1",
                      "pytz==2019.3",
                      "PyYAML==5.3.1",
                      "rsa==4.5",
                      "s3transfer==0.3.3",
                      "six==1.14.0",
                      "urllib3==1.25.10",
                      ],

    entrypoints={
        "console_scripts": [
            "realpython=ier_processor.__main__:main",
        ]
    },
)

#data_files = [('test_data/whole_pdf/Benaulim', ['test_data/whole_pdf/Benaulim/Part01.pdf'])],
