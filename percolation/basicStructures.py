import rdflib as r
def makeNetwork(rdf_file,relation_uri,label_uri,id_uri):
    """Make network whose vertices are objects and subjects of the relation_uri.

    With label_uri for the vertices labels
    and id_uri for identifying the vertices."""
    g=r.Graph()
    g.load(rdf_file)
    


