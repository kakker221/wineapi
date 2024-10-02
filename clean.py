import json
import math

# Define the path to the JSON file
JSON_FILE_PATH = "LWINdatabase.json"

# Function to replace NaN values with None
def replace_nan_with_none(data):
    if isinstance(data, dict):
        return {k: replace_nan_with_none(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_nan_with_none(v) for v in data]
    elif isinstance(data, float) and math.isnan(data):
        return None
    return data

# Load the original JSON file
with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
    data = json.load(file)

# Replace NaN with None
cleaned_data = replace_nan_with_none(data)

# Save the cleaned data back to the file
with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
    json.dump(cleaned_data, file, indent=4)

print("NaN values replaced with null!")
