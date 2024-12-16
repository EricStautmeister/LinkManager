from setuptools import find_packages, setup


if __name__ == "__main__":
    setup(
        name = 'LinkManager',
        version = '0.0.1',
        desciption="A command line interface for managing and querying collections of links.",
        package_dir={"": "app"},
        packages=find_packages(where="app"),
        url="https://github.com/EricStautmeister/LinkManager",
        author="EricStautmeister",
        license="MIT",
        # packages = ['app'],
        entry_points = {
            'console_scripts': [
                'LinkManager = LinkManager.link_manager:main'
            ]
        },
        install_requires=[
            "termcolor >= 2.5.0",
            "setuptools >= 75.6.0"
        ],
        python_requires=">=3.11",
    )