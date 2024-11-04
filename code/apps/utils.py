import os
import json

def read_json(file_path):
    """
    Load data from a JSON file.

    Parameters:
    - file_path (str): The path to the JSON file.

    Returns:
    - success (bool): True if the data was successfully loaded, False otherwise.
    - data (dict): The loaded data from the JSON file.
    """
    
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        return True, data
    except FileNotFoundError as e:
        return False, f"Error: {e}"
    except json.JSONDecodeError as e:
        return False, f"Error decoding JSON: {e}"
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"


def save_json(file_path, json_data):
    """
    Save data to a JSON file.

    Parameters:
    - file_path (str): The path to the JSON file.
    - json_data (dict): The data to save.

    Returns:
    - success (bool): True if the data was successfully saved, False otherwise.
    - error_message (str): A message indicating the result of the save operation.

    """
    
    try:
        with open(file_path, 'w') as json_file:
            json_data.pop("desc", None)
            json.dump(json_data, json_file, indent=2)
        return True, None
    except Exception as e:
        return False, f"Error saving data to JSON: {e}"
