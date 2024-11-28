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
        link_data = {
            'url': self.url,
            'categories': self.categories,
            'tags': self.tags
        }
        return json.dumps(link_data)

    def __repr__(self):
        return f"Link(url='{self.url}'\ncategories:{self.categories}\n tags:{self.tags})"


class LinkCollection:
    def __init__(self):
        self.links = []
        self.categories = []
        self.tags = []
        self.db = 'links.json'

    def import_from_file(self):
        try:
            with open(self.db, 'r') as f:
                data = json.load(f)

        
                self.categories = data.get('categories', [])
                self.tags = data.get('tags', [])

                for link_data in data.get('links', []):
                    link = Link(link_data['url'], link_data['categories'], link_data['tags'])
                    self.links.append(link)
        except FileNotFoundError:
            print("File not found.")


    def export_to_file(self):
        data = {
                "links": [{'url': link.url, 'categories': link.categories, 'tags': link.tags} for link in self.links],
                "categories": self.categories,
                "tags": self.tags  # Assuming you want to add links into "tags". If not, update this.
                }
        with open(self.db, 'w') as f:
            json.dump(data, f)
    
    def add_link(self):
        url = input("Enter the URL: ")
        category = [cat.strip() for cat in input("Enter the category: ").split(',')]
        tags = [tag.strip() for tag in input("Enter the tags (comma-separated): ").split(',')]
        link = Link(url, category, tags)
        self.links.append(link)
        if type(category) == list and len(category) > 0:
            self.categories = list(set(self.categories) | set(category))
        if type(tags) == list and len(tags) > 0:
            self.tags = list(set(self.tags) | set(tags))
        print("Link added successfully!")

    def list_all(self):
        for link in self.links:
            print(colored(f'URL: {link.url} \n ', 'light_magenta'), f'Categories: {str(link.categories)} \n Tags: {str(link.tags)}')

    def list_links(self):
        print("Existing Links:")
        for link in self.links:
            print(f'{link.url}')

    def list_categories(self):
        print("Existing Categories:")
        for link in self.links:
            print(f'{str(link.categories)}')

    def list_tags(self):
        print("Existing Tags:")
        for link in self.links:
            print(f'{str(link.tags)}')

    def query(self, text=None, cat=None, tag=None) -> list:
        active_data:list = []
        
        for link in self.links:
            if cat in [None, ""]: break
            active_data = [s for s in link.categories if cat in s]
        for link in self.links:
            if tag in [None, ""]: break
            active_data = active_data if len(active_data) > 0 else link.tags
            matching_tags = [s for s in link.tags if cat in s]
            active_data = matching_tags
        for link in self.links:
            if text in [None, ""]: break
            active_data = active_data if len(active_data) > 0 else link.tags
            matching_links = [s for s in active_data if cat in s]
            active_data = matching_links

        return active_data