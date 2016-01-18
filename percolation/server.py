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

            #nick=datetime.datetime.now().isoformat()+'r'++''.join(["%s" % random.randint(0, 9) for num in range(0, 5)])
            #uri_=NS.per.Participant+"#"+NICK
        else:
            assert rt == VALID_STORE, 'The underlying store is corrupt'
        # add percolationdir and dbdir to percolation_graph
        self.percolationpercolation_graph
        return self
def startSession():
    current_user_uri=P.get(NS.per.currentUser)
    if not current_user_uri:
        current_user_uri=P.rdf.timestampedURI(NS.per.Participant)
    session_uri=P.rdf.timestampedURI(NS.per.Session)
    current_state_uri=NS.per.CurrentState # shout be in ontology
    now=datetime.datetime.now()
    triples=[
            (current_state_uri,NS.per.currentSession,session_uri),
            (session_uri,NS.per.started,now),
            (session_uri,NS.per.user,current_user_uri),
            ]


def start(): # duplicate in legacy/outlines.py
    PercolationServer()
    P.utils.startSession()
    P.utils.aaSession()
