
import os

def record_and_cleanup_failed_cases(workdir):
    failed_cases = []

    # Assuming the naming convention is model_i.pdb and lig_i.pdb
    for filename in os.listdir(workdir):
        if filename.startswith("model_") and filename.endswith(".pdb"):
            model_id = filename.split("_")[1].split(".")[0]
            lig_filename = f"lig_{model_id}.pdb"
            if os.path.exists(os.path.join(workdir, lig_filename)):
                # If both model and lig files exist, this is considered a failed case
                failed_cases.append(int(model_id))
                # Delete the model and ligand files
                os.remove(os.path.join(workdir, filename))
                os.remove(os.path.join(workdir, lig_filename))

    # Sort failed_cases to ensure the order
    failed_cases.sort()

    # Write failed case IDs to a CSV file
    with open(os.path.join(workdir, "16b-extract_pocket_failed_case_id_from0.csv"), "w") as failed_file:
        for case_id in failed_cases:
            failed_file.write(f"{case_id}\n")

    if failed_cases:
        print(f"Recorded and cleaned up {len(failed_cases)} failed cases.")
    else:
        print("No failed cases found.")

# Example usage
record_and_cleanup_failed_cases(".")
