import numpy as np
import pandas as pd
import os
from os.path import exists
import argparse
import shutil

from utilities.writeFiles import *

parser = argparse.ArgumentParser(description="Generate related work shell scripts")
parser.add_argument('--parallelGrid', nargs='?', type=int, default=1, help="Split grid prep to N chunks for parallel execution")
parser.add_argument('--parallelCreateFolder', nargs='?', type=int, default=1, help="create folder for each system")
parser.add_argument('--serialXCG', nargs='?', type=int, default=1, help="run xcg serially")
parser.add_argument('--config', nargs='?', type=str, default=None, help="File logging locations of executables")



args = parser.parse_args()

config = {}
config['parallelGrid'] = args.parallelGrid
config['parallelCreateFolder'] = args.parallelCreateFolder
config['serialXCG'] = args.serialXCG

os.makedirs('../03_CreateFolder', exist_ok=True)
os.makedirs('../04_1prep', exist_ok=True)
os.makedirs('../05_LIG4gz', exist_ok=True)
os.makedirs('../06_2prep', exist_ok=True)
os.makedirs('../07_prep4xcgENM', exist_ok=True)
os.makedirs('../08_protein-lig-prep', exist_ok=True)
os.makedirs('../09_get-solv-aacg', exist_ok=True)



if args.config is not None:
    with open(args.config,'r') as f:
        cont = f.readlines()
    for line in cont:
        try:
            if line.split('=')[0] in ['parallelGrid', 'parallelCreateFolder', 'serialXCG']:
                try:
                    config[line.split('=')[0]] = int(line.split('=')[1].strip())
                except:
                    pass
            else:
                config[line.split('=')[0]] = line.split('=')[1].strip()
        except:
            pass

Jobs = pd.read_csv('../02_Input/aacg_job_description.csv')
Jobs['Ligand_name'] = Jobs['Ligand_file_name'].str.split('/').str[-1].str.split('.').str[0] 

print(Jobs)

Receptors = Jobs.drop(columns=['Ligand_file_name', 'Job_name'])
Receptors = Receptors.drop_duplicates()

if config['parallelGrid'] > len(Receptors):
    print(f"parallelGrid is updated from {config['parallelGrid']} to {len(Receptors)}")
    config['parallelGrid'] = min(config['parallelGrid'], len(Receptors))
for item in ['parallelCreateFolder', 'serialXCG']:
    if config[item] > len(Jobs):
        print(f"{item} is updated from {config[item]} to {len(Jobs)}")
        config[item] = min(config[item], len(Jobs))

print(config)
try:
    os.mkdir('../03_CreateFolder')
except:
    pass

fh = []  

g = open('../03_CreateFolder/01batch_CreateFolder.sh', 'w')
g.write('#!/bin/bash\n')

for ii in range(config['parallelGrid']):
    fh.append(open(f'../03_CreateFolder/CreateFolder{ii}.py','w'))
    g.write(f'python3 CreateFolder{ii}.py & \n')

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()

for idx, row in Jobs.iterrows():
    jname = row["Job_name"]
    pose_number = row["pose_number"]
    k_value = row["k"]
    cutoff_value = row["cutoff"]
    os.makedirs(f'../{jname}', exist_ok=True)
    write_CreateFolder(fh[idx % config['parallelGrid']], jname, pose_number, k_value, cutoff_value)

for ii in range(config['parallelGrid']):
    fh[ii].close()
try:
    os.mkdir('../04_1prep')
except:
    pass

fh = []  

g = open('../04_1prep/02batch_1prep.sh', 'w')
g.write('#!/bin/bash\n')

for ii in range(config['parallelGrid']):
    fh.append(open(f'../04_1prep/1prep{ii}.py','w'))
    g.write(f'python3 1prep{ii}.py & \n')

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()

for idx, row in Jobs.iterrows():
    jname = row["Job_name"]
    aacg_parameter = row["aacg_parameter"]
    write_1prep(fh[idx % config['parallelGrid']], jname, aacg_parameter)

for ii in range(config['parallelGrid']):
    fh[ii].close()

try:
    os.mkdir('../05_LIG4gz')
except:
    pass

fh = []  # File handle array

g = open('../05_LIG4gz/03batch_LIGgz.sh', 'w')
g.write('#!/bin/bash\n')

for ii in range(config['parallelGrid']):
    fh.append(open(f'../05_LIG4gz/prep_LIGgz{ii}.py','w'))
    g.write(f'python3 prep_LIGgz{ii}.py & \n')

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()

for idx, row in Jobs.iterrows():
    jname = row["Job_name"]
    lname = row["Ligand_name"]

    write_prep_LIGgz(fh[idx % config['parallelGrid']], jname, lname)

for ii in range(config['parallelGrid']):
    fh[ii].close()


try:
    os.mkdir('../06_2prep')
except:
    pass

fh = []  

g = open('../06_2prep/04batch_2prep.sh', 'w')
g.write('#!/bin/bash\n')

for ii in range(config['parallelGrid']):
    fh.append(open(f'../06_2prep/2prep{ii}.py','w'))
    g.write(f'python3 2prep{ii}.py & \n')

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()

for idx, row in Jobs.iterrows():
    jname = row["Job_name"]

    write_2prep(fh[idx % config['parallelGrid']], jname)

for ii in range(config['parallelGrid']):
    fh[ii].close()


