import MDAnalysis as mda
from MDAnalysis.analysis import align
import pandas as pd
import warnings
import os
warnings.filterwarnings('ignore')
current_directory = os.getcwd()
print("current_directory:", current_directory)
md = mda.Universe("./cg.gro", 'run.xtc') 
ref_dock_initial = mda.Universe("./cg.gro")
align.AlignTraj(md,  # trajectory to align
                ref_dock_initial,  # reference
                select='(protein and not name H*) or (resname XMA) or (resname XUA)',  # selection of atoms to align
                filename='./aligned-pbc-correct.xtc',  # file to write the trajectory to
                match_atoms=True,  # whether to match atoms based on mass
               ).run()
