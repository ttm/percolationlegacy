__doc__="useful sparql queries or routines"

import time, os
import rdflib as r, networkx as x, percolation as P
from SPARQLWrapper import SPARQLWrapper, JSON
c=P.utils.check
NS=P.rdf.ns
a=P.rdf.ns.rdf.type
class EndpointInterface:
    def __init__(self,endpoint_url):
        self.endpoint_url=endpoint_url
        self.endpoint=SPARQLWrapper(endpoint_url)
        self.endpoint.method = 'POST'
        self.endpoint.setReturnFormat(JSON)
    def addFileToEndpoint(self,tfile,snapshotclass=None,autoid_graph=False):
        tgraph=P.utils.urifyFilename(tfile)
        cmd="s-post {} {} {}".format(self.endpoint_url, "default", tfile)
        os.system(cmd)
        # ask in tgraph what is the snapshot uri
        query_triples=(
                ("?s",a,NS.po.Snapshot),
                )
        snapshot_uri=r.URIRef(self.getQuery(query_triples)["results"]["bindings"][0]["s"]["value"])

        if not snapshotclass:
            snapshotclass=P.rdf.ns.po.Snapshot
        if autoid_graph:
            snapshotclass=P.utils.identifyProvenance(tfile)
        triples=(
                    (snapshot_uri,a,snapshotclass),
                    (snapshot_uri,NS.po.graphName,tgraph),
                )
        c("\n\n{}\n\n".format(triples))
        self.insertTriples(triples)
    def getAllTriples(self):
        qtriples=(
                ("?s", "?p", "?o"),
                )
        self.triples=plainQueryValues(self.getQuery(qtriples))
    def getFoo(self):
        qtriples=(
                ("?snapshot", a, NS.po.BananaSnapshot),
                ("?snapshot", NS.po.graphName, "?graph"),
                )
        self.graphs=dictQueryValues(self.getQuery(qtriples))

    def getGraphs(self):
        qtriples=(
#                ("?snapshot", a, NS.po.Snapshot),
#                ("?snapshot", a, NS.po.InteractionSnapshot),
                ("?snapshot", a, NS.po.GmaneSnapshot),
                )
        self.graphs=dictQueryValues(self.getQuery(qtriples))
    def insertTriples(self,triples,graphid=None):
        lines=""
        for triple in triples:
            line=self.formatQueryLine(triple)
            lines+=line
        if graphid:
            querystring = 'INSERT DATA { GRAPH <%s> { %s } }'%(graphid,lines)
        else:
            querystring = 'INSERT DATA {  %s  }'%(lines,)
        self.result=self.postQuery(querystring)
    def getQuery(self,querystring_or_triples,graphid=None):
        if isinstance(querystring_or_triples,(tuple,list)):
            tvars=[]
            for line in querystring_or_triples:
                tvars+=[i for i in line if i[0]=="?"]
            tvars=P.utils.uniqueItems(tvars)
            tvars_string=(" %s "*len(tvars))%tuple(tvars)
            body=""
            for line in querystring_or_triples:
                body+=self.formatQueryLine(line)
            if graphid:
                querystring="SELECT "+tvars_string+" WHERE { GRAPH <"+graphid+"> { "+body+" } }"
            else:
                querystring="SELECT "+tvars_string+" WHERE { "+body+" } "
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
            else:
                line+=" '%s' "%(term,)
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

    def renderOntology(self,triples_dir="/disco/triplas/"):

        triples_=(
                (NS.po.InteractionSnapshot, a, NS.rdfs.Class),
                (NS.po.GmaneSnapshot, a, NS.rdfs.Class),
                (NS.po.Snapshot, a, NS.rdfs.Class),
                (NS.po.InteractionSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # fb, part, tw, irc, gmane, cidade
                (NS.po.GmaneSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),
                )
        triples=(
                (NS.po.InteractionSnapshot, a, NS.rdfs.Class),
                (NS.po.GmaneSnapshot, a, NS.rdfs.Class),
                (NS.po.Snapshot, a, NS.rdfs.Class),


                (NS.po.InteractionSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # fb, part, tw, irc, gmane, cidade
                (NS.po.FriendshipSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # fb, part
                (NS.po.ReportSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # aa

                (NS.po.FacebookSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot),
                (NS.po.FacebookInteractionSnapshot, NS.rdfs.subClassOf, NS.po.FacebookSnapshot),
                (NS.po.FacebookInteractionSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

                (NS.po.FacebookFriendshipSnapshot, NS.rdfs.subClassOf, NS.po.FacebookSnapshot),
                (NS.po.FacebookFriendshipSnapshot, NS.rdfs.subClassOf, NS.po.FriendshipSnapshot),

                (NS.po.TwitterSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

                (NS.po.GmaneSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

                (NS.po.IRCSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

                (NS.po.AASnapshot, NS.rdfs.subClassOf, NS.po.ReportSnapshot),

                (NS.po.ParticipaSnapshot, NS.rdfs.subClassOf, NS.po.CompleteSnapshot),

                (NS.po.CidadeDemocraticaSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

                (NS.gmane.gmaneID, NS.rdfs.subPropertyOf, NS.po.auxID),
                (NS.fb.groupID, NS.rdfs.subPropertyOf, NS.po.auxID),

                (P.rdf.ns.po.interactionXMLFile, NS.rdfs.subPropertyOf,NS.po.defaultXML), # fb
                (P.rdf.ns.po.rdfFile           , NS.rdfs.subPropertyOf,NS.po.defaultXML), # twitter, gmane
                (P.rdf.ns.po.friendshipXMLFile , NS.rdfs.subPropertyOf,NS.po.defaultXML), # fb
                # type of relation retrievement: 1, 2 or 3

                # labels equivalence: irc, etc
                # date equivalence
                # interaction/relation uris equivalence
                # textual content equivalence

                # if text is available
               )
        g=r.Graph()
        for triple in triples_:
            g.add(triple)
        f=open("{}po.ttl".format(triples_dir),"wb")
        f.write(g.serialize(format="turtle"))
        f.close()
        c("po ttl written")
        self.insertTriples(triples)


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

def plainQueryValues(result_dict):
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
                if result[key]["datatype"]==(P.rdf.ns.xsd.integer).toPython():
                    value=int(value)
                elif result[key]["datatype"]==(P.rdf.ns.xsd.datetime).toPython():
                    value=value
                else:
                    raise TypeError("Type of incomming variable not understood")
            else:
                raise TypeError("Type of incomming variable not understood")
            this_result+=[value]
        results+=[this_result]
    return results

