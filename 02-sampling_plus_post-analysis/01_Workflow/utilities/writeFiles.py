def write_CreateFolder(fh, jname, pose_number, k_value, cutoff_value):#没有用上config里面的内容就不用加个config子项了
    fh.write(f'''
import os
def create_folders():
    # Step 1: Ask for the system name，字符串需要被单引号或双引号包裹。数值就不用
    system_name = '{jname}'
    # Step 2: Ask for the number of aacg modeling systems,0表示参考结构，那么aacg建模体系总个数为
    range_input = '{pose_number}'
    start, end = map(int, range_input.split('-'))
    total_systems = end - start + 1
    # Step 4: Ask for ENM's k value
    enm_k = {k_value}
    # Step 5: Ask for ENM's cutoff
    enm_cutoff = {cutoff_value}
    # Step 6: Ask for the solvent,目前统一先用WT4
    solvent = 'fullWT4'
    # Creating folders
    for i in range(start, end + 1):
        folder_name = f"{{system_name}}_{{i}}-aacg-{{enm_k}}k-{{enm_cutoff}}cutoff-{{solvent}}-newxcg"
        os.makedirs(folder_name, exist_ok=True)
        print(f"创建文件夹: {{folder_name}}") 
        
base_path = "../"
system_path = "./{jname}"
# Run the function
if __name__ == "__main__":
    if os.path.exists(base_path):      # 检查路径是否存在
        os.chdir(base_path)            # 在Python脚本中，若要实现类似于Shell命令 cd 的功能，您需要使用 os 模块来改变当前工作目录。
        os.makedirs("{jname}", exist_ok=True)   #任何非数字字面量（如目录名）都必须被引号包围，以指明它们是字符串。也就是说数值就不用引号
        if os.path.exists(system_path):
            os.chdir(system_path)
            create_folders()
        else:
            print(f"路径不存在: {{system_path}}")
    else:
        print(f"路径不存在: {{base_path}}")
''')

def write_1prep(fh, jname, aacg_parameter):#没有用上config里面的内容就不用加个config子项了
    fh.write(f'''
import os
import shutil
#当定义一个函数并在括号中指定参数时，这些参数就成为了函数的局部变量。
#这意味着当您调用这个函数时，需要提供这两个参数的值。函数内部的代码将使用这些提供的值来执行其任务。
def create_subfolders_and_copy_files(base_directory, xcg_input_dir):
    # Listing directories in the base directory that contain '-aacg-'
    directories = [d for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d)) and '-aacg-' in d]

    # Creating subfolders and copying files
    for directory in directories:
        full_path = os.path.join(base_directory, directory)
        subfolders = ['LIG-prep', 'protein-lig-prep', 'anneal']
        for subfolder in subfolders:
            os.makedirs(os.path.join(full_path, subfolder), exist_ok=True)

        # Copy files
        for file_name in ['second.inp', 'get-cg-protein.sh', 'first.inp', 'holo-ref-second.inp', 'holo-ref-get-cg-protein.sh', 'solvate.sh', 'solvation.in']:
            src_file = os.path.join(xcg_input_dir, file_name)
            if os.path.exists(src_file):
                shutil.copy(src_file, full_path)
            else:
                print(f"文件 {{file_name}} 未找到于 {{xcg_input_dir}}")

        print(f"在 {{full_path}} 中创建子文件夹并复制文件完成")

base_path = "../"
system_path = "./{jname}"


# Run the function
if __name__ == "__main__":
    if os.path.exists(base_path):      # 检查路径是否存在
        os.chdir(base_path)            # 在Python脚本中，若要实现类似于Shell命令 cd 的功能，您需要使用 os 模块来改变当前工作目录。
        os.makedirs("{jname}", exist_ok=True)   #任何非数字字面量（如目录名）都必须被引号包围，以指明它们是字符串。也就是说数值就不用引号
        if os.path.exists(system_path):
            os.chdir(system_path)
            current_directory = os.getcwd()
            print("当前目录是:", current_directory)
            #--------------------------------
            #这里可以用来控制aacg的参数文件
            #--------------------------------
            xcg_input_relative_dir = "../aacg-script/{aacg_parameter}"
            xcg_input_absolute_dir = os.path.abspath(xcg_input_relative_dir)   #使用os.path.abspath() 将相对路径转化成绝对路径
            create_subfolders_and_copy_files(current_directory, xcg_input_absolute_dir)
        else:
            print(f"路径不存在: {{system_path}}")
    else:
        print(f"路径不存在: {{base_path}}")

''')


def write_prep_LIGgz(fh, jname, lname):#没有用上config里面的内容就不用加个config子项了
    fh.write(f'''
import os
import shutil
import subprocess

# Step 1: Create the LIG-prep directory
lig_prep_path = '../{jname}/LIG-prep'
os.makedirs(lig_prep_path, exist_ok=True)

# Step 2: Copy the files
#-------------------------
#控制配体参数文件的目录
#-------------------------
source_dir = '../../000-111-prep-flow-tinyIFDfailed-SARS/05_Refinement/{jname}/Structure/lig_param'
files_to_copy = ['{lname}_H_bcc_sim.prmtop', '{lname}_H_bcc_sim.rst7']
for file in files_to_copy:
    shutil.copy(os.path.join(source_dir, file), lig_prep_path)

# Step 3: Create and write to xcg-lig.inp
xcg_lig_inp_path = '../{jname}/LIG-prep/xcg-lig.inp'
with open(xcg_lig_inp_path, 'w') as file:
    #---------------------------------------------------------------------------
    #f-string（格式化字符串）会解释转义字符，比如“\加n”会被解释为换行符。使用双反斜杠“\\\\”来避免转义。
    #---------------------------------------------------------------------------
    file.write("amber\\n")
    file.write("   prmtop {lname}_H_bcc_sim.prmtop\\n")
    file.write("   inpcrds {{\\n")
    file.write("      {lname}_H_bcc_sim.rst7\\n")
    file.write("   }}\\n")
    file.write("   tolammps LIG\\n")
    file.write("/\\n")

# Step 4: Execute the command
os.chdir('../{jname}/LIG-prep')
subprocess.run(['../../xcg', 'mapping', '-i', 'xcg-lig.inp'])

''')

