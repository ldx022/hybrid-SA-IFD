import os
import shutil
import subprocess

def main():
    current_directory = os.getcwd()
    target_folder = os.path.abspath(os.path.join(current_directory, os.pardir))
    print(target_folder)
    script_dir = os.path.dirname(os.path.realpath(__file__))  
    print(script_dir)

    if not os.path.isdir(target_folder):
        print(f"The folder {target_folder} does not exist.")
        return

    # Iterate through subfolders in the target folder
    for i in range(1, 21):
        folder_name = f"_{i}-aacg-"
        for folder in os.listdir(target_folder):
            if folder_name in folder:
                anneal_path = os.path.join(target_folder, folder, ".")
                print(anneal_path)
                
                # Check if the anneal path exists
                if os.path.isdir(anneal_path):
                    # Change to the anneal directory
                    os.chdir(anneal_path)
                    
                    # Construct the gmx trjconv command
                    t0 = 1150 * (125 * (i - 1) + 1)
                    output_file = os.path.join(script_dir, f"{i}-align.xtc")
                    command = ["gmx", "trjconv", "-f", "aligned-pbc-correct.xtc", "-b", "1150", "-t0", str(t0), "-timestep", "1150", "-o", output_file, "-n", "./index.ndx"]

                    # Execute the command and automatically input '6'
                    try:
                        process = subprocess.Popen(command, stdin=subprocess.PIPE, text=True)
                        process.communicate(input='6\n')
                        print(f"Command executed successfully, file saved as {output_file}")
                    except subprocess.CalledProcessError as e:
                        print(f"Error executing command in {anneal_path}: {e}")
                else:
                    print(f"Anneal path {anneal_path} does not exist.")

if __name__ == "__main__":
    main()

