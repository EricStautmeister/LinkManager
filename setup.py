import os
import sys
import shutil

def db_setup() -> str:
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
    
#TODO: File is not callable globally after installing using this script. Extension Association .py is set to python3.11. See if it can be fixed
def move_program_to_global_env():
    entry_file = "link_manager.py"
    ignore_list = ['.gitignore', '.git', 'whiteboard.txt', '__pycache__']

    def get_files(path):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)) and file not in ignore_list:
                yield file

    cwd = os.getcwd()
    for file in get_files(cwd):
        shutil.copyfile(os.path.join(cwd, file), os.path.join(app_dir, file))
    
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)



if __name__ == "__main__":
    home_directory = os.path.expanduser('~')
    link_dir = "LinkManager"
    app_dir = os.path.join(home_directory, link_dir)

    db_path = db_setup()
    move_program_to_global_env()
    print(sys.path)
    print("\n")
    print(os.listdir(app_dir))