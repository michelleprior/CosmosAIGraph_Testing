import json
from pathlib import Path
from typing import Dict, List

class EntityOwlGenerator:
    def __init__(self):
        self.entities_dir = Path('entities')
        self.template = """<?xml version="1.0"?>

<rdf:RDF
  xmlns      = "http://cosmosdb.com/caig#"
  xmlns:owl  = "http://www.w3.org/2002/07/owl#"
  xmlns:rdf  = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:rdfs = "http://www.w3.org/2000/01/rdf-schema#"
  xmlns:xsd  = "http://www.w3.org/2001/XMLSchema#"
  xml:base   = "http://cosmosdb.com/caig">

  <owl:Ontology rdf:about="">
    <rdfs:comment>Entity Dependencies Ontology</rdfs:comment>
  </owl:Ontology>

  <!-- Classes -->
  {classes}

  <!-- Data Properties -->
  <owl:DatatypeProperty rdf:ID="humanReadableId">
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#integer"/>
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="title">
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="type">
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="description">
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="frequency">
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#integer"/>
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="degree">
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#integer"/>
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="x">
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#float"/>
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="y">
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#float"/>
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="libtype">
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="pk">
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string"/>
  </owl:DatatypeProperty>

  <!-- Object Properties -->
  <owl:ObjectProperty rdf:ID="dependsOn">
    <rdfs:comment xml:lang="en">Represents a dependency relationship between entities</rdfs:comment>
    <rdfs:domain rdf:resource="#Entity"/>
    <rdfs:range rdf:resource="#Entity"/>
  </owl:ObjectProperty>

  <owl:DatatypeProperty rdf:ID="weight">
    <rdfs:comment xml:lang="en">Weight of the dependency relationship</rdfs:comment>
    <rdfs:domain rdf:resource="#dependsOn"/>
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#float"/>
  </owl:DatatypeProperty>

  <!-- Instances and their relationships -->
  {instances}

</rdf:RDF>"""

    def generate_owl(self) -> str:
        entities = self._load_entities()
        
        # Generate classes section
        classes = ['  <owl:Class rdf:ID="Entity"/>']
        
        # Generate instances and relationships section
        instances = []
        relationships = []
        
        for entity_data in entities:
            entity_id = entity_data['id'].replace('-', '_')
            
            # Create instance with all properties
            instance = [f"""
  <Entity rdf:ID="{entity_id}">
    <rdfs:label>{entity_data['title']}</rdfs:label>"""]
            
            # Add all data properties
            if 'human_readable_id' in entity_data:
                instance.append(f'    <humanReadableId rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{entity_data["human_readable_id"]}</humanReadableId>')
            
            if 'title' in entity_data:
                instance.append(f'    <title rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{entity_data["title"]}</title>')
            
            if 'type' in entity_data:
                instance.append(f'    <type rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{entity_data["type"]}</type>')
            
            if 'description' in entity_data:
                instance.append(f'    <description rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{entity_data["description"]}</description>')
            
            if 'frequency' in entity_data:
                instance.append(f'    <frequency rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{entity_data["frequency"]}</frequency>')
            
            if 'degree' in entity_data:
                instance.append(f'    <degree rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{entity_data["degree"]}</degree>')
            
            if 'x' in entity_data:
                instance.append(f'    <x rdf:datatype="http://www.w3.org/2001/XMLSchema#float">{entity_data["x"]}</x>')
            
            if 'y' in entity_data:
                instance.append(f'    <y rdf:datatype="http://www.w3.org/2001/XMLSchema#float">{entity_data["y"]}</y>')
            
            if 'libtype' in entity_data:
                instance.append(f'    <libtype rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{entity_data["libtype"]}</libtype>')
            
            if 'pk' in entity_data:
                instance.append(f'    <pk rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{entity_data["pk"]}</pk>')
            
            instance.append('  </Entity>')
            instances.append('\n'.join(instance))
            
            # Add dependency relationships with weights
            if 'dependencies' in entity_data:
                for dep in entity_data['dependencies']:
                    source = dep['source'].replace(' ', '_').replace('-', '_')
                    weight = dep.get('weight', 1.0)
                    relationships.append(f"""
  <rdf:Description rdf:about="#{entity_id}">
    <dependsOn rdf:resource="#{source}"/>
    <weight rdf:datatype="http://www.w3.org/2001/XMLSchema#float">{weight}</weight>
  </rdf:Description>""")

        # Combine all sections
        owl_content = self.template.format(
            classes='\n'.join(classes),
            instances='\n'.join(instances + relationships)
        )
        
        return owl_content

    def _load_entities(self) -> List[Dict]:
        entities = []
        for json_file in self.entities_dir.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    entity_data = json.load(f)
                    entities.append(entity_data)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        return entities

    def save_owl(self, output_path: str = 'entities.owl'):
        owl_content = self.generate_owl()
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(owl_content)
        print(f"OWL file saved to: {output_path}")

if __name__ == "__main__":
    generator = EntityOwlGenerator()
    generator.save_owl() 