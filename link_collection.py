import json
from link import Link, LinkCollection
from termcolor import colored
from setup import db_setup

class help_manager():
    def __init__(self):
        self.helpdata = None

        with open("helpmsg.json", "r") as h:
            self.helpdata = json.load(h)
    
    def base_msg(self):
        basemsg = self.helpdata["base"]
        print(colored(basemsg, 'light_cyan'))
    
    def extensive_msg(self):
        extensivemsg = self.helpdata["extensive"]
        print(colored(extensivemsg, 'light_cyan'))

# Main program loop
def main(db_path):
    """Setup"""
    link_collection = LinkCollection(db_path)
    link_collection.import_from_file()
    
    help = help_manager()

    try:
        help.base_msg()
        while True:
            
            choice = input("Enter your choice (0-7): ")
            
            #TODO: Add link management, such that you can edit link properties and delete the link
            #TODO: Add multiple links from a csv or similar format
            if choice in {'0', 'h', 'help'}:
                help.base_msg()
            elif choice in {'1', 'exh', 'exhelp'}:
                help.extensive_msg()
            elif choice in {'2', 'add'}:
                link_collection.add_link()
            elif choice in {'3', 'll'}:
                link_collection.list_links()
            elif choice in {'4', 'lc'}:
                link_collection.list_categories()
            elif choice in {'5', 'lt'}:
                link_collection.list_tags()
            elif choice in {'6', 'db', 'all'}:
                link_collection.list_all()
            elif choice in {'7', 'query', 'q', '?', 'find'}:
                link_collection.query()
            elif choice in {'8', 'import'}:
                link_collection.import_from_file()
            elif choice in {'9', 'export'}:
                link_collection.export_to_file()
            elif choice in {'10', 'exit', 'close', 'quit'}:
                link_collection.export_to_file()
                break
            else:
                print("Invalid choice. Please try again.\n")
    
    except (KeyboardInterrupt, SystemExit):
        print("\nProgram interrupted. Saving data...")
    finally:
        try:
            link_collection.export_to_file()
            print("Link data saved successfully.")
        except Exception as e:
            print("Could not save link data. Reason:", e)

if __name__ == "__main__":
    db_path = db_setup()
    main(db_path)