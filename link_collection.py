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
        print(colored(basemsg, 'light_magenta'))
    
    def extensive_msg(self):
        extensivemsg = self.helpdata["extensive"]
        print(colored(extensivemsg, 'light_magenta'))


def main(db_path):
    """Setup"""
    link_collection = LinkCollection(db_path)
    link_collection.load_from_db()
    
    help = help_manager()

    try:
        help.base_msg()
        print("\nEnter Command")
        while True:
            choice = input("[>>]: ")
            
            #TODO: Add link management, such that you can edit link properties and delete the link
            #TODO: Implement functionality for the new Class Methods on LinkManager
            match choice:
                case '0' | 'h' | 'help':
                    help.base_msg()
                    #FIXME: Go over help message usage and commands after updates
                case '1' | 'exh' | 'exhelp':
                    help.extensive_msg()
                case '2':
                    link_collection.add_link()
                case '3' | 'll':
                    link_collection.list_links()
                case '4' | 'lc':
                    link_collection.list_categories()
                case '5' | 'lt':
                    link_collection.list_tags()
                case '6' | 'db' | 'all':
                    link_collection.list_all()
                case '7' | 'query' | 'q' | '?' | 'find':
                    link_collection.query()
                case '8' | 'import' | '9' | 'export':
                    link_collection.save_to_db()
                case '10' | 'exit' | 'close' | 'quit':
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
    db_path = db_setup()
    main(db_path)