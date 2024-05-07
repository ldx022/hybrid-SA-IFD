#!/bin/bash

PDB_FILES=$1    # string w/ regex that points to the pdb files of ligands to parameterized
NET_CHARGE=$2    
for pdb in "${PDB_FILES[@]}"
do
	temp=${pdb##*/}		# removing any potential directories of a local or global file path; we only want the molecule name for future file naming
	temp2=${temp%.*}	# removing any potential file extension from the remaining string
	echo $temp2		# printing ligand information currently being used to create respective directory and file naming
	temp3=${temp2%_protonated} # removing the '_protonated' part from the string
	echo $temp3           # printing ligand information currently being used to create respective directory and file naming
	cp $pdb ./${temp3%.*}_H.pdb
	echo Creating charges for the molecule at GAFF2/AM1-BCC lvl of theory
	echo $pdb
	antechamber -i ./${temp3%.*}_H.pdb -fi pdb -o "$temp3"_H_bcc.mol2 -fo mol2 -nc $NET_CHARGE -at gaff2 -c bcc -s 2 2>antechamber_error.log	# read the ligand mol2 file into antechamber to assign gaff2 atom types and calculate AM1-BCC atomic point charges


	echo Checking parameters w/ parmchk2
	parmchk2 -i "$temp3"_H_bcc.mol2 -f mol2 -o "$temp3"_H_bcc.frcmod -s 2	# check the mol2 file for the potential for missing parameters; if any are found, fill in the gaps w/ other parameters that  are potentially adequate. CHECK THIS FILE FOR HIGH PENALTY SCORES
	echo Creating the prmtop file
	sed -e 's,aaa,'"$temp3"'_H_bcc,g' < ../../../01_Workflow/utilities/leap_input.in > temp.in	
	tleap -f temp.in 
	# clean up the working directory
	mkdir $temp3
	mv $temp3* $temp3/
	mv leap.log $temp3/
	mv ANTECHAMBER* $temp3/ 
	mv ATOMTYPE* $temp3/ 
	mv sqm* $temp3/ 
done

