import os
import sys

def create_prep_tleap_script(base_directory):
    for folder in os.listdir(base_directory):
        # Check if the folder name contains "_1-aacg-" to "_20-aacg-"
        if any(f"_{i}-aacg-" in folder for i in range(1, 21)):
            protein_lig_prep_folder = os.path.join(base_directory, folder, 'protein-lig-prep')
            if os.path.exists(protein_lig_prep_folder):
                # Extract the relevant part from the folder name for the pdb file
                relevant_part = folder.split('-aacg')[0]
                pdb_file = f"{relevant_part}.pdb"

                # Find the relevant .mol2 and .frcmod files
                mol2_file = None
                frcmod_file = None
                for file in os.listdir(protein_lig_prep_folder):
                    if file.endswith('_bcc.mol2'):
                        mol2_file = file
                    elif file.endswith('_bcc.frcmod'):
                        frcmod_file = file
                
                # Check if necessary files are present
                if mol2_file and frcmod_file and os.path.exists(os.path.join(protein_lig_prep_folder, pdb_file)):
                    # Construct the prep-tleap.in file content
                    content_tleap = f"""#amber20才可以用，相应的力场位置可以看tleap的信息，记得ssbond，如果有需要将CYS改成CYX
addPath /export/home/ldx022/tmp-flexopt/own/anneal/sirah_x2.2_20-08.amber
source leaprc.sirah
source leaprc.protein.ff19ipq
source leaprc.gaff2
LIG = loadmol2 {mol2_file}
loadamberparams {frcmod_file}
check LIG
all= loadpdb {pdb_file}
#savepdb all prot.pdb
#saveamberparm all prot.prmtop prot.inpcrd
#savepdb LIG only-lig.pdb
# Info on system charge 
charge all
# Set S-S bridges 
#bond all.3.BSG all.40.BSG 
#bond all.4.BSG all.32.BSG 
solvateBox all WT4BOX 12 0.4
addIons all NaW 0
addIons all ClW 0
saveamberparm all system_solv.prmtop system_solv.inpcrd
quit"""

                    # Construct the prep-solv-prot.in file content
                    content_solv_prot = f"""#amber20才可以用，相应的力场位置可以看tleap的信息，记得ssbond，如果有需要将CYS改成CYX
addPath /export/home/ldx022/tmp-flexopt/own/anneal/sirah_x2.2_20-08.amber
source leaprc.sirah
source leaprc.protein.ff19ipq
source leaprc.gaff2
LIG = loadmol2 {mol2_file}
loadamberparams {frcmod_file}
check LIG
all= loadpdb prot-system_solv.pdb
savepdb all prot.pdb
saveamberparm all prot.prmtop prot.inpcrd
quit"""

                    # Write the content to prep-tleap.in file
                    script_path_tleap = os.path.join(protein_lig_prep_folder, 'prep-tleap.in')
                    with open(script_path_tleap, 'w') as file:
                        file.write(content_tleap)
                    print(f"'prep-tleap.in' script created in {protein_lig_prep_folder}")

                    # Write the content to prep-solv-prot.in file
                    script_path_solv_prot = os.path.join(protein_lig_prep_folder, 'prep-solv-prot.in')
                    with open(script_path_solv_prot, 'w') as file:
                        file.write(content_solv_prot)
                    print(f"'prep-solv-prot.in' script created in {protein_lig_prep_folder}")

def main():
    base_directory = sys.argv[1]
    create_prep_tleap_script(base_directory)

if __name__ == "__main__":
    main()
