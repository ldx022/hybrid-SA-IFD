'''
请你帮我写一个脚本1.py，解析当前目录下2prg-BRL-to-2g0g_0.dssp文件和2prg-BRL-to-2g0g_0.stride文件，从中提取出具有特定二级结构的残基，具体而言：
1、dssp文件以“  #  RESIDUE AA STRUCTURE BP1 BP2  ACC     N-H-->O    O-->H-N    N-H-->O    O-->H-N    TCO  KAPPA ALPHA  PHI   PSI    X-CA   Y-CA   Z-CA
”该标题行作为起始行，往下则是残基对应的二级结构的信息，具体而言，第一列和第二列表示残基序号（从1开始编号），第三列表示氨基酸名称（用单字母表示），第四列则是表示该氨基酸对应的二级结构情况，具体有以下几种类型：'H'表示alpha helix，'B'表示reside in  isolated beta-bridge,'E'表示extended strand，'G'表示3/10 helix，'I'表示pi helix，'T'表示hydrogen bonded turn，'S'表示bend，以及啥都没有，也就是'blank'表示loop or irregular。请你帮我把形成二级结构'G'和'I'的残基提取出来，提成一个元组的形式，元组中的元素分别是({第1列}，{第3列}，{{第4列}-与之对应的类型名称})，举个例子，如果说匹配到了这一行：  154  154   F  G X4 S+     0   0   11     -3,-1.2     3,-1.1     1,-0.2     4,-0.4   0.657  98.4  69.9 -70.3 -22.8   48.5  -39.3   30.6
则产生一个元组的该元素为(154,F,G-3/10 helix)，最后赋值给dssp_G_I_residue
2、stride文件以“REM  |---Residue---|    |--Structure--|   |-Phi-|   |-Psi-|  |-Area-|      ~~~~”该标题行作为起始行，往下则是残基对应的二级结构的信息，具体而言，第二列表示残基名称（用三字母表示），第4列表示残基序号（从1开始编号），第6列表示该氨基酸对应的二级结构情况（简写），第7列则是该二级情况的具体写法。具体有以下几种类型：'T'，表示Turn,'E'表示strand,'B'表示isolated_bridge,'H'表示的是alpha helix，'G'表示3/10 helix，'I'表示pi helix，'C'表示coil。请你帮我把形成二级结构'E','B','H','G','I'的残基提取出来，提成一个元组的形式，元组中的元素分别是({第四列}，{第二列}，{{第6列}-{第7列}})，举个例子，如果说匹配到了这一行：ASG  VAL -  109  109    H    AlphaHelix    -61.45    -42.68      65.3      ~~~~
则产生一个元组的该元素为(109,VAL,H-AlphaHelix)，最后赋值给dssp_G_I_residue
该脚本运行的命令是python3 1.py 2prg-BRL-to-2g0g_0脚本

之后再根据残基号把这两部分取一个并集！
最后生成的merged_residues 是一个集合（set），而不是列表（list）或元组（tuple）。集合是一个不包含重复元素的无序集，这在这种情况下是非常有用的，因为它自动去除了任何重复的残基号。
如果您需要将最终的结果转换为列表或元组，这可以很容易地实现。例如，如果您想要一个列表，可以在返回之前将集合转换为列表：
return list(merged_residues)
如果您希望结果是一个元组，可以这样做：
return tuple(merged_residues)
'''

# 导入所需的库
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