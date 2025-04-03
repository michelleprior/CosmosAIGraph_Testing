package com.microsoft.cosmosdb.caig.graph;

import java.util.List;
import java.util.Map;

import org.apache.jena.rdf.model.Model;
import org.apache.jena.rdf.model.Resource;
import org.apache.jena.rdf.model.impl.PropertyImpl;
import org.apache.jena.vocabulary.RDF;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * Class LibrariesGraphTriplesBuilder creates RDF triples for documents
 * and adds them to the graph model incrementally.
 *
 * Chris Joakim, Microsoft, 2025
 */

public class LibrariesGraphTriplesBuilder {

    public static final String CAIG_NAMESPACE = "http://cosmosdb.com/caig#";

    private static Logger logger = LoggerFactory.getLogger(LibrariesGraphTriplesBuilder.class);

    private AppGraph graph;
    private Model model;
    private String namespace;
    private long documentsIngested = 0;
    private ObjectMapper objectMapper;

    private PropertyImpl titleProperty;
    private PropertyImpl descriptionProperty;
    private PropertyImpl typeProperty;
    private PropertyImpl frequencyProperty;
    private PropertyImpl degreeProperty;
    private PropertyImpl libtypeProperty;
    private PropertyImpl dependsOnProperty;
    private PropertyImpl weightProperty;

    public LibrariesGraphTriplesBuilder(AppGraph g) {
        super();
        this.graph = g;
        this.model = g.getModel();
        this.objectMapper = new ObjectMapper();
        this.namespace = CAIG_NAMESPACE;

        // Initialize properties based on the ontology
        this.titleProperty = new PropertyImpl(this.namespace, "title");
        this.descriptionProperty = new PropertyImpl(this.namespace, "description");
        this.typeProperty = new PropertyImpl(this.namespace, "type");
        this.frequencyProperty = new PropertyImpl(this.namespace, "frequency");
        this.degreeProperty = new PropertyImpl(this.namespace, "degree");
        this.libtypeProperty = new PropertyImpl(this.namespace, "libtype");
        this.dependsOnProperty = new PropertyImpl(this.namespace, "dependsOn");
        this.weightProperty = new PropertyImpl(this.namespace, "weight");
    }

    public long getDocumentsIngested() {
        return documentsIngested;
    }

    /**
     * Add to the graph the zero-to-many triples that correspond to the given
     * document.
     */
    public void ingestDocument(Map<String, Object> doc) {
        try {
            if (doc != null) {
                this.documentsIngested++;
                String entityId = doc.get("title").toString();
                String entityUri = this.namespace + entityId;
                Resource entityResource = lookupResource(entityUri);

                // Create the entity resource if it doesn't already exist
                entityResource = model.createResource(entityUri);
                model.add(entityResource, RDF.type, model.createResource(this.namespace + "Entity"));

                logger.info("Created entityResource: " + entityUri);

                // Add properties/attributes of the entity
                if (doc.containsKey("title")) {
                    String title = doc.get("title").toString().strip();
                    entityResource.addProperty(titleProperty, title);
                }
                if (doc.containsKey("description")) {
                    String description = doc.get("description").toString().strip();
                    entityResource.addProperty(descriptionProperty, description);
                }
                if (doc.containsKey("type")) {
                    String type = doc.get("type").toString().strip();
                    entityResource.addProperty(typeProperty, type);
                }
                if (doc.containsKey("frequency")) {
                    String frequency = doc.get("frequency").toString();
                    entityResource.addProperty(frequencyProperty, frequency);
                }
                if (doc.containsKey("degree")) {
                    String degree = doc.get("degree").toString();
                    entityResource.addProperty(degreeProperty, degree);
                }
                if (doc.containsKey("libtype")) {
                    String libtype = doc.get("libtype").toString().strip();
                    entityResource.addProperty(libtypeProperty, libtype);
                }

                // Add dependency relationships
                if (doc.containsKey("dependencies")) {
                    List<Map<String, Object>> dependencies = (List<Map<String, Object>>) doc.get("dependencies");
                    for (Map<String, Object> dependency : dependencies) {
                        String source = dependency.get("source").toString();
                        String weight = dependency.get("weight").toString();

                        String dependencyUri = this.namespace + source;
                        Resource dependencyResource = lookupResource(dependencyUri);
                        if (dependencyResource == null) {
                            dependencyResource = model.createResource(dependencyUri);
                            model.add(dependencyResource, RDF.type, model.createResource(this.namespace + "Entity"));
                        }

                        entityResource.addProperty(dependsOnProperty, dependencyResource);
                        dependencyResource.addProperty(weightProperty, weight);
                    }
                }

                logger.info("Document ingested: " + entityId);
            }
        } catch (Exception e) {
            throw new RuntimeException("Error ingesting document", e);
        }
    }

    /**
     * Lookup the given URI in the model. Return either the Resource, or null.
     */
    public Resource lookupResource(String uri) {
        Resource res = null;
        if (uri != null) {
            res = this.model.getResource(uri);
        }
        return res;
    }
}
