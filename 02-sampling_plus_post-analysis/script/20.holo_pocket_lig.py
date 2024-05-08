
# Step 1: Read the model indices from 23.screened_summary.txt
model_indices = []
with open("19-summary.txt", "r") as summary_file:
    for line in summary_file:
        parts = line.strip().split(",")
        if parts:  # Make sure there's at least one element
            model_indices.append(int(parts[0]))  # Add the first column as an integer

# Step 2: Adjust model indices from 1-based to 0-based
model_indices = [x - 1 for x in model_indices]

# Step 3: Extract corresponding models from lig.pdb
extracted_models = []
with open("lig.pdb", "r") as pdb_file:
    lines = pdb_file.readlines()
    # Track whether we're in a model of interest
    in_model = False
    for line in lines:
        if line.startswith("MODEL"):
            model_index = int(line.split()[1])
            # Check if this model is one of the ones we're interested in
            in_model = model_index in model_indices
        if in_model:
            extracted_models.append(line)
        if line.startswith("ENDMDL"):
            in_model = False

# Step 4: Save extracted models to 23.holo_pocket_lig.pdb
with open("20.holo_pocket_lig.pdb", "w") as output_file:
    for line in extracted_models:
        output_file.write(line)
