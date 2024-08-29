import json

def process_eqp_entry(entry, set_id):
    binary = format(entry, '064b')
    original_binary = binary
    changed = False

    # If HeadShowVieraHat (bit 57) is 0, set it to 1
    if binary[6] == '0':
        binary = binary[:6] + '1' + binary[7:]
        changed = True

    # # If HeadShowEarHuman (bit 50) is 0, set HeadShowEarViera (bit 53) to 0
    # if binary[13] == '0':
    #     binary = binary[:10] + '0' + binary[11:]
    #     changed = True

    # Only exclude if BOTH HeadShowVieraHat and HeadShowEarHuman were already 1
    if original_binary[6] == '1' and original_binary[13] == '1':
        return None, f"SetId: {set_id}, Entry: {entry} (unchanged)\n"

    return int(binary, 2), None if changed else f"SetId: {set_id}, Entry: {entry} (unchanged)\n"

def process_json(data):
    new_manipulations = []
    unchanged_entries = []
    
    def process_manipulations(manipulations):
        for manipulation in manipulations:
            if manipulation['Type'] == 'Eqp':
                entry = manipulation['Manipulation']['Entry']
                set_id = manipulation['Manipulation']['SetId']
                new_entry, log_entry = process_eqp_entry(entry, set_id)
                if new_entry is not None:
                    manipulation['Manipulation']['Entry'] = new_entry
                    new_manipulations.append(manipulation)
                elif log_entry:
                    unchanged_entries.append(log_entry)

    # Check if 'Options' key exists
    if 'Options' in data:
        for option in data['Options']:
            if 'Manipulations' in option:
                process_manipulations(option['Manipulations'])
        data['Options'][0]['Manipulations'] = new_manipulations
    # If 'Options' doesn't exist, assume manipulations are at the top level
    elif 'Manipulations' in data:
        process_manipulations(data['Manipulations'])
        data['Manipulations'] = new_manipulations
    else:
        print("Unable to find 'Manipulations' in the JSON structure.")
        return data, unchanged_entries

    return data, unchanged_entries

# Read JSON file
try:
    with open('all_helmets_eqp_data.json', 'r', encoding='utf-8-sig') as file:
        file_contents = file.read()
        json_data = json.loads(file_contents)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON: {e}")
    print("File contents:")
    print(file_contents)
    exit(1)
except FileNotFoundError:
    print("input.json file not found.")
    exit(1)

# Process the JSON
processed_data, unchanged_entries = process_json(json_data)

# Write the processed JSON to a new file
with open('output.json', 'w', encoding='utf-8') as file:
    json.dump(processed_data, file, indent=2)

# Write unchanged entries to not_changed.txt
with open('not_changed.txt', 'w', encoding='utf-8') as file:
    file.writelines(unchanged_entries)

print("Processing complete. Check output.json for results and not_changed.txt for unchanged entries.")