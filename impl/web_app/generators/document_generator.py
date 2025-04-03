import pandas as pd
import os
import re
import openai

client = openai.OpenAI(api_key=os.get('OPENAI_API_KEY'))

parquet_file = 'output/documents.parquet'
df = pd.read_parquet(parquet_file)

parquet_file_entities = 'output/entities.parquet'
df_entities = pd.read_parquet(parquet_file_entities)
df_entities

relationship_file_path = 'output/relationships.parquet' 
df_relationships = pd.read_parquet(relationship_file_path)
df_relationships

json_file_path = 'output/entities/'
invalid_characters_pattern = r'[\/:*?"<>|]'

def sanitize_filename(name, index):
    if pd.isnull(name) or name.strip() == "":
        return f"untitled_{index}"  
    return re.sub(invalid_characters_pattern, '_', name)

def map_dependencies_with_weighting(entity_title):
    dependencies = df_relationships[df_relationships['target'] == entity_title]
    dependency_list = dependencies.apply(
        lambda row: {"source": row['source'], "weight": row['weight']}, axis=1
    ).tolist()
    return dependency_list

def get_openai_embedding(text):
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Failed to get embedding for text: {text}. Error: {e}")
        return []

df_entities['dependencies'] = df_entities['title'].apply(map_dependencies_with_weighting)

df_entities['libtype'] = "en"

df_entities['title'] = [
    sanitize_filename(row['title'], index) for index, row in df_entities.iterrows()
]
df_entities['embedding'] = df_entities['description'].apply(get_openai_embedding)

for index, row in df_entities.iterrows():
    entity_title = row.get('title', f"untitled_{index}")  
    sanitized_title = sanitize_filename(entity_title, index)  
    json_file = os.path.join(json_file_path, f"{sanitized_title}.json")
    
    try:
        row.to_json(json_file, orient='columns', indent=4)
        print(f"Saved: {json_file}")
    except Exception as e:
        print(f"Failed to save {json_file}: {e}")

print(f"All entities saved to: {json_file_path}")