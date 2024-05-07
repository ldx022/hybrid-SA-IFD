import glob
import os
import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: python script.py <parameter>")
    sys.exit(1)

user_input = sys.argv[1]

prmtop_dir = "./prmtop"
inpcrd_dir = "./inpcrd"
pdb_dir = "./pdb"

os.makedirs(pdb_dir, exist_ok=True)

prmtop_file = os.path.join(prmtop_dir, f"{user_input}.prmtop")
inpcrd_files = glob.glob(f"{inpcrd_dir}/{user_input}_*.inpcrd")

for inpcrd_file in inpcrd_files:
    base_name = os.path.basename(inpcrd_file).split('.')[0]
    pdb_file = os.path.join(pdb_dir, f"{base_name}.pdb")
    cpptraj_cmd = f"cpptraj -p {prmtop_file} -c {inpcrd_file} -y {inpcrd_file} -x {pdb_file}"
    subprocess.run(cpptraj_cmd, shell=True)

print("Conversion complete.")
