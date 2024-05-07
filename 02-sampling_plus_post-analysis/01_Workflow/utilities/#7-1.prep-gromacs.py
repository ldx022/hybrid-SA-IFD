import os
import shutil
import subprocess

#注意这个脚本的index创建文件没有考虑离子的问题！！！！！！！！！
#这个脚本考虑了index的离子的问题

def main():
    # 获取基本目录
    base_directory = input("请输入aacg-prep.py创建的文件夹所在的基目录: ")

    # 获取需要拷贝的文件夹和文件
    directories = input("请你提供需要拷贝的1个或多个文件夹（用空格分隔）: ").split()
    files = input("请你提供需要拷贝的1个或多个文件（用空格分隔）: ").split()

    # 遍历基本目录中的目标文件夹
    for folder in os.listdir(base_directory):
        target_folder = os.path.join(base_directory, folder)
        if os.path.isdir(target_folder) and "-aacg-" in folder and not "_0-aacg-" in folder:
            anneal_path = os.path.join(target_folder, "anneal")
            workdir_path = os.path.join(target_folder, "workdir")

            # 拷贝文件夹
            for dir in directories:
                if os.path.isdir(dir):
                    shutil.copytree(dir, os.path.join(anneal_path, os.path.basename(dir)), dirs_exist_ok=True)

            # 拷贝文件
            for file in files:
                if os.path.isfile(file):
                    shutil.copy(file, anneal_path)

            # 在workdir中执行命令
            if os.path.isdir(workdir_path):
                os.chdir(workdir_path)
                subprocess.run("source /export/home/ldx022/software/GROMACS/gmx2022.6-GPU/bin/GMXRC", shell=True, executable='/bin/bash')
                process = subprocess.Popen("gmx make_ndx -f cg.gro", stdin=subprocess.PIPE, shell=True, executable='/bin/bash')
                process.communicate(input="5|6\nname 18 env\n!18\nname 19 pro-lig\nquit\n".encode())

if __name__ == "__main__":
    main()
