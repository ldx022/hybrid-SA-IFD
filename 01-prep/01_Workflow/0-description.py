import numpy as np
import pandas as pd
import os
from os.path import exists
import argparse
import shutil

from utilities.writeFiles import *

parser = argparse.ArgumentParser(description="Generate related work shell scripts")
parser.add_argument('--parallelGrid', nargs='?', type=int, default=1, help="Split grid prep to N chunks for parallel execution")
parser.add_argument('--parallelDock', nargs='?', type=int, default=1, help="Split docking to N chunks for parallel execution")
parser.add_argument('--dockingMode', type=str, default='rigid', help="Whether to use flexible docking (changes some residue orientations) (rigid|flex)")
parser.add_argument('--parallelAntechamber', nargs='?', type=int, default=1, help="Split ligand parametrization to N chunks for parallel execution")
parser.add_argument('--parallelPrepareComplex', nargs='?', type=int, default=1, help="Split complex preparation to N chunks for parallel execution")
parser.add_argument('--parallelGetPDB', nargs='?', type=int, default=1, help="Split getpdb to N chunks for parallel execution")
parser.add_argument('--dockOutputPoses', type=int, default='20', help="Number of poses to output in docking")
parser.add_argument('--dockEnergyRange', type=str, default='None', help="Energy range in Vina docking settings (float or ['inf', 'np.inf', 'infinity'] for infinite energy range, or any other string to let Vina decide")
parser.add_argument('--config', nargs='?', type=str, default=None, help="File logging locations of executables")

args = parser.parse_args()
config = {}
config['parallelGrid'] = args.parallelGrid
config['parallelDock'] = args.parallelDock
config['dockingMode'] = args.dockingMode
config['parallelAntechamber'] = args.parallelAntechamber
config['parallelPrepareComplex'] = args.parallelPrepareComplex
config['parallelGetPDB'] = args.parallelGetPDB
config['dockOutputPoses'] = args.dockOutputPoses
config['dockEnergyRange'] = args.dockEnergyRange


os.makedirs('../03_PrepProtein', exist_ok=True)
os.makedirs('../04_Docking', exist_ok=True)
os.makedirs('../05_Refinement', exist_ok=True)

if args.config is not None:
    with open(args.config,'r') as f:
        cont = f.readlines()
    for line in cont:
        try:
            if line.split('=')[0] in ['parallelGrid', 'parallelDock', 'parallelAntechamber', 'parallelPrepareComplex', 'parallelGetPDB', 'dockOutputPoses']:
                try:
                    config[line.split('=')[0]] = int(line.split('=')[1].strip())
                except:
                    pass
            else:
                config[line.split('=')[0]] = line.split('=')[1].strip()
        except:
            pass

if config['dockingMode'] == 'rigid':
    rigid = True
elif config['dockingMode'] == 'flex':
    rigid = False
else:
    raise ValueError('dockingMode must be either rigid or flex')
Jobs = pd.read_csv('../02_Input/job_description.csv')
Jobs['Receptor_name'] = Jobs['Receptor_file_name'].str.split('/').str[-1].str.split('.').str[0] 
Jobs['Ligand_name'] = Jobs['Ligand_file_name'].str.split('/').str[-1].str.split('.').str[0] 
Jobs['holo_ref_name'] = Jobs['Ref_receptor_nolig_file_name'].str.split('/').str[-1].str.split('.').str[0] 

print(Jobs)

Rec = Jobs['Receptor_file_name'].unique()
Lig = Jobs['Ligand_file_name'].unique()
print(Rec, Lig)

for R in Rec:
    if not exists(f'../02_Input/{R}'):
        print(f'Receptor {R} does not exist!')
        raise FileNotFoundError
for L in Lig:
    if not exists(f'../02_Input/{L}'):
        print(f'Ligand {L} does not exist!')
        raise FileNotFoundError

print("All files in job description exist")        

Receptors = Jobs.drop(columns=['Ligand_file_name', 'Job_name', 'Ligand_name'])
Receptors = Receptors.drop_duplicates()

if config['parallelGrid'] > len(Receptors):
    print(f"parallelGrid is updated from {config['parallelGrid']} to {len(Receptors)}")
    config['parallelGrid'] = min(config['parallelGrid'], len(Receptors))
for item in ['parallelDock', 'parallelAntechamber', 'parallelPrepareComplex', 'parallelGetPDB']:
    if config[item] > len(Jobs):
        print(f"{item} is updated from {config[item]} to {len(Jobs)}")
        config[item] = min(config[item], len(Jobs))
print(config)

try:
    os.mkdir('../03_PrepProtein/script')
except:
    pass

fh = []  

g = open('../03_PrepProtein/script/batch_prepDock.sh', 'w')
g.write('#!/bin/bash\n')

for ii in range(config['parallelGrid']):
    fh.append(open(f'../03_PrepProtein/script/prepDock{ii}.sh','w'))
    g.write(f'sh prepDock{ii}.sh & \n')

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()

for idx, row in Jobs.iterrows():
    dname = row["Job_name"]
    holo_ref = row["Ref_receptor_nolig_file_name"]
    os.makedirs(f'../03_PrepProtein/{dname}', exist_ok=True)
    write_preppdbqt(fh[idx % config['parallelGrid']], config, dname, row["Receptor_name"], row["Receptor_file_name"], holo_ref, row["holo_ref_name"], row["dockX"], row["dockY"], row["dockZ"], rigid)
    write_fix_protein(f'../03_PrepProtein/{dname}/fix_protein.in', row["Receptor_name"], row["holo_ref_name"])
