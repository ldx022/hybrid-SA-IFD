import os, re
import prody as pr
from openbabel import openbabel as ob

def write_file(output_file, outline):
    with open(output_file, 'w') as buffer:
        buffer.write(outline)

def lig_rename(infile, outfile):
    # Rename the ligand for pocket generation
    lines = open(infile, 'r').readlines()
    newlines = [line[:17] + "LIG" + line[20:] if re.search(r'^HETATM|^ATOM', line) else line for line in lines]
    write_file(outfile, ''.join(newlines))

def check_mol(infile, outfile):
    # Remove ligands that might be mistaken as part of the pocket
    os.system("sed '/LIG/d' {} > {}".format(infile, outfile))

def extract_pocket(protpath, ligpath, cutoff=5.0, workdir='.'):
    # Extracts pockets for each model in protpath and ligpath
    prot_models = parse_models(protpath, 'MODEL', 'ENDMDL')
    lig_models = parse_models(ligpath, 'lig.pdb', '$$$$')

    for i, (prot_model, lig_model) in enumerate(zip(prot_models, lig_models)):
        protname = f"model_{i}"
        ligname = f"lig_{i}"

        with open(f"{workdir}/{protname}.pdb", "w") as f:
            f.write(prot_model)
        with open(f"{workdir}/{ligname}.pdb", "w") as f:
            f.write(lig_model)

        # Convert ligand to PDB if necessary and rename ligand for pocket generation
        convert_and_rename_ligand(ligpath, ligname, workdir)

        # Load protein and ligand structures
        xprot = pr.parsePDB(f"{workdir}/{protname}.pdb")
        xlig = pr.parsePDB(f"{workdir}/{ligname}.pdb")
        lresname = xlig.getResnames()[0]
        xcom = xlig + xprot

        # Extract pocket
        ret = xcom.select(f'same residue as exwithin {cutoff} of resname {lresname}')
        if ret is not None and ret.numAtoms() > 0:
            pr.writePDB(f"{workdir}/{protname}_pocket_{cutoff}_temp.pdb", ret)

            # Check molecule and save final pocket
            check_mol(f"{workdir}/{protname}_pocket_{cutoff}_temp.pdb", f"{workdir}/{protname}_pocket_{cutoff}.pdb")
            os.remove(f"{workdir}/{protname}_pocket_{cutoff}_temp.pdb")

            # Append model index and pocket to the final file
            with open(f"{workdir}/final_pockets.pdb", "a") as final_file:
                final_file.write(f"MODEL     {i+1}\n")
                with open(f"{workdir}/{protname}_pocket_{cutoff}.pdb") as pocket_file:
                    final_file.write(pocket_file.read())
                final_file.write("ENDMDL\n")

            # Clean up temporary files
            os.remove(f"{workdir}/{protname}.pdb")
            os.remove(f"{workdir}/{ligname}.pdb")
            os.remove(f"{workdir}/{protname}_pocket_{cutoff}.pdb")
        else:
            print(f"No pocket found for model {i+1} within the cutoff of {cutoff} Å.")

def parse_models(filepath, start_marker, end_marker):
    # Parses the file and splits it into models based on start and end markers
    with open(filepath, 'r') as file:
        content = file.read()
    models = content.split(start_marker)[1:]
    models = [start_marker + model.split(end_marker)[0] + end_marker for model in models]
    return models

def convert_and_rename_ligand(ligpath, ligname, workdir):
    # Converts the ligand to PDB format if necessary and renames it
    obConversion = ob.OBConversion()
    obConversion.SetInAndOutFormats(ligpath.split('.')[-1], "pdb")
    ligand = ob.OBMol()
    obConversion.ReadFile(ligand, f"{workdir}/{ligname}.pdb")
    obConversion.WriteFile(ligand, f"{workdir}/{ligname}_converted.pdb")
    lig_rename(f"{workdir}/{ligname}_converted.pdb", f"{workdir}/{ligname}.pdb")
    os.remove(f"{workdir}/{ligname}_converted.pdb")

# Example usage
extract_pocket("./pro.pdb", "lig.sdf", cutoff=10.0, workdir=".")
