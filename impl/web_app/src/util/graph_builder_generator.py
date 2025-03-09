from src.util.fs import FS

# This class is used to generate a RdflibTriplesBuilder python class that
# can be used in the GraphBuilder process that loads a rdflib in-memory graph
# from the contents of JSON documents (i.e. - Cosmos DB documents).
#
# Chris Joakim, Microsoft, 2025


class GraphBuilderGenerator:

    def __init__(self, using_flat_csv_data=True):
        self.using_flat_csv_data = using_flat_csv_data

    def generate(self, vertex_signatures_filename):

        vertex_signatures_dict = sorted(FS.read_json(vertex_signatures_filename).keys())
        labels = self.collect_vertex_names(vertex_signatures_dict)

        code = list()
        code.append("import logging")
        code.append("import os")
        code.append("import psutil")
        code.append("import time")
        code.append("import traceback")
        code.append("")
        code.append("import rdflib")
        code.append("from rdflib import Graph, Literal, RDF, URIRef, BNode")
        code.append("from rdflib.namespace import Namespace, NamespaceManager")
        code.append(
            "from rdflib.extras.infixowl import AllClasses, AllProperties, GetIdentifiedClasses"
        )
        code.append("")
        code.append(
            "# This module was generated by CosmosAIGraph from source data metadata."
        )
        code.append(
            "# This class is used by class GraphBuilder to build the in-memory rdflib graph"
        )
        code.append(
            "# from JSON documents provided to the append_doc_to_graph(...) method."
        )
        code.append(
            "# The JSON documents will be read from Cosmos DB vCore, but the initial"
        )
        code.append("# implementation obtains the JSON documents from a tmp/ file.")
        code.append("")
        code.append("class RdflibTriplesBuilder:")
        code.append("")
        code.append("    def __init__(self, attributes_root=None):")
        code.append("        self.attributes_root = attributes_root")
        code.append("")
        code.append("    def append_doc_to_graph(self, g, doc, CNS, ns):")
        code.append('        """ this method is called by GraphBuilder """')
        code.append("        try:")
        code.append('            label = doc["label"]')
        code.append("")
        logical_word = "if"
        for label in labels:
            code.append("            {} label == '{}':".format(logical_word, label))
            code.append(
                "                self.add_{}_to_graph(g, label, doc, CNS, ns)".format(
                    label
                )
            )
            logical_word = "elif"
        code.append("        except Exception as e:")
        code.append("            print(str(e))")
        code.append("            print(traceback.format_exc())")

        for label in labels:
            attr_names = self.collect_vertex_attributes(vertex_signatures_dict, label)
            code.append("")
            code.append(
                "    def add_{}_to_graph(self, g, label, doc, CNS, ns):".format(label)
            )
            code.append(
                '        #print("add_{}_to_graph, doc: {} ns: {}".format(label, doc, ns))'
            )
            code.append("        try:")
            code.append("            attr_keys, edges = list(), list()")
            code.append("            attributes_dict = doc")

            if self.using_flat_csv_data:
                pass
            else:
                code.append("            if self.attributes_root is not None:")
                code.append(
                    "                # allow for nested attributes (i.e. - doc['properties'])"
                )
                code.append(
                    "                attributes_dict = doc[self.attributes_root]"
                )

            code.append("            attr_keys = attributes_dict.keys()")

            if self.using_flat_csv_data:
                pass
            else:
                code.append("            if 'edges' in doc.keys():")
                code.append('                edges = doc["edges"]')

            code.append('            doc_id = str(doc["id"])')
            code.append("            if len(doc_id) > 0:")
            code.append('                cref = URIRef("{}/{}".format(ns, label))')
            code.append('                eref = URIRef("{}/{}".format(ns, doc_id))')
            code.append("                g.add((eref, RDF.type, cref))")
            for aname in attr_names:
                code.append("                if '{}' in attr_keys:".format(aname))
                code.append(
                    "                    value = attributes_dict['{}']".format(aname)
                )
                code.append(
                    "                    g.add((eref, CNS.{}, Literal(value)))".format(
                        aname
                    )
                )
            code.append("")

            if self.using_flat_csv_data:
                pass
            else:
                code.append("                self.add_edges(g, ns, doc_id, edges, CNS)")

            code.append("            else:")
            code.append('                print("invalid {} doc {}".format(label, doc))')
            code.append("        except Exception as e:")
            code.append("            print(str(e))")
            code.append("            print(traceback.format_exc())")

        code.append("")
        code.append("    def add_edges(self, g, ns, doc_id, edges, CNS):")
        code.append("        for edge in edges:")
        code.append('            label     = edge["label"]')
        code.append('            sink_id   = edge["sink_id"]')
        code.append('            sourceref = URIRef("{}/{}".format(ns, doc_id))')
        code.append('            sinkref   = URIRef("{}/{}".format(ns, sink_id))')
        code.append("            predicate = CNS[label]")
        code.append("            g.add((sourceref, predicate, sinkref))")
        code.append("")

        FS.write_lines(code, "tmp/rdflib_triples_builder.py")
        return code

    def collect_vertex_names(self, vertex_signatures_dict):
        names = dict()
        for key in vertex_signatures_dict:
            tokens = key.split("|")
            lab = tokens[0]
            names[lab] = key
        return sorted(names.keys())

    def collect_vertex_attributes(self, vertex_signatures_dict, label):
        attr_names = dict()
        for key in vertex_signatures_dict:
            tokens = key.split("|")
            lab, aname = tokens[0], tokens[1]
            if lab == label:
                attr_names[aname] = aname
        return sorted(attr_names.keys())
