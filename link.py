import os
import json
from termcolor import colored
from threading import Thread


class Link:
    """
    Represents a hyperlink with associated metadata.

    Args:
        url (str): The URL of the link.
        description (str, optional): Description of the link. Defaults to None.
        categories (list[str], optional): Categories associated with the link. Defaults to None.
        tags (list[str], optional): Tags associated with the link. Defaults to None.
    """

    def __init__(self, url, description=None, categories=None, tags=None):
        self.url: str = url
        self.description: str = description or ""
        self.categories: list[str] = categories or []
        self.tags: list[str] = tags or []

    def add_category(self, category):
        self.categories.append(category)

    def add_tags(self, *tags):
        self.tags.extend(tags)

    def update_link_url(self, new_url):
        self.url = new_url

    def update_description(self, description):
        self.description = description

    def remove_category(self, category):
        if category in self.categories:
            self.categories.remove(category)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def to_json(self):
        link_data = {
            "url": self.url,
            "description": self.description,
            "categories": self.categories,
            "tags": self.tags,
        }
        return json.dumps(link_data)

    def __repr__(self):
        return f"Link(url='{self.url}'\ncategories:{self.categories}\n tags:{self.tags})\nDescription:\n{self.description}"


# TODO: Add functionality to bulk delete and update tags and categories
# FIXME: Test addition, deletion and update methods


