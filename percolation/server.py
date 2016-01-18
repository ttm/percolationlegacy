import percolation as P, rdflib as r, os, builtins

class PercolationServer:
    def standardPercolationStartup(self,percolationdir="~/.percolation/"):
        percolationdir=os.path.expanduser(percolationdir)
        if not os.path.isdir(percolationdir):
            os.mkdir(percolationdir)
        dbdir=percolationdir+"sleepydb/"
        if not os.path.isdir(dbdir):
            os.mkdir(dbdir)
        percolation_graph=r.ConjunctiveGraph(store="Sleepycat")
        try:
            percolation_graph.open(dbdir, create=False)
        except:
            percolation_graph.open(dbdir, create=True)
            po=P.rdf.minimumOntology("triples")
            metadata=P.rdf.legacyMetadata("triples")
            percolation_graph.add(po+metadata)
        else:
            assert rt == VALID_STORE, 'The underlying store is corrupt'
        # add percolationdir and dbdir to percolation_graph
        self.percolationpercolation_graph
        return self