def write_2prep(fh, jname):#没有用上config里面的内容就不用加个config子项了
    fh.write(f'''
import os
import shutil

def copy_lig_prep_files(base_directory, lig_prep_source):
    # Copying files to LIG-prep folders
    for folder in os.listdir(base_directory):
        if any(f"_{{i}}-aacg-" in folder for i in range(0, 21)):
            lig_prep_folder = os.path.join(base_directory, folder, 'LIG-prep')
            if os.path.exists(lig_prep_folder):
                for file in os.listdir(lig_prep_source):
                    src_file = os.path.join(lig_prep_source, file)
                    shutil.copy(src_file, lig_prep_folder)
                print(f"文件已复制到 {{lig_prep_folder}}")

def copy_protein_lig_prep_files(base_directory, structure_directory):
    # Copying files to protein-lig-prep folders
    prmtop_source = os.path.join(structure_directory, 'prmtop')
    pdb_source = os.path.join(structure_directory, 'pdb')
    inpcrd_source = os.path.join(structure_directory, 'inpcrd')
    lig_param_source = os.path.join(structure_directory, 'lig_param')

    for folder in os.listdir(base_directory):
        if any(f"_{{i}}-aacg-" in folder for i in range(0, 21)):
            protein_lig_prep_folder = os.path.join(base_directory, folder, 'protein-lig-prep')
            if os.path.exists(protein_lig_prep_folder):
                # Copy prmtop, lig_param (bcc.frcmod and bcc.mol2), pdb, and inpcrd files
                for source_dir in [prmtop_source, lig_param_source]:
                    for file in os.listdir(source_dir):
                        if source_dir == lig_param_source and not (file.endswith('_bcc.frcmod') or file.endswith('_bcc.mol2')):
                            continue
                        src_file = os.path.join(source_dir, file)
                        shutil.copy(src_file, protein_lig_prep_folder)

                # Extract the relevant part from the folder name for pdb and inpcrd files
                relevant_part = folder.split('-aacg')[0]
                pdb_file = f"{{relevant_part}}.pdb"
                inpcrd_file = f"{{relevant_part}}.inpcrd"

                pdb_file_path = os.path.join(pdb_source, pdb_file)
                inpcrd_file_path = os.path.join(inpcrd_source, inpcrd_file)

                # Copy pdb and inpcrd files if they exist
                if os.path.exists(pdb_file_path):
                    shutil.copy(pdb_file_path, protein_lig_prep_folder)
                if os.path.exists(inpcrd_file_path):
                    shutil.copy(inpcrd_file_path, protein_lig_prep_folder)

                print(f"文件 {{pdb_file}} 和 {{inpcrd_file}} 已复制到 {{protein_lig_prep_folder}}")

base_path = "../"
system_path = "./{jname}"

# Run the function
if __name__ == "__main__":
    if os.path.exists(base_path):      # 检查路径是否存在
        os.chdir(base_path)            # 在Python脚本中，若要实现类似于Shell命令 cd 的功能，您需要使用 os 模块来改变当前工作目录。
        os.makedirs("{jname}", exist_ok=True)   #任何非数字字面量（如目录名）都必须被引号包围，以指明它们是字符串。也就是说数值就不用引号
        if os.path.exists(system_path):
            os.chdir(system_path)
            system_path = os.getcwd()
            #提供LIG-prep准备文件目录
            lig_prep_source_relative_path = "./LIG-prep"
            lig_prep_source = os.path.abspath(lig_prep_source_relative_path)
            #提供复合物incprd\prmtop\pdb文件目录
            structure_directory_relative_path = "../../000-111-prep-flow-tinyIFDfailed-SARS/05_Refinement/{jname}/Structure"
            structure_directory = os.path.abspath(structure_directory_relative_path)
            copy_lig_prep_files(system_path, lig_prep_source)
            copy_protein_lig_prep_files(system_path, structure_directory)
        else:
            print(f"路径不存在: {{system_path}}")
    else:
        print(f"路径不存在: {{base_path}}")
''')


def write_prep4xcgENM(fh, jname, core_residue):#没有用上config里面的内容就不用加个config子项了
    fh.write(f'''
#!/bin/bash
cd ../{jname}
BASE_DIRECTORY=$(pwd)
# 1. 运行 #$BASE_DIRECTORY要转化成字符串吗？
#------------------------------------------------------------------------------------
#4-1这个脚本里面有填写控制topology的力场！！！
#------------------------------------------------------------------------------------
python3 ../01_Workflow/utilities/4-1.prep-forENM-20231226uacg.py "$BASE_DIRECTORY" {core_residue}  
python3 ../01_Workflow/utilities/4-2.prep-protein-lig.in.py "$BASE_DIRECTORY" "../../000-111-prep-flow-tinyIFDfailed-SARS/05_Refinement/{jname}/reference_structure/holo_ref_structure_final.pdb"

# 2. 进入目标文件夹执行 get-cg-protein.sh
for folder in "$BASE_DIRECTORY"/*; do
    if [[ -d $folder && $folder == *"_0-aacg-"* ]]; then
        cd "$folder/protein-lig-prep"
        module add amber/20
        tleap -s -f protein-lig.in
        tleap -s -f holo-ref-protein-lig.in
        cd ..
        sh get-cg-protein.sh
        sh holo-ref-get-cg-protein.sh
        # 读取 template_id 内容部分（不包括开头和结尾）并保存到临时文件
        sed -n '/template_id {{/,/}}/p' first.inp | grep -v "template_id {{" | grep -v "}}" > ../template_id_content.txt
        break
    fi
done

# 3. 处理 mix.data 文件
cd prot-workdir
grep "XMA-XA" mix.data > ENM.log
awk '{{print $1}}' ENM.log > newfile.txt

# 4. 将 newfile.txt 和 template_id 内容添加到其他文件夹中的 first.inp
for folder in "$BASE_DIRECTORY"/*; do
    if [[ -d $folder && $folder != *"_0-aacg-"* && $folder == *"-aacg-"* ]]; then
        echo "Processing folder: $folder"
        # 构造 sed 命令来插入 newfile.txt 的内容
        sed -i "/mask {{/r newfile.txt" "$folder/first.inp"
        echo "in directory: $(pwd)"
        # 插入 template_id 内容
        sed -i "/template_id {{/r ../../template_id_content.txt" "$folder/first.inp"
    fi
done

cd ../../../07_prep4xcgENM/ || exit
''')

def write_prepsolv(fh, jname):#没有用上config里面的内容就不用加个config子项了
    fh.write(f'''
#!/bin/bash
cd ../{jname}
BASE_DIRECTORY=$(pwd)
# 1. 运行 create_prep_tleap.py
python3 ../01_Workflow/utilities/5.create_prep_tleap.py "$BASE_DIRECTORY"

# 2. 加载 Amber 20 模块
module add amber/20

# 3. 遍历每个 protein-lig-prep 文件夹，并运行 prep-tleap.in

for folder in "$BASE_DIRECTORY"/*; do
    if [[ -d $folder && $folder != *"_0-aacg-"* && $folder == *"-aacg-"* ]]; then
        echo "Processing folder: $folder"
        protein_lig_prep_folder="$folder/protein-lig-prep"
        if [ -d "$protein_lig_prep_folder" ]; then
            cd "$protein_lig_prep_folder"
            if [ -f "prep-tleap.in" ]; then
                # 运行 prep-tleap.in
                tleap -s -f prep-tleap.in
                cpptraj -p system_solv.prmtop -y system_solv.inpcrd -x system_solv.pdb
                #prot加完水之后坐标会发生改变
                awk '/NaW|WT4|ClW/{{exit}} {{print}}' system_solv.pdb > prot-system_solv.pdb
                tleap -s -f prep-solv-prot.in 
            fi
            cd - # 返回到原始目录
        fi
    fi
done
''')

def write_bsub06(bsub):
    with open(bsub, 'w') as f:
        f.write(f'''
#!/bin/bash

#BSUB -q q36cores
#BSUB -J prep_solv
#BSUB -o prep_solv.out
#BSUB -e prep_solv.err
#BSUB -n 36
#BSUB -R "span[ptile=36]"

echo job runs at the following node:
echo $LSB_HOSTS 
NP=$(echo $LSB_HOSTS | awk '{{print NF}}')
echo ""
echo Number of processor: $NP
echo ""

#add modulefiles

#EXECUTE
sh 06batch_prep_solv.sh
''')

