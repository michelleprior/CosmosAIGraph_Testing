from src.util.prompts import Prompts
from src.util.fs import FS

# pytest -v tests/test_prompts.py


def test_generate_sparql_system_prompt():
    p = Prompts()
    ptext = p.generate_sparql_system_prompt(sample_owl())
    print("---")
    print(ptext)
    print("---")
    FS.write("tmp/test_generate_sparql_system_prompt.txt", ptext)

    expected_literals = [
        "You are a helpful agent designed to generate a RDF SPARQL 1.1 query",
        '<?xml version="1.0"?>',
        "http://cosmosdb.com/caig#",
        "</rdf:RDF>",
        "Include only the caig ontology prefix.",
    ]

    for literal in expected_literals:
        assert literal in ptext


def sample_owl():
    return """
<?xml version="1.0"?>

<rdf:RDF
  xmlns      = "http://cosmosdb.com/caig#"
  xmlns:owl  = "http://www.w3.org/2002/07/owl#"
  xmlns:rdf  = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:rdfs = "http://www.w3.org/2000/01/rdf-schema#"
  xmlns:xsd  = "http://www.w3.org/2001/XMLSchema#">

  <owl:Ontology rdf:about="">
    <rdfs:comment>
      A custom ontology for the PyPi Libraries reference graph
    </rdfs:comment>
    <rdfs:label>PyPi Software Libraries Ontology</rdfs:label>
  </owl:Ontology>

  <owl:Class rdf:ID="Library">
    <rdfs:label xml:lang="en">Library</rdfs:label>
    <rdfs:comment xml:lang="en">A PyPi software library</rdfs:comment>
  </owl:Class>

  <owl:Class rdf:ID="Developer">
    <rdfs:label xml:lang="en">Developer</rdfs:label>
    <rdfs:comment xml:lang="en">A software Developer of a library</rdfs:comment>
  </owl:Class>

  <owl:ObjectProperty rdf:ID="uses_library">
	<rdfs:label xml:lang="en">uses_library</rdfs:label>
	<rdfs:comment xml:lang="en">Library uses another Library</rdfs:comment>
    <rdfs:domain rdf:resource="#Library" />
    <rdfs:range  rdf:resource="#Library" />
  </owl:ObjectProperty>

  <owl:ObjectProperty rdf:ID="used_by_library">
	<rdfs:label xml:lang="en">used_by_library</rdfs:label>
	<rdfs:comment xml:lang="en">Library is used by another Library</rdfs:comment>
    <rdfs:domain rdf:resource="#Library" />
    <rdfs:range  rdf:resource="#Library" />
  </owl:ObjectProperty>

  <owl:ObjectProperty rdf:ID="developer_of">
	<rdfs:label xml:lang="en">developer_of</rdfs:label>
	<rdfs:comment xml:lang="en">Developer is the creator/author/maintainer of a Library</rdfs:comment>
    <rdfs:domain rdf:resource="#Developer" />
    <rdfs:range  rdf:resource="#Library" />
  </owl:ObjectProperty>

  <owl:ObjectProperty rdf:ID="developed_by">
	<rdfs:label xml:lang="en">developed_by</rdfs:label>
	<rdfs:comment xml:lang="en">Library is created/authored/maintained by a Developer</rdfs:comment>
    <rdfs:domain rdf:resource="#Library" />
    <rdfs:range  rdf:resource="#Developer" />
  </owl:ObjectProperty>

  <owl:DatatypeProperty rdf:ID="name">
    <rdfs:label xml:lang="en">name</rdfs:label>
    <rdfs:comment xml:lang="en">The name of a Library</rdfs:comment>
    <rdfs:domain rdf:resource="#Library" />
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string" />
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="keywords">
    <rdfs:label xml:lang="en">keywords</rdfs:label>
    <rdfs:comment xml:lang="en">The list of Keywords associated with a Library</rdfs:comment>
    <rdfs:domain rdf:resource="#Library" />
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string" />
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="description">
    <rdfs:label xml:lang="en">description</rdfs:label>
    <rdfs:comment xml:lang="en">The description of a Library</rdfs:comment>
    <rdfs:domain rdf:resource="#Library" />
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#string" />
  </owl:DatatypeProperty>

  <owl:DatatypeProperty rdf:ID="release_count">
    <rdfs:label xml:lang="en">release_count</rdfs:label>
    <rdfs:comment xml:lang="en">The number of releases, or published versions, of the Library</rdfs:comment>
    <rdfs:domain rdf:resource="#Library" />
    <rdfs:range rdf:resource="http://www.w3.org/2001/XMLSchema#int" />
  </owl:DatatypeProperty>

</rdf:RDF>
""".strip()
