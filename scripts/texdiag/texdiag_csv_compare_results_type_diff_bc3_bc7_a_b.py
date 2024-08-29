import csv

def find_specific_format_conversion(input_csv, output_csv, old_format, new_format):
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
                if (results[0][3] == old_format and results[1][3] == new_format) or (results[0][3] == new_format and results[1][3] == old_format):
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
        if (results[0][3] == old_format and results[1][3] == new_format) or (results[0][3] == new_format and results[1][3] == old_format):
            for result in results:
                with open(output_csv, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(result)

if __name__ == "__main__":
    input_csv = 'comparison_results_type_difference.csv'
    output_csv = 'specific_format_conversion.csv'
    old_format = 'BC3_UNORM'
    new_format = 'BC7_UNORM'

    # Initialize the output CSV file with the same header as input
    with open(input_csv, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
    
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    find_specific_format_conversion(input_csv, output_csv, old_format, new_format)

    print("Specific format conversion identified and output to specific_format_conversion.csv")