def write_get_solv_aacg(fh, jname):#没有用上config里面的内容就不用加个config子项了
    fh.write(f'''
#!/bin/bash
cd ../{jname}
BASE_DIRECTORY=$(pwd)
#python3 ../01_Workflow/utilities/6.prep-forAACG_solv.py "$BASE_DIRECTORY"

# 遍历基目录中的每个文件夹
for folder in "$BASE_DIRECTORY"/*; do
    if [[ -d $folder && $folder != *"_0-aacg-"* && $folder == *"-aacg-"* ]]; then
        echo "进入文件夹: $folder"
        cd "$folder"
        # 检查get-cg-protein.sh脚本是否存在
        if [ -f "get-cg-protein.sh" ]; then
            # 执行脚本
            chmod +x ./get-cg-protein.sh
            chmod +x ./solvate.sh
            ./get-cg-protein.sh
            ./solvate.sh
            echo "在 $folder 中执行了 get-cg-protein.sh和 solvate.sh"
        else
            echo "在 $folder 中未找到 get-cg-protein.sh"
        fi
        cd - # 返回到原始目录
    fi
done
''')


"""
对于以上bash脚本，可以改成如下形式，让for循环里面的那些子任务并行化：
for folder in "$BASE_DIRECTORY"/*; do
    if [[ -d $folder && $folder != *"_0-aacg-"* && $folder == *"-aacg-"* ]]; then
        (
            echo "进入文件夹: $folder"
            cd "$folder"
            if [ -f "get-cg-protein.sh" ]; then
                chmod +x ./get-cg-protein.sh
                ./get-cg-protein.sh
                echo "在 $folder 中执行了 get-cg-protein.sh"
            else
                echo "在 $folder 中未找到 get-cg-protein.sh"
            fi
        ) &
    fi
done
wait
其中使用了 () 来创建一个子 shell，并在子 shell 中运行代码块，然后使用 & 将其放在后台运行。wait 命令是用来等待所有后台进程完成。
"""

def write_bsub09(bsub):
    with open(bsub, 'w') as f:
        f.write(f'''
#!/bin/bash

#BSUB -q q32cores
#BSUB -J get-solv-aacg
#BSUB -o get-solv-aacg.out
#BSUB -e get-solv-aacg.err
#BSUB -n 32
#BSUB -R "span[ptile=32]"

echo job runs at the following node:
echo $LSB_HOSTS 
NP=$(echo $LSB_HOSTS | awk '{{print NF}}')
echo ""
echo Number of processor: $NP
echo ""

#add modulefiles

#EXECUTE
source /export/home/ldx022/software/miniconda3/etc/profile.d/conda.sh
conda activate flexopt
sh 07batch_get_solv_aacg.sh
''')




def write_prep_gromacs(fh, jname, SAcontrol):#没有用上config里面的内容就不用加个config子项了
    fh.write(f'''
import os
import shutil
import subprocess

def copySA(base_directory):
    # 获取需要拷贝的文件夹和文件
    #directories = input("请你提供需要拷贝的1个或多个文件夹（用空格分隔）: ").split() #生成列表
    #files = input("请你提供需要拷贝的1个或多个文件（用空格分隔）: ").split()

    # 遍历基本目录中的目标文件夹
    for folder in os.listdir(base_directory):
        target_folder = os.path.join(base_directory, folder)
        if os.path.isdir(target_folder) and "-aacg-" in folder and not "_0-aacg-" in folder:
            anneal_path = os.path.join(target_folder, "anneal")
            workdir_path = os.path.join(target_folder, "workdir")

            # 拷贝文件夹
            #------------------------------------------------------------------------
            #注意 目前的脚本是会覆盖掉已有的文件夹
            #------------------------------------------------------------------------
            #if os.path.isdir("../anneal-script/{SAcontrol}"):
            #    shutil.copytree("../anneal-script/{SAcontrol}", os.path.join(anneal_path, os.path.basename("../anneal-script/{SAcontrol}")), dirs_exist_ok=True) #os.path.basename(dir)表示dir 的基本名称（即目录的最后一部分，不包含前面的路径）
            source_path = "../anneal-script/{SAcontrol}"
            destination_path = os.path.join(anneal_path, os.path.basename(source_path))
            # 如果目标目录存在，则删除它
            if os.path.exists(destination_path):
                shutil.rmtree(destination_path)
            # 然后复制新的目录
            shutil.copytree(source_path, destination_path)

            # 在workdir中执行命令
            if os.path.isdir(workdir_path):
                os.chdir(workdir_path)
                subprocess.run("source /export/home/ldx022/software/GROMACS/gmx2022.6-GPU/bin/GMXRC", shell=True, executable='/bin/bash')
                process = subprocess.Popen("gmx make_ndx -f cg.gro", stdin=subprocess.PIPE, shell=True, executable='/bin/bash')
                process.communicate(input="del 5-20\\nr WT4 NaW ClW\\nname 5 env\\n!5\\nname 6 pro-lig\\nquit\\n".encode())
                os.chdir(base_directory) #注意，在for循环中切换目录，最后要切换回去！         

base_path = "../"
system_path = "./{jname}"

# Run the function
if __name__ == "__main__":
    if os.path.exists(base_path):      # 检查路径是否存在
        os.chdir(base_path)            # 在Python脚本中，若要实现类似于Shell命令 cd 的功能，您需要使用 os 模块来改变当前工作目录。
        os.makedirs("{jname}", exist_ok=True)   #任何非数字字面量（如目录名）都必须被引号包围，以指明它们是字符串。也就是说数值就不用引号
        if os.path.exists(system_path):
            os.chdir(system_path)
            current_directory = os.getcwd()
            print("当前目录是:", current_directory)
            copySA(current_directory)
        else:
            print(f"路径不存在: {{system_path}}")
    else:
        print(f"路径不存在: {{base_path}}")

''')

