__doc__="""

NOTES:
    INSERTs and DELETEs without a WHERE clause have the DATA keyword: INSERT DATA { ... } DELETE DATA { ... }.
    DELETE INSERT WHERE queries can't swap to INSERT DELETE WHERE. (The DELETE WHERE is in fact a D I W query without I) 
    
    Even so, I cant get this query to work: DELETE  {  GRAPH <http://purl.org/socialparticipation/po/AuxGraph#1> {  ?s  ?p  ?o  .  } }  INSERT  {      GRAPH <urn:x-arq:DefaultGraph> {  ?s  ?p  ?o  .  } }  WHERE   {  GRAPH <http://purl.org/socialparticipation/po/AuxGraph#1> {  ?s  <http://purl.org/socialparticipation/po/snapshot>  <http://purl.org/socialparticipation/po/Snapshot#GeorgeSanders08032014_fb>  .  } } '

    URI: tdb:unionDefaultGraph the union graph (don't seem to work now, maybe bugged)
    URI: urn:x-arq:DefaultGraph the default graph (seem to work)

    Legacy have had to split delete insert where query in 2: a insert where and delete where because of the bug above.


    
"""

import os
import rdflib as r, networkx as x, percolation as P
from SPARQLWrapper import SPARQLWrapper, JSON
c=P.utils.check
NS=P.rdf.NS
a=NS.rdf.type


class SparQLEndpoint:
    """Fuseki connection maintainer through rdflib"""
    def __init__(self,endpoint_url):
        self.endpoint=SPARQLWrapper(endpoint_url)
        self.endpoint_url=endpoint_url
        self.endpoint.method = 'POST'
        self.endpoint.setReturnFormat(JSON)
    def addLocalFileToEndpoint(self,tfile,tgraph="default"):
        cmd="s-post {} {} {}".format(self.endpoint_url,tgraph,tfile)
        os.system(cmd)
    def restablishConnection(self,endpoint_url=None):
        if not endpoint_url:
            endpoint_url=self.endpoint_url
        self.endpoint=SPARQLWrapper(endpoint_url)
        self.endpoint_url=endpoint_url
        self.endpoint.method = 'POST'
        self.endpoint.setReturnFormat(JSON)
class SparQLQueries:
    """Covenience class for inheritance with SparQLEndpoint and SparQLLegacy"""
    def clearEndpoint(self,tgraph=None):
        if tgraph:
            query="CLEAR GRAPH <%s>"%(tgraph,)
        else:
            query="CLEAR DEFAULT"
        self.updateQuery(query)
    def addRepmoteFileToEndpoint(self,remote_file_url,tgraph=None):
        part1="LOAD <%s> "%(remote_file_url)
        if tgraph:
            part2=" [ INTO <%s> ] "%(tgraph,)
        query=part1+part2
        self.updateQuery(query)
        raise NotImplementedError("Need to validate. Never been used")
    def insertTriples(self,triples,graph1=None):
        querystring=P.sparql.functions.buildQuery(triples,graph1=graph1,method="insert")
        self.result=self.updateQuery(querystring)
    def retrieveFromTriples(self,triples,graph1=None,modifier1="",startB_=None):
        querystring=P.sparql.functions.buildQuery(triples,graph1=graph1,modifier1=modifier1,startB_=startB_)
        return self.retrieveQuery(querystring)
    def retrieveQuery(self,querystring):
        """Query for retrieving information (e.g. through select)"""
         # self.method=POST
        return self.performQuery(querystring)
    def updateQuery(self,querystring):
        """Query to insert, delete and modify knowledge https://www.w3.org/Submission/SPARQL-Update/"""
         # self.method=POST
        return self.performQuery(querystring)
    def performQuery(self,querystring):
        """Query method is defined at SparQLEndpoint initialization."""
         # self.method=POST
        self.endpoint.setQuery(querystring) 
        return self.endpoint.queryAndConvert()
    def getAllTriples(self,graph1=None):
        qtriples=(("?s", "?p", "?o"),)
        self.ntriples=P.sparql.functions.plainQueryValues(self.retrieveFromTriples(qtriples,graph1=graph1,startB_=" (COUNT(*) as ?nt) WHERE { "))
    def insertOntology(self):
        self.insertTriples(P.rdf.makeOntology())
        # self.getAllTriples(), P.utils.writeTriples(self.triples,"{}dummy.ttl".format(triples_dir))

class SparQLLegacyConvenience:
    """Convenience class for query and renderind analysis strictures, tables and figures"""
    graphidAUX=NS.po.AuxGraph+"#1"
    def __init__(self):
        ontology_triples=P.rdf.makeOntology()
        self.insertTriples(ontology_triples,self.graphidAUX) # SparQLQueries TTM
        self.getAllTriples(self.graphidAUX)
        self.ntriplesAUX=self.ntriples
        triples=("?s","?p","?o")
        self.alltriplesAUX=self.retrieveFromTriples(triples,graph1=self.graphidAUX)
    def getSnapshots(self,snaphot_type=None):
        if not snaphot_type:
            uri=NS.po.Snapshot
        else:
            uri=eval("NS.po.{}Snapshot".format(snaphot_type.title()))
            # NS.po.InteractionSnapshot, NS.po.GmaneSnapshot
        triples=(("?snapshot", a, uri),)
        self.snapshots=P.sparql.functions.plainQueryValues(self.retrieveFromTriples(triples)) # SparQLQuery
    def addTranslatesFromSnapshots(self,snapshots=None):
        if snapshots==None:
            if not hasattr(self,"snapshots"):
                self.getSnapshots()
            snapshots=self.snapshots
        # query each snapshot to get translates through ontology
        for snapshot in snapshots:
            self.addTranslatesFromSnapshot(snapshot)
    def addTranslatesFromSnapshot(self,snapshot):
        # busco localdir e translates (GROUP BY?)
        triples=(snapshot,NS.po.defaultXML,"?translate"),
        translates=P.sparql.functions.plainQueryValues(self.retrieveFromTriples(triples))
        triples=(snapshot,NS.po.localDir,"?localdir"),
        localdir=P.sparql.functions.plainQueryValues(self.retrieveFromTriples(triples))[0]
        self.tmp=locals()
        # com os translates e o dir, carrego os translates
        c("into translates from snapshot")
#        P.utils.callDebugger()
        for translate in translates:
            fname=translate.split("/")[-1]
            fname2="{}/{}".format(localdir,fname)
            graphid=self.addTranslationFileToEndpoint(fname2,snapshot)
            # add the relation of po:associatedTranslate to the "graphs" graph
    def addTranslationFileToEndpoint(self,tfile,snapshot):
        #http://purl.org/socialparticipation/po/AuxGraph#1
        self.addLocalFileToEndpoint(tfile,self.graphidAUX)
        c("first insert")
        insert=(
                ("_:mblank",a,NS.po.ParticipantAttributes),
                ("_:mblank",NS.po.participant,"?i"),
                ("_:mblank","?p","?o"),
                ("_:mblank",NS.po.snapshot,snapshot),
               )
        where=(
                ("?i1",a,NS.po.Participant),
                ("?i1","?p","?o"),
              )
        querystring=P.sparql.functions.buildQuery(triples1=insert,graph1=self.graphidAUX,triples2=where,graph2=self.graphidAUX,method="insert_where")
        self.updateQuery(querystring)

        c("second insert")
        insert=("?m",NS.po.snapshot,snapshot),
        where= ("?m",a,NS.po.InteractionInstance), # tw,gmane:message or fb interaction
        querystring=P.sparql.functions.buildQuery(triples1=insert,graph1=self.graphidAUX,triples2=where,graph2=self.graphidAUX,method="insert_where")
        self.updateQuery(querystring)

#        querystring="MOVE <%s> TO DEFAULT"%(self.graphidAUX,)
        c("graph move")
        insert=("?s","?p","?o") # DEFAULT
        delete=("?s","?p","?o") # aux
        where=("?s",NS.po.snapshot,snapshot) # aux
        querystring=P.sparql.functions.buildQuery(
                                                  #triples1=delete,graph1=self.graphidAUX,
                                                  #triples2=insert,graph2="urn:x-arq:DefaultGraph",#graph2="DEFAULT",
                                                  triples1=insert,graph1="urn:x-arq:DefaultGraph",#graph2="DEFAULT",
                                                  triples2=delete,graph2=self.graphidAUX,
                                                  triples3=where,graph3=self.graphidAUX,
                                                  method="delete_insert_where")
        # tentar soh o insert depois 
        # tentar soh o delete depois 
        self.updateQuery(querystring)
        self.mquery=querystring
        self.getAllTriples(self.graphidAUX)
        if self.ntriples==self.ntriplesAUX:
            c("graphAUX restored correctly")
        else:
            c("somethig went wrong in restoring graphidAUX")
            self.ntriplesAUX2=self.ntriples
            triples=("?s","?p","?o")
            self.alltriplesAUX2=self.retrieveFromTriples(triples,graph1=self.graphidAUX)
        c("insert triple to default")
        triples=(snapshot,NS.po.translateFilePath,tfile),
        self.insertTriples(triples)
        c("end of translation add")
#        querystring=P.sparql.functions.buildQuery(triples,method="insert")
        # if empty afterwards, make dummy inference graph to copy triples from or load rdfs file
    def addMetafileToEndpoint(self,tfile):
        self.addLocalFileToEndpoint(tfile) # SparQLQueries
        snapshoturi=[i for i in P.sparql.functions.performFileGetQuery(tfile,(("?s",a,NS.po.Snapshot),))][0][0]
        snapshotsubclass=P.utils.identifyProvenance(tfile)
        triples=(
                    (snapshoturi,a,snapshotsubclass), # Gmane, FB, TW, ETC
                    (snapshoturi,NS.po.localDir,os.path.dirname(tfile)),
                    (snapshoturi,NS.po.metaFilepath,tfile),
                )
        self.insertTriples(triples) # SparQLQueries
    def makeNetwork(self,relation_uri,label_uri=None,rtype=1,directed=False):
        """Make network from data SparQL queried in endpoint_url.

        relation_uri hold the predicate uri to which individuals are the range or oboth range and domain.
        label_uri hold the predicate to which the range is the label (e.g. name or nick) of the individual.
        rtype indicate which type of structure to be queried, as exposed in:
        http://ttm.github.io/doc/semantic/report/2015/12/05/semantic-social-networks.html
        directed indicated weather the resulting network is a digraph or not."""
        sparql=self.endpoint
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

class SparQL(SparQLEndpoint,SparQLQueries):
    """Class that holds sparql endpoint connection and convenienves for query"""
    def __init__(self,endpoint_url):
        SparQLEndpoint.__init__(self,endpoint_url)
class SparQLLegacy(SparQLEndpoint,SparQLQueries,SparQLLegacyConvenience):
    """Class that holds sparql endpoint connection and convenienves for query and renderind analysis strictures, tables and figures"""
    def __init__(self,endpoint_url):
        SparQLEndpoint.__init__(self,endpoint_url)
        SparQLLegacyConvenience.__init__(self)