try:
    os.mkdir('../07_prep4xcgENM')
except:
    pass

fh = []  

g = open('../07_prep4xcgENM/05batch_prep4xcgENM.sh', 'w')
g.write('#!/bin/bash\n')

for ii in range(config['parallelGrid']):
    fh.append(open(f'../07_prep4xcgENM/prep4xcgENM{ii}.sh','w'))
    g.write(f'sh prep4xcgENM{ii}.sh & \n')

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()

for idx, row in Jobs.iterrows():
    jname = row["Job_name"]
    core_residue = row["core_residue"]

    write_prep4xcgENM(fh[idx % config['parallelGrid']], jname, core_residue)

for ii in range(config['parallelGrid']):
    fh[ii].close()


try:
    os.mkdir('../08_protein-lig-prep')
except:
    pass

fh = []  

g = open('../08_protein-lig-prep/06batch_prep_solv.sh', 'w')
g.write('#!/bin/bash\n')

for ii in range(config['parallelGrid']):
    fh.append(open(f'../08_protein-lig-prep/prep_solv{ii}.sh','w'))
    g.write(f'sh prep_solv{ii}.sh & \n')

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()

for idx, row in Jobs.iterrows():
    jname = row["Job_name"]
    
    write_prepsolv(fh[idx % config['parallelGrid']], jname)

for ii in range(config['parallelGrid']):
    fh[ii].close()



try:
    os.mkdir('../09_get-solv-aacg')
except:
    pass

fh = []  

write_bsub09('../09_get-solv-aacg/get_solv_aacg.bsub')
g = open('../09_get-solv-aacg/07batch_get_solv_aacg.sh', 'w')
g.write('#!/bin/bash\n')

for ii in range(config['parallelGrid']):
    fh.append(open(f'../09_get-solv-aacg/get_solv_aacg{ii}.sh','w'))
    g.write(f'sh get_solv_aacg{ii}.sh & \n')

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()

for idx, row in Jobs.iterrows():
    jname = row["Job_name"]
    
    write_get_solv_aacg(fh[idx % config['parallelGrid']], jname)

for ii in range(config['parallelGrid']):
    fh[ii].close()


try:
    os.mkdir('../10_prep_SA_control')
except:
    pass

fh = []  
gh = []
eh = []
hh = []

g = open('../10_prep_SA_control/08batch_prep_SA_control.sh', 'w')
f = open('../10_prep_SA_control/09batch_multi_job.sh', 'w')
h = open('../10_prep_SA_control/10batch_restrain_secondary.sh', 'w')
e = open('../10_prep_SA_control/11batch_submit_job.sh', 'w')
g.write('#!/bin/bash\n')
f.write('#!/bin/bash\n')
h.write('#!/bin/bash\n')
e.write('#!/bin/bash\n')
for idx, row in Jobs.iterrows():
    jname = row["Job_name"]
    eh.append(open(f'../{jname}/submit_job.sh','w'))
    e.write(f'cd ../{jname}/  \n')
    e.write(f'sh submit_job.sh  \n')
    e.write(f'cd -  \n')

for ii in range(config['parallelGrid']):
    fh.append(open(f'../10_prep_SA_control/prep_SA_control{ii}.py','w'))
    gh.append(open(f'../10_prep_SA_control/multi_job{ii}.py','w'))
    hh.append(open(f'../10_prep_SA_control/restrain_secondary{ii}.py','w'))
    
    g.write(f'python3 prep_SA_control{ii}.py & \n')
    f.write(f'python3 multi_job{ii}.py & \n')
    h.write(f'python3 restrain_secondary{ii}.py > restrain_secondary{ii}.log& \n')
    

g.write('wait\n\n')
g.write('echo "`date`: All done!\n\n"')
g.close()
f.write('wait\n\n')
f.write('echo "`date`: All done!\n\n"')
f.close()
e.write('wait\n\n')
e.write('echo "`date`: All done!\n\n"')
e.close()
h.write('wait\n\n')
h.write('echo "`date`: All done!\n\n"')
h.close()

for idx, row in Jobs.iterrows():
    jname = row["Job_name"]
    SAcontrol = row["SA_control"]
    time_per_round = row['time_per_round']
    write_prep_gromacs(fh[idx % config['parallelGrid']], jname, SAcontrol)
    write_multi_job(gh[idx % config['parallelGrid']], jname, SAcontrol)
    write_job_submit(eh[idx % config['parallelGrid']], jname, SAcontrol)
    write_create_core(f'../{jname}/1create_core.sh', SAcontrol, jname)
    write_check_job(f'../{jname}/2check_job_core.sh', SAcontrol, jname)
    write_restrain_secondary(hh[idx % config['parallelGrid']], jname, SAcontrol)
    write_merge_whole(f'../{jname}/3merge_whole.sh', SAcontrol, jname, time_per_round)
    write_ie(f'../{jname}/4analysis-ie.sh', SAcontrol, jname)
    write_merge_total_ie_rmsd(f'../{jname}/5merge-ie-rmsd.sh', SAcontrol, jname)
    write_merge_ie_rmsd2csv(f'../{jname}/6.merge_ie_rmsd2csv.py')


for ii in range(config['parallelGrid']):
    fh[ii].close()
for ii in range(config['parallelGrid']):
    gh[ii].close()
for ii in range(config['parallelGrid']):
    hh[ii].close()