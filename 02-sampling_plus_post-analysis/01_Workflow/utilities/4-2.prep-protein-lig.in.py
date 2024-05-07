import os
import re
import sys
import shutil

def create_protein_lig_in_script(base_directory, src_file):
    target_folder = None
    for folder in os.listdir(base_directory):
        if '_0-aacg' in folder:
            target_folder = os.path.join(base_directory, folder, 'protein-lig-prep')
            shutil.copy(src_file, target_folder)
            print(f"target_folder is {target_folder}")
            break

    if target_folder:
        mol2_file, frcmod_file, pdb_file = None, None, None
        for file in os.listdir(target_folder):
            if file.endswith('_bcc.mol2'):
                mol2_file = file
            elif file.endswith('_bcc.frcmod'):
                frcmod_file = file
            elif file.endswith('_0.pdb'):
                pdb_file = file

        if mol2_file and frcmod_file and pdb_file:
            script_path = os.path.join(target_folder, 'protein-lig.in')
            with open(script_path, 'w') as file:
                file.write("#amber20才可以用，相应的力场位置可以看tleap的信息，记得ssbond，如果有需要将CYS改成CYX\n")
                file.write("source leaprc.protein.ff19ipq\n")
                file.write("source leaprc.gaff2\n")
                file.write(f"LIG = loadmol2 {mol2_file}\n")
                file.write(f"loadamberparams {frcmod_file}\n")
                file.write("check LIG\n")
                file.write(f"all= loadpdb {pdb_file}\n")
                file.write("savepdb all prot.pdb   #实际上并没有溶剂，只不过为了脚本的名字好统一\n")
                file.write("saveamberparm all prot.prmtop prot.inpcrd  #实际上并没有溶剂，只不过为了脚本的名字好统一\n")
                file.write("quit\n\n")
            print(f"'protein-lig.in' script created in {target_folder}")

            holo_script_path = os.path.join(target_folder, 'holo-ref-protein-lig.in')
            with open(holo_script_path, 'w') as file:
                file.write("#amber20才可以用，相应的力场位置可以看tleap的信息，记得ssbond，如果有需要将CYS改成CYX\n")
                file.write("source leaprc.protein.ff19ipq\n")
                file.write("source leaprc.gaff2\n")
                file.write(f"LIG = loadmol2 {mol2_file}\n")
                file.write(f"loadamberparams {frcmod_file}\n")
                file.write("check LIG\n")
                file.write(f"all= loadpdb holo_ref_structure_final.pdb\n")
                file.write("savepdb all prot-holo-ref.pdb   #实际上并没有溶剂，只不过为了脚本的名字好统一\n")
                file.write("saveamberparm all prot-holo-ref.prmtop prot-holo-ref.inpcrd  #实际上并没有溶剂，只不过为了脚本的名字好统一\n")
                file.write("quit\n\n")
        else:
            print("Required files not found in the target folder.")
    else:
        print("Target folder not found.")

if __name__ == "__main__":
    base_directory = sys.argv[1]  # Replace with your actual directory path
    src_file = sys.argv[2]
    create_protein_lig_in_script(base_directory, src_file)
