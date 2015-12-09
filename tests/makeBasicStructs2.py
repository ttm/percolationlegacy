import rdflib as r, percolation as P
c=P.utils.check

endpoint_url,relation_uri="200.144.255.210:8082/labMacambiraLaleniaLog2"
relation_uri=P.rdf.ns.foaf.knows
makeNetwork(endpoint_url,relation_uri,label_uri=None,rtype=1,directed=False):