def write_multi_job(gh, jname, SAcontrol):#没有用上config里面的内容就不用加个config子项了
    gh.write(f'''
import os
import shutil
import subprocess
import re

def generate_multi_job(base_directory):
    # 遍历基本目录中的目标文件夹
    for folder in os.listdir(base_directory):
        target_folder = os.path.join(base_directory, folder)
        if os.path.isdir(target_folder) and "-aacg-" in folder and not "_0-aacg-" in folder:
            anneal_path = os.path.join(target_folder, "anneal")
            workdir_path = os.path.join(target_folder, "workdir")
            SAcontrol_path = os.path.join(target_folder, "anneal", "{SAcontrol}")
            match = re.search(r'{jname}_[0-9]+', target_folder)#匹配以 {jname}_ 开头，后面跟着至少一个数字的字符串。
            SAcontrol = "{SAcontrol}"
            if match:
                system_name = match.group()#match.group()：如果找到匹配的部分，group() 方法将返回匹配的字符串。
                print("提取的部分：", system_name)
            else:
                print("未找到匹配的部分")


            #在SAcontrol中执行命令           
            if os.path.isdir(SAcontrol_path):
                os.chdir(SAcontrol_path)
                for i in range(1, 21):
                    folder_path = os.path.join(SAcontrol_path, str(i))
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)

                    with open(os.path.join(SAcontrol_path, f"{{i}}.bsub"), 'w') as file:
                        file.write(f"""#!/bin/bash

#BSUB -q gpu
#BSUB -o {{system_name}}-{{i}}.out
#BSUB -e {{system_name}}-{{i}}.err
#BSUB -J {{system_name}}-{{i}}-{{SAcontrol}}
#BSUB -n 8
#BSUB -R "span[ptile=8]"
##BSUB -m g004

#export CUDA_VISIBLE_DEVICES=3
#INPUT_NAME=combined
# choose CUDA (0,1,2,3)# 
#export CUDA_VISIBLE_DEVICES=1,2，

#--- LSF ---
echo job runs at the following node:
echo $LSB_HOSTS 
NP=$(echo $LSB_HOSTS | awk '{{{{print NF}}}}')
NNODE=$(echo $LSB_HOSTS | sed -e "s/ /\\\\n/g" | uniq - | wc -l)
echo ""
echo Number of processor: $NP

NP2=$((NP%8))

if [ $NP2 -ne 0 ]; then
  echo NP only can be 8, 16, 24 or 32
  exit
fi

echo 0 > gpu-info-1
for lineNum in {{{{1..3}}}}
do
  echo $lineNum >> gpu-info-1
done
/usr/bin/nvidia-smi | awk '/Default/{{{{print $(NF-2)}}}}' | sed 's/\%//' > gpu-info-2

paste gpu-info-1 gpu-info-2 > gpu-info
awk '$2==0{{{{print $1}}}}' gpu-info > free-card

ncard=$((NP/4))
export CUDA_VISIBLE_DEVICES="$(cat free-card | awk 'NR<ncard{{{{printf"%s,",$1}}}};NR==ncard{{{{printf"%s\\\\n",$1}}}}' ncard=$ncard)"
echo $CUDA_VISIBLE_DEVICES

rm -rf gpu-info* free-card

# Environment for gromacs
#module add gromacs/2019.6
source /export/home/ldx022/software/GROMACS/gmx2022.6-GPU/bin/GMXRC

ulimit -s unlimited

#if [ $NGPU -eq 1 ]; then
cd {{i}}
gmx grompp -f ../em.mdp -p ../../../workdir/cg.top -c ../../../workdir/cg.gro -o em.tpr  -maxwarn 2
gmx mdrun -deffnm em -nt 8 -pin on -pinstride 1 -gpu_id 0

#https://www.hpc.dtu.dk/?page_id=3106
# set NGPUS to the number of GPUs requested in the job
NGPUS=1
# set OMPTHREADS to the number of OpenMP threads desired
OMPTHREADS=8
export OMP_NUM_THREADS=$OMPTHREADS # like this it works

gmx grompp -f ../nvt.mdp -p ../../../workdir/cg.top -c ./em.gro -r ./em.gro -o run.tpr -n ../../../workdir/index.ndx -maxwarn 2
#Remove "-gpu_id 0 -nb gpu  -pme gpu -bonded gpu -update gpu" add "-v" option to debug
gmx mdrun -cpt 5 -deffnm run -ntmpi $NGPUS -ntomp $OMPTHREADS -gpu_id 0 -nb gpu  -pme gpu -bonded gpu -update gpu 

echo $(date)""")
                os.chdir(base_directory)   
        

base_path = "../"
system_path = "./{jname}"

# Run the function
if __name__ == "__main__":
    if os.path.exists(base_path):      # 检查路径是否存在
        os.chdir(base_path)            # 在Python脚本中，若要实现类似于Shell命令 cd 的功能，您需要使用 os 模块来改变当前工作目录。
        os.makedirs("{jname}", exist_ok=True)   #任何非数字字面量（如目录名）都必须被引号包围，以指明它们是字符串。也就是说数值就不用引号
        if os.path.exists(system_path):
            os.chdir(system_path)
            current_directory = os.getcwd()
            print("当前目录是:", current_directory)
            generate_multi_job(current_directory)
        else:
            print(f"路径不存在: {{system_path}}")
    else:
        print(f"路径不存在: {{base_path}}")

''')



def write_job_submit(eh, jname, SAcontrol):
    eh.write(f'''
#!/bin/bash

: '
以下的为注释段落
请你帮我写一个批量提交作业的bash脚本实现以下目的：
1、首先初始化作业列表，也就是使用bjobs | grep 600K_heat-1.0-cool-2.0-2fs |wc -l,看看目前有多少个作业在运行，如果目前正在运行的作业数小于40个（不包括40），则开始执行当前脚本；
2、在当前目录的文件中，遍历当前文件夹下文件夹名中带有"2g0g-SP0-to-2prg_{{i}}-aacg"格式的文件夹$system_folder，其中i的范围从1-20（注意取到两个端点），进入$system_folder文件夹的anneal/600K_heat-1.0-cool-2.0-2fs目录，该目录下已经提前生成好了作业脚本，分别是{{k}}.bsub，其中k的范围从1-20（注意取到两个端点）,分别需要循环使用"bsub < {{k}}.bsub"命令来提交作业，注意每个作业的提交需要间隔30秒，同时需要保证正在运行的作业数不大于40个！！
3、请你中间echo一些信息让我知道目前的提交作业情况
4、system_folder的名字并不叫做2g0g-SP0-to-2prg_${{i}}-aacg，而是带有"2g0g-SP0-to-2prg_${{i}}-aacg"格式的文件夹名！！
5、如果target_folder="/export/home/ldx022/tmp-flexopt/own/0-2-anneal-19ipq-modified-cg-flow-25rounds*20/2g0g-SP0-to-2prg/2g0g-SP0-to-2prg_10-aacg-25k-12cutoff-fullWT4-newxcg"，如何提取2g0g-SP0-to-2prg_10这一部分复制给一个叫做system的变量
6、echo "等待中... 当前作业数：$current_jobs"这一部分在等待的过程中只需要输出一次就好了
'

# 设置最大作业数限制
MAX_JOBS=45

echo "开始检查当前运行的作业数..."
current_jobs=$(bjobs -w| grep {SAcontrol} | wc -l)
echo "当前运行的作业数：$current_jobs"

if [ "$current_jobs" -le "$MAX_JOBS" ]; then
    # 遍历当前目录下符合特定模式的文件夹
    for i in {{1..20}}; do
        pattern="{jname}_${{i}}-aacg*"
        for system_folder in $pattern/ ; do
            if [ -d "$system_folder/anneal/{SAcontrol}" ]; then
                echo "进入文件夹：$system_folder/anneal/{SAcontrol}"

                # 进入目标文件夹
                cd "$system_folder/anneal/{SAcontrol}"
                
                # 提交作业脚本
                for k in {{1..20}}; do
                    # 检查作业数，确保不超过40个
                    # 引入了一个名为 waiting_message_shown 的标志变量。这个变量在进入等待循环前设置为 false，并且在首次打印等待消息后设置为 true。这确保了即使循环多次执行，等待消息也只会打印一次。
                    waiting_message_shown=false
                    while true; do
                        current_jobs=$(bjobs -w| grep {SAcontrol} | wc -l)
                        if [ "$current_jobs" -lt "$MAX_JOBS" ]; then
                            break
                        fi
                        if [ "$waiting_message_shown" = false ]; then
                            echo "等待中... 当前作业数：$current_jobs"
                            waiting_message_shown=true
                        fi
                        sleep 10  # 等待10秒后再次检查
                    done

                    # 提交作业
                    echo "提交作业：${{k}}.bsub"
                    bsub < "${{k}}.bsub"
                    sleep 30  # 每次提交后暂停30秒，显存只要没占满，应该不会影响速度
                done
                
                # 返回原始目录
                cd - > /dev/null
            else
                echo "未找到文件夹：$system_folder/anneal/{SAcontrol}"
            fi
        done
    done
    echo "脚本已成功执行完毕。所有作业提交完成。"
else
    echo "当前运行的作业数已达或超过40个，不再提交新作业。"
fi

echo "脚本结束。"

''')

