import json
from link import Link, LinkCollection
from termcolor import colored
from setup import db_setup

# Main program loop
def main(db_path):
    """Setup"""
    link_collection = LinkCollection(db_path)
    link_collection.import_from_file()
    helpmsg = ""

    with open("helpmsg.txt", "r") as h:
        helpmsg = h.read()

    try:
        print(colored(helpmsg, 'light_cyan'))
        while True:
            
            choice = input("Enter your choice (0-7): ")

            #TODO: Implement Query method into cli interface
            match choice:
                case '0', 'h', 'help':
                    print(helpmsg)
                    #TODO: Add more help info by adding choise to quit help menu or get more info on the option
                case '1', 'import':
                    link_collection.import_from_file()
                case '2', 'export':
                    link_collection.export_to_file()
                case '3', 'add':
                    link_collection.add_link()
                case '4', 'll':
                    link_collection.list_links()
                case '5':
                    link_collection.list_categories()
                case '6':
                    link_collection.list_tags()
                case '7':
                    link_collection.list_all()
                case '8':
                    text = input(colored("Text to look for in the link:", 'light_blue'))
                    cat = input(colored("Category to look for:", 'light_blue'))
                    tag = input(colored("Tag to look for in the link:", 'light_blue'))
                    link_collection.query(text, cat, tag)
                case "9", 'exit', 'close':
                    link_collection.export_to_file()
                    break
                case _:
                    print("Invalid choice. Please try again.\n")
    
    except (KeyboardInterrupt, SystemExit):
        print("\nProgram interrupted. Saving data...")
    finally:
        try:
            # Always attempt to save the data to the default file
            link_collection.export_to_file()
            print("Link data saved successfully.")
        except Exception as e:
            print("Could not save link data. Reason:", e)

# Run the main program
if __name__ == "__main__":
    db_path = db_setup()
    main(db_path)