class LinkManager:
    """
    Represents a collection of links with associated categories and tags.

    ### Args:
        db_path: str --> The path to the database file.

    ### Methods:
        load_from_db()
        save_to_db()
        add_link()
        add_link_category(index: int, category: str)
        add_link_tag(index: int, tag: str)
        update_link_url(index: int, new_url: str)
        update_link_description(index: int, new_description: str)
        remove_link_category(index: int, category: str)
        remove_link_tag(index: int, tag: str)
        list_all()
        list_links()
        list_categories()
        list_tags()
        query() -> list
    """

    def __init__(self, db_path: str):
        self.links: list[Link] = []
        self.categories: list[str] = []
        self.tags: list[str] = []
        self.db = db_path

    def bulk_import(self):
        """
            Import data from a csv or a text file in csv.
        """
        try:
            file_path = os.path(input("File to import (with file path)"))
            with open(file_path, "r+") as f:
                data = f.readlines()

        except Exception as e:
            print(e)

    def load_from_db(self):
        try:
            with open(self.db, "r") as f:
                data = json.load(f)

                self.categories = data.get("categories", [])
                self.tags = data.get("tags", [])

                for link_data in data.get("links", []):
                    link = Link(
                        url=link_data["url"],
                        description=link_data["description"],
                        categories=link_data["categories"],
                        tags=link_data["tags"],
                    )
                    self.links.append(link)
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(e)

    #TODO: Add multiple links from a csv or similar format    
    def save_to_db(self):
        data = {
            "links": [
                {
                    "url": link.url,
                    "description": link.description,
                    "categories": link.categories,
                    "tags": link.tags,
                }
                for link in self.links
            ],
            "categories": self.categories,
            "tags": self.tags,
        }
        with open(self.db, "w") as f:
            json.dump(data, f)

    def add_link(self):
        url = input("URL: ")
        description = input("Description: ")

        print(
            r"For an overview of all categories or tags, enter '#' in the respective field"
        )

        category = input("Category ('#' for all existing categories): ").strip()
        match category:
            case "#":
                for cat in self.categories:
                    print(cat)
            case _:
                category = [cat.strip() for cat in category.split(",")]

        tags = input("Tags (comma-separated, '#' for all existing tags): ")
        match category:
            case "#":
                for tag in self.tags:
                    print(tag)
            case _:
                tags = [tag.strip() for tag in tags.split(",")]

        link = Link(url, description, category, tags)
        self.links.append(link)

        if type(category) == list and category:
            self.categories = list(set(self.categories) | set(category))
        if type(tags) == list and tags:
            self.tags = list(set(self.tags) | set(tags))
        print("Link added successfully!")

    def add_link_category(self, index, category):
        if index >= len(self.links):
            raise IndexError("Index is out of range.")
        self.links[index].add_category(category)
        if category not in self.categories:
            self.categories.append(category)

    def add_link_tag(self, index, tag):
        if index >= len(self.links):
            raise IndexError("Index is out of range.")
        self.links[index].add_tags(tag)
        if tag not in self.tags:
            self.tags.append(tag)

    def update_link_url(self, index, new_url):
        if index < len(self.links):
            self.links[index].update_url(new_url)
            print("Link updated")
        else:
            raise IndexError("Index is out of range.")

    def update_link_description(self, index, new_description):
        if index < len(self.links):
            self.links[index].update_description(new_description)
            print("Description updated")
        else:
            raise IndexError("Index is out of range.")

    def remove_link_category(self, index, category):
        def search_cat_existence(target):
            try:
                flag = next(
                    (
                        cat
                        for link in self.links
                        for cat in link.categories
                        if target in cat or target == cat
                    ),
                    None,
                )
                if flag:
                    self.categories.remove(flag)
            except Exception as e:
                print(e)

        if index < len(self.links):
            self.links[index].remove_category(category)
            Thread(target=search_cat_existence, args=(category), daemon=True).start()
        else:
            raise IndexError("Index is out of range.")

    def remove_link_tag(self, index, tag):
        def search_tag_existence(target):
            try:
                flag = next(
                    (
                        tag
                        for link in self.links
                        for tag in link.categories
                        if target in tag or target == tag
                    ),
                    None,
                )
                if flag:
                    self.categories.remove(flag)
            except Exception as e:
                print(e)

        if index < len(self.links):
            self.links[index].remove_tag(tag)
            Thread(target=search_tag_existence, args=(tag), daemon=True).start()
        else:
            raise IndexError("Index is out of range.")

    def list_all(self):
        print("\n")
        for index, link in enumerate(self.links):
            print(
                colored(f"[{index}] URL: {link.url}\n", "light_magenta"),
                f"Categories: {str(link.categories)}\nTags: {str(link.tags)}\nDescription: {link.description}\n",
            )

    def list_links(self):
        print("Existing Links:")
        for index, link in enumerate(self.links):
            print(colored(f"[{index}] {link.url}", "light_magenta"))

    def list_categories(self):
        print(colored("Existing Categories:", "light_blue"))
        for cat in self.categories:
            print(colored(f"{str(cat).strip()}", "light_magenta"))

    def list_tags(self):
        print(colored("Existing Tags:", "light_blue"))
        for tag in self.tags:
            print(colored(f"{str(tag).strip()}", "light_magenta"))

    #TODO: Currently the query uses AND logic. If two search params are passed, they are queried according to search ranking which is the order as it appears in the terminal. Implement a OR search and an improved AND seach.  
    def query(self) -> list:
        active_data: list = self.links.copy()

        search_params: list[tuple[str, str]] = [
            ("url", input(colored("Search in url:", "light_blue"))),
            ("description", input(colored("Search in description:", "light_blue"))),
            ("categories", input(colored("Search in categories:", "light_blue"))),
            ("tags", input(colored("Search in tags:", "light_blue"))),
        ]

        for attribute, key in search_params:
            if (key and key.strip()):
                temp = []
                for link in active_data:
                    if type((target := getattr(link, attribute))) == str and key in target:
                        temp.append(link)
                    if type(target) == list:
                        temp.extend(link for item in target if key in item or key == target)
                active_data = temp


        print(colored("Search Results:", "red"))
        for link in active_data:
            print(
                colored(f"URL: {link.url} \n ", "light_magenta"),
                f"Categories: {str(link.categories)} \n Tags: {str(link.tags)}",
            )

        return active_data

    # TODO: After implementing Link Description, make text search available
    # def query(self) -> list:
    #     active_data: list = self.links.copy()

    #     def search(active_data, attribute, key, condition):
    #         if key not in [None, ""]:
    #             matching = [
    #                 link
    #                 for link in active_data
    #                 if any(condition(key, s) for s in getattr(link, attribute))
    #             ]
    #             if matching:
    #                 return matching
    #         return active_data

    #     def render_results(data):
    #         print(colored("Search Results:", "red"))
    #         for link in data:
    #             print(
    #                 colored(f"URL: {link.url} \n ", "light_magenta"),
    #                 f"Categories: {str(link.categories)} \n Tags: {str(link.tags)}",
    #             )

    #     text = input(colored("Text to look for in the link:", "light_blue"))
    #     active_data = search(active_data, "url", text, lambda key, s: key in s)

    #     cat = input(colored("Category to look for:", "light_blue"))
    #     active_data = search(active_data, "categories", cat, lambda key, s: key in s)

    #     tag = input(colored("Tag to look for in the link:", "light_blue"))
    #     active_data = search(active_data, "tags", tag, lambda key, s: key in s)

    #     render_results(active_data)
    #     return active_data