def write_create_core(fname, SAcontrol, jname):
    with open(fname, 'w') as f:
        f.write(f'''
#!/bin/bash
core_count=0
# 遍历 i 的范围
for i in {{1..20}}; do
    pattern="{jname}_${{i}}-aacg*"
    for system_folder in $pattern/ ; do
        if [ -d "$system_folder/anneal/{SAcontrol}" ]; then
            cd "$system_folder/anneal/{SAcontrol}"
            system_name="${{system_folder%%-aacg*}}"

            for k in {{1..20}}; do
                if [ -d "${{k}}" ]; then
                    cd "${{k}}"
                    
                    # 检查是否存在 run.gro 文件和任何 core.* 文件
                    if [ ! -f "run.gro" ] && ! ls core.* 1> /dev/null 2>&1; then
                        # 如果两种文件都不存在，创建一个名为 core.1 的新文件
                        touch core.1
                        # 输出哪个文件夹执行了操作
                        echo "在 ${{system_name}}/${{k}} 目录下创建了 core.1 文件"
                    fi

                    # 如果目录中存在任何 core.* 文件，增加计数
                    if ls core.* 1> /dev/null 2>&1; then
                        core_count=$((core_count + 1))
                    fi
                    
                    cd ..
                fi
            done
            cd ../../..
        fi
    done
done

echo "含有 core.* 文件的目录总数: $core_count"

''')

def write_check_job(fname, SAcontrol, jname):
    with open(fname, 'w') as f:
        f.write(f'''
#!/bin/bash

# 设置最大作业数限制
MAX_JOBS=45

# 遍历 i 的范围
for i in {{1..20}}; do
    pattern="{jname}_${{i}}-aacg*"
    for system_folder in $pattern/ ; do
        if [ -d "$system_folder/anneal/{SAcontrol}" ]; then
            cd "$system_folder/anneal/{SAcontrol}"
            #这里使用的 ${{variable%%pattern}} 语法会从变量的值中删除匹配 pattern 的最长部分。在这个例子中，它会删除 -aacg 及其后面的所有内容，从而留下 2prg-BRL-to-2g0g_1。
            system_name="${{system_folder%%-aacg*}}"

            for k in {{1..20}}; do
                if [ -d "${{k}}" ]; then
                    cd "${{k}}"
                    #1> /dev/null: 这部分将 ls 命令的标准输出（成功的输出）重定向到 /dev/null，一个特殊的设备，会丢弃掉所有写入其中的数据。这意味着即使 ls 命令找到了匹配的文件，其输出也不会显示在终端上。
                    #2>&1: 这部分将标准错误（即错误消息）重定向到标准输出，这在此处已经被重定向到了 /dev/null。因此，无论是正常的输出还是错误消息，都不会显示在终端上。                   
                    if ls core.* 1> /dev/null 2>&1; then
                        if ls run.cpt 1> /dev/null 2>&1; then
                            # 同时找到 core.* 和 run.cpt
                            echo "找到.core和run.cpt文件在: $(pwd)"
                        else
                            # 只找到 core.*
                            echo "找到.core文件在: $(pwd)"
                        fi

                        # 创建 continue.bsub 文件并写入内容
                        cat > continue.bsub <<EOF
#!/bin/bash
#BSUB -q gpu
#BSUB -o $system_name-$k.out
#BSUB -e $system_name-$k.err
#BSUB -J $system_name-$k-continue
EOF

#在 EOF 前加上引号，比如 <<'EOF'，这会告诉 shell 将 Heredoc 内的内容视为纯文本
cat >> continue.bsub <<'EOF'
#BSUB -n 8
#BSUB -R "span[ptile=8]"
##BSUB -m g004

#export CUDA_VISIBLE_DEVICES=3
#INPUT_NAME=combined
# choose CUDA (0,1,2,3)# 
#export CUDA_VISIBLE_DEVICES=1,2，

#--- LSF ---
echo job runs at the following node:
echo $LSB_HOSTS 
NP=$(echo $LSB_HOSTS | awk '{{print NF}}')
NNODE=$(echo $LSB_HOSTS | sed -e "s/ /\\n/g" | uniq - | wc -l)
echo ""
echo Number of processor: $NP

NP2=$((NP%8))

if [ $NP2 -ne 0 ]; then
  echo NP only can be 8, 16, 24 or 32
  exit
fi

echo 0 > gpu-info-1
for lineNum in {{1..3}}
do
  echo $lineNum >> gpu-info-1
done
/usr/bin/nvidia-smi | awk '/Default/{{print $(NF-2)}}' | sed 's/\%//' > gpu-info-2

paste gpu-info-1 gpu-info-2 > gpu-info
awk '$2==0{{print $1}}' gpu-info > free-card

ncard=$((NP/4))
export CUDA_VISIBLE_DEVICES="$(cat free-card | awk 'NR<ncard{{printf"%s,",$1}};NR==ncard{{printf"%s\\n",$1}}' ncard=$ncard)"
echo $CUDA_VISIBLE_DEVICES

rm -rf gpu-info* free-card

# Environment for gromacs
#module add gromacs/2019.6
source /export/home/ldx022/software/GROMACS/gmx2022.6-GPU/bin/GMXRC

ulimit -s unlimited

#if [ $NGPU -eq 1 ]; then

#https://www.hpc.dtu.dk/?page_id=3106
# set NGPUS to the number of GPUs requested in the job
NGPUS=1
# set OMPTHREADS to the number of OpenMP threads desired
OMPTHREADS=8
export OMP_NUM_THREADS=$OMPTHREADS # like this it works
#Remove "-gpu_id 0 -nb gpu  -pme gpu -bonded gpu -update gpu" add "-v" option to debug
gmx mdrun -v -deffnm run -cpi run.cpt -cpt 5 -ntmpi $NGPUS -ntomp $OMPTHREADS  -gpu_id 0  -update gpu -nb gpu  -pme gpu -bonded gpu 

echo $(date)
EOF
                        # 检查当前作业数并在必要时等待
                        while true; do
                            current_jobs=$(bjobs -w | grep -c .)
                            if [ "$current_jobs" -lt "$MAX_JOBS" ]; then
                                # 提交作业
                                bsub < continue.bsub
                                echo "作业已提交。当前作业数：$current_jobs"
                                break
                            else
                                echo "等待提交作业。当前作业数：$current_jobs"
                                sleep 10  # 等待30秒
                            fi
                        done

                        # 删除 core.* 文件
                        rm core.*

                        # 等待30秒以间隔提交作业
                        sleep 30
                    fi
                    cd ..
                fi
            done
            cd ../../..
        else
            echo "目录 ${{system_folder}}/anneal/{SAcontrol} 不存在"
        fi
    done
done

''')



