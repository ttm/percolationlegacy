def start():
    po=P.rdf.ontology()
    metadata=P.rdf.legacyMetadata()
    percolation_graph=po+metadata
    return percolation_graph
