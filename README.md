# LinkManager

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)

A powerful command-line interface for organizing, managing, and querying collections of web links, designed for developers and power users who prefer terminal-based workflows.

## 🌟 Features

-   **Organize web links** with categories and tags
-   **Powerful search** with AND/OR logic and advanced filtering
-   **Bulk operations** for efficient link management
-   **Data import/export** via CSV files
-   **Backups and Recovery** to prevent data loss
-   **Rich command-line interface** with color-coded outputs

## 📋 Description

LinkManager is a Python CLI application that helps you organize your collection of web links with categories and tags. Whether you're a researcher collecting references, a developer saving useful resources, or just someone who wants to keep track of interesting websites, LinkManager provides a fast, efficient way to store and retrieve your links.

The application stores your link collection in a simple JSON format which makes it easy to backup, version control, or integrate with other tools. LinkManager provides a robust interface to query your data, making it easy to find exactly what you're looking for.

## 🚀 Getting Started

### Prerequisites

-   Python 3.11 or higher
-   Required Python libraries:
    -   setuptools >= 75.6.0
    -   termcolor >= 2.5.0

### Installation

1. Clone the repository:

```bash
git clone https://github.com/EricStautmeister/LinkManager.git
cd LinkManager
```

2. Install the package and its dependencies:

```bash
pip install --upgrade setuptools[core] setuptools termcolor
pip install -e .
```

For development work, the `-e` flag installs the package in "editable" mode.

### Usage

After installation, you can run LinkManager from anywhere in your terminal:

```bash
LinkManager
```

Or use command-line arguments for specific operations:

```bash
# Add a new link
LinkManager --add https://example.com

# Search for links
LinkManager --query python

# Export links to a CSV file
LinkManager --export links_backup.csv

# Import links from a CSV file
LinkManager --import links_to_import.csv

# Create a database backup
LinkManager --backup
```

## 📋 Commands

When running the interactive CLI, you'll have access to these commands:

| Command                        | Description                                           |
| ------------------------------ | ----------------------------------------------------- |
| `0`, `h`, `help`               | Print help message                                    |
| `1`, `exh`, `exhelp`           | Print extensive help message                          |
| `2`, `add`                     | Add a link with URL, description, categories and tags |
| `3`, `ll`                      | List existing links                                   |
| `4`, `lc`                      | List existing categories                              |
| `5`, `lt`                      | List existing tags                                    |
| `6`, `db`, `all`               | List entire database with details                     |
| `7`, `query`, `q`, `?`, `find` | Query the database by URL, category and/or tags       |
| `8`, `adv`, `advanced`         | Advanced search with multiple criteria                |
| `9`, `edit`                    | Edit a link's properties                              |
| `10`, `rm`, `remove`           | Remove a link from the database                       |
| `11`, `bulk`                   | Bulk operations menu (add/remove tags or categories)  |
| `12`, `import`, `export`       | Import/Export links from/to CSV                       |
| `13`, `backup`, `restore`      | Backup or restore the database                        |
| `20`, `exit`, `close`, `quit`  | Save and exit the application                         |

## 🗄️ Data Storage

LinkManager creates a `links.json` file in a folder called `LinkManager` under your home directory. This file serves as the database for your link collection.

The data structure is a simple JSON format that includes:

-   All links with their URLs, descriptions, categories, and tags
-   Lists of all categories and tags for quick reference

## 🔄 Bulk Operations

LinkManager supports bulk operations to help you manage large collections efficiently:

-   Add or remove categories across multiple links
-   Add or remove tags across multiple links
-   Import and export links in CSV format
-   Create and restore backups

## 🔍 Advanced Search

The advanced search feature allows you to:

-   Use AND/OR logic between search terms
-   Search across URLs, descriptions, categories, and tags
-   Filter results based on multiple criteria
-   Save search results for further processing

## 🛠️ Building Distributions

To build both a binary distribution (wheel) and a source distribution:

```bash
python setup.py bdist_wheel sdist
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Download the VSCode Extension "TODO Tree" and help with the TODOs and FIXMEs throughout the codebase.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

-   Eric Stautmeister
