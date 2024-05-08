def label_lines_and_group(filename, output_filename):
    line_counter = 1
    group_counter = 1
    system_counter = 1
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    with open(output_filename, 'w') as outfile:
        for i, line in enumerate(lines):
            outfile.write(f"{system_counter}-{group_counter}-{line_counter}: {line}")
            
            if line_counter == 25:
                line_counter = 1
                if group_counter == 5:
                    group_counter = 1
                    system_counter += 1
                else:
                    group_counter += 1
            else:
                line_counter += 1

filename = 'total-ie.txt'
output_filename = 'labeled-total-ie.txt'

label_lines_and_group(filename, output_filename)

print("File processing complete. Check", output_filename, "for output.")

