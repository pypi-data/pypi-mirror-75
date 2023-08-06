import setuptools
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding='utf-8' ) as fh:
    long_description = fh.read()

setuptools.setup(
    name="scam",
    version="0.2.3", 
    author="Codalyzers",
    author_email="djoni.austin@gmail.com",
    description="Source Code Analyzing Maching is an pplication for the analysis of similarities between separate files. Currently with Python, Java, and '*.txt' file checking capabilities.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dcaust1n/SourceAnalyzer",
#    package_dir={"": "source_analyzer"},
    packages=setuptools.find_packages(), #where='source_analyzer'
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['javalang'],
    include_package_data=True,
    package_data={
        "": [ "*.txt","*.py","*.png", "test_files/*.txt","test_files/*.py", "test_files/*.java"],
    },
    entry_points={
        'console_scripts': [
            'source_analyzer=source.source_analyzer:main',
            'source-analyzer=source.source_analyzer:main', 
            'scam=source.source_analyzer:main',
        ],
    },
)
