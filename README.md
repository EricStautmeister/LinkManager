# LinkManager
A command line interface for managing and querying collections of links.

## Description
The LinkManager is a Python application that allows you to organize a collection of web links by categories and tags. Link data is organized via a LinkManager object, which is stored in JSON format.
This application also provides a built-in interface to query data, and import/export data from/to a JSON file. The interface options include adding a new link, listing all existing links, categories or tags, and querying specific links by the previously mentioned categories, and exiting the application.

## Getting Started
### Dependencies
The program requires Python 3+, and relies on the following Python libraries:

- setuptools >= 75.6.0
- termcolor >= 2.5.0

### Programm information
The Programm will upon running it the first time create a JSON file in a Folder called "LinkManager" under the users home directory. This file acts as the database for the link collection. 


### Installing
Clone the repository to your local machine, navigate to the project directory, then install any missing dependencies using pip. The "-e" flag is optional, and only necessary if you plan on doing dev work on the project. 

```bash
git clone https://github.com/EricStautmeister/LinkManager.git
cd LinkManager
pip install --upgrade setuptools[core], setuptools, termcolor
pip install -e .
```

## Executing the Program
After running the above pip installs, you can call the app from anywhere using:
```bash
LinkManager
```

### Build binary and source distribution
To build both a binary distribution (wheel) and a source distribution (sdist) run the following:
```bash
python setup.py bdist_wheel sdist
```

## Contribute
Download the VSCode Extension TODO Tree and help with the TODOs and FIXMEs

## License 
This project is licensed under the MIT License - see the LICENSE.md file for details. 

## Authors
- Eric Stautmeister
