# LinkCollector
A command line interface for managing and querying collections of links.

## Description
The LinkCollector is a Python application that allows you to organize a collection of web links by categories and tags. Link data is organized via a LinkCollection object, which is stored in JSON format.
This application also provides a built-in interface to query data, and import/export data from/to a JSON file. The interface options include adding a new link, listing all existing links, categories or tags, querying specific links, and exiting the application.

## Getting Started
### Dependencies
The program requires Python 3+, and relies on the following Python libraries:

termcolor

### Installing
Clone the repository to your local machine, navigate to the project directory, then install any missing dependencies using pip.

```
git clone https://github.com/user/linkManager.git
cd linkManager
pip install termcolor
```

## Executing the Program
Run the script using Python 3. It was developed using python 3.11
The entry file is link_collection.py

```
python link_collection.py
```

## Help
After executing the program, you will be prompted with a series of choices to interact with your LinkCollection. You can input the number or the character associated with your desired action.

You can also print the help message or extensive help message showing all commands by typing '0', 'h', 'help' or '1', 'exh', 'exhelp' respectively.

## Contribute
Download the VSCode Extension TODO Tree and help with the TODOs

## License 
This project is licensed under the MIT License - see the LICENSE.md file for details. 

## Authors
- Eric Stautmeister
