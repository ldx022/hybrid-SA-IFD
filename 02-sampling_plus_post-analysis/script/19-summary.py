import csv

top500_coords = {}
with open('top500.csv', 'r') as file:
    for lineno, line in enumerate(file, 1):
        coords = line.strip()
        top500_coords[lineno] = coords

coords_ie = {}

with open('sorted_results.csv', 'r') as ie_file:
    for line in ie_file:
        coords, data = line.strip().split(':')
        coords_ie[coords] = data

with open('18-total-out-adjusted.csv', 'r') as infile, open('19-summary.txt', 'w') as outfile:
    reader = csv.reader(infile)
    next(reader)  
    for row in reader:
        try:
            system_id = int(row[0])  
            second_column_content = row[1] 
            third_column_content = row[2] if len(row) > 2 else 'NA'  
            if system_id in top500_coords:
                coords = top500_coords[system_id]
                ie_data = coords_ie.get(coords, 'NA')
                outfile.write(f'{system_id},{second_column_content},{third_column_content},{coords},{ie_data}\n')
        except ValueError:
            continue

print("The integration is complete and the results have been saved to the file 19-summary.txt.")


