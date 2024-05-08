import os

pdb_filename = 'updated_system-aacg2aa.pdb'

def extract_models(pdb_filename):
    if not os.path.exists(pdb_filename):
        print(f"file {pdb_filename} does not exist")
        return
    
    model_content = [] # Store the contents of the current model
    current_model = None # Index of the current model

    with open(pdb_filename, 'r') as file:
        for line in file:
            if line.startswith('MODEL'):
                current_model = line.split()[1] # Get model index
                model_content = [] 
            elif line.startswith('ENDMDL'):
                # The current model is finished. Save the model contents to the corresponding folder
                save_model(current_model, model_content)
            else:
                model_content.append(line)

def save_model(model_index, content):
    folder_name = model_index
    if not os.path.exists(folder_name):
        os.makedirs(folder_name) 
    
    model_filename = os.path.join(folder_name, f'model_{model_index}.pdb')
    
    with open(model_filename, 'w') as model_file:
        model_file.writelines(content)
    print(f"model {model_index} has saved as {model_filename}")

extract_models(pdb_filename)