def write_merge_whole(fname, SAcontrol, jname, time_per_round):
    with open(fname, 'w') as f:
        f.write(f'''
#!/bin/bash

source /export/home/ldx022/software/miniconda3/etc/profile.d/conda.sh
conda activate spyrmsdkit

<<COMMENT
    使用while IFS= read -r line循环读取../first.inp文件的每一行。
    使用start_reading变量来标记是否开始读取模板ID之后的内容。
    当start_reading为true，并且当前行不包含'/'时，将行内的每个元素（默认以空格为分隔符）与'2', '3', '4'比较。
    如果数字匹配，将其索引添加到aa_ua_residues数组中。
    最后，打印出所有匹配项的索引。
    将所有匹配项的索引用空格隔开，赋予一个新变量UA_AA_index
    balsh
COMMENT

BASE_DIRECTORY=$(pwd)
matched_folder=""

# 寻找符合条件的文件夹
for folder in "$BASE_DIRECTORY"/*; do
    if [[ -d $folder && $folder == *"_0-aacg-"* ]]; then
        matched_folder=$folder
        break # 找到第一个匹配的文件夹后退出循环
    fi
done

# 检查是否找到了匹配的文件夹
if [[ -n $matched_folder ]]; then
    # 初始化数组
    aa_ua_residues=()
    index=0
    start_reading=false

    # 读取文件并处理
    while IFS= read -r line || [[ -n "$line" ]]; do
        if [[ "$line" == *"template_id"* ]]; then
            start_reading=true
            continue
        fi

        if $start_reading; then
            if [[ "$line" == *"/"* ]]; then
                break
            fi

            # 分割行为数字，并迭代处理
            for number in $line; do
                ((index++))
                #if [[ "$number" == "2" || "$number" == "3" || "$number" == "4" ]]; then
                if [[ "$number" == "2" || "$number" == "3" ]]; then
                    aa_ua_residues+=($index)
                fi
            done
        fi
    done < "$matched_folder/first.inp"

    # 将匹配项的索引用空格隔开
    UA_AA_index=$(IFS=' '; echo "${{aa_ua_residues[*]}}")

    # 打印结果
    echo -e "\\nAA UA Residues Indexes:"
    echo $UA_AA_index
else
    echo "No folder matches the specified pattern."
fi

for i in {{1..20}}; do
    pattern="${{BASE_DIRECTORY}}/{jname}_${{i}}-aacg*"
    for system_folder in $pattern; do
        if [ -d "$system_folder" ]; then
            (
                echo "进入文件夹: $pattern"
                cd "$system_folder/workdir" || exit

                # 运行gmx make_ndx命令并提供输入
                printf "del 7-10\\nr $UA_AA_index\\nname 7 pocket\\nquit\\n" | gmx make_ndx -f cg.gro -n index.ndx 

                # 回到基础目录，为下一次迭代做准备
                cd "$BASE_DIRECTORY" || exit
            )&
        else
            echo "文件夹 $pattern 不存在"
        fi
    done
done

wait # 等待所有后台进程完成

base_directory=$(pwd)
sub_directory=anneal/{SAcontrol}/total
sub_directory_system=$(echo "$sub_directory" | awk -F'/' '{{print $2}}')
# 创建或清空特定的汇总文件
total_rmsd2ref_file="${{sub_directory_system}}-total-rmsd2ref.txt"
> "$total_rmsd2ref_file"
total_rmsd2ref_spyrmsd_file="${{sub_directory_system}}-total-rmsd2ref-spyrmsd.txt"
> "$total_rmsd2ref_spyrmsd_file"

# 创建一个空数组来存储后台进程的 PID
pids=()

# 遍历当前目录下符合特定格式的文件夹
for i in {{1..20}}; do
    pattern="{jname}_${{i}}-aacg*"
    for system_folder in $pattern/ ; do
    # 检查文件夹是否存在
        if [ -d "$system_folder" ]; then
            (
            echo "进入文件夹: $system_folder"
            cd "$system_folder/anneal/{SAcontrol}/total"

            # 遍历1到20的k值
            for k in {{1..20}}; do
                # 计算$t0的值，注意，25表示每条轨迹的轮数！！！！！！！
                t0=$(({time_per_round} * (25 * (k - 1) + 1)))

                # 执行gmx trjconv命令
                #注意 这些都是去掉初始结构的！！！！都是从第一轮退火的结构开始！！！
                echo "正在处理: $k"
                gmx trjconv -f "../${{k}}/run.xtc" -b {time_per_round} -t0 $t0 -timestep {time_per_round} -o "${{k}}_changed_inital_time.xtc" 
            done

            # 执行处理轨迹的周期性
            sh 9.deal-pbc-new.sh
            
            # 执行gmx trjcat命令
            echo "正在合并轨迹文件..."
            gmx trjcat -f $(for k in {{1..20}}; do echo -n "run-whole-nojump-center-per-{time_per_round}ps-${{k}}.xtc "; done) -o run.xtc -cat yes

            #分析轨迹
            python 11-1.rmsd2ref-ipq.py
            )&
            #获取后台进程的 PID 并存储
            pids+=($!)


            # 返回上一级目录，在子 shell (()) 中执行 cd 是个好做法，因为它只会影响该子 shell，而不会改变主脚本的当前工作目录。这意味着您不需要在脚本的末尾切换回原来的目录。
            #cd ../../../..
        else
            echo "文件夹不存在: $system_folder"
        fi
    done
done

# 等待所有后台 Python 脚本完成
for pid in "${{pids[@]}}"; do
    wait $pid
done

# 执行文件追加操作
for folder in "$base_directory"/*; do
    if [[ -d "$folder" && "$folder" != *"_0-aacg-"* && "$folder" == *"-aacg-"* ]]; then
        target_subfolder="$folder/$sub_directory"

        if [[ -d "$target_subfolder" ]]; then
            # 提取体系编号
            system_number=$(echo "$folder" | grep -oP '(?<=_)\d+(?=-aacg-)')

            # 将LIGnoH_analysis*文件的内容追加到特定的汇总文件
            for file in "$target_subfolder"/LIGnoH_analysis_2ref.txt; do
                if [[ -f "$file" ]]; then
                    echo "体系 $system_number:" >> "$total_rmsd2ref_file"
                    cat "$file" >> "$total_rmsd2ref_file"
                    echo -e "\\n" >> "$total_rmsd2ref_file" # 在每个体系间添加空行
                fi
            done
        fi

        if [[ -d "$target_subfolder" ]]; then
            # 提取体系编号
            system_number=$(echo "$folder" | grep -oP '(?<=_)\d+(?=-aacg-)')

            # 将LIGnoH_spyrmsd_analysis*文件的内容追加到特定的汇总文件
            for file in "$target_subfolder"/LIGnoH_spyrmsd_analysis_2ref.txt; do
                if [[ -f "$file" ]]; then
                    echo "体系 $system_number:" >> "$total_rmsd2ref_spyrmsd_file"
                    cat "$file" >> "$total_rmsd2ref_spyrmsd_file"
                    echo -e "\\n" >> "$total_rmsd2ref_spyrmsd_file" # 在每个体系间添加空行
                fi
            done
        fi
    fi
done

echo "所有的target文件夹执行完毕。"
        ''')


