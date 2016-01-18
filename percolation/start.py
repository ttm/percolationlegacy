import percolation as P, rdflib as r, os
NS=P.rdf.NS

class Status:
    pass
class Start:
    def __init__(self,percolationdir="~/.percolation/"):
        percolationdir=os.expanduser(percolationdir)
        if not os.path.isdir(percolationdir):
            os.mkdir(percolationdir)
        dbpath=percolationdir+"prdflibstore")
        status_graph=r.ConjunctiveGraph("Sleepycat")
        rt = status_graph.open(path, create=False)
        if rt == NO_STORE:
            status_graph.open(path, create=True)
            po=P.rdf.ontology()
            metadata=P.rdf.legacyMetadata()
            status_graph+=po+metadata
        else:
            assert rt == VALID_STORE, 'The underlying store is corrupt'
        Status.status_graph=status_graph
        return status_graph
