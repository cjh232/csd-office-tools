import os
import shutil
from PyPDF2 import PdfFileMerger

root_directory = r'C:\Users\chunt\OneDrive\Desktop\Electron Tutorial\files'

normalizedPath = lambda path: os.path.normpath(path)
endsWith = lambda file_name, ext: os.path.splitext(file_name)[1] == ext


def combinePdfFiles(entry: os.DirEntry, index: int):

    print(f'Combining {entry.name}...')

    merger = PdfFileMerger()
    root_entry_path = entry.path

    # Order summary should be of form "<Order Id> <Product Type>" ex: "6099403 CO"
    order_summary = entry.name

    merge_list: list[DirEntry] = [entry for entry in os.scandir(root_entry_path) 
                                if (entry.is_file() and endsWith(entry.name, '.pdf'))]

    if len(merge_list) < 2:
        return
            
    """
    Each file will be named 1_file_name, 2_file_name and so on.
    PDF will merge in ascending order using the first digit.
    """

    for item in merge_list:
        merger.append(item.path)
        
    
    merger.write(os.path.join(root_entry_path, f'{order_summary}.pdf'))

    # Important to close the merger process so that we can move
    # the files after merging.
    merger.close()

    # Move the old files to the history directory
    history_dir = os.path.join(root_entry_path, 'history')
    os.mkdir(history_dir)

    for item in merge_list:
        shutil.move(item.path, history_dir)

    
def execute_on_directory(root_directoy: str) -> None:
    sub_directories = [entry for entry in os.scandir(root_directory) if entry.is_dir()]

    for index, sub_directory in enumerate(sub_directories):
        try:
            combinePdfFiles(sub_directory, index)
        except Exception as err:
            print(err)
    
    print('Finished...')
        


    

execute_on_directory(root_directory)
