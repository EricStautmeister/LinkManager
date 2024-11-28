import json
from termcolor import colored


class Link:
    def __init__(self, url, categories=None, tags=None):
        self.url = url
        self.categories = categories or []
        self.tags = tags or []

    def add_category(self, category):
        self.categories.append(category)

    def remove_category(self, category):
        if category in self.categories:
            self.categories.remove(category)

    def add_tags(self, *tags):
        self.tags.extend(tags)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def to_json(self):
        link_data = {"url": self.url, "categories": self.categories, "tags": self.tags}
        return json.dumps(link_data)

    def __repr__(self):
        return (
            f"Link(url='{self.url}'\ncategories:{self.categories}\n tags:{self.tags})"
        )


class LinkCollection:
    def __init__(self, db_path):
        self.links = []
        self.categories = []
        self.tags = []
        self.db = db_path

    def import_from_file(self):
        try:
            with open(self.db, "r") as f:
                data = json.load(f)

                self.categories = data.get("categories", [])
                self.tags = data.get("tags", [])

                for link_data in data.get("links", []):
                    link = Link(
                        link_data["url"], link_data["categories"], link_data["tags"]
                    )
                    self.links.append(link)
        except FileNotFoundError:
            print("File not found.")

    def export_to_file(self):
        data = {
            "links": [
                {"url": link.url, "categories": link.categories, "tags": link.tags}
                for link in self.links
            ],
            "categories": self.categories,
            "tags": self.tags, 
        }
        with open(self.db, "w") as f:
            json.dump(data, f)

    def add_link(self):
        url = input("Enter the URL: ")
        category = [cat.strip() for cat in input("Enter the category: ").split(",")]
        tags = [
            tag.strip()
            for tag in input("Enter the tags (comma-separated): ").split(",")
        ]
        link = Link(url, category, tags)
        self.links.append(link)
        if type(category) == list and len(category) > 0:
            self.categories = list(set(self.categories) | set(category))
        if type(tags) == list and len(tags) > 0:
            self.tags = list(set(self.tags) | set(tags))
        print("Link added successfully!")

    def list_all(self):
        for link in self.links:
            print(
                colored(f"URL: {link.url} \n ", "light_magenta"),
                f"Categories: {str(link.categories)} \n Tags: {str(link.tags)}",
            )

    def list_links(self):
        print("Existing Links:")
        for link in self.links:
            print(f"{link.url}")

    def list_categories(self):
        print(colored("Existing Categories:", "light_blue"))
        for cat in self.categories:
            print(colored(f"{str(cat).strip()}", "light_cyan"))

    def list_tags(self):
        print(colored("Existing Tags:", "light_blue"))
        for tag in self.tags:
            print(colored(f"{str(tag).strip()}", "light_cyan"))

    def query(self, text=None, cat=None, tag=None) -> list:
        #TODO: Add multithreading
        #TODO: Make the querying happen while the user enters the searches
        active_data: list = []

        for link in self.links:
            if cat in [None, ""]:
                break
            for s in link.categories:
                if cat in s: active_data.append(link)

        active_data = active_data if len(active_data) > 0 else self.links
        matching_tags = []
        for link in active_data:
            if tag in [None, ""]:
                break
            for s in link.tags:
                if tag in s:
                    matching_tags.append(link)
            active_data = matching_tags

        active_data = active_data if len(active_data) > 0 else self.links
        matching_urls = []
        for link in active_data:
            if text in [None, ""]:
                break
            if text in link.url:
                matching_urls.append(link)
            active_data = matching_urls

        print(colored("Search Results:", "red"))
        for link in active_data:
            print(
                colored(f"URL: {link.url} \n ", "light_magenta"),
                f"Categories: {str(link.categories)} \n Tags: {str(link.tags)}",
            )
        return active_data
