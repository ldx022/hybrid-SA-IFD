file_name = 'labeled-total-ie.txt'
output_file_name = 'sorted_results.csv'
data = []
with open(file_name, 'r') as file:
    for line in file:
        parts = line.strip().split('  ')
        parts = [part for part in parts if part]
        if len(parts) < 3:  
            continue
        try:
            sum_of_last_two = float(parts[-2]) + float(parts[-1])
            data.append((parts, sum_of_last_two))
        except ValueError:
            continue

sorted_data = sorted(data, key=lambda x: (x[1], x[0]))

with open(output_file_name, 'w') as csvfile:
    for item in sorted_data:
        line = ','.join(item[0]) + ',' + str(item[1])
        csvfile.write(line + '\n')

print(f"Results have been saved to {output_file_name}")
