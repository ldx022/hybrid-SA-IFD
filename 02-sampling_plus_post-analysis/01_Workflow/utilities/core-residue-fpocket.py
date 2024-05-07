import sys

def classify_by_column(pdb_file):
    with open(pdb_file, 'r') as f:
        lines = f.readlines()

    atom_lines = [line for line in lines if line.startswith("ATOM")]
    header_lines = [line for line in lines if line.startswith("HEADER")]

    # 使用字典来存储每个残基的信息
    residues = {}
    for line in atom_lines:
        key = line[22:27].strip() + line[17:20].strip()
        if key not in residues:
            residues[key] = []
        residues[key].append(line)

    # 按照key进行排序输出
    sorted_residues = sorted(residues.keys(), key=lambda x: (int(x[:-3]), x[-3:]))

    # 输出结果
    for header in header_lines:
        print(header, end='')
    
    for res in sorted_residues:
        for line in residues[res]:
            print(line, end='')

    # 输出核心口袋的残基，并按照序号进行排序
    residue_names = sorted([res[:-3] + res[-3:] for res in sorted_residues], key=lambda x: int(x[:-3]))

    # 修改的部分：输出核心口袋残基的数量
    num_of_residues = len(residue_names)
    #print(f"核心口袋的残基共有{num_of_residues}个，核心口袋的残基分别是：" + "、".join(residue_names))
    print(f"核心口袋的残基共有{num_of_residues}个，核心口袋的残基分别是：" + " ".join(residue_names))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 core-residue.py <pdb_file>")
        sys.exit(1)
    classify_by_column(sys.argv[1])
