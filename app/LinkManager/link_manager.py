import json
from . import Link, LinkManager, helpmsg
from termcolor import colored
import time
import os

# Update README.md

class help_manager:
    def __init__(self):
        self.helpdata = helpmsg()

    def base_msg(self):
        basemsg = self.helpdata["base"]
        print(colored(basemsg, "light_magenta"))

    def extensive_msg(self):
        extensivemsg = self.helpdata["extensive"]
        print(colored(extensivemsg, "light_magenta"))

#FIXME: Just a Note: This might be buggy. Changing the install scripts and Project setup overwrote my previous db. However it appears to still work as I could not reproduce this. 
def db_setup():
    link_dir = "LinkManager"
    db_name = "links.json"

    if not (home_directory := os.path.expanduser('~')):
        raise EnvironmentError("User Directory not found.")
    
    link_collection_dir = os.path.join(home_directory, link_dir)
    if not os.path.exists(link_collection_dir):
        os.mkdir(link_collection_dir)

    db_path = os.path.join(link_collection_dir, db_name)

    if not os.path.exists(db_path): 
        with open(db_path, 'w') as db: 
            print(f'Database created under: {db_path}')

    return db_path


def main():
    db_path = db_setup()
    """Setup"""
    link_collection = LinkManager(db_path)
    link_collection.load_from_db()

    help = help_manager()

    try:
        help.base_msg()
        print("\nEnter Command")
        while True:
            choice = input("[>>]: ")

            # TODO: Add link management, such that you can edit link properties and delete the link
            # TODO: Implement functionality for the new Class Methods on LinkManager
            match choice:
                case "0" | "h" | "help":
                    help.base_msg()
                    # FIXME: Go over help message usage and commands after updates
                case "1" | "exh" | "exhelp":
                    help.extensive_msg()
                case "2":
                    link_collection.add_link()
                case "3" | "ll":
                    link_collection.list_links()
                case "4" | "lc":
                    link_collection.list_categories()
                case "5" | "lt":
                    link_collection.list_tags()
                case "6" | "db" | "all":
                    link_collection.list_all()
                case "7" | "query" | "q" | "?" | "find":
                    link_collection.query()
                case "8" | "import" | "9" | "export":
                    link_collection.save_to_db()
                case "10" | "exit" | "close" | "quit":
                    link_collection.save_to_db()
                    exit()
                case _:
                    print("Invalid choice. Please try again.\n")

    except (KeyboardInterrupt, SystemExit):
        print("\nProgram interrupted. Saving data...")
    finally:
        try:
            link_collection.save_to_db()
            print("Link data saved successfully.")
        except Exception as e:
            print("Could not save link data. Reason:", e)


if __name__ == "__main__":
    main()
    

    

