import os  # Used (file operations, paths)
import json  # Used (database operations)
import csv  # Used (import/export functions)
from termcolor import colored  # Used (output formatting)
import shutil  # Used (backup operations)
from typing import List, Dict, Optional, Any  # Used (type hints)

class Link:
    """
    Represents a hyperlink with associated metadata.

    Args:
        url (str): The URL of the link.
        description (str, optional): Description of the link. Defaults to "".
        categories (list[str], optional): Categories associated with the link. Defaults to [].
        tags (list[str], optional): Tags associated with the link. Defaults to [].
    """

    def __init__(self, url: str, description: str = "", categories: List[str] = None, tags: List[str] = None):
        self.url: str = self._validate_url(url)
        self.description: str = description or ""
        self.categories: List[str] = categories or []
        self.tags: List[str] = tags or []
        self.created_at: str = self._get_timestamp()
        self.last_updated: str = self.created_at
    
    def _validate_url(self, url: str) -> str:
        """Validate and standardize URLs."""
        url = url.strip()
        # Basic URL validation
        if not (url.startswith('http://') or url.startswith('https://')):
            url = f'https://{url}'
        return url
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def add_category(self, category: str) -> None:
        """Add a category to the link if it's not already present."""
        category = category.strip()
        if category and category not in self.categories:
            self.categories.append(category)
            self._update_timestamp()

    def add_tags(self, *tags: str) -> None:
        """Add one or more tags to the link if they're not already present."""
        for tag in tags:
            tag = tag.strip()
            if tag and tag not in self.tags:
                self.tags.append(tag)
        self._update_timestamp()

    def update_url(self, new_url: str) -> None:
        """Update the URL of the link."""
        self.url = self._validate_url(new_url)
        self._update_timestamp()

    def update_description(self, description: str) -> None:
        """Update the description of the link."""
        self.description = description.strip()
        self._update_timestamp()

    def remove_category(self, category: str) -> bool:
        """Remove a category from the link if it exists."""
        if category in self.categories:
            self.categories.remove(category)
            self._update_timestamp()
            return True
        return False

    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the link if it exists."""
        if tag in self.tags:
            self.tags.remove(tag)
            self._update_timestamp()
            return True
        return False
    
    def _update_timestamp(self) -> None:
        """Update the last_updated timestamp."""
        self.last_updated = self._get_timestamp()

    def to_json(self) -> str:
        """Convert link to JSON string."""
        return json.dumps(self.to_dict())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert link to dictionary."""
        return {
            "url": self.url,
            "description": self.description,
            "categories": self.categories,
            "tags": self.tags,
            "created_at": self.created_at,
            "last_updated": self.last_updated
        }

    def __repr__(self) -> str:
        return f"Link(url='{self.url}'\ncategories:{self.categories}\ntags:{self.tags})\nDescription:\n{self.description}"


