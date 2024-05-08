
import os

def extract_model_and_index(content, start_marker, end_marker, is_ligand=False):
    models = content.split(start_marker)[1:]  
    for model in models:
        if is_ligand:
            # Find MODEL tags and serial numbers for ligand file processing
            model_lines = model.split('\n')
            model_info_line = next((line for line in model_lines if ">  <MODEL>" in line), None)
            model_index_line = model_lines[model_lines.index(model_info_line) + 1] if model_info_line else None
            model_index = int(model_index_line.strip()) + 1 if model_index_line else None
            model_content = start_marker + model.split(end_marker, 1)[0] + end_marker
        else:
            # For pocket file processing
            model_info = model.split('\n', 1)[0]  
            model_index = int(model_info.split()[-1])  
            model_content = start_marker + model.split(end_marker, 1)[0] + end_marker
        
        yield model_content, model_index

def write_model_file(model_content, filename, is_ligand=False):
    with open(filename, "w") as file:
        file.write(model_content)
        if is_ligand:
            # If it is a lig model, add a blank line at the end
            file.write("\n")
    print(f"Wrote model to {filename}")

workdir = "."
pockets_path = "./final_pockets.pdb"
ligands_path = "./lig.sdf"

with open(pockets_path, 'r') as file:
    pockets_content = file.read()
with open(ligands_path, 'r') as file:
    ligands_content = file.read()

for pocket_model, pocket_model_index in extract_model_and_index(pockets_content, 'MODEL', 'ENDMDL', is_ligand=False):
    pocket_file = f"{workdir}/pro-pocket-{pocket_model_index}.pdb"
    write_model_file(pocket_model, pocket_file, is_ligand=False)

for ligand_model, ligand_model_index in extract_model_and_index(ligands_content, 'lig.pdb', '$$$$', is_ligand=True):
    ligand_file = f"{workdir}/lig-{ligand_model_index}.sdf"
    write_model_file(ligand_model, ligand_file, is_ligand=True)