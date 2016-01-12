__doc__="useful sparql queries or routines"

import time, os
from IPython import embed
import rdflib as r, networkx as x, percolation as P
from SPARQLWrapper import SPARQLWrapper, JSON
c=P.utils.check
NS=P.rdf.NS
a=NS.rdf.type
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
def performFileGetQuery(tfile,triples=(("?s",a,NS.po.Snapshot),)):
    g=r.Graph()
    g.parse(tfile)
    tvars=[]
    body=""
    for line in triples:
        tvars+=[i for i in line if i[0]=="?" and "foo" not in i]
        body+=formatQueryLine(line)
    tvars=P.utils.uniqueItems(tvars)
    tvars_string=(" %s "*len(tvars))%tuple(tvars)
    querystring="SELECT "+tvars_string+" WHERE { "+body+" } "
    return g.query(querystring)
def formatQueryLine(triple):
    line=""
    for term in triple:
        if isinstance(term,(r.Namespace,r.URIRef)):
            line+=" <%s> "%(term,)
        elif term[0]=="?":
            line+=" %s "%(term,)
        elif isinstance(term,str) and term[0]!="?":
             line+=' "%s" '%(term,)
        else:
            line+=' "%s" '%(term,)
    line+= " . "
    return line

