import json  # Used in db_setup()
import os    # Used in db_setup()
import sys   # Used in command-line argument handling
import argparse  # Used for command-line argument parsing

from . import Link, LinkManager, bulk_operations_menu, import_export_menu, backup_restore_menu  # Used throughout the code
from termcolor import colored  # Used for text coloring in multiple places


# Update README.md

class HelpManager:
    """Enhanced help message manager with color formatting."""
    
    def __init__(self):
        self.helpdata = {
            "base": "0. Print this message\n"
                   "1. Print extensive help message\n"
                   "2. Add a link\n"
                   "3. List existing links\n"
                   "4. List existing categories\n"
                   "5. List existing tags\n"
                   "6. List Entire Database\n"
                   "7. Query Database\n"
                   "8. Advanced Search\n"
                   "9. Edit a link\n"
                   "10. Remove a link\n"
                   "11. Bulk operations\n"
                   "12. Import/Export\n"
                   "13. Backup/Restore\n"
                   "20. Exit",
            
            "extensive": (
                "[0, h, help]: Print help message\n"
                "[1, exh, exhelp]: Print extensive help message\n"
                "[2, add]: Add a link with URL, description, categories and tags\n"
                "[3, ll]: List existing links, returns only the URLs\n"
                "[4, lc]: List existing categories registered in the database\n"
                "[5, lt]: List existing tags registered in the database\n"
                "[6, db, all]: List Entire Database with all link details\n"
                "[7, query, q, ?, find]: Query the database by URL, category and/or tags\n"
                "[8, adv, advanced]: Advanced search with multiple criteria and boolean operators\n"
                "[9, edit]: Edit a link's properties\n"
                "[10, rm, remove]: Remove a link from the database\n"
                "[11, bulk]: Bulk operations menu (add/remove tags or categories)\n"
                "[12, import, export]: Import/Export links from/to CSV\n"
                "[13, backup, restore]: Backup or restore the database\n"
                "[20, exit, close, quit]: Save and exit the application"
            )
        }
    
    def base_msg(self):
        """Print the basic help message."""
        print(colored(self.helpdata["base"], "light_magenta"))

    def extensive_msg(self):
        """Print the extensive help message."""
        print(colored(self.helpdata["extensive"], "light_magenta"))

#FIXME: Just a Note: This might be buggy. Changing the install scripts and Project setup overwrote my previous db. However it appears to still work as I could not reproduce this. 
def db_setup():
    """Set up the database directory and file."""
    link_dir = "LinkManager"
    db_name = "links.json"

    # Get user's home directory
    home_directory = os.path.expanduser('~')
    if not home_directory:
        raise EnvironmentError("User Directory not found.")
    
    # Create LinkManager directory if it doesn't exist
    link_collection_dir = os.path.join(home_directory, link_dir)
    if not os.path.exists(link_collection_dir):
        os.makedirs(link_collection_dir, exist_ok=True)
        print(f"Created directory: {link_collection_dir}")

    # Set up database file path
    db_path = os.path.join(link_collection_dir, db_name)

    # Create empty database file if it doesn't exist
    if not os.path.exists(db_path): 
        with open(db_path, 'w') as db:
            json.dump({"links": [], "categories": [], "tags": []}, db)
            print(f'Database created under: {db_path}')

    return db_path


def main():    # sourcery skip: low-code-quality
    """Main function for the LinkManager CLI."""
    # Setup
    try:
        db_path = db_setup()
        link_collection = LinkManager(db_path)
        link_collection.load_from_db()
        help_mgr = HelpManager()

        print(colored("Welcome to LinkManager!", "light_blue"))
        print(colored("Version 2.0.0 - Enhanced Edition", "light_green"))
        help_mgr.base_msg()

        while True:
            try:
                print("\nEnter Command")
                choice = input(colored("[>>]: ", "light_green")).strip().lower()

                if choice in ["0", "h", "help"]:
                    help_mgr.base_msg()

                elif choice in ["1", "exh", "exhelp"]:
                    help_mgr.extensive_msg()

                elif choice in ["2", "add"]:
                    link_collection.add_link()

                elif choice in ["3", "ll"]:
                    link_collection.list_links()

                elif choice in ["4", "lc"]:
                    link_collection.list_categories()

                elif choice in ["5", "lt"]:
                    link_collection.list_tags()

                elif choice in ["6", "db", "all"]:
                    link_collection.list_all()

                elif choice in ["7", "query", "q", "?", "find"]:
                    link_collection.query()

                elif choice in ["8", "adv", "advanced"]:
                    link_collection.advanced_search()

                elif choice in ["9", "edit"]:
                    link_collection.list_links()
                    try:
                        index = int(input("Enter link index to edit: ").strip())
                        link_collection.edit_link(index)
                    except ValueError:
                        print("Invalid input. Please enter a number.")

                elif choice in ["10", "rm", "remove"]:
                    link_collection.list_links()
                    try:
                        index = int(input("Enter link index to remove: ").strip())
                        if (
                            input("Are you sure? (y/n): ").strip().lower()
                            == 'y'
                        ):
                            link_collection.remove_link(index)
                    except ValueError:
                        print("Invalid input. Please enter a number.")

                elif choice in ["11", "bulk"]:
                    bulk_operations_menu(link_collection)

                elif choice in ["12", "import", "export"]:
                    import_export_menu(link_collection)

                elif choice in ["13", "backup", "restore"]:
                    backup_restore_menu(link_collection)

                elif choice in ["20", "exit", "close", "quit"]:
                    print("Saving data and exiting...")
                    link_collection.save_to_db()
                    print("Goodbye!")
                    break

                else:
                    print("Invalid choice. Please try again.")

            except KeyboardInterrupt:
                print("\nOperation cancelled.")
            except Exception as e:
                print(f"Error: {e}")

    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        try:
            link_collection.save_to_db()
            print("Link data saved successfully.")
        except Exception as e:
            print(f"Could not save link data: {e}")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="LinkManager - CLI tool for managing and querying collections of links.")
    parser.add_argument('--add', help="Add a link with the given URL", metavar="URL")
    parser.add_argument('--query', help="Search for links containing the given text", metavar="QUERY")
    parser.add_argument('--export', help="Export links to CSV file", metavar="FILENAME")
    parser.add_argument('--import', dest='import_file', help="Import links from CSV file", metavar="FILENAME")
    parser.add_argument('--backup', action='store_true', help="Create a backup of the database")
    
    args = parser.parse_args()
    
    # Handle command line operations if any arguments are provided
    if len(sys.argv) > 1:
        try:
            db_path = db_setup()
            link_collection = LinkManager(db_path)
            link_collection.load_from_db()
            
            if args.add:
                print(f"Adding link: {args.add}")
                link = Link(args.add)
                link_collection.links.append(link)
                link_collection.save_to_db()
                print("Link added successfully.")
                
            elif args.query:
                print(f"Searching for: {args.query}")
                search_params = {"url": args.query, "description": args.query, "categories": args.query, "tags": args.query}
                results = link_collection.query(interactive=False, search_params=search_params)
                print(f"Found {len(results)} matching links:")
                for link in results:
                    print(f"URL: {link.url}")
                    
            elif args.export:
                result = link_collection.export_to_csv(args.export)
                print(result)
                
            elif args.import_file:
                result = link_collection.bulk_import_from_csv(args.import_file)
                print(result)
                link_collection.save_to_db()
                
            elif args.backup:
                result = link_collection._create_backup()
                print(result)
                
        except Exception as e:
            print(f"Error: {e}")
        sys.exit(0)
    
    # Otherwise start the interactive CLI
    main()