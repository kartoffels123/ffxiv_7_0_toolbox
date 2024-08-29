import csv

def find_type_differences(input_csv, output_csv):
    rows = []
    
    with open(input_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    results = []
    current_index = -1

    for row in rows:
        index, filename, dimensions, format = row
        index = int(index)
        
        if index != current_index:
            if len(results) == 2 and results[0][2] == results[1][2] and results[0][3] != results[1][3]:
                for result in results:
                    with open(output_csv, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(result)
            results = [row]
            current_index = index
        else:
            results.append(row)

    # Check the last pair
    if len(results) == 2 and results[0][2] == results[1][2] and results[0][3] != results[1][3]:
        for result in results:
            with open(output_csv, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(result)

if __name__ == "__main__":
    input_csv = 'comparison_results.csv'
    output_csv = 'comparison_results_type_difference.csv'

    # Initialize the output CSV file with the same header as input
    with open(input_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
    
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    find_type_differences(input_csv, output_csv)

    print("Type differences identified and output to comparison_results_type_difference.csv")
