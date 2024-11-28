#TODO: Implement setup (%appdata% add db, add script to path)
import os

def db_setup():
    home_directory = os.path.expanduser('~')
    print(home_directory)
    link_dir = "LinkCollection"
    db_name = "links.json"

    if home_directory:
        link_collection_dir = os.path.join(home_directory, link_dir)
        if not os.path.exists(link_collection_dir):
            os.mkdir(link_collection_dir)
        
        db_path = os.path.join(link_collection_dir, db_name)

        if not os.path.exists(db_path): 
            with open(db_path, 'w') as db: 
                print(f'Database created under: {db_path}')

        return db_path

    else:
        raise EnvironmentError("User Directory not found.")


if __name__ == "__main__":
    db_path = db_setup()