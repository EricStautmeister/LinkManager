import json
from link import Link, LinkCollection
from termcolor import colored

# Main program loop
def main():
    """Setup"""
    link_collection = LinkCollection()
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
                case 0:
                    print(helpmsg)
                case '1':
                    link_collection.import_from_file()
                case '2':
                    link_collection.export_to_file()
                case '3':
                    link_collection.add_link()
                case '4':
                    link_collection.list_links()
                case '5':
                    link_collection.list_categories()
                case '6':
                    link_collection.list_tags()
                case '7':
                    link_collection.list_all()
                case "8":
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
    main()