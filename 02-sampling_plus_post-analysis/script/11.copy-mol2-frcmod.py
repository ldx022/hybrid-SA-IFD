import shutil
import os

def find_files(directory, extensions):
    found_files = {ext: None for ext in extensions}
    for root, dirs, files in os.walk(directory):
        for file in files:
            for ext in extensions:
                if file.endswith(ext) and found_files[ext] is None:
                    found_files[ext] = os.path.join(root, file)
                    break  
    return found_files

current_directory = os.getcwd()
target_folder = os.path.abspath(os.path.join(current_directory, os.pardir))
print(target_folder)
folder_name = f"_0-aacg-"
for folder in os.listdir(target_folder):
    if folder_name in folder:
        ref_workdir = os.path.join(target_folder, folder, ".")
        print(ref_workdir)
        extensions = ['.mol2', '.frcmod']
        found_files = find_files(ref_workdir, extensions)
        mol2 = found_files['.mol2']
        frcmod = found_files['.frcmod']

        if mol2 and frcmod:
            shutil.copy(mol2, os.path.join(current_directory, "LIG.mol2"))
            shutil.copy(frcmod, os.path.join(current_directory, "LIG.frcmod"))
            print(f"Files copied to {current_directory}: LIG.mol2 and LIG.frcmod")
        else:
            print("Required files were not found.")
