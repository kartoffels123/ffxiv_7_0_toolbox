import csv

def find_type_differences(input_csv, output_diff_csv, output_same_csv):
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
            if len(results) == 2 and results[0][2] == results[1][2]:
                if results[0][3] != results[1][3]:
                    output_csv = output_diff_csv
                else:
                    output_csv = output_same_csv
                
                for result in results:
                    with open(output_csv, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(result)
            results = [row]
            current_index = index
        else:
            results.append(row)

    # Check the last pair
    if len(results) == 2 and results[0][2] == results[1][2]:
        if results[0][3] != results[1][3]:
            output_csv = output_diff_csv
        else:
            output_csv = output_same_csv
        
        for result in results:
            with open(output_csv, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(result)

if __name__ == "__main__":
    input_csv = 'comparison_results_dimension_same.csv'
    output_diff_csv = 'comparison_results_dimension_same_type_difference.csv'
    output_same_csv = 'comparison_results_dimension_same_type_same.csv'

    # Initialize the output CSV files with the same header as input
    with open(input_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
    
    for output_csv in [output_diff_csv, output_same_csv]:
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)

    find_type_differences(input_csv, output_diff_csv, output_same_csv)

    print("Type differences and same types identified and output to respective CSV files.")
