import mdtraj as md

#对binding pocket residues的定义式binding pocket residues are defined as those having at least one heavy atom within 5 Å of the ligand。其中ligand的残基名是LIG。mdtraj如何把binding pocket residues给print出来，最后请以"{氨基酸index}{氨基酸名字}"呈现出来，比如"4ALA 9GLU..."这种形式
#将index按照升序排列print出来
#最后输出的残基需要加1才是从1开始编号的残基

# 加载PDB文件
pdb_file = '2g0g-SP0-to-2prg_0.pdb'  # 替换为你的PDB文件路径
traj = md.load(pdb_file)

# 寻找配体（LIG）
ligand_atoms = traj.topology.select('resname LIG')

# 计算距离并识别口袋残基
binding_pocket_residues = set()
for atom in traj.topology.atoms:
    if atom.residue.name != 'LIG':
        distances = md.compute_distances(traj, ([atom.index, ligand_index] for ligand_index in ligand_atoms))
        if any(distance < 0.5 for distance in distances[0]):  # 0.5纳米 = 5埃
            binding_pocket_residues.add((atom.residue.index, atom.residue.name))

# 按照氨基酸索引升序排列并格式化打印结果
sorted_residues = sorted(binding_pocket_residues, key=lambda x: x[0])
formatted_residues = ' '.join(f'{index}{name}' for index, name in sorted_residues)
print(formatted_residues)
