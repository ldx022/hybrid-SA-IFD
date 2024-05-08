import mdtraj as md
import os

def update_atom_names(pdb_traj, gro_traj):
    for residue in pdb_traj.topology.residues:
        if residue.name == 'XUA':
            for atom in residue.atoms:
                gro_atom = gro_traj.topology.atom(atom.index)
                pdb_traj.topology.atom(atom.index).name = gro_atom.name
    return pdb_traj

def rename_atoms_in_multi_model_pdb_parallel(pdb_file, gro_file, output_file):
    gro_traj = md.load(gro_file)
    pdb_traj = md.load(pdb_file, top=pdb_file)

    updated_traj = update_atom_names(pdb_traj, gro_traj)

    updated_traj.save(output_file)

# User input for the target folder
current_directory = os.getcwd()
target_folder = os.path.abspath(os.path.join(current_directory, os.pardir))
print(target_folder)
folder_name = f"_0-aacg-"
for folder in os.listdir(target_folder):
    if folder_name in folder:
        ref_workdir = os.path.join(target_folder, folder, ".")
        print(ref_workdir)
        rename_atoms_in_multi_model_pdb_parallel('aa-pro-lig_cleaned.pdb', f'{ref_workdir}/2-1-1.cg_ua2aaname.gro', 'modified_UAname.pdb')    



