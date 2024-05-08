import csv

failed_case_ids = []
with open('16b-extract_pocket_failed_case_id_from0.csv', 'r') as f:
    for row in csv.reader(f):
        if row:  
            failed_case_ids.append(int(row[0]))  

adjusted_rows = []
with open('17-2-total.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  

    current_id = 1  
    for row in reader:
        if not row:
            continue  

        if any(keyword in row[0] for keyword in ["ERROR:", "lig.pdb", "MISSING"]):
            adjusted_rows.append([str(current_id)] + row)
            current_id += 1
        else:
            adjusted_rows.append(row)

with open('18-total-out-adjusted.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ID', 'Other Columns...'])  
    writer.writerows(adjusted_rows)

print("The processing is complete and the results have been saved to the 18-total-out-adjusted.csv file.")

