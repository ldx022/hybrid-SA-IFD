import sys
import shutil

def read_pka_file(pka_file):
    pka_values = {}
    start_reading = False
    with open(pka_file, 'r') as file:
        for line in file:
            if start_reading:
                parts = line.split()
                if len(parts) > 3 and parts[1].isdigit():
                    residue = parts[0]
                    number = int(parts[1])
                    pka = float(parts[3])
                    pka_values[(residue, number)] = pka
            if "SUMMARY OF THIS PREDICTION" in line:
                start_reading = True
    return pka_values

def modify_pdb_file(pdb_file, pka_values):
    modified_residues = []
    with open(pdb_file, 'r') as file:
        lines = file.readlines()

    with open(pdb_file, 'w') as file:
        for line in lines:
            if line.startswith("ATOM") or line.startswith("HETATM"):
                residue = line[17:20].strip()
                number = int(line[22:26].strip())
                if (residue, number) in pka_values:
                    pka = pka_values[(residue, number)]
                    if residue in ["ASP", "GLU", "HIS"] and pka > 7.2:
                        if residue == "ASP":
                            line = line[:17] + "ASH" + line[20:]
                        elif residue == "GLU":
                            line = line[:17] + "GLH" + line[20:]
                        elif residue == "HIS":
                            line = line[:17] + "HIP" + line[20:]
                        modified_residues.append(f"{residue}{number}")
            file.write(line)

    return modified_residues

def main(pdb_file):
    shutil.copyfile(pdb_file, pdb_file + ".bak")

    pka_file = pdb_file.replace(".pdb", ".pka")
    pka_values = read_pka_file(pka_file)
    modified_residues = modify_pdb_file(pdb_file, pka_values)

    if modified_residues:
        print("Modified residues:", ", ".join(modified_residues))
    else:
        print("No residues were modified.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python add_H4apo.py [pdb_file]")
        sys.exit(1)

    pdb_file = sys.argv[1]
    main(pdb_file)
