import os
import sys
import mdtraj
import re

def get_residue_count(pdb_file):
    try:
        traj = mdtraj.load(pdb_file)
        return traj.n_residues
    except Exception as e:
        print(f"Error loading PDB file: {e}")
        return 0

def create_template_file(folder, residue_count, special_residues):
    template_path = os.path.join(folder, 'first.inp')
    
    # Check if first.inp already exists
    if os.path.exists(template_path):
        print(f"'{template_path}' already exists and will be overwritten.")
    
    template_id = ['1'] * residue_count
    template_id[-1] = '4'  # Last residue is always 4

    # Update based on user input
    for residue in special_residues:
        # 使用正则表达式分离位置和残基类型
        match = re.match(r'(\d+)([A-Z]+)', residue)
        if match:
            pos = int(match.group(1)) - 1
            template_id[pos] = '3'

    # 更新编号为3的残基周围的残基编号为2
    for i, id in enumerate(template_id):
        if id == '3':
            for j in range(max(0, i-2), min(residue_count, i+3)):
                if template_id[j] not in ['3', '4']:
                    template_id[j] = '2'

    with open(template_path, 'w') as file:
        file.write('assembling\n  template_dirs {\n')
        file.write('    ../../../topo-fragments/martini\n')
        file.write('    ../../../topo-fragments/united-19ipq\n')
        file.write('    ../../../topo-fragments/ff19ipq\n')
        file.write('    ../LIG-prep\n  }\n  template_id {\n    ')
        
        # Write template_id in a formatted way
        for i in range(residue_count):
            file.write(template_id[i] + ' ')
            if (i + 1) % 25 == 0:
                file.write('\n    ')

        file.write('\n  }\n/\n\nexclusion\n/\n')

    print(f"'first.inp' created in {folder}")


def main(base_directory, special_residues_str):
    target_folder = None
    for folder in os.listdir(base_directory):
        if '_0-aacg' in folder:
            target_folder = os.path.join(base_directory, folder)
            break

    if target_folder:
        # 构造正确的 .pdb 文件名
        base_name = folder.split('_0-aacg')[0]
        pdb_file = os.path.join(target_folder, 'protein-lig-prep', f"{base_name}_0.pdb")
        residue_count = get_residue_count(pdb_file)
        print(f"Residue count: {residue_count}")

        # Splitting the single string argument into a list of residues
        #special_residues = special_residues_str.replace('、', ' ').split()
        #special_residues = special_residues_str.split()
        create_template_file(target_folder, residue_count, special_residues_str)
    else:
        print("Target folder not found.")

if __name__ == "__main__":
    base_directory = sys.argv[1]  # Replace with your actual directory path
    # Assuming the entire residue string is passed as one argument
    special_residues_str = sys.argv[2:]  # Residues from command line arguments.python的index从0开始,'sys.argv[2:]'这个不行，这样写会把字符串 'sys.argv[2:]' 赋值给 special_residues_str，而不是命令行参数的值。同时获取的 special_residues_str 已经是一个列表了，而用顿号的那个，是一整个字符串，.split() 方法通常用于字符串，用于将字符串分割成一个列表
    main(base_directory, special_residues_str)
