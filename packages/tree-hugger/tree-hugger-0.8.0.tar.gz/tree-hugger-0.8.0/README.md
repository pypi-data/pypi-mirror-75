# tree-hugger
Mining source code repositories at scale easily. Tree-hugger is a light-weight, high level library which provides Pythonic APIs  to mine recursively trough Github repositories.
Tree-hugger is built on top of tree-sitter.

Covered languages:
* Python
* PHP
* Java
* JavaScript
* C++ _(coming)_

_System Requirement: Python 3.6_

## Contents

1. [Installation](#installation)

2. [Setup](#setup)

3. [Hello world example](#hello-world-example)

4. [API reference](#api-reference)

5. [Extending tree-hugger](#extending-tree-hugger)
  
    - [Adding languages](#adding-languages)

    - [Adding queries](#adding-queries)

6. [Roadmap](#roadmap)

-------------


## Installation

### From pip:

```
pip install tree-hugger
```

### From Source:

```
git clone https://github.com/autosoft-dev/tree-hugger.git

cd tree-hugger

pip install -e .
```

_The installation process is tested in macOS Mojave, we have a [separate docker binding](https://github.com/autosoft-dev/tree-sitter-docker) for compiling the libraries for Linux and soon this library will be integrated in that as well_

_You may need to install libgit2. In case you are in mac just use `brew install libgit2`_

## Setup

### Building the .so files

_Please note that building the libraries has been tested under a macOS Mojave with Apple LLVM version 10.0.1 (clang-1001.0.46.4)_

_Please check out our Linux specific instructions [here](https://github.com/autosoft-dev/tree-sitter-docker)_

Once this library is installed it gives you a command line utility to download and compile tree-sitter .so files with ease. As an example - 

```
create_libs python
```

Here is the full usage guide of the command

```
usage: create_libs [-h] [-c] [-l LIB_NAME] langs [langs ...]

positional arguments:
  langs                 Give the name of languages for tree-sitter (php,
                        python, go ...)

optional arguments:
  -h, --help            show this help message and exit
  -c, --copy-to-workspace
                        Shall we copy the created libs to the present dir?
                        (default: False)
  -l LIB_NAME, --lib-name LIB_NAME
                        The name of the generated .so file
```

### Environment variables
You can set up `TS_LIB_PATH` environment variable for the tree-sitter lib path and then the libary will use them automatically. Otherwise, as an alternative, you can pass it when creating any `Parser` object.


## Hello world example

1. **Generate the librairies** : run the above command to generate the libraries. 

    In our settings we use the `-c` flag to copy the generated `tree-sitter` library's `.so` file to our workspace. Once copied, we place it under a directory called `tslibs` (It is in the .gitignore).
    
    ⚠ If you are using linux,you will need to use our [tree-sitter-docker](https://github.com/autosoft-dev/tree-sitter-docker) image and manually copy the final .so file.

2. **Setup environment variable** (optional)
Assuming that you have the necessary environment variable setup. The following line of code will create a `PythonParser` object

```python
from tree_hugger.core import PythonParser

pp = PythonParser()
```

And then you can pass in any Python file that you want to analyze, like so :

```python
pp.parse_file("tests/assets/file_with_different_functions.py")
Out[3]: True
```

`parse_file` returns `True` if success

And then you are free to use the methods exposed by that particular Parser object. As an example - 

```python
pp.get_all_function_names()
Out[4]:
['first_child',
 'second_child',
 'say_whee',
 'wrapper',
 'my_decorator',
 'parent']
```

OR

```python
pp.get_all_function_documentations()
Out[5]:
{'parent': '"""This is the parent function\n    \n    There are other lines in the doc string\n    This is the third line\n\n    And this is the fourth\n    """',
 'first_child': "'''\n        This is first child\n        '''",
 'second_child': '"""\n        This is second child\n        """',
 'my_decorator': '"""\n    Outer decorator function\n    """',
 'say_whee': '"""\n    Hellooooooooo\n\n    This is a function with decorators\n    """'}
 ```

 *(Notice that, in the last call, it only returns the functions which has a documentation comment)*

## API reference


| Language      | Functions        | Methods      | Classes |
| ------------- |-------------|-------------|-------------|
| **Python**        |  all_function_names all_function_doctrings  all_function_names_and_params  all_function_bodies  |  all_class_methods  all_class_method_docstrings |  all_class_names  all_class_docstrings |
| **PHP**           | all_function_names  all_function_names_and_params   all_function_bodies | all_class_methods  |  all_class_names |
| **Java**          |   |  all_class_methods   all_method_names_and_params  all_method_bodies   |  all_class_names   |
| **JavaScript**    | all_function_names  all_function_names_and_params  all_function_bodies  |  all_class_methods   |  all_class_names |
   

## Extending tree-hugger

Extending tree-hugger for other languages and/or more functionalities for the already provided ones, is easy. 

1. ### Adding languages:
Parsed languages can be extended through adding a parser class from the BaseParser class. The only mandatory argument that a Parser class should pass to the parent is the `language`. This is a string. Such as `python` (lower case). Each parser class must have the options to take in the path of the tree-sitter library (.so file that we are using to parse the code) and the path to the queries yaml file, in their constructor.

The BaseParser class can do few things: 
- Loading and preparing the .so file with respect to the language you just mentioned.
- Loading, preparing and parsing the query yaml file. (for the queries, we internally use an extended UserDict class)
- Providing an API to parse a file and prepare it for query. `BaseParser.parse_file`

It also gives you another (most likely not to be exposed outside) API `_run_query_and_get_captures` which lets you run any queries and return back the matched results (if any) from the parsed tree.

We use those APIs once we have called `parse_file` and parsed the file.


2. ### Adding queries: 
Queries processed on source code are s-expressions, they are listed in a `queries.yml`file for each parser class. Tree-hugger gives you a way to write your queries in yaml file for each language parsed.

**Query structure**: A name of a query followed by the query itself. Written as an s-expression. *Example*:

```
all_function_docstrings:
        "
        (
            function_definition
            name: (identifier) @function.def
            body: (block(expression_statement(string))) @function.docstring
        )
        "
```
You have to follow yaml grammar while writing these queries. You can see a bit more about writng these queries in the [documentation of tree-sitter](https://tree-sitter.github.io/tree-sitter/using-parsers#pattern-matching-with-queries). 

Some example queries, that you will find in the yaml file (and their corresponding API from the PythonParser class) - 

```
* all_function_names => get_all_function_names()

* all_function_docstrings => get_all_function_documentations()

* all_class_methods => get_all_class_method_names()
```


## Roadmap


 * Documentation: tutorial on queries writing

 * Write *Parser class for other languages

| Languages     | Status-Finished           | Author  |
| ------------- |:-------------:| :-----:|
| Python     |✅  | [Shubhadeep](https://github.com/rcshubhadeep) |
| PHP      | ✅    |   [Clément](https://github.com/CDluznie) |
| Java | ✅      |   [Clément](https://github.com/CDluznie)  |
| JavaScript |✅    | [Clément](https://github.com/CDluznie) | 
| C++ |  ▶ | [Clément](https://github.com/CDluznie)  |
