# k3testdocumentation-generator

Tool for generating test documentation & test coverage out of a file/folder hierarchy (or an equivalent json file).
A default file/folder hierarchy is defined below with which the tool will work without customisations/custom templates.

__Tool for generationg the Documentation:__
k3testdocumentation-generator

__Tool for generationg the Coverage:__
k3testdocumentation-generate-coverage

## Installation (use within viruatlenv or equivalent)
```
pip install k3testdocumentation-generator
```

### Prerequisites/Limitations:
When generating PDFs from HTML wkhtmltopdf __needs__ to be installed (required by the pdfkit library). It is available in the package managers of the common linux distributions.  
May require running a virtual X server on a headless environment.

When generating PDFs from LATEX pdflatex __needs__ to be installed. It is also available in the package managers of the common linux distributions.

## Default File/Folder Hierarchy
```
Create a the test directory structure (example included in src).
This structure works with the inbuilt template. To support a different
structure create a custom template and pass it using the --template parameter.

Note: any json file will be opened and interpreted. In the default structure
all json files need contain a list of strings 

example_test_dir/
├── TC.XX.01
│   ├── precondition.md
│   ├── required_equiptment.json
│   ├── requirements_fully_tested.json
│   ├── requirements_partially_tested.json
│   ├── test_description.md
│   └── test_name.txt
└── TC.XX.02
    ├── test_descrition.md
    └── __test__.json (Abbreviated form allowing the direct instanciation of
                       keys in one file. Will be overwritten if the file also
                       exists)
```
__Corresponding k3testdocumentation-generator command:__  

```
k3testdocumentation-generator example_test_dir/ -v -o output.pdf
```

__Corresponding k3testdocumentation-generate-coverage command:__  
and a required json file exists with requirements in the folling format
```
["R1","R2","P1","P2"]
```

```
k3testdocumentation-generate-coverage requirements_list.json example_test_dir/ -v -o output.pdf
```