'''
User
请你帮我写一个完整的restrain_secondary_structure_atom.py脚本，实现以下目的：
1、在当前文件夹目录下，进入到文件夹名中带有"_0-aacg-"的文件夹（可以使用以下代码筛选该文件夹：    
for folder in os.listdir(base_directory):
        target_folder = os.path.join(base_directory, folder)
        if os.path.isdir(target_folder) and "-aacg-" in folder and "_0-aacg-" in folder:）
再进入protein-lig-prep子文件夹，在该文件夹下面运行以下两条命令：
stride 2prg-BRL-to-2g0g_0.pdb > 2prg-BRL-to-2g0g_0.stride
dssp -i 2prg-BRL-to-2g0g_0.pdb -o 2prg-BRL-to-2g0g_0.dssp

2、不更换目录，仍然使用如下脚本，找到merged_residues：
import sys

def parse_dssp(file_name):
    dssp_G_I_residues = []
    with open(file_name, 'r') as file:
        start_reading = False
        for line in file:
            if start_reading:
                parts = line.split()
                if len(parts) > 3 and parts[3] in ['G', 'I']:
                    structure_name = '3/10 helix' if parts[3] == 'G' else 'pi helix'
                    dssp_G_I_residues.append((int(parts[0]), parts[2], f"{parts[3]}-{structure_name}"))
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
                        stride_residues.append((residue_number, residue_name, f"{parts[5]}-{structure_name}"))
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 1.py <file_prefix>")
        sys.exit(1)

    file_prefix = sys.argv[1]
    dssp_file = f"{file_prefix}.dssp"
    stride_file = f"{file_prefix}.stride"

    dssp_G_I_residue = parse_dssp(dssp_file)
    stride_residue = parse_stride(stride_file)
    merged_residues = merge_residues(dssp_G_I_residue, stride_residue)


    # 输出结果
    print("DSSP G/I Residues:")
    print(dssp_G_I_residue)
    print("\nSTRIDE E/B/H/G/I Residues:")
    print(stride_residue)
    print("Merged Residues:")
    print(merged_residues)

之后得到merged_residues这个变量，是一个集合，其中元素为残基号
3、读取../first.inp这个文件，找到  template_id用大括号{}括起来的字段，里面是一些数字，请你提取出数字2、3、4对应的索引号！（从1开始），赋值给变量aa_ua_residues，同时也print出来
4、取merged_residues这个集合和变量aa_ua_residues的元素的交集！！！！赋值给helix_etc_residues,同时也print出来
4、之后切换到../workdir/目录下，执行
python3 ../../../01_Workflow/utilities/0-1.restore_UA_atomname.py > 0-1.restore_UA_atomname.log

我的template_id 部分的内容是一个整体，每一行都是连续的，编号也是连续的！！

'''
'''
得到的Helix and Other Residues是一个集合，该集合中的残基号以逗号分隔，请你去掉逗号，改为用空格分隔，提取这些{残基号}，仍然在当前目录下(也就是workdir目录下)执行命令：gmx make_ndx -f 2-1-1.cg_ua2aaname.gro -o temp_index.ndx，依次交互式地输入
del 5-15
r {残基号} & a CA C N O
'''


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
                    dssp_G_I_residues.append((int(parts[0]), parts[2], f"{parts[3]}-{structure_name}"))
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
                        stride_residues.append((residue_number, residue_name, f"{parts[5]}-{structure_name}"))
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
base_directory = os.getcwd()
for folder in os.listdir(base_directory):
    target_folder = os.path.join(base_directory, folder)
    if os.path.isdir(target_folder) and "-aacg-" in folder and "_0-aacg-" in folder:
        os.chdir(os.path.join(target_folder, "protein-lig-prep"))
        ref_0_path = os.getcwd()
        os.system("stride 2prg-BRL-to-2g0g_0.pdb > 2prg-BRL-to-2g0g_0.stride")
        os.system("dssp -i 2prg-BRL-to-2g0g_0.pdb -o 2prg-BRL-to-2g0g_0.dssp")

        # 解析文件并获取合并的残基
        dssp_G_I_residues = parse_dssp("2prg-BRL-to-2g0g_0.dssp")
        stride_residues = parse_stride("2prg-BRL-to-2g0g_0.stride")
        merged_residues = merge_residues(dssp_G_I_residues, stride_residues)

        # 打印结果
        print("DSSP G/I Residues:")
        print(dssp_G_I_residues)
        print("\nSTRIDE E/B/H/G/I Residues:")
        print(stride_residues)
        print("\nMerged Residues:")
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

        print("\nAA UA Residues Indexes:")
        print(aa_ua_residues)

        # 计算交集
        helix_etc_residues = set(merged_residues).intersection(aa_ua_residues)
        print("\nHelix and Other Residues:")
        print(helix_etc_residues)

        # 切换目录并执行另一个脚本
        os.chdir("../workdir")
        os.system("python3 ../../../01_Workflow/utilities/0-1.restore_UA_atomname.py > 0-1.restore_UA_atomname.log")
        residue_numbers = " ".join(map(str, sorted(helix_etc_residues)))
        # 在当前目录下执行 gmx make_ndx 命令
        process = subprocess.Popen("gmx make_ndx -f 2-1-1.cg_ua2aaname.gro -o temp_index.ndx", stdin=subprocess.PIPE, shell=True, executable='/bin/bash')
        process.communicate(input=f"del 5-20\nr {residue_numbers} & a CA C N O\nquit\n".encode())
        '''
        注意，这里涉及到了限制那些具有二级结构的主链原子的力常数!!!,但是用的式位置限制而非二级结构限制，这里用的10000，换算成amber的单位是10000/418=23.92
        '''
        process1 = subprocess.Popen("gmx genrestr -f 2-1-1.cg_ua2aaname.gro -n temp_index.ndx -fc 10000 -o posre.itp", stdin=subprocess.PIPE, shell=True, executable='/bin/bash')
        process1.communicate(input=f"5\n".encode())

        # 返回到初始目录
        os.chdir(base_directory)
        for i in range(1, 2):
            folder_pattern = f"_{i}-aacg-"
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
                                if line.strip() == "[ system ]":
                                    file.write("; Include Position restraint file\n")
                                    file.write("#ifdef POSRES\n")
                                    file.write(f'#include "{ref_0_path}/../workdir/posre.itp"\n')
                                    file.write("#endif\n")
                                file.write(line)

        print("Modification completed.")