class LinkManager:
    """
    Enhanced LinkManager class for managing a collection of links with associated categories and tags.
    Includes bulk operations, improved search, backup functionality, and more secure file handling.
    """

    def __init__(self, db_path: str):
        self.links: List[Link] = []
        self.categories: List[str] = []
        self.tags: List[str] = []
        self.db = db_path
        self.backup_dir = os.path.join(os.path.dirname(db_path), "backups")
        # Ensure backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)

    def _create_backup(self) -> str:
        """Create a backup of the current database file."""
        if not os.path.exists(self.db):
            return "No database file to backup."
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"links_backup_{timestamp}.json")
        
        try:
            shutil.copy2(self.db, backup_file)
            return f"Backup created: {backup_file}"
        except Exception as e:
            return f"Backup failed: {str(e)}"
    
    def list_backups(self) -> List[str]:
        """List available backups."""
        if not os.path.exists(self.backup_dir):
            return []
        
        backups = [f for f in os.listdir(self.backup_dir) if f.startswith("links_backup_") and f.endswith(".json")]
        return sorted(backups, reverse=True)  # Most recent first
    
    def restore_backup(self, backup_file: str = None) -> str:
        """Restore from a backup file."""
        if not backup_file:
            backups = self.list_backups()
            if not backups:
                return "No backups available."
            backup_file = backups[0]  # Most recent
        
        backup_path = os.path.join(self.backup_dir, backup_file)
        if not os.path.exists(backup_path):
            return f"Backup file not found: {backup_file}"
        
        try:
            # First create a backup of current state
            self._create_backup()
            # Copy backup to current db
            shutil.copy2(backup_path, self.db)
            # Reload from db
            self.load_from_db()
            return f"Database restored from {backup_file}"
        except Exception as e:
            return f"Restore failed: {str(e)}"

    def load_from_db(self) -> None:
        """Load links from the database file."""
        self.links = []
        self.categories = []
        self.tags = []
        
        try:
            if not os.path.exists(self.db):
                print(f"Database file not found at {self.db}. Creating a new one.")
                self.save_to_db()
                return
                
            with open(self.db, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print("Error: Database file is corrupted. Creating backup and starting fresh.")
                    if os.path.getsize(self.db) > 0:
                        self._create_backup()
                    self.save_to_db()
                    return

                self.categories = data.get("categories", [])
                self.tags = data.get("tags", [])

                for link_data in data.get("links", []):
                    link = Link(
                        url=link_data["url"],
                        description=link_data.get("description", ""),
                        categories=link_data.get("categories", []),
                        tags=link_data.get("tags", [])
                    )
                    # Handle timestamps for older data
                    if "created_at" in link_data:
                        link.created_at = link_data["created_at"]
                    if "last_updated" in link_data:
                        link.last_updated = link_data["last_updated"]
                    self.links.append(link)
                
                print(f"Loaded {len(self.links)} links from database.")
        except Exception as e:
            print(f"Error loading database: {e}")
            
    def save_to_db(self) -> None:
        """Save links to the database file with error handling."""
        data = {
            "links": [link.to_dict() for link in self.links],
            "categories": self.categories,
            "tags": self.tags,
        }
        
        try:
            # Create a backup before saving
            if os.path.exists(self.db):
                self._create_backup()
                
            # Write to temporary file first
            temp_file = f"{self.db}.tmp"
            with open(temp_file, "w") as f:
                json.dump(data, f, indent=2)
            
            # Rename to actual file (atomic operation)
            os.replace(temp_file, self.db)
            print(f"Database saved to {self.db}")
        except Exception as e:
            print(f"Error saving database: {e}")
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass

    def add_link(self, interactive: bool = True) -> Optional[Link]:
        """Add a new link to the collection."""
        try:
            if interactive:
                url = input("URL: ")
                description = input("Description: ")

                print("For an overview of all categories or tags, enter '#' in the respective field")

                category_input = input("Category ('#' for all existing categories): ").strip()
                if category_input == "#":
                    self.list_categories()
                    category_input = input("Category (comma-separated): ").strip()
                
                categories = [cat.strip() for cat in category_input.split(",")] if category_input else []

                tags_input = input("Tags (comma-separated, '#' for all existing tags): ")
                if tags_input == "#":
                    self.list_tags()
                    tags_input = input("Tags (comma-separated): ").strip()
                
                tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []
            else:
                # Called programmatically - would be implemented by caller
                return None

            link = Link(url, description, categories, tags)
            self.links.append(link)

            # Update global categories and tags
            if categories:
                self.categories = list(set(self.categories) | set(categories))
            if tags:
                self.tags = list(set(self.tags) | set(tags))
            
            print("Link added successfully!")
            return link
            
        except KeyboardInterrupt:
            print("\nCancelled adding link.")
            return None
        except Exception as e:
            print(f"Error adding link: {e}")
            return None

    def bulk_import_from_csv(self, file_path: str) -> str:
        """Import links from a CSV file."""
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"
        
        added_count = 0
        error_count = 0
        
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                if not reader.fieldnames:
                    return "Error: CSV file appears to be empty or invalid"
                
                # Check required fields
                required_fields = ['url']
                for field in required_fields:
                    if field not in reader.fieldnames:
                        return f"Error: CSV file missing required field '{field}'"
                
                for row in reader:
                    try:
                        url = row['url'].strip()
                        if not url:
                            continue
                            
                        description = row.get('description', '').strip()
                        
                        categories = []
                        if 'categories' in row and row['categories']:
                            categories = [cat.strip() for cat in row['categories'].split(',')]
                            
                        tags = []
                        if 'tags' in row and row['tags']:
                            tags = [tag.strip() for tag in row['tags'].split(',')]
                        
                        link = Link(url, description, categories, tags)
                        self.links.append(link)
                        
                        # Update global categories and tags
                        if categories:
                            self.categories = list(set(self.categories) | set(categories))
                        if tags:
                            self.tags = list(set(self.tags) | set(tags))
                            
                        added_count += 1
                    except Exception as e:
                        error_count += 1
                        print(f"Error processing row: {e}")
        
            return f"Import completed: {added_count} links added, {error_count} errors"
        except Exception as e:
            return f"Import failed: {e}"
    
    def export_to_csv(self, file_path: str) -> str:
        """Export links to a CSV file."""
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['url', 'description', 'categories', 'tags', 'created_at', 'last_updated']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for link in self.links:
                    writer.writerow({
                        'url': link.url,
                        'description': link.description,
                        'categories': ','.join(link.categories),
                        'tags': ','.join(link.tags),
                        'created_at': link.created_at,
                        'last_updated': link.last_updated
                    })
                
            return f"Exported {len(self.links)} links to {file_path}"
        except Exception as e:
            return f"Export failed: {e}"

    def add_link_category(self, index: int, category: str) -> bool:
        """Add a category to a link."""
        if index >= len(self.links):
            print("Error: Index is out of range.")
            return False
            
        self.links[index].add_category(category)
        if category not in self.categories:
            self.categories.append(category)
        return True

    def add_link_tag(self, index: int, tag: str) -> bool:
        """Add a tag to a link."""
        if index >= len(self.links):
            print("Error: Index is out of range.")
            return False
            
        self.links[index].add_tags(tag)
        if tag not in self.tags:
            self.tags.append(tag)
        return True

    def update_link_url(self, index: int, new_url: str) -> bool:
        """Update the URL of a link."""
        if index >= len(self.links):
            print("Error: Index is out of range.")
            return False
            
        self.links[index].update_url(new_url)
        print("Link URL updated")
        return True

    def update_link_description(self, index: int, new_description: str) -> bool:
        """Update the description of a link."""
        if index >= len(self.links):
            print("Error: Index is out of range.")
            return False
            
        self.links[index].update_description(new_description)
        print("Description updated")
        return True

    def remove_link(self, index: int) -> bool:
        """Remove a link from the collection."""
        if index >= len(self.links) or index < 0:
            print("Error: Index is out of range.")
            return False
            
        removed = self.links.pop(index)
        print(f"Removed link: {removed.url}")
        
        # Update categories and tags lists if needed
        self._refresh_categories_and_tags()
        return True
    
    def _refresh_categories_and_tags(self) -> None:
        """Refresh the global categories and tags lists based on actual link data."""
        # Get all unique categories and tags from links
        all_categories = set()
        all_tags = set()
        
        for link in self.links:
            all_categories.update(link.categories)
            all_tags.update(link.tags)
        
        # Update the lists
        self.categories = sorted(list(all_categories))
        self.tags = sorted(list(all_tags))

    def remove_link_category(self, index: int, category: str) -> bool:
        """Remove a category from a link."""
        if index >= len(self.links):
            print("Error: Index is out of range.")
            return False
            
        result = self.links[index].remove_category(category)
        if result:
            # Check if any other link uses this category
            category_in_use = any(category in link.categories for link in self.links)
            if not category_in_use and category in self.categories:
                self.categories.remove(category)
        return result

    def remove_link_tag(self, index: int, tag: str) -> bool:
        """Remove a tag from a link."""
        if index >= len(self.links):
            print("Error: Index is out of range.")
            return False
            
        result = self.links[index].remove_tag(tag)
        if result:
            # Check if any other link uses this tag
            tag_in_use = any(tag in link.tags for link in self.links)
            if not tag_in_use and tag in self.tags:
                self.tags.remove(tag)
        return result

    def bulk_add_tag(self, tag: str, indices: List[int] = None) -> int:
        """Add a tag to multiple links."""
        if not tag.strip():
            return 0
            
        count = 0
        tag = tag.strip()
        
        if indices is None:
            indices = range(len(self.links))
            
        for idx in indices:
            if 0 <= idx < len(self.links):
                self.links[idx].add_tags(tag)
                count += 1
                
        if count > 0 and tag not in self.tags:
            self.tags.append(tag)
            
        return count

    def bulk_add_category(self, category: str, indices: List[int] = None) -> int:
        """Add a category to multiple links."""
        if not category.strip():
            return 0
            
        count = 0
        category = category.strip()
        
        if indices is None:
            indices = range(len(self.links))
            
        for idx in indices:
            if 0 <= idx < len(self.links):
                self.links[idx].add_category(category)
                count += 1
                
        if count > 0 and category not in self.categories:
            self.categories.append(category)
            
        return count

    def bulk_remove_tag(self, tag: str) -> int:
        """Remove a tag from all links that have it."""
        count = 0
        for link in self.links:
            if tag in link.tags:
                link.remove_tag(tag)
                count += 1
                
        if tag in self.tags:
            self.tags.remove(tag)
            
        return count

    def bulk_remove_category(self, category: str) -> int:
        """Remove a category from all links that have it."""
        count = 0
        for link in self.links:
            if category in link.categories:
                link.remove_category(category)
                count += 1
                
        if category in self.categories:
            self.categories.remove(category)
            
        return count

    def list_all(self) -> None:
        """List all links with their details."""
        if not self.links:
            print(colored("No links found.", "yellow"))
            return
            
        print("\n" + colored("All Links:", "light_blue"))
        for index, link in enumerate(self.links):
            print(
                colored(f"[{index}] URL: {link.url}", "light_magenta"),
                f"\nCategories: {', '.join(link.categories)}\nTags: {', '.join(link.tags)}"
            )
            if link.description:
                print(f"Description: {link.description}")
            print(f"Created: {link.created_at.split('T')[0]} | Last Updated: {link.last_updated.split('T')[0]}\n")

    def list_links(self) -> None:
        """List all links (URLs only)."""
        if not self.links:
            print(colored("No links found.", "yellow"))
            return
            
        print(colored("Existing Links:", "light_blue"))
        for index, link in enumerate(self.links):
            print(colored(f"[{index}] {link.url}", "light_magenta"))

    def list_categories(self) -> None:
        """List all categories."""
        if not self.categories:
            print(colored("No categories found.", "yellow"))
            return
            
        print(colored("Existing Categories:", "light_blue"))
        for index, cat in enumerate(sorted(self.categories)):
            print(colored(f"[{index}] {cat}", "light_magenta"))
            # Count links using this category
            count = sum(1 for link in self.links if cat in link.categories)
            print(f"  Used in {count} link{'s' if count != 1 else ''}")

    def list_tags(self) -> None:
        """List all tags."""
        if not self.tags:
            print(colored("No tags found.", "yellow"))
            return

        print(colored("Existing Tags:", "light_blue"))
        for index, tag in enumerate(sorted(self.tags)):
            print(colored(f"[{index}] {tag}", "light_magenta"))
            # Count links using this tag
            count = sum(tag in link.tags for link in self.links)
            print(f"  Used in {count} link{'s' if count != 1 else ''}")

    def query(self, interactive: bool = True, search_params: Dict[str, str] = None) -> List[Link]:
        # sourcery skip: low-code-quality
        """
        Query links based on search parameters.
        Supports both AND and OR search logic.
        """
        if interactive:
            search_mode = input(colored("Search mode - AND (all terms must match) or OR (any term matches) [AND/OR]: ", "light_blue")).strip().upper()
            search_mode = "AND" if search_mode != "OR" else "OR"
            
            search_params = {
                "url": input(colored("Search in URL: ", "light_blue")).strip(),
                "description": input(colored("Search in description: ", "light_blue")).strip(),
                "categories": input(colored("Search in categories: ", "light_blue")).strip(),
                "tags": input(colored("Search in tags: ", "light_blue")).strip(),
            }
        else:
            search_mode = "AND"  # Default to AND logic when called programmatically
            search_params = search_params or {}
        
        # Filter out empty search parameters
        search_params = {k: v for k, v in search_params.items() if v}
        
        if not search_params:
            if interactive:
                print(colored("No search criteria provided.", "yellow"))
            return []
            
        results = []
        
        if search_mode == "AND":
            # Start with all links and filter down
            results = self.links.copy()
            
            for attribute, key in search_params.items():
                temp_results = []
                for link in results:
                    if attribute == "url" and key.lower() in link.url.lower():
                        temp_results.append(link)
                    elif attribute == "description" and key.lower() in link.description.lower():
                        temp_results.append(link)
                    elif attribute == "categories" and any(key.lower() in cat.lower() for cat in link.categories):
                        temp_results.append(link)
                    elif attribute == "tags" and any(key.lower() in tag.lower() for tag in link.tags):
                        temp_results.append(link)
                results = temp_results
        else:  # OR logic
            seen_links = set()
            for attribute, key in search_params.items():
                for link in self.links:
                    # Skip links we've already found
                    if id(link) in seen_links:
                        continue
                        
                    found = False
                    if attribute == "url" and key.lower() in link.url.lower():
                        found = True
                    elif attribute == "description" and key.lower() in link.description.lower():
                        found = True
                    elif attribute == "categories" and any(key.lower() in cat.lower() for cat in link.categories):
                        found = True
                    elif attribute == "tags" and any(key.lower() in tag.lower() for tag in link.tags):
                        found = True
                        
                    if found:
                        results.append(link)
                        seen_links.add(id(link))
        
        if interactive:
            if results:
                print(colored(f"Search Results ({len(results)} links found):", "light_blue"))
                for index, link in enumerate(results):
                    print(
                        colored(f"[{index}] URL: {link.url}", "light_magenta"),
                        f"\nCategories: {', '.join(link.categories)}\nTags: {', '.join(link.tags)}"
                    )
                    if link.description:
                        print(f"Description: {link.description}\n")
            else:
                print(colored("No matching links found.", "yellow"))
                
        return results

    def advanced_search(self) -> List[Link]:
        """Advanced search with multiple criteria and boolean operators."""
        print(colored("Advanced Search", "light_blue"))
        print("Enter search criteria. Multiple terms separated by commas will be treated as OR.")
        print("Leave blank to skip a field.\n")
        
        url_terms = input(colored("URL contains: ", "light_blue")).strip()
        desc_terms = input(colored("Description contains: ", "light_blue")).strip()
        cat_terms = input(colored("Categories (comma-separated OR): ", "light_blue")).strip()
        tag_terms = input(colored("Tags (comma-separated OR): ", "light_blue")).strip()
        
        # Split terms by comma
        url_list = [t.strip() for t in url_terms.split(",")] if url_terms else []
        desc_list = [t.strip() for t in desc_terms.split(",")] if desc_terms else []
        cat_list = [t.strip() for t in cat_terms.split(",")] if cat_terms else []
        tag_list = [t.strip() for t in tag_terms.split(",")] if tag_terms else []
        
        results = []
        for link in self.links:
            # URL check
            url_match = not url_list or any(term.lower() in link.url.lower() for term in url_list)
            
            # Description check
            desc_match = not desc_list or any(term.lower() in link.description.lower() for term in desc_list)
            
            # Category check
            cat_match = not cat_list or any(
                any(term.lower() in cat.lower() for cat in link.categories)
                for term in cat_list
            )
            
            # Tag check
            tag_match = not tag_list or any(
                any(term.lower() in tag.lower() for tag in link.tags)
                for term in tag_list
            )
            
            # All criteria must match (AND logic between fields)
            if url_match and desc_match and cat_match and tag_match:
                results.append(link)
        
        if results:
            print(colored(f"Search Results ({len(results)} links found):", "light_blue"))
            for index, link in enumerate(results):
                print(
                    colored(f"[{index}] URL: {link.url}", "light_magenta"),
                    f"\nCategories: {', '.join(link.categories)}\nTags: {', '.join(link.tags)}"
                )
                if link.description:
                    print(f"Description: {link.description}\n")
        else:
            print(colored("No matching links found.", "yellow"))
            
        return results
        
    def edit_link(self, index: int) -> bool:
        """Edit a link's properties interactively."""
        if index >= len(self.links) or index < 0:
            print("Error: Index is out of range.")
            return False

        link = self.links[index]
        print(colored(f"Editing link: {link.url}", "light_blue"))
        print("Press Enter to keep current values, or enter new values.")

        if new_url := input(f"URL [{link.url}]: ").strip():
            link.update_url(new_url)

        if new_desc := input(f"Description [{link.description}]: ").strip():
            link.update_description(new_desc)

        # Categories
        print(f"Current categories: {', '.join(link.categories)}")
        new_cats = input("Categories (comma-separated, leave empty to keep current, '!' to clear all): ").strip()
        if new_cats == '!':
            link.categories = []
        elif new_cats:
            link.categories = [cat.strip() for cat in new_cats.split(",")]
            # Update global categories
            for cat in link.categories:
                if cat and cat not in self.categories:
                    self.categories.append(cat)

        # Tags
        print(f"Current tags: {', '.join(link.tags)}")
        new_tags = input("Tags (comma-separated, leave empty to keep current, '!' to clear all): ").strip()
        if new_tags == '!':
            link.tags = []
        elif new_tags:
            link.tags = [tag.strip() for tag in new_tags.split(",")]
            # Update global tags
            for tag in link.tags:
                if tag and tag not in self.tags:
                    self.tags.append(tag)

        # Refresh categories and tags
        self._refresh_categories_and_tags()
        print("Link updated successfully.")
        return True


def bulk_operations_menu(link_collection):
    """Menu for bulk operations on links."""
    print(colored("\nBulk Operations Menu:", "light_blue"))
    print("1. Add tag to multiple links")
    print("2. Add category to multiple links")
    print("3. Remove tag from all links")
    print("4. Remove category from all links")
    print("0. Return to main menu")

    choice = input(colored("[BULK]> ", "light_green")).strip()

    if choice == "1":
        # Add tag to multiple links
        link_collection.list_links()
        indices_input = input("Enter link indices (comma-separated, or 'all' for all links): ").strip()

        if indices_input.lower() == 'all':
            indices = None  # Will be interpreted as all links
        else:
            try:
                indices = [int(idx.strip()) for idx in indices_input.split(",") if idx.strip()]
            except ValueError:
                print("Invalid indices. Please enter numbers separated by commas.")
                return

        if tag := input("Tag to add: ").strip():
            count = link_collection.bulk_add_tag(tag, indices)
            print(f"Added tag '{tag}' to {count} links.")

    elif choice == "2":
        # Add category to multiple links
        link_collection.list_links()
        indices_input = input("Enter link indices (comma-separated, or 'all' for all links): ").strip()

        if indices_input.lower() == 'all':
            indices = None  # Will be interpreted as all links
        else:
            try:
                indices = [int(idx.strip()) for idx in indices_input.split(",") if idx.strip()]
            except ValueError:
                print("Invalid indices. Please enter numbers separated by commas.")
                return

        if category := input("Category to add: ").strip():
            count = link_collection.bulk_add_category(category, indices)
            print(f"Added category '{category}' to {count} links.")

    elif choice == "3":
        # Remove tag from all links
        link_collection.list_tags()
        if tag := input("Tag to remove from all links: ").strip():
            count = link_collection.bulk_remove_tag(tag)
            print(f"Removed tag '{tag}' from {count} links.")

    elif choice == "4":
        # Remove category from all links
        link_collection.list_categories()
        if category := input("Category to remove from all links: ").strip():
            count = link_collection.bulk_remove_category(category)
            print(f"Removed category '{category}' from {count} links.")

    elif choice == "0":
        return
    else:
        print("Invalid choice.")


def import_export_menu(link_collection):
    """Menu for import/export operations."""
    print(colored("\nImport/Export Menu:", "light_blue"))
    print("1. Import links from CSV")
    print("2. Export links to CSV")
    print("0. Return to main menu")

    choice = input(colored("[IMPORT/EXPORT]> ", "light_green")).strip()

    if choice == "1":
        if file_path := input("Enter CSV file path: ").strip():
            result = link_collection.bulk_import_from_csv(file_path)
            print(result)

    elif choice == "2":
        # Export to CSV
        default_path = os.path.join(os.path.dirname(link_collection.db), "links_export.csv")
        file_path = input(f"Enter CSV file path [{default_path}]: ").strip()
        if not file_path:
            file_path = default_path

        result = link_collection.export_to_csv(file_path)
        print(result)

    elif choice == "0":
        return
    else:
        print("Invalid choice.")


def backup_restore_menu(link_collection):
    """Menu for backup/restore operations."""
    print(colored("\nBackup/Restore Menu:", "light_blue"))
    print("1. Create backup")
    print("2. List available backups")
    print("3. Restore from backup")
    print("0. Return to main menu")

    choice = input(colored("[BACKUP/RESTORE]> ", "light_green")).strip()

    if choice == "1":
        # Create backup
        result = link_collection._create_backup()
        print(result)

    elif choice == "2":
        if backups := link_collection.list_backups():
            print(colored("Available backups:", "light_blue"))
            for i, backup in enumerate(backups):
                print(f"[{i}] {backup}")
        else:
            print("No backups available.")

    elif choice == "3":
        # Restore from backup
        backups = link_collection.list_backups()
        if not backups:
            print("No backups available.")
            return

        print(colored("Available backups:", "light_blue"))
        for i, backup in enumerate(backups):
            print(f"[{i}] {backup}")

        if backup_idx := input(
            "Enter backup index to restore, or press Enter for most recent: "
        ).strip():
            try:
                idx = int(backup_idx)
                if 0 <= idx < len(backups):
                    result = link_collection.restore_backup(backups[idx])
                    print(result)
                else:
                    print("Invalid backup index.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            # Restore most recent
            result = link_collection.restore_backup()
            print(result)

    elif choice == "0":
        return
    else:
        print("Invalid choice.")