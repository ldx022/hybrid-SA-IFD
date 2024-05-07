
import parmed
import os, sys
import glob
import re
import rdkit
from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize

ps_dir = sys.argv[1]
try:
    ps0 = parmed.load_file(f'{ps_dir}/apo_continue.prmtop',f'{ps_dir}/apo_continue.inpcrd')
    ps_holo_ref = parmed.load_file(f'{ps_dir}/apo_continue4holoref.prmtop',f'{ps_dir}/apo_continue4holoref.inpcrd')
except:
    try:
        ps0 = parmed.load_file(f'{ps_dir}/apo_continue.prmtop',f'{ps_dir}/apo_continue.inpcrd')
        ps_holo_ref = parmed.load_file(f'{ps_dir}/apo_continue4holoref.prmtop',f'{ps_dir}/apo_continue4holoref.inpcrd')
    except:
        print(f"{ps_dir}/apo_continue files not found! Exiting ...")
        exit()
lig_param_dir = sys.argv[2]
lig_dir = sys.argv[3]
if lig_dir[-1] == '/':
    lig_dir = lig_dir[:-1]
lig_param_suffix = '_H_bcc_sim' 
lig_base_name = sys.argv[4]
lig_names = os.listdir(lig_dir) # should be rank[1-20].pdb
print(f"lig_names is {lig_names}")
ref_lig_name = glob.glob(f'{lig_param_dir}/*_H.pdb')
print(f"ref_lig_name is {ref_lig_name}")

lig_prmtop_fname = [x for x in os.listdir(lig_param_dir) if f'{lig_param_suffix}.prmtop' in x][0]
print(f"lig_prmtop_fname is {lig_prmtop_fname}")

output_inpcrd = 'inpcrd'
output_prmtop = 'prmtop'
output_reference = '../reference_structure'

try:
    os.mkdir(output_inpcrd)
except:
    pass
try:
    os.mkdir(output_prmtop)
except:
    pass
try:
    os.mkdir(output_reference)
except:
    pass

for ii in lig_names:
    try:
        print(f'Ligand {ii}')  
        lig_base = ii.split('_')[0]  
        lig_id = ii.split('.')[0]  
        ligand_structure = parmed.load_file(f'{lig_param_dir}/{lig_prmtop_fname}',
                                            f'{lig_dir}/{ii}')
        complex_structure = ps0 + ligand_structure
        print(f"complex_structure is {complex_structure}")
        print('Complex assembled')  
        complex_structure.save(f'{output_inpcrd}/{lig_id}.inpcrd', overwrite=True)
        complex_structure.save(f'{output_prmtop}/{lig_base}.prmtop', overwrite=True)
    except:
        print('Complex assembly failed')

# Finally prepare the reference
print(f'Reference_complex')         # rank1.pdb
lig_id = lig_base + '_0'     
print(f"Reference lig_id is {lig_id}")
ligand_structure = parmed.load_file(f'{lig_param_dir}/{lig_prmtop_fname}',
                                    ref_lig_name[0])
complex_structure = ps0 + ligand_structure
holo_ref_structure = ps_holo_ref + ligand_structure
print('Complex assembled')
ligand_structure.save(f'{output_reference}/ligand.inpcrd', overwrite=True)
ligand_structure.save(f'{output_reference}/ligand.prmtop', overwrite=True)
ligand_structure.save(f'{output_reference}/ligand.pdb', overwrite=True)
ps0.save(f'{output_reference}/protein.inpcrd', overwrite=True)
ps0.save(f'{output_reference}/protein.prmtop', overwrite=True)

complex_structure.save(f'{output_reference}/complex.inpcrd', overwrite=True)
complex_structure.save(f'{output_reference}/complex.prmtop', overwrite=True)
complex_structure.save(f'{output_reference}/complex.pdb', overwrite=True)

holo_ref_structure.save(f'{output_reference}/holo_ref_structure.inpcrd', overwrite=True)
holo_ref_structure.save(f'{output_reference}/holo_ref_structure.prmtop', overwrite=True)
holo_ref_structure.save(f'{output_reference}/holo_ref_structure.pdb', overwrite=True)
complex_structure.save(f'{output_inpcrd}/{lig_id}.inpcrd', overwrite=True)

