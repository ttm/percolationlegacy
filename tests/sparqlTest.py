__doc__="""this file should hold test SparQL related routines\n
        
        designed for use with a Jena/Fuseki SparQL endpoint."""
import sys, os, time
keys=tuple(sys.modules.keys())
for key in keys:
    if "percolation" in key:
        print(key)
        del sys.modules[key]

import percolation as P, importlib
importlib.reload(P.utils)
importlib.reload(P.sparql)
importlib.reload(P.sparql.classes)
NS=P.rdf.NS
a=NS.rdf.type

c=P.utils.check

data_dir="/disco/data/"
url="http://200.144.255.210:8082/RTDB"
update_all=1
update_metas=0
update_translates=0
if update_all:
    update_translates=1
    update_metas=1
metafiles=P.utils.getFiles(data_dir,".owl")
metafiles_=P.utils.fileProvenanceDict(metafiles)
metafiles__=metafiles_["dummy_diversified"] # one from gmane, another from fb, another from tw
metafiles__=metafiles_["dummy2"] # three from gmane
metafiles__=metafiles_["all_ok"] # all metafiles from fb, tw, gmane
metafiles__=metafiles_["all_"] # all metafiles, including irc and eventual aa, participa and cidade democratica
metafiles__=metafiles_["dummy"] # one from gmane
metafiles__=metafiles_["fb"][-13:-12] # a small snapshot with both interaction and friendship
metafiles__=metafiles_["dummyfb"] # one from fb
metafiles__=metafiles_["fb"][1:2] # one small from fb
sparql_interface=P.sparql.SparQLLegacy(url)
sparql_interface.getNTriples()
c("n triples: ",sparql_interface.ntriples,"going to add metafiles")
for metafile in metafiles__:
    if update_metas:
        sparql_interface.addMetafileToEndpoint(metafile)
sparql_interface.getNTriples()
c("n triples with meta: ",sparql_interface.ntriples,"going to add metafiles")
sparql_interface.insertOntology()
sparql_interface.getNTriples()
c("n triples with ontology: ",sparql_interface.ntriples,"going to add metafiles")
sparql_interface.getSnapshots()
if sparql_interface.snapshots:
    c("snapshots: ",sparql_interface.snapshots)
if update_translates:
    sparql_interface.addTranslatesFromSnapshots()
    c("update_translates")
sparql_interface.getNTriples()
c("n triples with translates: ",sparql_interface.ntriples)

# should be possible to get each meta, each translate and each 
# translate related to a meta
# should be easy to retrieve information values such as nUsers, nTranslates, Snapshot subclass, etc

# think of uses for updating and retrieving data
# take measures and place them in endpoint

# make CanonicSparQLInterface para herdar classe atual
# e talvez fazer uma classe anterior a atual para base de conexão com o endpoint

# retomar renderLegacy
si=sparql_interface



