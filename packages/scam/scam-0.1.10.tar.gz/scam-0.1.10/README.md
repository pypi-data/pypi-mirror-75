# SourceAnalyzer 

[GitHub Repo Link](https://github.com/dcaust1n/SourceAnalyzer.git)

- A locally run application that demonstrates different matching algorithms 
- Current release compares files as a one to one connection
- Outputs given percentage of similarity and highlighted visualization of the matching sections of input documents
- Supports, raw text files and python files currently, with C++ and java planned in the future releases

Manual pdf link: 

https://www.dropbox.com/s/tdtd9n7aubkxf9u/Codalyzers%20Project.pdf?dl=0

## Getting Started

#### STEP 1 

it is recommended to create and navigate to virtual environemnt using python to run script

    python3.8 -m venv <dir> 
    source <dir>/bin/activate

#### STEP 2

install source_analyzer python package from Python Package Index.
**Note:** must be running python version 3.8 or greater

    pip install scam


###### OR

Download the latest built compressed file release from [source_analyzer-X.X.X.tar.gz](https://github.com/dcaust1n/SourceAnalyzer/tree/master/dist)



then install downloaded file

    pip3 install /<path_to_file>/scam-0.0.2.tar.gz


#### STEP 3
(make sure xlaunch is running)
run script

    scam

## Known Errors/Issues
Errors- 
Multiple of the same substring found in file B will return only the first instance of that substring. 

Issues- 
Python files featuring a heavy amount of print statements may cause skewed data. 

## Test Files
Test files can be found in: 
    <dir>/lib/python3.8/site-packages/source/test_file
there are python files and .txt files, make sure to change the file filter down below to be able to see either of them.

## Project Group: Codalyzers
- Djoni Austin | @dcaust1n
- Jared Dawson | @lukinator1
- Shane Eising | @seising99
- Julian Marott | @jmmoratta

## References: 
https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf
