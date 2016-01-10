__doc__="useful sparql queries or routines"

import time, os
import rdflib as r, networkx as x, percolation as P
from SPARQLWrapper import SPARQLWrapper, JSON
c=P.utils.check
NS=P.rdf.ns
a=P.rdf.ns.rdf.type
class endpointInterface():
    def __init__(self,endpoint_url):
        self.endpoint_url=endpoint_url
        self.spql_endpoint=SPARQLWrapper(endpoint_url)
        self.sparql.method = 'POST'
    def addFileToEndpoint(self,tfile,graphclass=None,autoid_graph=False):
        tgraph=P.utils.urifyFilename(tfile)
        cmd="s-post {} {} {}".format(self.endpoint_url, tgraph, tfile)
        c(cmd)
        os.system(cmd)
        c("Going to update endpoint on the info service")
        if not graphclass:
            graphclass=P.rdf.ns.po.Graph
        if autoid_graph:
            graphclass=P.utils.identifyProvenance(tfile)
        triples=(
                    (graphclass+"#"+tgraph,a,graphclass),
                )
        self.insertTriples(triples,tgraph)
    def insertTriples(self,triples,tgraph=None)
        lines=""
        for triple in triples:
            line=self.formatQueryLine(triple)
            lines+=line
        if tgraph:
            queryString = 'INSERT DATA { GRAPH <%s> { %s } }'%(disc_graph,lines)
        else:
            queryString = 'INSERT DATA {  %s  }'%(lines,)
        self.result=self.postQuery(querystring)
    def postQuery(querystring):
        sparql.setQuery(queryString) 
        return sparql.query()
    def formatQueryLine(triple):
        if isinstance(triple[2],(r.Namespace,r.URIRef)):
            return " <%s> <%s> <%s> . "
        else:
            return " <%s> <%s> %s . "


   def addOntology(self):
       triples=(
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

                (NS.gmane., NS.rdfs.subPropertyOf, NS.gmane),

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



def addToFusekiEndpoint(end_url,tfiles):
    aa=[]
    for tfile in tfiles:
        time.sleep(.1)
        tgraph=P.utils.urifyFilename(tfile)
        cmd="s-post {} {} {}".format(end_url, tgraph, tfile)
        c(cmd)
        aa+=[os.system(cmd)]; c("pos\n\n")

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
