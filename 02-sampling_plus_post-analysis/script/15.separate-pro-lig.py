def extract_protein_and_ligand(source_pdb, protein_output, ligand_output):
    with open(source_pdb, 'r') as file:
        protein_lines = []
        ligand_lines = []
        current_model = None

        for line in file:
            if line.startswith("MODEL"):
                current_model = line
                protein_lines.append(line)
                ligand_lines.append(line)
            elif line.startswith("ENDMDL"):
                protein_lines.append(line)
                ligand_lines.append(line)
            elif line.startswith("ATOM") or line.startswith("HETATM"):
                residue_name = line[17:20].strip()
                if residue_name != "LIG":
                    protein_lines.append(line)
                else:
                    ligand_lines.append(line)

    with open(protein_output, 'w') as protein_file:
        protein_file.writelines(protein_lines)

    with open(ligand_output, 'w') as ligand_file:
        ligand_file.writelines(ligand_lines)

extract_protein_and_ligand('14.total_openmm_minimized.pdb', 'pro.pdb', 'lig.pdb')
