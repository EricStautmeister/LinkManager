import json
from termcolor import colored
from threading import Thread


class Link:
    def __init__(self, url, description=None, categories=None, tags=None):
        self.url: str = url
        self.description: str = description or ""
        self.categories: list[str] = categories or []
        self.tags: list[str] = tags or []

    def update_description(self, description):
        self.description = description

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
        link_data = {
            "url": self.url,
            "description": self.description,
            "categories": self.categories,
            "tags": self.tags,
        }
        return json.dumps(link_data)

    def __repr__(self):
        return f"Link(url='{self.url}'\ncategories:{self.categories}\n tags:{self.tags})\nDescription:\n{self.description}"

#TODO: Add functionality to bulk delete and update tags and categories
#FIXME: Fix addition, deletion and update methods
class LinkCollection:
    def __init__(self, db_path: str):
        self.links: list[Link] = []
        self.categories: list[str] = []
        self.tags: list[str] = []
        self.db = db_path

    def save_wrapper(self, func):
        def threaded_daemon_save_wrapper(*args, **kwargs):
            result = func(*args, **kwargs) 
            Thread(target=self.save_to_db, args=(), daemon=True).start()
            return result
        return threaded_daemon_save_wrapper

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

    @save_wrapper
    def add_link(self):
        url = input("URL: ")
        description = input("Description:")

        print(
            r"For an overview of all categories or tags, enter '#' in the respective field"
        )

        category = input("Category: ")
        match category.strip():
            case "#":
                for cat in self.categories:
                    print(cat)
            case _:
                category = [cat.strip() for cat in category.split(",")]

        tags = input("Tags (comma-separated): ")
        match category.strip():
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
    @save_wrapper
    def update_link_url(self, index, new_url):
        if index < len(self.links):
            self.links[index].update_url(new_url)
            print("Link updated")
        else:
            raise IndexError("Index is out of range.")
    @save_wrapper
    def update_link_description(self, index, new_description):
        if index < len(self.links):
            self.links[index].update_description(new_description)
            print("Description updated")
        else:
            raise IndexError("Index is out of range.")

    def remove_link_category(self, index, category):
        def search_cat_existence(cat):
            try:
                flag = True
                cat_to_remove = False
                for link in self.links:
                    for c in link.categories:
                        if cat in c or cat == c:
                            flag = False
                            cat_to_remove = c
                            break
                    if not flag: break
                if flag:
                    self.categories.remove(cat_to_remove)
            except Exception as e:
                print(e)

        if index < len(self.links):
            self.links[index].remove_category(category)
            Thread(target=search_cat_existence, args=(category), daemon=True).start()
        else:
            raise IndexError("Index is out of range.")

    @save_wrapper
    def add_link_category(self, index, category):
        if index < len(self.links):
            self.links[index].add_category(category)
        else:
            raise IndexError("Index is out of range.")
        self.update_categories([category])

    def remove_link_tag(self, index, tag):
        if index < len(self.links):
            self.links[index].remove_tag(tag)
        else:
            raise IndexError("Index is out of range.")

    def add_link_tag(self, index, tag):
        if index < len(self.links):
            self.links[index].add_tags(tag)
        else:
            raise IndexError("Index is out of range.")
        self.update_tags([tag])

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
            print(colored(f"{str(cat).strip()}", "light_cyan"))

    def list_tags(self):
        print(colored("Existing Tags:", "light_blue"))
        for tag in self.tags:
            print(colored(f"{str(tag).strip()}", "light_cyan"))

    # TODO: After implementing Link Description, make text search available
    def query(self) -> list:
        active_data: list = self.links.copy()

        def search(active_data, attribute, key, condition):
            if key not in [None, ""]:
                matching = [
                    link
                    for link in active_data
                    if any(condition(key, s) for s in getattr(link, attribute))
                ]
                if matching:
                    return matching
            return active_data

        def render_results(data):
            print(colored("Search Results:", "red"))
            for link in data:
                print(
                    colored(f"URL: {link.url} \n ", "light_magenta"),
                    f"Categories: {str(link.categories)} \n Tags: {str(link.tags)}",
                )

        text = input(colored("Text to look for in the link:", "light_blue"))
        active_data = search(active_data, "url", text, lambda key, s: key in s)

        cat = input(colored("Category to look for:", "light_blue"))
        active_data = search(active_data, "categories", cat, lambda key, s: key in s)

        tag = input(colored("Tag to look for in the link:", "light_blue"))
        active_data = search(active_data, "tags", tag, lambda key, s: key in s)

        render_results(active_data)
        return active_data
