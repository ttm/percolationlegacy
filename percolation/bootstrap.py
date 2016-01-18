import percolation as P, builtins as B

def start():
    percolation_server=P.PercolationServer()
    B.percolation_server=percolation_server
    P.B=B
    P.rdf.renderMinimumOntology() # ontology in "minimum_contology" context/named graph
    P.legacy.renderMetadata() # ontology in "legacy_metadata" context/named graph
    # P.analyses.describeSnapshots() should render a description of available social structures


