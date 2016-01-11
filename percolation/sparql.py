__doc__="useful sparql queries or routines"

import time, os
from IPython import embed
import rdflib as r, networkx as x, percolation as P
from SPARQLWrapper import SPARQLWrapper, JSON
c=P.utils.check
NS=P.rdf.NS
a=NS.rdf.type
class EndpointInterface:
    def __init__(self,endpoint_url):
        self.endpoint=SPARQLWrapper(endpoint_url)
        self.endpoint_url=endpoint_url
        self.endpoint.method = 'POST'
        self.endpoint.setReturnFormat(JSON)

    def addTranslatesFromMetas(self,metagraphids=None):
        if metagraphids==None:
            if not hasattr(self,"metagraphids"):
                self.getMetaGraphs()
            metagraphids=self.metagraphids
        # query each metagraph to get translates through ontology
        for metagraphid in metagraphids:
            self.addTranslatesFromMeta(metagraphid)
    def addTranslatesFromMeta(self,metagraphid):
        # busco SnapshotURI no grafo com o nome fo urified metagraphid
        triples=(
                    ("?foometagraph",NS.po.graphID,metagraphid),
                    ("?snapshot_uri",NS.po.metaGraph,"?foometagraph"),
                    ("?snapshot_uri",NS.po.localDir,"?localdir"),
                )
        snapshot_uri,localdir=plainQueryValues(self.performRetrieveQuery(triples))[0]
        #snapshot_uri,local_dir=plainQueryValues(self.performRetrieveQuery(triples))
#        embed()
        # com SnapshotURI pego no defaultgraph os translates
        triples=(
            (snapshot_uri, NS.po.defaultXML,"?xmlfilename"),
            )
        translates=plainQueryValues(self.performRetrieveQuery(triples))
        self.tmp=locals()
        # com os translates e o dir, carrego os translates
        for translate in translates:
            fname=translate.split("/")[-1]
            fname2="{}/{}".format(localdir,fname)
            graphid=self.addTranslationFileToEndpoint(fname2,metagraphid)
            # add the relation of po:associatedTranslate to the "graphs" graph
    def addTranslationFileToEndpoint(self,tfile,metagraphid):
        graphid=P.utils.urifyFilename(tfile)
        #http://purl.org/socialparticipation/po/AuxGraph#1
        graphid_=NS.po.AuxGraph+"#1"
        cmd="s-post {} {} {}".format(self.endpoint_url, graphid_, tfile)

        # make updates on auxgraph
        triples=(
                UPDATE=("?a",NS.po.referenceSnapshot,snapshot_uri)
              WHERE=  ("?a", a ,NS.po.Participant),
                ("?m", a ,NS.po.Message),
                )
        # write all triples from auxgraph to defaultgraph

        return graphid

    def addMetafileToEndpoint(self,tfile,snapshotclass=None,autoid_graph=True):
#        self.addFileToEndpoint(tfile)
        graphuri=self.addFileToEndpoint(tfile,None)
        # ask in tgraph what is the snapshot uri
        query_triples=(
                ("?s",a,NS.po.Snapshot),
                )
        snapshot_uri=r.URIRef(self.performRetrieveQuery(query_triples,graphuri)["results"]["bindings"][0]["s"]["value"])
        if autoid_graph:
            snapshotclass=P.utils.identifyProvenance(tfile)
        elif not snapshotclass:
            snapshotclass=NS.po.Snapshot
        triples=(
                    (snapshot_uri,a,snapshotclass), # Gmane, FB, TW, ETC
                )
        self.insertTriples(triples,graphuri)
        # add the existance of this graph to the "graphs" named graph
        triples=(
                    (snapshot_uri,NS.po.metaGraph,NS.po.NamedGraph+"#"+graphuri),
                    (snapshot_uri,NS.po.localDir,os.path.dirname(tfile)),
                    (NS.po.NamedGraph+"#"+graphuri,NS.po.localFilepath,tfile),
                    (NS.po.NamedGraph+"#"+graphuri,NS.po.graphID,graphuri),
                    (NS.po.NamedGraph+"#"+graphuri,a,NS.po.MetaNamedGraph),
                )
        self.insertTriples(triples,graphuri)
