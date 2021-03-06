__doc__="""for querying the endpoint without loading and doing other stuff in sparqlTest.py."""
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
importlib.reload(P.sparql.functions)
NS=P.rdf.NS
a=NS.rdf.type
c=P.utils.check
PF=P.sparql.functions.plainQueryValues
DF=P.sparql.functions.dictQueryValues
data_dir="/disco/data/"
url="http://200.144.255.210:8082/RTDB"
url="http://127.0.0.1:9082/RTDB"

metafiles=P.utils.getFiles(data_dir,".owl")
metafiles_=P.utils.fileProvenanceDict(metafiles)
tfile=metafiles_["fb"][1]
tfile=metafiles_["fb"][-8]

si=sparql_interface=P.sparql.SparQLLegacy(url)
c("get ntriples in all graphs")
q="SELECT ?g (COUNT(?s) as ?co) WHERE { GRAPH ?g  { ?s ?p ?o . } } GROUP BY ?g "
res=si.retrieveQuery(q)
c("now the number of triples in the default/unnamed graph")
q="SELECT (COUNT(?s) as ?co) WHERE { ?s ?p ?o . } "
res2=si.retrieveQuery(q)

c("add local file to endpoint at aux graph")
si.addLocalFileToEndpoint(tfile,si.graphidAUX)
c("count again the number of triples in respective graphs")
qc="SELECT ?g (COUNT(?s) as ?co) WHERE { GRAPH ?g  { ?s ?p ?o . } } GROUP BY ?g "
res3=si.retrieveQuery(qc)

c("get snapshot in local file")
snapshot=[i for i in P.sparql.functions.performFileGetQuery(tfile,(("?s",a,NS.po.Snapshot),))][0][0]

c("insert few metadata triples in")
snapshotsubclass=P.utils.identifyProvenance(tfile)
triples=(
            (snapshot,a,snapshotsubclass), # Gmane, FB, TW, ETC
            (snapshot,NS.po.localDir,os.path.dirname(tfile)),
            (snapshot,NS.po.metaFilePath,tfile),
        )
c("perfortm insert")
si.insertTriples(triples,si.graphidAUX)

c("get localdir for snapshot from aux graph")
triples=(snapshot,NS.po.localDir,"?localdir"),
localdir=P.sparql.functions.plainQueryValues(  si.retrieveFromTriples(triples,graph1=si.graphidAUX))[0]
c("insert ontology in aux graph")
si.insertOntology(si.graphidAUX)

c("get translates")
triples=(snapshot,NS.po.defaultXML,"?translate"),
translates=PF(si.retrieveFromTriples(triples,graph1=si.graphidAUX))

c("make translates local filepath")
translates_local=[]
for translate in translates:
    fname=translate.split("/")[-1]
    fname2="{}/{}".format(localdir,fname)
    translates_local+=[fname2]
trans=translates_local[1]
c("add to the endpoint the translates local filepath")
si.addLocalFileToEndpoint(trans,si.graphidAUX)
c("retrieve triples that have po:Participants as their subjects")
select=(
        ("?as",a,NS.po.Participant),
        ("?as","?bp","?co"),
       )
participants1=PF(si.retrieveFromTriples(select,graph1=si.graphidAUX))
c("retrieve triples that have po:Participants as their objects")
select=(
        ("?cs",a,NS.po.Participant),
        ("?as3","?bp3","?cs"),
      )
participants2=PF(si.retrieveFromTriples(select,graph1=si.graphidAUX))
c("make localuris for substitution")
participants1_=[]
for tr_ in participants1:
    tr=tr_[:]
    genericuri=tr[0]
    newuri=genericuri+"-_-"+snapshot
    tr[0]=newuri
    tr2=newuri,NS.po.genericURI,genericuri,
    tr3=newuri,NS.po.snapshot,snapshot,
    participants1_+=[tr]+[tr2]+[tr3]
p1=set([i[0] for i in participants1])
participants2_=[]
for tr_ in participants2:
    tr=tr_[:]
    tr[2]=tr[2]+"-_-"+snapshot
    if tr[0] in p1:
        tr[0]=tr[0]+"-_-"+snapshot

    participants2_+=[tr]
c("insert new triples in graph AUX 2, ntriples=%s !!"%(len(participants1+participants2),)) # 2228 in 217 seconds
si.insertTriples(participants1_+participants2_,si.graphidAUX2)
# 0.02678 por query, 65s for ~2,3k triples TTM

c("update where in AUX to tag messages")
insert=("?m",NS.po.snapshot,snapshot),
where= ("?m",a,NS.po.InteractionInstance), # tw,gmane:message or fb interaction
querystring=P.sparql.functions.buildQuery(triples1=insert,graph1=si.graphidAUX,
                                          triples2=where,graph2= si.graphidAUX,method="insert_where")
c("perform update where")
si.updateQuery(querystring)
c("count number of messages or interactions")
select=("?m",a,NS.po.InteractionInstance)
querystring=P.sparql.functions.buildQuery(triples1=select,graph1=si.graphidAUX,method="select")
nInteractions=si.retrieveQuery(querystring)
c("nmessages=%s !!"%(len(participants1+participants2),)) # 2228 in 217 seconds
c("finish")

"""
Full run:
0.220 get ntriples in all graphs
0.079 now the number of triples in the default/unnamed graph
0.045 add local file to endpoint at aux graph
0.232 count again the number of triples in respective graphs
0.046 get snapshot in local file
0.021 insert few metadata triples in
0.000 perfortm insert
/usr/local/lib/python3.4/dist-packages/SPARQLWrapper/Wrapper.py:728: RuntimeWarning: unknown response content type, returning raw response...
warnings.warn("unknown response content type, returning raw response...", RuntimeWarning)
0.024 get localdir for snapshot from aux graph
0.015 insert ontology in aux graph
0.033 get translates
0.019 make translates local filepath
0.000 add to the endpoint the translates local filepath
0.288 retrieve triples that have po:Participants as their subjects
0.370 retrieve triples that have po:Participants as their objects
0.103 make localuris for substitution
0.036 insert new triples in graph AUX 2 !!
217.035 update where in AUX to tag messages
0.000 perform update where
0.019 count number of messages or interactions
0.013 finish

If the number of triples to insert is low, the time it takes is not so high:
0.227 get ntriples in all graphs
0.079 now the number of triples in the default/unnamed graph
0.042 add local file to endpoint at aux graph
0.264 count again the number of triples in respective graphs
0.042 get snapshot in local file
0.039 insert few metadata triples in
0.000 perfortm insert
/usr/local/lib/python3.4/dist-packages/SPARQLWrapper/Wrapper.py:728: RuntimeWarning: unknown response content type, returning raw response...
warnings.warn("unknown response content type, returning raw response...", RuntimeWarning)
0.021 get localdir for snapshot from aux graph
0.014 insert ontology in aux graph
0.032 get translates
0.020 make translates local filepath
0.000 add to the endpoint the translates local filepath
0.197 retrieve triples that have po:Participants as their subjects
0.100 retrieve triples that have po:Participants as their objects
0.024 make localuris for substitution
0.002 insert new triples in graph AUX 2, ntriples=106 !!
0.784 update where in AUX to tag messages
0.000 perform update where
0.017 count number of messages or interactions
0.014 nmessages=106 !!
0.000 finish

with Fuseki 2.3.1 and this config.tt file:
https://github.com/ttm/percolation/blob/master/misc/newConfigReasonersCombinedV.ttl



"""
