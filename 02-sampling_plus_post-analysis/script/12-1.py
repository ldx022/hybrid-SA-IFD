import glob
import os
import subprocess
update_pdbs = glob.glob('model_*.pdb')
update_pdb = update_pdbs[0] if update_pdbs else None

def remove_first_h_atom(pdb_filename, output_filename):
    with open(pdb_filename, 'r') as file:
        lines = file.readlines()

    first_residue_ended = False
    h_atom_removed = False

    with open(output_filename, 'w') as file:
        for line in lines:
            # Check for atomic rows
            if line.startswith("ATOM"):
                # Parse residue information and atom names
                residue_info = line[22:26].strip()  
                atom_name = line[12:16].strip()    

                # If the first residue has ended, no deletion action is performed
                if first_residue_ended:
                    file.write(line)
                else:
                    if atom_name == 'H':
                        # Delete the atomic row named H and mark it deleted
                        h_atom_removed = True
                    else:
                        file.write(line)

                    if h_atom_removed and residue_info != '1':
                        first_residue_ended = True

            else:
                file.write(line)


def write_addUA_H(tleap, pdb_file):
    with open(tleap, 'w') as f:
        f.write(f'''
source leaprc.protein.ff14SB
source leaprc.gaff2
source leaprc.water.tip3p
LIG = loadmol2 ../LIG.mol2
loadamberparams ../LIG.frcmod
check LIG
all= loadpdb {pdb_file}
#savepdb all protein-lig.pdb
#savepdb LIG only-lig.pdb
#saveamberparm all system_dry.prmtop system_dry.inpcrd
charge all
solvatebox all TIP3PBOX 12
addions all Na+ 0
addions all Cl- 0
saveamberparm all system_solv.prmtop system_solv.inpcrd
quit
''')


if update_pdb:
    remove_first_h_atom(update_pdb, f"1{update_pdb}")
    write_addUA_H('./prep-tleap.in', f"1{update_pdb}")

    subprocess.run(['tleap', '-s', '-f', 'prep-tleap.in'])
else:
    print("No update_*.pdb files found.")