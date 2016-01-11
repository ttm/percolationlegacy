import sys, os
keys=tuple(sys.modules.keys())
for key in keys:
    if "percolation" in key:
        print(key)
        del sys.modules[key]
import percolation as P, importlib
importlib.reload(P.utils)
importlib.reload(P.sparql)

c=P.utils.check
#remote_urls="http://200.144.255.210:8082/ds","http://200.144.255.210:8082/books","http://200.144.255.210:8082/inf"
remote_urls="http://200.144.255.210:8082/ds","http://200.144.255.210:8082/dstdb",\
            "http://200.144.255.210:8082/books",\
            "http://200.144.255.210:8082/inf","http://200.144.255.210:8082/infEmpty",\
            "http://200.144.255.210:8082/infT","http://200.144.255.210:8082/infTEmpty",\

urls=remote_urls
services=[]
for url in urls:
    service=P.sparql.EndpointInterface(url)
    services+=[service]
    service.getAllTriples()
    c(len(service.triples))
    service.getGraphs()
    c(str(service.graphs)+"\n\n")
