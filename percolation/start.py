import builtins as B
import percolation as P, rdflib as r
NS=P.rdf.NS

B.status_graph=r.Graph()
B.status_vars=object()
BG=B.status_graph
BV=B.status_vars

def start():
    po=P.rdf.ontology()
    metadata=P.rdf.legacyMetadata()
    BV.percolation_graph=po+metadata
    BG.add((NS.per.CurrentRun, NS.per.percolationGraph,"percolation_graph"))
    return BV.percolation_graph
