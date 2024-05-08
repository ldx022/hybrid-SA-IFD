
import sys

def extract_model(pdb_file, model_number):
    adjusted_model_number = model_number - 1  
    start_line = f"MODEL        {adjusted_model_number}"
    end_line = "ENDMDL"
    model_found = False
    output_lines = []

    with open(pdb_file, 'r') as file:
        for line in file:
            if start_line in line:
                model_found = True
            if model_found:
                output_lines.append(line)
            if end_line in line and model_found:
                break

    if not model_found:
        print(f"Model {adjusted_model_number} not found in {pdb_file}.")
        return

    output_file_name = f"model_{model_number}.pdb"  
    with open(output_file_name, 'w') as output_file:
        output_file.writelines(output_lines)
    print(f"Model {model_number} has been extracted to {output_file_name}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 extract_pdb.py <model_number>")
        sys.exit(1)

    model_number = int(sys.argv[1])  
    pdb_file = "14.total_openmm_minimized.pdb"
    extract_model(pdb_file, model_number)

