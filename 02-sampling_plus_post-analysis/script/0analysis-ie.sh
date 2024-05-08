
#!/bin/bash
BASE_DIRECTORY=$(pwd)
for i in {1..20}; do
    pattern="${BASE_DIRECTORY}/../5R83-K0G-to-5R84_${i}-aacg*"
    for system_folder in $pattern; do
        if [ -d "$system_folder" ];  then
            (
                echo "Enter folder: $pattern"
                cd "$system_folder/" || exit

                for c in {1..5}; do
                    t0=$((1150 * (25 * (c - 1) + 1)))
                    echo "processing: $c"
                    gmx trjconv -f "./${c}.xtc" -b 1150 -t0 $t0 -timestep 1150 -o "${c}_changed_inital_time.xtc" 
                done

                for c in {1..5}; do
                    echo 0 | gmx trjconv -s "./run.tpr" -f "${c}_changed_inital_time.xtc" -pbc whole -o "run-whole-per-1150ps.xtc" -dt 1150
                    echo -e "7\n0\n" | gmx trjconv -s "./run.tpr" -f "run-whole-per-1150ps.xtc" -o "run-whole-nojump-center-per-1150ps-${c}.xtc" -center yes -n "./index.ndx"
                done

                echo "Merging trace files..."
                gmx trjcat -f $(for c in {1..5}; do echo -n "run-whole-nojump-center-per-1150ps-${c}.xtc "; done) -o run.xtc -cat yes

                gmx grompp -f ../extract-ie.mdp -c ./cg.gro -p ./cg.top -n ./index.ndx -o ie.tpr -r ./cg.gro -maxwarn 2

                gmx mdrun -deffnm ie -rerun run.xtc -nb cpu -ntmpi 1

                echo -e "18\n19\n" | gmx energy -f ie.edr -o ie.xvg

                cd "$BASE_DIRECTORY" || exit
            )&
        else
            echo "folder $pattern does not exist"
        fi
    done
done
wait 

for i in {1..20}; do
    pattern="5R83-K0G-to-5R84_${i}-aacg*"
    for system_folder in ../$pattern/ ; do
        if [ -d "$system_folder" ]; then
            (
            echo "Enter folder: $system_folder"
            cd "$system_folder"
            cp ../script/align-xtc.py .
            python3 align-xtc.py
            )&
        else
            echo "文件夹不存在: $system_folder"
        fi
    done
done    
wait         

for i in {1..20}; do
  tail -n +26 "$BASE_DIRECTORY/../5R83-K0G-to-5R84_${i}-aacg-25k-12cutoff-fullWT4-newxcg/ie.xvg" | sed 's/^[ 	]*//'
done > "$BASE_DIRECTORY/total-ie.txt"


        