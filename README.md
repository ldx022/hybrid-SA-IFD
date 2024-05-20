# hybrid-SA-IFD

hybrid-SA-IFD,also refers to AA/UA/CG-SA-IFD, is a workflow to refine docked poses through enhanced sampling by employing the hybrid All-Atom/United-Atom/Coarse-Grained(AA/UA/CG) model. 

## Requirements
biopython==1.81  
mdtraj==1.9.9  
numpy==1.23.5  
oddt==0.7  
openbabel==3.1.1  
openmm==8.0.0  
pandas==2.0.3  
parmed==3.4.3  
python==3.8.18  
rdkit==2023.03.3  
spyrmsd==0.6.0  
vina==1.2.3  
mdanalysis==2.0.0  
Fpocket==4.1  
prody==2.1.0  
RTMScore's environment  
AmberTools(tleap/antechamber/cpptraj)  
GROMACS==2022.5(GPU)  

## Usage
The workflow is divided into 2 stages. The sampling stage and the post-analysis stage.

In this tutorial we are simply present an example of cross-docking: docking and refine the ligand K0G(target ligand) from the SARS-CoV-2 5R83(target protein) to the structure of 5R84(template protein without native ligand). Because the active site in 5R84 accommodates to its own ligand, rigid docking (such as by Vina) may not yield a correct structure.

### 1.sampling stage(including structure preparation)
Head into `01-prep/01_Workflow/` and do the following:
```bash
python3 0-description.py  --config 0_config
```
The `0_config` file is used to define the number of parallel tasks, the docking mode, and the number of generated poses.
```bash
cd ../03_PrepProtein/script
sh batch_prepDock.sh
cd ../../04_Docking/script
sh 00_batch_dock.sh
sh 01_check_docking_batch.sh
cd ../../05_Refinement/script
sh 00_batch_antechamber.sh
sh 01_batch_prepareComplex.sh
sh 02_check_atom_num.sh
sh 03_batch_getPDB.sh
```
Using `Fpocket` to get core residues:(pymol is needed for visualization)
Head into `01-prep/03_PrepProtein/5R83-K0G-to-5R84`
```bash
fpocket -f apo_continue.pdb
cd apo_continue_out
```
Open pymol and enter the following command:
```bash
@apo_continue.pml
```
On insertion of the template ligand, residues predicted by Fpocket whose spheres overlapped with or are in close proximity to the template ligand are designated as core residues, as demonstrated in the following Figure. For this example, there are a total of 3 pockets respectively. It’s pocket3, pocket13, pocket23
<div align=center>
<img src='./fpocket.png' width='600',height="300px">
</div> 

```bash
cd pockets
cat pocket3_atm.pdb pocket13_atm.pdb pocket23_atm.pdb > pocket3-13-23.pdb
python3 ../../../../01_Workflow/utilities/core-residue-fpocket.py pocket3-13-23.pdb > core_residue.txt
```
At the end of the `core_residue.txt` file, core residues are output:
`There are a total of 24 residues in the core pockets, and they are :25THR 26THR 27LEU 41HIE 44CYS 49MET 52PRO 54TYR 140PHE 141LEU 142ASN 143GLY 145CYS 163HIE 164HIE 165MET 166GLU 167LEU 168PRO 170GLY 187ASP 188ARG 189GLN 190THR`

Write this information into the `core_residue` column of `02-sampling_plus_post-analysis\02_Input\aacg_job_description.csv`
Head into `02-sampling_plus_post-analysis/` and perform simulated annealing MD sampling:

AA/UA/CG modeling tools and required scripts are available from the corresponding authors upon reasonable request.(`ywzhang@nnu.edu.cn`) 
What is currently provided here is the initial structure that has been modeled to AA/UA/CG model for this case.
1-20 represents the initial structure of the 1-20th rigid docking respectively, and 0 represents the complex composed of template protein and target ligand. The mdp files required for dynamic simulation are `em.mdp` and `nvt.mdp`. The function of `posre.itp` is to restrict main chain atoms forming secondary structures in the AA and UA regions to prevent the secondary structure of the protein from being destroyed in high temperature environments.

Then performing simulated annealing on each rigid docking structure.

For each pose, 5 independent, energy minimization and 25 rounds simulated annealing for each trajectory, were performed, saving snapshots every 1150 ps.

All dynamics simulations are done on the cluster. Each trajectory using a single GPU core `RTX3090`
### 2.post-analysis stage
Analyze the resulting trajectories:
```bash
sh 0analysis-ie.sh
python3 1-label-ie.py
python3 2-sort-according2ie.py
python3 3-select-top500.py
python3 4.prep-cluster-traj.py
sh 5.gmxcat-genpdb.sh
python3 6.extract-top500pdb.py
python3 7.remove-boxinfo.py
python3 8.convert_uaname2aa.py
python3 9.aacg2aa.py
python3 10.separate-model.py
python3 11.copy-mol2-frcmod.py
sh 13-parellel.sh
python3 14.sum_minimized_pdb.py
python3 15.separate-pro-lig.py
obabel -ipdb lig.pdb -O lig.sdf
python3 16a.extract_pocket.py
python3 16b.process_failed_pocket.py
python3 17-1.separate-pairs.py
python3 17-2.rtmscore4all.py
python3 18.modified_total_out.py
python3 19-summary.py
sh 20.execute.sh
python3 21-rank_holo_pocket_cluster.py
```
Finally, users can use the `extract_pdb_from_total_openmm.py` script to extract the AA model based on the ` 21_holo_pocket_rank_sort.txt`.
```bash
python3 extract_pdb_from_total_openmm.py 113
```
means to extract the 113th model.
### Output
For the output of the entire process, please see zenodo(10.5281/zenodo.11084549)

## Reference
- Shen, C.; Zhang, X.; Deng, Y.; Gao, J.; Wang, D.; Xu, L.; Pan, P.; Hou, T.; Kang, Y., J. Med. Chem. 2022, 65 (15), 10691–10706.
[Boosting Protein–Ligand Binding Pose Prediction and Virtual Screening Based on Residue–Atom Distance Likelihood Potential and Graph Transformer](https://pubs.acs.org/doi/10.1021/acs.jmedchem.2c00991)
