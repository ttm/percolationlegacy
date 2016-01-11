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

c=P.utils.check

data_dir="/disco/data/"
#remote_urls="http://200.144.255.210:8082/ds","http://200.144.255.210:8082/dsInference","http://200.144.255.210:8082/dsInference2","http://200.144.255.210:8082/dsInference3"
remote_urls="http://200.144.255.210:8082/ds","http://200.144.255.210:8082/dstdb",\
            "http://200.144.255.210:8082/books",\
            "http://200.144.255.210:8082/inf","http://200.144.255.210:8082/infEmpty",\
            "http://200.144.255.210:8082/infT","http://200.144.255.210:8082/infTEmpty",\

remote_urls="http://200.144.255.210:8082/ds","http://200.144.255.210:8082/dstdb",\
            "http://200.144.255.210:8082/REmpty","http://200.144.255.210:8082/RTDB",\

remote_urls="http://200.144.255.210:8082/REmpty","http://200.144.255.210:8082/RTDB"
remote_urls=("http://200.144.255.210:8082/RTDB",)

urls=remote_urls
urls=remote_urls
metafiles=P.utils.getFiles(data_dir,".owl")
c('identifiers="gmane-", "_fb", "_tw"')
metafiles_=[i for i in metafiles if "gmane-" in i]
metafiles__=metafiles_[10:11]
metafiles__=metafiles_[8:12]
services=[]
for url in urls:
    service=P.sparql.EndpointInterface(url)
    services+=[service]
    for metafile in metafiles__:
        service.addMetafileToEndpoint(metafile,autoid_graph=True)
        pass
#        service.getGraphs()
    #    services[-1].getGraphs()
for service in services:
    service.insertOntology()
    service.getGraphs()
    if service.graphs:
        c("\n\n","---> ",service.endpoint_url)
        c(service.graphs)
    service.getAllTriples()
    #service.renderDummyGraph()
    c(len(service.triples))

# partir somente da URI de informação.
# colocar nela as infos necessárias:
# 1) datadir
# 2) services online
# 3) update com info de cada graph, com nome, arquivo de origem, e grafos relacionados.



"""
c("hold baisc variables, like datadir, local and remote endpoint url")
local_urls="http://127.0.0.1:82/ds","http://127.0.0.1:82/dsInference","http://127.0.0.1:82/dsInference2","http://127.0.0.1:82/dsInference3"
local_urls="http://localhost:9082/ds/upload","http://localhost:9082/dsInference/dataInference","http://localhost:9082/dsInference2","http://localhost:9082/dsInference3"
#local_urls="http://localhost:9082/dsfoo",
remote_urls="http://200.144.255.210:8082/ds","http://200.144.255.210:8082/dsInference","http://200.144.255.210:8082/dsInference2","http://200.144.255.210:8082/dsInference3"
urls=local_urls
urls=remote_urls
data_dir="/disco/data/"
c("get all .*** file in tree")
metafiles=P.utils.getFiles(data_dir,".owl")
c('identifiers="gmane-", "_fb", "_tw"')
metafiles_=[i for i in metafiles if "gmane-" in i]
metafile=metafiles_[10]
graphnames=[]
for url in urls:
    P.sparql.addToFusekiEndpoint(url,[metafile])
    graphnames+=[P.utils.urifyFilename(metafile)]

gname=graphnames[0]
qq="SELECT "+"?{} "*2+"WHERE \
     {{ GRAPH <"+ gname +"> {{            \
   OPTIONAL {{ ?s <"+str(P.rdf.ns.po.interactionXMLFile)+">  ?if .}} . \
   OPTIONAL {{ ?s <"+str(P.rdf.ns.po.rdfFile)+">  ?if .}} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.friendshipXMLFile)+">  ?ff .}} . \
                 }} }}"
keys="if","ff"
vals=[]
for url in urls:
    vals+=P.utils.mQuery(url,qq,keys)
# load translates:
tgraphnames=[]
for url in urls:
    for files in vals:
        for file_ in files:
            if file_:
                fname_=file_.split("/")[-1]
                fname2="{}{}".format(data_dir,fname_)
                tgraphnames+=[P.utils.urifyFilename(fname2)]
                cmd="s-post {} {} {}".format(url, tgraphnames[-1], fname2)
                c(cmd)
                os.system(cmd)

# test the update to see how it delivers the zeros
# make rdfs of testing graphs
# write them back to the endpoint in the URL (through a-post if necessary).
"""
