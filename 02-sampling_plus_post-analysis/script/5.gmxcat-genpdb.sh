#!/bin/bash

gmx trjcat -f $(for i in {1..20}; do echo -n "$i-align.xtc "; done) -o merge1-20.xtc -cat yes

base_directory=$(dirname "$PWD")

for folder in "$base_directory"/*; do
    if [[ -d "$folder" && "$folder" != *"_0-aacg-"* && "$folder" == *"_1-aacg-"* ]]; then
        target_subfolder="$folder/"
        echo "6" | gmx trjconv -f merge1-20.xtc -o merge1-20.pdb -s $target_subfolder/cg.gro -n $target_subfolder/index.ndx
    fi
done


