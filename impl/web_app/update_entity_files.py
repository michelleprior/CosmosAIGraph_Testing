import json
from pathlib import Path

def update_entity_files():
    # Define the input directory
    entities_dir = Path('entities')
    
    # Process all JSON files in the entities directory
    for json_file in entities_dir.glob('*.json'):
        try:
            # Read the existing JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                entity_data = json.load(f)
            
            # Add the libtype field
            entity_data['libtype'] = "en"
            
            # Write back the updated JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(entity_data, f, indent=4)
            
            print(f"Updated: {json_file}")
                
        except Exception as e:
            print(f"Error processing {json_file}: {e}")

if __name__ == "__main__":
    update_entity_files() 