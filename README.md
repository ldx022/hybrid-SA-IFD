# hybrid-SA-IFD

hybrid-SA-IFD,also refers to AA/UA/CG-SA-IFD, is a workflow to refine docked poses through enhanced simulated annealing MD simulations employing the hybrid All-Atom/United-Atom/Coarse-Grained(AA/UA/CG) model to balance accuracy and computational efficiency.

### Requirements
dgl-cuda11.1==0.7.0   
mdanalysis==2.0.0    
pandas==1.0.3   
prody==2.1.0   
python==3.8.11   
pytorch==1.9.0   
rdkit==2021.03.5   
openbabel==3.1.0    
scikit-learn==0.24.2    
scipy==1.6.2   
seaborn==0.11.2   
numpy==1.20.3    
pandas==1.3.2   
matplotlib==3.4.3   
joblib==1.0.1   

```
conda create --prefix xxx --file ./requirements_conda.txt      
pip install -r ./requirements_pip.txt
```

## Tutorial with one docking case

In this tutorial we are simply going to dock and refine the ligand 
from the SARS-CoV-2 main protease 7QBB to the structure of 5R84, 
a typical "cross-docking" job. Because the active site in 5R84 accommodates to 
its own ligand, simple docking (such as by Vina) may not yield a correct structure.

Head into `01-prep/01_Workflow/` and do the following
python3 0-description.py  --config 0_config
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


Head into `02-sampling_plus_post-analysis/01_Workflow/` and do the following