#        self.insertTriples(triples)
        self.graphuri=graphuri
        return graphuri

    def addFileToEndpoint(self,tfile,graphid="default"):
        if not graphid:
            graphid=P.utils.urifyFilename(tfile)
        cmd="s-post {} {} {}".format(self.endpoint_url, graphid, tfile)
        os.system(cmd)
        cmd="s-post {} {} {}".format(self.endpoint_url, "default", tfile)
        os.system(cmd)
        return graphid
    def getAllTriples(self,graphid=None):
        qtriples=(
                ("?s", "?p", "?o"),
                )
        if not graphid:
            self.triples=plainQueryValues(self.performRetrieveQuery(qtriples))
        else:
            self.triples=plainQueryValues(self.performRetrieveQuery(qtriples,graphid))
    def getMetaGraphs(self):
        qtriples=(
                ("?foonamedgraph", a, NS.po.NamedGraph),
                ("?foonamedgraph", NS.po.graphID, "?graphid"),
                )
        
        self.metagraphids=plainQueryValues(self.performRetrieveQuery(qtriples))
    def getGraphs(self):
        qtriples=(
#                ("?snapshot", a, NS.po.Snapshot),
#                ("?snapshot", a, NS.po.GmaneSnapshot),
#                ("?snapshot", a, NS.po.InteractionSnapshot),
                ("?snapshot", NS.po.graphID, "?graph"),
                )
        self.graphids=plainQueryValues(self.performRetrieveQuery(qtriples))
    def insertTriples(self,triples,graphid=None):
        lines=""
        for triple in triples:
            line=self.formatQueryLine(triple)
            lines+=line
        if graphid:
            self.insertTriples(triples)
            querystring = 'INSERT DATA { GRAPH <%s> { %s } }'%(graphid,lines)
        else:
            querystring = 'INSERT DATA {  %s  }'%(lines,)
        self.result=self.postQuery(querystring)
    def performRetrieveQuery(self,querystring_or_triples,graphid=None):
        if isinstance(querystring_or_triples,(tuple,list)):
            tvars=[]
            for line in querystring_or_triples:
                tvars+=[i for i in line if i[0]=="?" and "foo" not in i]
            tvars=P.utils.uniqueItems(tvars)
            tvars_string=(" %s "*len(tvars))%tuple(tvars)
            body=""
            for line in querystring_or_triples:
                body+=self.formatQueryLine(line)
            if graphid:

                querystring="SELECT "+tvars_string+" WHERE { GRAPH <"+graphid+"> { "+body+" } }"
            else:
                querystring="SELECT "+tvars_string+" WHERE { "+body+" } "
                #union=" UNION { GRAPH ?g { ?s ?p ?o } } "
                #querystring="SELECT DISTINCT %s WHERE { { %s } %s }"%(tvars_string,body,union)
                #union=" GRAPH ?anygraph "
                #querystring="SELECT %s WHERE { %s { %s }  }"%(tvars_string,union,body)
#                querystring="SELECT "+tvars_string+" WHERE { { "+body+" } "+union+" }"
        elif isinstance(querystring_or_triples,str):
            querystring=querystring_or_triples
        self.query=querystring
        self.endpoint.setQuery(querystring) 
        return self.endpoint.query().convert()
    def postQuery(self,querystring):
        self.endpoint.setQuery(querystring) 
        return self.endpoint.query().convert()
#        return self.endpoint.query()
    def formatQueryLine(self,triple):
        line=""
        for term in triple:
            if isinstance(term,(r.Namespace,r.URIRef)):
                line+=" <%s> "%(term,)
            elif term[0]=="?":
                line+=" %s "%(term,)
#            elif isinstance(term,str) and term[0]!="?":
#                line+=' "%s" '%(term,)
            else:
                line+=' "%s" '%(term,)
        line+= " . "
        return line
    def renderDummyGraph(self,triples_dir="/disco/triplas/"):
        self.getAllTriples()
        g=r.Graph()
        for triple in self.triples:
            if not isinstance(triple[2],r.URIRef):
                triple[2]=r.Literal(triple[2])
            g.add(triple)
        f=open("{}dummy.ttl".format(triples_dir),"wb")
        f.write(g.serialize(format="turtle"))
        f.close()
        c("dummy ttl written")

    def insertOntology(self,triples_dir="/disco/triplas/",graphid=None):
        self.insertTriples(P.rdf.makeOntology(),graphid)

def addToFusekiEndpoint(end_url,tfiles):
    aa=[]
    for tfile in tfiles:
        time.sleep(.1)
        tgraph=P.utils.urifyFilename(tfile)
        cmd="s-post {} {} {}".format(end_url, tgraph, tfile)
        aa+=[os.system(cmd)]