for ii in range(config['parallelGrid']):
    fh[ii].close()

try:
    os.mkdir('../04_Docking/script')
except:
    pass

fh = []  

g = open('../04_Docking/script/00_batch_dock.sh', 'w')
g.write('#!/bin/bash\n')

for ii in range(config['parallelDock']):
    fh.append(open(f'../04_Docking/script/dock{ii}.sh','w'))
    g.write(f'sh dock{ii}.sh > dock{ii}.log & \n')

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()

with open(f'../04_Docking/script/01_check_docking.sh','w') as f, open(f'../04_Docking/script/01_check_docking_batch.sh','w') as g:
    g.write('#!/bin/bash\n')
    g.write('echo "`date`: Job starts"\n')
    g.write('mkdir docking_results\n')
    for idx, row in Jobs.iterrows():
        dname = row["Job_name"]
        lname = row["Ligand_name"]
        jname = row["Job_name"]
        os.makedirs(f'../04_Docking/{jname}', exist_ok=True)
        if rigid:
            write_vina_dock(fh[idx % config['parallelDock']], config, jname, dname, row["Receptor_name"], row["Ligand_name"], row["Ligand_file_name"], row["holo_ref_name"], row['dockX'], row['dockY'], row['dockZ'], config['dockOutputPoses'], config['dockEnergyRange'])
        else:
            write_vina_flex_dock(fh[idx % config['parallelDock']], config, jname, dname, row["Receptor_name"], row["Ligand_name"], row["Ligand_file_name"], row['dockX'], row['dockY'], row['dockZ'])
            write_flex_assembly(f'../03_PrepProtein/{dname}/flex_assembly.py',row["Receptor_name"], jname, row["dockX"], row["dockY"], row["dockZ"])
        f.write(f'python ../../01_Workflow/utilities/check_dock.py {jname} {lname}.pdb > docking_results/{jname}.txt \n')
        g.write(f'python ../../01_Workflow/utilities/check_dock.py {jname} {lname}.pdb > docking_results/{jname}.txt & \n')
        if (idx > 0) and (idx + 1) % 32 == 0:
            g.write('wait\n\n')
    g.write('wait\n\n')
    g.write('echo "`date`: All done!\n\n"')
    g.close()

shutil.copyfile('utilities/check_docking.py', '../04_Docking/script/02_check_docking.py')

for ii in range(config['parallelDock']):
    fh[ii].close()


try:
    os.makedirs('../05_Refinement/script')
except:
    pass



fh = []
g = open('../05_Refinement/script/00_batch_antechamber.sh', 'w')
g.write('#!/bin/bash\n')

for ii in range(config['parallelAntechamber']):
    fh.append(open(f'../05_Refinement/script/antechamber{ii}.sh','w'))
    g.write(f'sh antechamber{ii}.sh & \n')

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()

for idx, row in Jobs.iterrows():
    dname = row["Job_name"]
    lname = row["Ligand_file_name"]
    jname = row["Job_name"]
    net_charge = row['nc']
    try:
        os.makedirs(f'../05_Refinement/{jname}/Structure/')
    except:
        pass
    write_antechamber(fh[idx % config['parallelAntechamber']], jname, lname, dname, net_charge)

for ii in range(config['parallelAntechamber']):
    fh[ii].close()

fh = []
gh = []
if rigid:
    g = open('../05_Refinement/script/01_batch_prepareComplex.sh', 'w')
    g.write('#!/bin/bash\n')
else:
    ih = open('../05_Refinement/script/01_batch_prepareFlexComplex.sh', 'w')
    ih.write('#!/bin/bash\n')

for ii in range(config['parallelPrepareComplex']):
    if rigid:
        fh.append(open(f'../05_Refinement/script/prepareComplex{ii}.sh','w'))
        g.write(f'sh prepareComplex{ii}.sh & \n')
    else:
        gh.append(open(f'../05_Refinement/script/prepareFlexComplex{ii}.sh','w'))
        ih.write(f'sh prepareFlexComplex{ii}.sh & \n')

if rigid:
    g.write('wait\n\n\n')
else:
    ih.write('wait\n\n\n')

for idx, row in Jobs.iterrows():
    dname = row["Job_name"]
    lname = row["Ligand_file_name"]
    jname = row["Job_name"]
    os.makedirs(f'../05_Refinement/{jname}/Structure/', exist_ok=True)
    if rigid:
        write_prepareComplex(fh[idx % config['parallelPrepareComplex']], jname, lname, dname)
    else:
        write_prepareFlexComplex(gh[idx % config['parallelPrepareComplex']], jname, lname, dname)

for ii in range(config['parallelPrepareComplex']):
    if rigid:
        fh[ii].close()
    else:
        gh[ii].close()

shutil.copyfile('utilities/check_atom_num.sh', '../05_Refinement/script/02_check_atom_num.sh')

fh = []
g = open('../05_Refinement/script/03_batch_getPDB.sh', 'w')
g.write('#!/bin/bash\n')
for ii in range(config['parallelGetPDB']):
    fh.append(open(f'../05_Refinement/script/GetPDB{ii}.sh','w'))
    g.write(f'sh GetPDB{ii}.sh & \n')
g.write('wait\n\n\n')

for idx, row in Jobs.iterrows():
    dname = row["Job_name"]
    lname = row["Ligand_file_name"]
    jname = row["Job_name"]
    write_getPDB(fh[idx % config['parallelGetPDB']], jname, lname, dname)

g.write('echo "`date`: All done!\n\n"')
g.close()

for ii in range(config['parallelPrepareComplex']):
    fh[ii].close()

