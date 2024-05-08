import os
import shutil
import glob

parent_dir = os.path.join(os.getcwd(), '..')

pattern = os.path.join(parent_dir, '*_0-aacg-*', '.', 'prot.pdb')
files = glob.glob(pattern)

for file in files:
    shutil.copy(file, os.getcwd())

import mdtraj as md
import numpy as np

def remove_residues_after_lig(input_pdb, output_pdb):
    with open(input_pdb, 'r') as file:
        lines = file.readlines()

    last_lig_line = None
    for i, line in enumerate(lines):
        if line.startswith("ATOM") or line.startswith("HETATM"):
            residue_name = line[17:20].strip()
            if residue_name == 'LIG':
                last_lig_line = i

    if last_lig_line is not None:
        lines = lines[:last_lig_line + 1]

    with open(output_pdb, 'w') as file:
        file.writelines(lines)
        return True

    print("LIG residue not found in file")
    return False

def replace_coordinates(source_traj, target_traj):
    source_residues = list(source_traj.topology.residues)
    target_residues = list(target_traj.topology.residues)

    atoms_to_keep = list(range(target_traj.n_atoms))

    for source_residue in source_residues:
        if source_residue.name == "XUA":
            source_atoms = {atom.name: atom for atom in source_residue.atoms}
            target_residue = next((res for res in target_residues if res.resSeq == source_residue.resSeq), None)
            if target_residue:
                for target_atom in target_residue.atoms:
                    if target_atom.name in source_atoms:
                        source_atom = source_atoms[target_atom.name]
                        target_traj.xyz[0, target_atom.index] = source_traj.xyz[0, source_atom.index]
                    else:
                        atoms_to_keep.remove(target_atom.index)
        elif source_residue.name not in ["XMA"]:
            target_residue = next((res for res in target_residues if res.resSeq == source_residue.resSeq and res.name not in ["XMA", "XUA"]), None)
            if target_residue:
                # Alternate coordinates
                for source_atom, target_atom in zip(source_residue.atoms, target_residue.atoms):
                    target_traj.xyz[0, target_atom.index] = source_traj.xyz[0, source_atom.index]

    new_traj = target_traj.atom_slice(atoms_to_keep)
    return new_traj

def process_models(source_pdb, target_pdb, output_pdb):
    source_models = md.load_pdb(source_pdb)

    target_traj = md.load(target_pdb)

    processed_models = []

    for model in source_models:
        processed_model = replace_coordinates(model, target_traj)
        processed_models.append(processed_model)

    # Combine all the processed models into one trajectory
    combined_traj = md.join(processed_models)

    # Save the modified structure to a new PDB file
    combined_traj.save(output_pdb)

current_directory = os.getcwd()
target_folder = os.path.abspath(os.path.join(current_directory, os.pardir))
print(target_folder)
folder_name = f"_0-aacg-"
for folder in os.listdir(target_folder):
    if folder_name in folder:
        ref_workdir = os.path.join(target_folder, folder, ".")
        print(ref_workdir)

def main():
    # Delete residues after LIG
    if not remove_residues_after_lig(f'{ref_workdir}/prot.pdb', 'system.pdb'):
        return

    process_models('modified_UAname.pdb', 'system.pdb', 'system-aacg2aa.pdb')

if __name__ == "__main__":
    main()

def parse_pdb_residues(pdb_file):
    with open(pdb_file, 'r') as file:
        residues = {}
        for line in file:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                residue_id = int(line[22:26].strip())  # Extract the residue number
                residue_name = line[17:20].strip()     # Extract the residue name
                residues[residue_id] = residue_name
    return residues

def update_pdb_residue_names(source_pdb, reference_pdb, output_pdb):
    source_residues = parse_pdb_residues(reference_pdb)  

    updated_lines = []
    with open(source_pdb, 'r') as file:
        for line in file:
            if line.startswith("MODEL") or line.startswith("ENDMDL"):
                updated_lines.append(line)
            elif line.startswith("ATOM") or line.startswith("HETATM"):
                residue_id = int(line[22:26].strip())
                if residue_id in source_residues:
                    new_res_name = source_residues[residue_id]
                    line = line[:17] + new_res_name.ljust(3) + line[20:]
                updated_lines.append(line)

    with open(output_pdb, 'w') as file:
        file.writelines(updated_lines)

update_pdb_residue_names('system-aacg2aa.pdb', f'{ref_workdir}/prot.pdb', 'updated_system-aacg2aa.pdb')

