import json
import os
from pathlib import Path
import time
from datetime import datetime

def combine_entity_files():
    # Define the input and output paths
    entities_dir = Path('entities')
    output_file = Path('entities_doc.json')
    
    # Get current timestamp
    timestamp = time.time()
    datetime_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # Initialize the combined data structure
    combined_data = {
        "id": "entities",
        "pk": "entities",
        "created_at": timestamp,
        "created_date": datetime_str,
        "docs_read": 0,  # Will count the number of entities
        "elapsed_seconds": "0.0",
        "exception": "",
        "libraries": {}  # This will contain all our entities
    }
    
    # Counter for generating entity keys
    counter = 1
    
    # Read all JSON files in the entities directory
    for json_file in entities_dir.glob('*.json'):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                entity_data = json.load(f)
                # Add the entity to the libraries object
                combined_data["libraries"][entity_data['title']] = "en"
                counter += 1
                
        except Exception as e:
            print(f"Error processing {json_file}: {e}")
    
    # Update docs_read with number of entities processed
    combined_data["docs_read"] = counter - 1
    
    # Create directory if it doesn't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the combined data to entities_doc.json
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(combined_data, f, indent=2)
        print(f"Successfully created {output_file}")
    except Exception as e:
        print(f"Error writing combined file: {e}")

if __name__ == "__main__":
    combine_entity_files() 