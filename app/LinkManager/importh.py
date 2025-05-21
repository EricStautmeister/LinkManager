import os
import pprint
from bs4 import BeautifulSoup
from tkinter.filedialog import askopenfilename
from tqdm import tqdm

#TODO: Integrate the import handler into app
#TODO: Test / Expand functionality for different browsers (currently tested for chromium based html bookmark files)
class ImportHandler:
    def __init__(self):
        self.filename:str or None = None
        self.filecontent:str or None = None
        self.imported_data:list or None = None
        
        self.progress_bar_stack: list = [self.get_filename, 
                                        self.load_file, 
                                        self.parse_html_file]

    def f_import(self) -> list:
        for ps in tqdm(self.progress_bar_stack):
            ps()
        return self.imported_data

    def get_filename(self) -> str:
        initial_dir = os.path.expanduser("~/Downloads")
        file_types = [("HTML Files", "*.html")]
        filename = askopenfilename(filetypes=file_types, 
                            defaultextension=".html", 
                            initialdir=initial_dir, 
                            title="Select Bookmark File")
        if filename[-4:] != 'html':
            raise Exception("Only HTML Files are allowed.")

        self.filename = filename
        return filename
    
    def load_file(self) -> str:
        with open(self.filename, 'r') as f:
            self.filecontent = f.read()
        return self.filecontent
    
    def parse_html_file(self) -> list:
        soup = BeautifulSoup(self.filecontent, 'lxml')

        blocks = []
        current_block = {'header': None, 'links': []}

        for tag in tqdm(soup.find_all(['h3', 'a'])):
            if tag.name == 'h3':
                if current_block['header'] and current_block['links']:
                    blocks.append(current_block)
                current_block = {'header': tag.text.strip(), 'links': []}
            elif tag.name == 'a':
                current_block['links'].append({
                    'url': tag['href'],
                    'text': tag.text.strip(),
                })

        # Don't forget the last block
        if current_block['header'] and current_block['links']:
            blocks.append(current_block)

        self.imported_data = blocks
        return blocks

    def show_import(self) -> None:
        for block in self.imported_data:
            print(f"Category: {block['header'].encode('cp1252', errors='replace').decode('cp1252')}")
            for link in block['links']:
                print(f"  Link: {link['url'].encode('cp1252', errors='replace').decode('cp1252')}")
                print(f"  Text: {link['text'].encode('cp1252', errors='replace').decode('cp1252')}")

        
    def __repr__(self):
        return f"Data imported from {self.filename}"
        

if __name__ == '__main__':
    importer = ImportHandler()
    data = importer.f_import()
    # importer.show_import()