
import os

def process_pdb_files(output_path, start_id=0, end_id=499):
    with open(output_path, "w") as output_file:
        for i in range(start_id, end_id + 1):
            folder_name = str(i)
            pdb_file_path = os.path.join(folder_name, "minimized.pdb")
            
            if os.path.exists(pdb_file_path):
                with open(pdb_file_path, "r") as pdb_file:
                    output_file.write("MODEL        {}\n".format(i))
                    skip_lines = 2
                    found_LIG = False
                    for line in pdb_file:
                        if skip_lines > 0:
                            skip_lines -= 1
                            continue
                        if "LIG" in line:
                            found_LIG = True
                        # When a LIG is found, as long as the current line does not contain a LIG, the write stops
                        elif found_LIG and "LIG" not in line:
                            break
                        output_file.write(line)
                    output_file.write("ENDMDL\n")

process_pdb_files("14.total_openmm_minimized.pdb")
