import os
import mdtraj as md
import sys

def update_template_id(base_directory):
    residue_index_map = {'NaW': 5, 'ClW': 6, 'WT4': 7}  # Residue to index mapping

    for folder in os.listdir(base_directory):
        if any(f"_{i}-aacg-" in folder for i in range(1, 21)):
            pdb_path = os.path.join(base_directory, folder, 'protein-lig-prep', 'system_solv.pdb')
            first_inp_path = os.path.join(base_directory, folder, 'first.inp')

            if os.path.exists(pdb_path) and os.path.exists(first_inp_path):
                traj = md.load(pdb_path)
                residue_names = [res.name for res in traj.topology.residues]

                # Process only the residues after LIG
                if 'LIG' in residue_names:
                    lig_index = residue_names.index('LIG')
                    subsequent_residues = residue_names[lig_index + 1:]

                    # Count and record the order and count of residues after LIG
                    residue_order = []
                    residue_counts = {}
                    for res in subsequent_residues:
                        if res not in residue_order:
                            residue_order.append(res)
                        residue_counts[res] = residue_counts.get(res, 0) + 1

                    # Update the template_id section in the first.inp file
                    with open(first_inp_path, 'r') as file:
                        lines = file.readlines()

                    # Find and preserve the existing template_id section
                    template_id_start, template_id_end = None, None
                    for i, line in enumerate(lines):
                        if 'template_id {' in line:
                            template_id_start = i + 1
                        elif '}' in line and template_id_start is not None:
                            template_id_end = i
                            break

                    existing_template_ids = ' '.join(lines[template_id_start:template_id_end]).split()
                    new_template_ids = existing_template_ids + [str(residue_index_map[res]) for res in residue_order for _ in range(residue_counts[res])]
                    formatted_template_ids = [' '.join(new_template_ids[i:i + 25]) for i in range(0, len(new_template_ids), 25)]

                    # Replace the template_id section
                    lines[template_id_start:template_id_end] = [line + '\n' for line in formatted_template_ids]

                    with open(first_inp_path, 'w') as file:
                        file.writelines(lines)

                    print(f"Updated template_id in {first_inp_path}")
                    print(f"1) 在LIG之后的残基种类顺序是：{' '.join(residue_order)}")
                    print(f"2) 这些残基各有多少个：{residue_counts}")

def main():
    base_directory = sys.argv[1]
    update_template_id(base_directory)

if __name__ == "__main__":
    main()