def write_restrain_secondary(hh, jname, SAcontrol):#没有用上config里面的内容就不用加个config子项了
    hh.write(f'''
import os
import sys
import subprocess

# 定义解析函数
def parse_dssp(file_name):
    dssp_G_I_residues = []
    with open(file_name, 'r') as file:
        start_reading = False
        for line in file:
            if start_reading:
                parts = line.split()
                if len(parts) > 3 and parts[3] in ['G', 'I']:
                    structure_name = '3/10 helix' if parts[3] == 'G' else 'pi helix'
                    dssp_G_I_residues.append((int(parts[0]), parts[2], f"{{parts[3]}}-{{structure_name}}"))
            if line.startswith("  #  RESIDUE"):
                start_reading = True
    return dssp_G_I_residues

def parse_stride(file_name):
    stride_residues = []
    with open(file_name, 'r') as file:
        start_reading = False
        for line in file:
            if start_reading:
                if line.strip() and not line.startswith("REM"):
                    parts = line.split()
                    if len(parts) >= 7 and parts[5] in ['E', 'B', 'H', 'G', 'I']:
                        structure_name = parts[6]
                        residue_number = int(parts[3])
                        residue_name = parts[1]
                        stride_residues.append((residue_number, residue_name, f"{{parts[5]}}-{{structure_name}}"))
            if line.startswith("REM  |---Residue---|"):
                start_reading = True
    return stride_residues

def merge_residues(dssp_residues, stride_residues):
    merged_residues = set()
    # 将DSSP和STRIDE数据添加到集合中，自动去重
    for residue in dssp_residues:
        merged_residues.add(residue[0])  # 只取残基号

    for residue in stride_residues:
        merged_residues.add(residue[0])  # 只取残基号

    return merged_residues

# 进入特定文件夹并执行命令
base_path = "../"
system_path = "../{jname}"
os.chdir(system_path)
base_directory = os.getcwd()
for folder in os.listdir(base_directory):
    target_folder = os.path.join(base_directory, folder)
    if os.path.isdir(target_folder) and "-aacg-" in folder and "_0-aacg-" in folder:
        os.chdir(os.path.join(target_folder, "protein-lig-prep"))
        ref_0_path = os.getcwd()
        os.system("stride {jname}_0.pdb > {jname}_0.stride")
        os.system("dssp -i {jname}_0.pdb -o {jname}_0.dssp")

        # 解析文件并获取合并的残基
        dssp_G_I_residues = parse_dssp("{jname}_0.dssp")
        stride_residues = parse_stride("{jname}_0.stride")
        merged_residues = merge_residues(dssp_G_I_residues, stride_residues)

        # 打印结果
        print("DSSP G/I Residues:")
        print(dssp_G_I_residues)
        print("\\nSTRIDE E/B/H/G/I Residues:")
        print(stride_residues)
        print("\\nMerged Residues:")
        print(merged_residues)

        # 读取 ../first.inp 文件
        aa_ua_residues = []
        with open("../first.inp", "r") as file:
            start_reading = False
            template_id_content = ""

            for line in file:
                if "template_id" in line:
                    start_reading = True
                    continue

                if start_reading:
                    if '/' in line:
                        break
                    template_id_content += line.strip() + " "

            template_id_numbers = template_id_content.split()
            for i, number in enumerate(template_id_numbers, start=1):
                if number in ['2', '3', '4']:
                    aa_ua_residues.append(i)

        print("\\nAA UA Residues Indexes:")
        print(aa_ua_residues)

        # 计算交集
        helix_etc_residues = set(merged_residues).intersection(aa_ua_residues)
        print("\\nHelix and Other Residues:")
        print(helix_etc_residues)

        # 切换目录并执行另一个脚本
        os.chdir("../prot-workdir")
        os.system("python3 ../../../01_Workflow/utilities/0-1.restore_UA_atomname.py > 0-1.restore_UA_atomname.log")
        residue_numbers = " ".join(map(str, sorted(helix_etc_residues)))
        # 在当前目录下执行 gmx make_ndx 命令
        process = subprocess.Popen("gmx make_ndx -f 2-1-1.cg_ua2aaname.gro -o temp_index.ndx", stdin=subprocess.PIPE, shell=True, executable='/bin/bash')
        process.communicate(input=f"del 5-20\\nr {{residue_numbers}} & a CA C N O\\nquit\\n".encode())
        #--------------------------------------------------------------------------------------------------------------------------------------
        #注意，这里涉及到了限制那些具有二级结构的主链原子的力常数!!!,但是用的式位置限制而非二级结构限制，这里用的10000，换算成amber的单位是10000/418=23.92
        #--------------------------------------------------------------------------------------------------------------------------------------
        process1 = subprocess.Popen("gmx genrestr -f 2-1-1.cg_ua2aaname.gro -n temp_index.ndx -fc 10000 -o posre.itp", stdin=subprocess.PIPE, shell=True, executable='/bin/bash')
        process1.communicate(input=f"5\\n".encode())

        # 返回到初始目录
        os.chdir(base_directory)
        for i in range(1, 21):
            folder_pattern = f"_{{i}}-aacg-"
            for folder in os.listdir(base_directory):
                target_folder = os.path.join(base_directory, folder)
                # 检查文件夹名是否包含特定模式
                if os.path.isdir(target_folder) and folder_pattern in folder:
                    # 构造 workdir 下的 cg.top 文件的路径
                    cg_top_file_path = os.path.join(target_folder, "workdir", "cg.top")
                    print(cg_top_file_path)

                    if os.path.exists(cg_top_file_path):
                        with open(cg_top_file_path, 'r') as file:
                            lines = file.readlines()

                        with open(cg_top_file_path, 'w') as file:
                            for line in lines:
                                file.write(line)  # 首先写入当前行
                                # 检查当前行是否是目标行
                                if '#include "topol_CM1.itp"' in line:
                                    # 在找到的行之后写入额外的内容
                                    file.write("; Include Position restraint file\\n")
                                    file.write("#ifdef POSRES\\n")
                                    file.write(f'#include "{{ref_0_path}}/../prot-workdir/posre.itp"\\n')
                                    file.write("#endif\\n")

        print("Modification completed.")

''')

