def extract_model_numbers(csv_file):
    model_numbers = []
    with open(csv_file, 'r') as file:
        for line in file:
            a, b, c = map(int, line.strip().split('-'))
            model_number = 125*(a-1) + 25*(b-1) + c
            model_numbers.append(model_number)
    return model_numbers

def extract_and_write_models(pdb_file, model_numbers, output_file):
    with open(pdb_file, 'r') as file:
        pdb_content = file.read()

    models = pdb_content.split('ENDMDL')
    extracted_models = []

    for number in model_numbers:
        # Adjusting for 1-based indexing in PDB models
        if number-1 < len(models):
            extracted_models.append(models[number-1].strip() + '\nENDMDL')

    with open(output_file, 'w') as file:
        for model in extracted_models:
            file.write(model + '\n')

if __name__ == "__main__":
    csv_file = 'top500.csv'
    pdb_file = 'merge1-20.pdb'
    output_file = 'top500-aacg.pdb'
    
    model_numbers = extract_model_numbers(csv_file)
    extract_and_write_models(pdb_file, model_numbers, output_file)

    print("Extraction and writing of models complete.")
