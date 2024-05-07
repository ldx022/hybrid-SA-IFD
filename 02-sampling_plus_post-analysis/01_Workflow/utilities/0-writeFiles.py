

def write_preppdbqt(fh, config, dname, rname, rfname, dockX, dockY, dockZ, rigid=True):
    fh.write(f'''
        cd ../{dname}
        obabel -ipdb ../../02_Input/{rfname} -opdb -O {rname}_d.pdb -d
        propka3 {rname}_d.pdb
        python3 ../../01_Workflow/utilities/add_H4apo.py {rname}_d.pdb > convert_residue_name.log 
        tleap -f fix_protein.in > fix_protein.out
        python ../../01_Workflow/utilities/restore_residues.py {rname}
        obabel -ipdb {rname}_restored_h.pdb -opdb -O {rname}_restored_e.pdb # Just to get elements
        obabel -ipdb {rname}_restored_e.pdb -opdbqt -O {rname}.pdbqt --partialcharge gasteiger -xr -xp -xc''')
    if not rigid:#这个没用上
        fh.write(f'''
        python ../../01_Workflow/utilities/create_flex_res.py {rname}.pdbqt {dockX} {dockY} {dockZ}
        ''')


def write_fix_protein(fname, rname):
    with open(fname, 'w') as f:
        f.write(f'''
source leaprc.protein.ff14SB #Source leaprc file for ff14SB protein force field
mol = loadpdb {rname}_d.pdb
savepdb mol {rname}_full_h.pdb
''')


def write_vina_dock(fh, config, jname, dname, rname, lname, lfname, dockX, dockY, dockZ, numPose, energyRange):
    fh.write(f'''
        cd ../{jname}
        obabel -ipdb ../../02_Input/{lfname} -opdb -O {lname}_d.pdb -d # Remove hydrogens that may come with the ligand XRD
        python ../../01_Workflow/utilities/center_ligand_for_docking.py {lname}_d.pdb {dockX} {dockY} {dockZ} {lname}_d_c.pdb # Center the ligand file to be used in docking
        obabel -ipdb {lname}_d.pdb -opdbqt -O {lname}_d.pdbqt -p --partialcharge eem # Get an extra pdbqt (atom indices may change) for calculating RMSD in the subsequent analyses
        obabel -ipdb {lname}_d_c.pdb -opdbqt -O {lname}.pdbqt -p --partialcharge eem # Get the pdbqt file for docking
        obabel -ipdbqt {lname}_d.pdbqt -opdb -O {lname}.pdb -d # Get the extra pdb for calculating RMSD in the subseuqent analyses
        lig_atoms=`obabel -ipdb {lname}.pdb -opdb -h | grep "ATOM" | wc -l`
        echo "Ligand {lname} has $lig_atoms atoms including hydrogens"
        python ../../01_Workflow/utilities/vina_dock.py ../../03_PrepProtein/{dname}/{rname}.pdbqt {lname}.pdbqt {dockX} {dockY} {dockZ} {numPose} {energyRange}
        python ../../01_Workflow/utilities/parseVinaDock.py . {jname}
        mkdir -p docked_pdb
        #mkdir -p docked_pdb_h
        for i in `ls docked`;
        do
            obabel -ipdbqt docked/${{i}} -opdb -Odocked_pdb/${{i%.*}}.pdb -d
        done
        mkdir -p ../../05_Refinement/{jname}/Structure/docked_pdb_h
        cd ../../03_PrepProtein/{dname}
        python ../../01_Workflow/utilities/prep-apo.py {rname}_restored_e.pdb {rname}_restored_e_cleaned.pdb
        tleap -f prep_apo_antechamber.in > prep_apo_antechamber.out
        cd ../../04_Docking/{jname}
        ''')

def write_antechamber(fh, jname, lname, dname, net_charge):
    fh.write(f'''
        mkdir -p ../{jname}
        mkdir -p ../{jname}/Structure
        cd ../{jname}/Structure
        sh ../../../01_Workflow/utilities/pipeline_extra.sh ../../../02_Input/Ligands/{jname}/{lname.split('/')[-1].split('.')[0]}_protonated.pdb {net_charge} > antechamber.log
        mv {lname.split('/')[-1].split('.')[0]} lig_param
        cd ..
        ''')

def write_prepareComplex(fh, jname, lname, dname):
    # set -e ensures the script exits immediately upon failure, EOF must start at a new line without any leading spaces or indentation.
    fh.write(f'''
        # First convert all the docked_pdb files in 04_Docking
        cd ../{jname}/Structure
        cd ../../../04_Docking/{jname}/
        for i in docked_pdb/*; do
            if [ -f "$i" ]; then
                tleap -f - <<EOF
                source leaprc.gaff2
                LIG = loadmol2 ../../05_Refinement/{jname}/Structure/lig_param/{lname.split('/')[-1].split('.')[0]}_H_bcc.mol2
                loadamberparams ../../05_Refinement/{jname}/Structure/lig_param/{lname.split('/')[-1].split('.')[0]}_H_bcc.frcmod
                check LIG
                #f-strings中，两个左括号最后才会在f-string 中用来表示字面大左括号
                mol = loadpdb ./${{i}}
                savepdb mol ../../05_Refinement/{jname}/Structure/docked_pdb_h/${{i##*/}}
                quit
EOF
            fi
        done > tleap_temp.log
        cd ../../05_Refinement/{jname}/Structure
        python ../../../01_Workflow/utilities/prepareComplex.py ../../../03_PrepProtein/{dname} lig_param/ docked_pdb_h/ {jname}
        cd ../reference_structure
        obabel -ipdb ligand.pdb -opdb -O ligand_d.pdb -d
        obabel -ipdb ligand_d.pdb -omol -O ligand.mol
        cd ../
        ''')

def write_getPDB(fh, jname, lname, dname):
    fh.write(f'''
        cd ../{jname}/Structure
        python ../../../01_Workflow/utilities/get_pdb.py {dname}
        cd ../../script
        ''')