def write_ie(fname, SAcontrol, jname):
    with open(fname, 'w') as f:
        f.write(f'''
#!/bin/bash

BASE_DIRECTORY=$(pwd)

for i in {{1..20}}; do
    pattern="${{BASE_DIRECTORY}}/{jname}_${{i}}-aacg*"
    for system_folder in $pattern; do
        if [ -d "$system_folder" ]; then
            (
                echo "进入文件夹: $pattern"
                cd "$system_folder/workdir" || exit

                # 运行gmx make_ndx命令并提供输入
                #printf "del 7-10\\nr $UA_AA_index\\nname 7 pocket\\nquit\\n" | gmx make_ndx -f cg.gro -n index.ndx 

                cd "../anneal/{SAcontrol}/total" || exit

                # gmx grompp命令
                #gmx grompp -f ../extract-ie.mdp -c ../${{i}}/run.gro -p ../../../workdir/cg.top -n ../../../workdir/index.ndx -o ie.tpr -r ../${{i}}/run.gro -maxwarn 2
                gmx grompp -f ../../../../../anneal-script/{SAcontrol}/extract-ie.mdp -c ../${{i}}/run.gro -p ../../../workdir/cg.top -n ../../../workdir/index.ndx -o ie.tpr -r ../${{i}}/run.gro -maxwarn 2

                # gmx mdrun命令,rerun只是对每一帧计算能量,所以可以直接把热浴、压浴、退火等给去掉！
                gmx mdrun -deffnm ie -rerun run.xtc -nb cpu -ntmpi 1

                # gmx energy命令
                echo -e "18\\n19\\n" | gmx energy -f ie.edr -o ie.xvg

                # 回到基础目录，为下一次迭代做准备
                cd "$BASE_DIRECTORY" || exit
            )&
        else
            echo "文件夹 $pattern 不存在"
        fi
    done
done

wait # 等待所有后台进程完成
        ''')


def write_merge_total_ie_rmsd(fname, SAcontrol, jname):
    with open(fname, 'w') as f:
        f.write(f'''
#!/bin/bash
<<COMMENT
整合所有的rmsd文件：
for i in {{1..20}}; do tail -n +2 /export/home/ldx022/tmp-flexopt/own/000-222-anneal-19ipq-modified-cg-flow-25rounds*20-1.11/1eet-BFU-to-2b5j/1eet-BFU-to-2b5j_${{i}}-aacg-25k-12cutoff-fullWT4-newxcg/anneal/600K_heat-1.0-cool-2.0-2fs/total/LIG_noH_spyrmsd_2ref.csv; done > /export/home/ldx022/tmp-flexopt/own/000-222-anneal-19ipq-modified-cg-flow-25rounds*20-1.11/1eet-BFU-to-2b5j/total-rmsd.txt
以上这个命令是提取了1w帧。

如果要后5000帧，每个取后250个结构
for i in {{1..20}}; do tail -n +252 /export/home/ldx022/tmp-flexopt/own/000-222-anneal-19ipq-modified-cg-flow-25rounds*20-1.11/2prg-BRL-to-2g0g/2prg-BRL-to-2g0g_${{i}}-aacg-25k-12cutoff-fullWT4-newxcg/anneal/600K_heat-1.0-cool-2.0-2fs/total/LIG_noH_spyrmsd_2ref.csv; done > /export/home/ldx022/tmp-flexopt/own/000-222-anneal-19ipq-modified-cg-flow-25rounds*20-1.11/2prg-BRL-to-2g0g/total-rmsd.txt

要第2行到第251行的内容，也就是第1个结构到第250个结构
for i in {{1..21}}; do sed -n '2,251p' /export/home/ldx022/tmp-flexopt/own/000-222-anneal-19ipq-modified-cg-flow-25rounds*20-1.11/2prg-BRL-to-2g0g/2prg-BRL-to-2g0g_${{i}}-aacg-25k-12cutoff-fullWT4-newxcg/anneal/600K_heat-1.0-cool-2.0-2fs/total/LIGnoH_spyrmsd_analysis_2ref.txt; done > /export/home/ldx022/tmp-flexopt/own/000-222-anneal-19ipq-modified-cg-flow-25rounds*20-1.11/2prg-BRL-to-2g0g/total-rmsd.txt
#这个命令使用 sed -n '2,251p' 来选择每个文件的第2行到第251行并打印这些行。-n 选项与 p 命令一起使用，意味着只有被指定的行范围会被打印出来。然后，这个命令循环遍历所有指定的文件，并将选定的行范围的内容追加到 total-rmsd.txt 文件中。
    balsh
COMMENT


BASE_DIRECTORY=$(pwd)
for i in {{1..20}}; do
  tail -n +2 "$BASE_DIRECTORY/{jname}_${{i}}-aacg-25k-12cutoff-fullWT4-newxcg/anneal/{SAcontrol}/total/LIG_noH_spyrmsd_2ref.csv"
done > "$BASE_DIRECTORY/total-rmsd.txt"

for i in {{1..20}}; do
  tail -n +26 "$BASE_DIRECTORY/{jname}_${{i}}-aacg-25k-12cutoff-fullWT4-newxcg/anneal/{SAcontrol}/total/ie.xvg" | sed 's/^[ \t]*//'
done > "$BASE_DIRECTORY/total-ie.txt"




        ''')

def write_merge_ie_rmsd2csv(fname):
    with open(fname, 'w') as f:
        f.write(f'''
"""
请你帮我写一个python3的脚本，将total-ie.txt和total-rmsd.txt两个文件进行合并，合并为merge_ie_rmsd.csv文件。具体来说，total-ie.txt中每列以"  "隔开，比如其中一行的格式为"1150.000000  -154.532242  -181.635300"，而total-rmsd.txt文件每列以","进行隔开，对于merge_ie_rmsd.csv这个文件而言，第一列为行号，total-ie.txt的第一列作为merge_ie_rmsd.csv第二列（需将浮点数转化成整数，也就是1150.000000转化成1150），total-rmsd.txt的第2列作为merge_ie_rmsd.csv第三列，total-ie.txt的第二列和第三列分别作为merge_ie_rmsd.csv第四列和第五列，然后merge_ie_rmsd.csv的第六列则为merge_ie_rmsd.csv的第4列和第5列的加和。最后merge_ie_rmsd.csv的每一列之间用","进行隔开
"""

# 导入必要的库
import csv

# 读取 total-ie.txt 文件
with open('total-ie.txt', 'r') as file_ie:
    data_ie = file_ie.readlines()

# 读取 total-rmsd.txt 文件
with open('total-rmsd.txt', 'r') as file_rmsd:
    data_rmsd = file_rmsd.readlines()

# 准备写入CSV文件
with open('merge_ie_rmsd.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # 遍历文件中的数据行
    for i, (line_ie, line_rmsd) in enumerate(zip(data_ie, data_rmsd), start=1):
        # 处理 total-ie.txt 中的数据
        parts_ie = line_ie.strip().split("  ")  # 假设每列之间用两个空格分隔
        parts_ie = [part for part in parts_ie if part]  # 移除空字符串
        parts_ie[0] = int(float(parts_ie[0]))  # 将第一列的浮点数转换为整数
        
        # 处理 total-rmsd.txt 中的数据
        parts_rmsd = line_rmsd.strip().split(",")
        
        # 合并数据，计算第六列
        total = float(parts_ie[1]) + float(parts_ie[2])
        
        # 将数据写入CSV文件
        writer.writerow([i] + [parts_ie[0]] + [parts_rmsd[1]] + parts_ie[1:] + [total])

# 提示完成
print('合并文件创建成功')





        ''')