def makeNetwork(endpoint_url,relation_uri,label_uri=None,rtype=1,directed=False):
    """Make network from data SparQL queried in endpoint_url.

    relation_uri hold the predicate uri to which individuals are the range or oboth range and domain.
    label_uri hold the predicate to which the range is the label (e.g. name or nick) of the individual.
    rtype indicate which type of structure to be queried, as exposed in:
    http://ttm.github.io/doc/semantic/report/2015/12/05/semantic-social-networks.html
    directed indicated weather the resulting network is a digraph or not."""
    sparql = SPARQLWrapper(endpoint_url)
    if label_uri:
       mvars="i1","l1","i2","l2"
       label_qpart="""?i1  {} ?l1 .
                      ?i2  {} ?l2 .""".format(label_uri,label_uri)
    else: 
       mvars="i1","i2"
       label_qpart=""
    tvars=" ".join(["?{}" for i in mvars])
    if rtype==1: # direct relation 
        query="""SELECT  {}
                       WHERE {{ ?i1  {} ?i2 .
                                     {}      }}""".format(tvars,relation_uri,label_qpart)
    elif rtype==2: # mediated relation
        query="""SELECT  {} 
                       WHERE {{ ?foo  {} ?i1 .
                                ?foo  {} ?i2 .
                                      {}      }}""".format(tvars,relation_uri,relation_uri,label_qpart)
    elif rtype==3: # twice mediated relation
        query="""SELECT  {} 
                       WHERE {{ ?foo  ?baz ?bar .
                                ?foo   {} ?i1 .
                                ?bar   {} ?i2 .
                                       {}      }}""".format(tvars,relation_uri,relation_uri,label_qpart)
    else:
        raise ValueError("rtype --> {} <-- not valid".format(rtype))
    c("query build ok")
    res=P.utils.mQuery(sparql,query,mvars)
    c("response received")
    if directed:
        dg=x.DiGraph()
    else:
        dg=x.Graph()
    for rel in res:
        id1,l1,id2,l2=rel
        if dg.has_node(id1): dg.node[id1]["weight"]+=1.
        else:       dg.add_node(id1,label=l1,weight=1.)

        if dg.has_node(id2): dg.node[id2]["weight"]+=1.
        else:       dg.add_node(id2,label=l2,weight=1.)

        if dg.has_edge(id1,id2): dg[id1][id2]["weight"]+=1.
        else:       dg.add_edge(id1,id2,weight=2.)
    c("graph done")
    return dg
def dictQueryValues(result_dict):
    keys=result_dict["head"]["vars"]
    results=[]
    for result in result_dict["results"]["bindings"]:
        this_result={}
        for key in keys:
            value=result[key]["value"]
            type_=result[key]["type"]
            if type_=="uri":
                value=r.URIRef(value)
            elif type_=="literal":
                pass
            else:
                raise TypeError("Type of incomming variable not understood")
            this_result[key]=[value]
        results+=[this_result]
    return results

def plainQueryValues(result_dict,join_queries=False):
    """Return query values as simplest list.
    
    Set join_queries="hard" to keep list of lists structure
    when each result hold only one variable"""

    keys=result_dict["head"]["vars"]
    results=[]
    for result in result_dict["results"]["bindings"]:
        this_result=[]
        for key in keys:
            value=result[key]["value"]
            type_=result[key]["type"]
            if type_=="uri":
                value=r.URIRef(value)
            elif type_ in ("literal","bnode"):
                pass
            elif type_=="typed-literal":
                if result[key]["datatype"]==(NS.xsd.integer).toPython():
                    value=int(value)
                elif result[key]["datatype"]==(NS.xsd.datetime).toPython():
                    pass
                elif result[key]["datatype"]==(NS.xsd.date).toPython():
                    pass
                elif result[key]["datatype"]==(NS.xsd.boolean).toPython():
                    if value=="true":
                        value=True
                    elif value=="false":
                        value=False
                    else:
                        raise TypeError("Incomming boolean not understood")
                else:
                    raise TypeError("Incomming typed-literal variable not understood")
            else:
                raise TypeError("Type of incomming variable not understood")
            this_result+=[value]
        results+=[this_result]
    if len(results) and len(keys)==1 and join_queries !="hard":
        results=[i[0] for i in results]
    return results

