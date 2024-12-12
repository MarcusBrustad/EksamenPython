from functools import wraps
import os
import random as rd
import string

os.chdir(os.path.dirname(os.path.realpath(__file__)))
# --------------------------------------------------------------------------- #
"""
A. Lag en funksjon som oppretter en mappe kalt ‘Files’ og genererer 
100 tilfeldige filer med følgende filtyper i denne mappen:
    • .txt, .csv, og .log
    • Hver fil skal ha:
        ✓ Et tilfeldig navn med mellom 5 og 10 tegn.
        ✓ En tilfeldig filtype valgt fra de tre typene.
        ✓ Innhold i disse filen er ikke viktig – 
        lag gjerne disse filene uten innhold

B. Lag en funksjon som leser filene i ‘Files’ og 
sorterer dem i undermapper basert på filtype:
    • Opprett en ny mappe kalt ‘SortedFiles’
    • Opprett undermapper kalt ‘txt-files’, ‘csv-files’, og ‘log-files’
    inne i denne mappen kalt SortedFiles.
    • Flytt filene fra ‘Files’ til riktig undermappe i ‘SortedFiles’ 
    basert på deres filtype.
"""


# --------------------------------------------------------------------------- #
# Utility for this task and sub-tasks

# The Decorator is contained within the actual task-file instead
# of being imported to show it being used.
# Decorator to log what task is currently running.
def logging_current_task(task_id):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f'Now running task: {task_id}')
            result = func(*args, **kwargs)
            print()
            return result
        return wrapper
    return decorator


# Function to set filepath and subfolder
def set_file_path(filename, subfolder=None):
    """
    Generates a full file path and ensures the folder exists.

    Args:
        filename (str): Name of wanted file.
        subfolder (str, optional): Subfolder holding the file.
    Returns:
        str: Full file path.
    """
    base_path = os.getcwd()
    if subfolder:
        base_path = os.path.join(base_path, subfolder)
        os.makedirs(base_path, exist_ok=True)

    return os.path.join(base_path, filename)


# Function to get random filetype
def get_random_extension():
    """
    Selects a random file extension from a list.

    Returns:
        str: Random file extension. From ('.txt', '.csv', '.log')
    """

    file_types = ('.txt', '.csv', '.log')
    random_file_type = rd.choice(file_types)
    return random_file_type


# function to get random filename
def get_random_filename():
    """
    Generates a random filename with 5-10 lowercase letters.

    Returns:
        str: Random filename.
    """
    random_filename = f""
    for i in range(rd.randint(5,10)):
        random_filename += f"{rd.choice(string.ascii_lowercase)}"
    return random_filename


# --------------------------------------------------------------------------- #
# Tasks 4A

@logging_current_task('4A')
def tasks_4a():
    """
    Creates 100 random files in the 'Files' folder.

    Each file has a random name and one of these extensions: [.txt, .csv, .log].
    """
    foldername = 'Files'
    i = 0
    while i < 100:
        filename = f'{get_random_filename()}'
        filetype = f'{get_random_extension()}'
        full_filename = filename + filetype
        full_path = set_file_path(full_filename, foldername)
        try:
            with open(full_path, 'x'):
                i+=1
        except FileExistsError:
            continue
    print(f'{i} random files created and placed in folder: [{foldername}]')


# --------------------------------------------------------------------------- #
# Task 4B

@logging_current_task('4B')
def tasks_4b():
    """
    Sorts files in 'Files' into 'SortedFiles' subfolders by file type.
    """
    original_foldername = 'Files'
    sorted_folder = 'SortedFiles'
    files = os.listdir(original_foldername)

    files_moved = {}
    files_existed = {}
    for file in files:
        original_path = set_file_path(file, original_foldername)

        if os.path.isfile(original_path):
            file_name, file_ext = os.path.splitext(file)
            file_ext = file_ext.lstrip('.')

            # Creating sub directory
            sub_directory = set_file_path(
                '', os.path.join(sorted_folder, f'{file_ext}-files'))

            # Creating path for moving file.
            new_path = set_file_path(file, sub_directory)

            # Trying to move file and logging.
            if not os.path.exists(new_path):
                os.rename(original_path, new_path)
                files_moved[file_ext] = files_moved.get(file_ext, 0) +1
            else:
                files_existed[file_ext] = files_existed.get(file_ext, 0) + 1

    # Log of what files has been moved and to what folder
    for ext, amount in files_moved.items():
        print(f'{amount} {ext}-files moved to corresponding folder')

    # Log of what files already existed
    if files_existed:
        print("Summary of files not moved:")
        for ext, count in files_existed.items():
            print(f"{count} {ext}-files already existed in their target folders.")

    # Checks if the original folder is empty then removes it
    if not os.listdir(original_foldername):
        os.rmdir(original_foldername)
        print()
        print(f'Directory: {original_foldername} is now empty. Deleting!')


# --------------------------------------------------------------------------- #
# Main

def main():
    tasks_4a()
    tasks_4b()

# --------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()