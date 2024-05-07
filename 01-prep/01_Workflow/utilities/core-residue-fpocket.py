import sys

def classify_by_column(pdb_file):
    with open(pdb_file, 'r') as f:
        lines = f.readlines()

    atom_lines = [line for line in lines if line.startswith("ATOM")]
    header_lines = [line for line in lines if line.startswith("HEADER")]

    residues = {}
    for line in atom_lines:
        key = line[22:27].strip() + line[17:20].strip()
        if key not in residues:
            residues[key] = []
        residues[key].append(line)

    sorted_residues = sorted(residues.keys(), key=lambda x: (int(x[:-3]), x[-3:]))

    for header in header_lines:
        print(header, end='')
    
    for res in sorted_residues:
        for line in residues[res]:
            print(line, end='')

    residue_names = sorted([res[:-3] + res[-3:] for res in sorted_residues], key=lambda x: int(x[:-3]))

    num_of_residues = len(residue_names)
    print(f"There are a total of {num_of_residues} residues in the core pockets, and they are :" + " ".join(residue_names))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 core-residue.py <pdb_file>")
        sys.exit(1)
    classify_by_column(sys.argv[1])
