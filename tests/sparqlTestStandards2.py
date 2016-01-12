__doc__="""this file should hold routines and the synthesis of dummy networks for SparQL testing purpose\n
        
        designed for use with a Jena/Fuseki SparQL endpoint.
        Should create the testing networks in proper rdf graphid.
        Should also have the tests for the reasoner."""
import sys, os
keys=tuple(sys.modules.keys())
for key in keys:
    if "percolation" in key:
        print(key)
        del sys.modules[key]
import percolation as P, importlib
importlib.reload(P.utils)
importlib.reload(P.sparql)
NS=P.rdf.NS
a=NS.rdf.type

c=P.utils.check

data_dir="/disco/data/"
remote_urls=("http://200.144.255.210:8082/RTDB",)

urls=remote_urls
url=remote_urls[0]
metafiles=P.utils.getFiles(data_dir,".owl")
ids="gmane-", "_fb", "_tw"
c("identifiers= ",ids)
metafiles_=[i for i in metafiles if "gmane-" in i]
metafilesf=[i for i in metafiles if ids[1] in i] # FB
metafilest=[i for i in metafiles if ids[2] in i] # TW
metafiles__=metafiles_[8:12]
metafiles__=metafiles_[10:11]
metafiles__=metafiles_[10:11] +metafilesf[3:4]+metafilest[3:4]+metafilest[7:8]
service=P.sparql.EndpointInterface(url)
for metafile in metafiles__:
    service.addMetafileToEndpoint(metafile,autoid_graph=True)
    pass
service.insertOntology()
service.getGraphs()
if service.graphids:
    c(service.graphids)
service.getAllTriples()
c(len(service.triples))

service.getMetaGraphs()
c("metagraphs: ",service.metagraphids)
# put translationgraph of in each metagraph 
# and associate it to the metagraph
service.addTranslatesFromMetas()
# should be possible to get each meta, each translate and each 
# translate related to a meta
# should be easy to retrieve information values such as nUsers, nTranslates, Snapshot subclass, etc

# think of uses for updating and retrieving data
# take measures and place them in endpoint

# make CanonicSparQLInterface para herdar classe atual
# e talvez fazer uma classe anterior a atual para base de conexão com o endpoint

# retomar renderLegacy





