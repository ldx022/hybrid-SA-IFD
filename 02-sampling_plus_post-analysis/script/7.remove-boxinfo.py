keywords_to_remove = ['CRYST1']

with open('top500-aacg.pdb', 'r') as file, open('aa-pro-lig_cleaned.pdb', 'w') as new_file:
    for line in file:
        if not any(keyword in line for keyword in keywords_to_remove):
            new_file.write(line)
