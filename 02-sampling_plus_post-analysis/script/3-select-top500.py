import csv

input_file_name = 'sorted_results.csv'
output_file_name = 'top500.csv'

data = []
with open(input_file_name, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i >= 500:  
            break
        first_column = row[0].split(':')[0]  
        data.append(first_column)

sorted_data = sorted(data, key=lambda x: tuple(int(part) for part in x.split('-')), reverse=False)

with open(output_file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for item in sorted_data:
        writer.writerow([item])

print(f"Top 500 sorted results have been saved to {output_file_name}")
