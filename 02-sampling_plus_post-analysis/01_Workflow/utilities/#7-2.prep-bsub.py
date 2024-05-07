import os

def modify_gro_bsub_file(file_path, new_job_name):
    """ 修改 gro.bsub 文件，替换特定行中的内容 """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            if line.strip().startswith('#BSUB -J'):
                line = f'#BSUB -J {new_job_name}\n'
            file.write(line)

def main():
    # 获取基本目录
    base_directory = input("请输入aacg-prep.py创建的文件夹所在的基目录: ")

    # 遍历基本目录中的目标文件夹
    for folder in os.listdir(base_directory):
        target_folder = os.path.join(base_directory, folder, "anneal")
        if os.path.isdir(target_folder) and "-aacg-" in folder and not "_0-aacg-" in folder:
            gro_bsub_path = os.path.join(target_folder, "gro.bsub")

            # 检查 gro.bsub 文件是否存在
            if os.path.isfile(gro_bsub_path):
                new_job_name = folder.split('-aacg-')[0]
                modify_gro_bsub_file(gro_bsub_path, new_job_name)

if __name__ == "__main__":
    main()
