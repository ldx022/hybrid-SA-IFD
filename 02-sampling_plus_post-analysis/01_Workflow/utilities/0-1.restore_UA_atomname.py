#请你帮我写一个0.restore_UA_atomname.py脚本，实现读取cg.gro文件，对XUA残基中的原子名$ua_name进行更改的目的：提取残基名为XUA的残基中的所有原子序号$atom_uaid，根据该原子序号$atom_uaid找到cg.rst7文件(标准的amber文件)中对应的该原子的xyz坐标{cg_xyz}，将该xyz坐标去匹配../protein-lig-prep/system_solv.inpcrd文件(标准的amber inpcrd文件格式)中相同的xyz坐标{aa_xyz}，提取对应的原子序号$atom_aaid，再根据该原子序号$atom_aaid到../protein-lig-prep/system_solv.pdb文件中找到对应的原子名$aa_name，替换掉cg.gro对应的$ua_name，保存为新文件：cg_ua2aaname.gro。
#注意，rst7格式文件和system_solv.inpcrd格式一样，都是从第3行开始，每一行有6个数字，每三个是一组xyz坐标，也就是对应1个原子的坐标，比如第三行就写明了1号原子和2号原子的坐标，对应pdb文件中的相应的原子序号
#目前脚本的部分内容是：
import re


def read_gro_file(gro_file):
    with open(gro_file, 'r') as file:
        lines = file.readlines()
    return lines

def extract_xua_atoms(gro_lines):
    xua_atoms = {}
    for line in gro_lines:
        if 'XUA' in line:
            atom_id = int(line[16:20].strip())  #(line[:5].strip()表示行的前5个，但是在gro文件中那个是residue number，但是https://manual.gromacs.org/archive/5.0.3/online/gro.html中写道gro文件的atom number应该是16-20
            atom_name = line[10:15].strip()
            xua_atoms[atom_id] = atom_name
    return xua_atoms

def read_rst7_file(rst7_file):
    with open(rst7_file, 'r') as file:
        lines = file.readlines()[2:]  # Skipping first two lines
    return lines

# 新函数：从 RST7 文件中提取原子坐标
def extract_coordinates(rst7_lines):
    coords = {}
    atom_id = 1
    for line in rst7_lines:
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        for i in range(0, len(numbers), 3):
            coords[atom_id] = (float(numbers[i]), float(numbers[i+1]), float(numbers[i+2]))
            atom_id += 1
    return coords

# 新函数：在 INPCRD 文件中查找相同坐标的原子 ID
#已知rst7和inpcrd文件的内容形如以下格式：
#[x1,y1,z1,x2,y2,z2
#x3,y3,z3,x4,y4,z4
#x5,y5,z5,x6,y6,z6
#...]
#其中1，2，3，4...对应atom_id，x1,y1,z1表示1号原子的xyz坐标，不一定用逗号隔开。
#我想做的是，根据{atom_id}来定位到cg.rst7文件中该原子的xyz坐标，再根据这个xyz数值去找system_solv.inpcrd相同的xyz坐标数值，反推出该原子在system_solv.inpcrd文件中的id号 

def find_atom_id_in_inpcrd(inpcrd_file, target_coords):
    with open(inpcrd_file, 'r') as file:
        lines = file.readlines()
    
    atom_id = 0  # 初始化为 0
    for line in lines:
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", line)
        for i in range(0, len(numbers), 3):
            # 确保列表中有足够的元素来形成一个坐标
            if i + 2 < len(numbers):
                coords = (float(numbers[i]), float(numbers[i+1]), float(numbers[i+2]))
                if coords == target_coords:
                    return atom_id
            atom_id += 1  # 每次循环迭代末尾递增 atom_id
    return None

#---------------------------------------------------------------------------------------------

def read_pdb_file(pdb_file):
    with open(pdb_file, 'r') as file:
        lines = file.readlines()
    return lines

def find_aa_name_in_pdb(pdb_lines, inpcrd_atom_id):
    for line in pdb_lines:
        if line.startswith('ATOM') or line.startswith('HETATM'):
            current_atom_id = int(line[6:11].strip())
            if current_atom_id == inpcrd_atom_id:
                return line[12:16].strip()  # 返回原子名称
    return None

def replace_atom_name_in_gro(gro_lines, atom_id, aa_name):
    new_gro_lines = []
    for line in gro_lines:
        try:
            line_atom_id = int(line[15:20].strip())
        except ValueError:
            # Skip lines that do not represent atom entries
            new_gro_lines.append(line)
            continue

        if line_atom_id == atom_id:
            # 保持行的其它部分不变，仅替换原子名称部分，在原子名称的格式化中使用了 : >3，这意味着原子名称将右对齐，并且总共占用3个字符的空间。这应该确保新名称正确地填充到原来的位置。
            #    line[:10] 获取当前行的前10个字符。在 GRO 文件的每一行中，前10个字符通常包含分子类型或序号等信息，这部分在替换原子名称时需要保留。
            #line[15:] 获取从第16个字符开始到行尾的所有字符。这部分通常包含原子的坐标信息，同样需要在替换时保留。
            #f"{new_name:<5}" 使用了格式化字符串（f-string），其中 new_name 是要插入的新原子名称。
            #<5 指定了一个字段宽度为5个字符，确保新原子名称占据与原有原子名称相同的空间。如果 new_name 短于5个字符，它将使用空格在右侧填充至5个字符的宽度，保证文件格式的一致性。
            line = line[:10] + f"{aa_name: >5}" + line[15:]
        new_gro_lines.append(line)
    return new_gro_lines

def write_gro_file(gro_lines, output_file):
    with open(output_file, 'w') as file:
        file.writelines(gro_lines)


gro_file = 'cg.gro'
rst7_file = 'cg.rst7'
inpcrd_file = '../protein-lig-prep/prot.inpcrd'
pdb_file = '../protein-lig-prep/prot.pdb'

# 主程序流程
gro_lines = read_gro_file(gro_file)
xua_atoms = extract_xua_atoms(gro_lines)  # 获取 XUA 原子的 atom_id
rst7_lines = read_rst7_file(rst7_file)
rst7_coords = extract_coordinates(rst7_lines)

# 查找 XUA 原子在 INPCRD 文件中的 ID
for atom_id in xua_atoms:
    target_coords = rst7_coords.get(atom_id)
    if target_coords:
        inpcrd_atom_id = find_atom_id_in_inpcrd(inpcrd_file, target_coords)
        if inpcrd_atom_id:
            print(f"XUA 原子 {atom_id} 在 INPCRD 文件中的 ID 为: {inpcrd_atom_id}")
        else:
            print(f"未在 INPCRD 文件中找到与原子 {atom_id} 相同坐标的原子")

pdb_lines = read_pdb_file(pdb_file)
new_gro_lines = gro_lines.copy()

# 对于每个 XUA 原子，找到对应的原子名称并替换
for atom_id, xua_atom_name in xua_atoms.items():
    target_coords = rst7_coords.get(atom_id)
    if target_coords:
        inpcrd_atom_id = find_atom_id_in_inpcrd(inpcrd_file, target_coords)
        if inpcrd_atom_id:
            aa_name = find_aa_name_in_pdb(pdb_lines, inpcrd_atom_id)
            print(aa_name)
            if aa_name:
                new_gro_lines = replace_atom_name_in_gro(new_gro_lines, atom_id, aa_name)

write_gro_file(new_gro_lines, '2-1-1.cg_ua2aaname.gro')