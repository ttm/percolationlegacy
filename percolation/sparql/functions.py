__doc__="""generic routines that don't require a sparql connection"""
import percolation as P, rdflib as r
NS=P.rdf.NS
a=NS.rdf.type

def buildQuery(triples1,graph1=None,triples2=None,graph2=None,modifier1="",modifier2="",distinct1=None,method="select",startB_=None):
    """The general query builder from fields and respective triples or uris"""
    if isinstance(triples1,str):
        querystring=triples1
    elif isinstance(triples1,(tuple,list)):
        if distinct1:
            distinct1=" DISTINCT "
        if graph1:
            graphpart1=" GRAPH <%s> { "%(graph1,)
            body1close=" } } "
        else:
            graphpart1=""
            body1close=" } "
        if len(triples1[0])!=3:
            triples1=(triples1,)
        tvars=[]
        body=""
        for line in triples1:
            tvars+=[i for i in line if i[0]=="?" and "foo" not in i]
            body+=formatQueryLine(line)
        tvars=P.utils.uniqueItems(tvars)
        tvars_string=(" %s "*len(tvars))%tuple(tvars)
        if "select"==method.lower():
            start="SELECT "
            startB=tvars_string+" WHERE { "
        elif "insert"==method.lower():
            start="INSERT DATA "
            startB=" { "
        elif "insert_where"==method.lower():
            start="INSERT "
            startB=" { "
        elif method.lower()=="delete":
            pass
        if startB_:
            startB=startB_
        querystring=start+startB+graphpart1+body+body1close+modifier1
    if isinstance(triples2,str):
        querystring+=triples2
    elif isinstance(triples2,(tuple,list)):
        if graph2:
            graphpart2=" GRAPH <%s> { "%(graph2,)
            body2close=" } } "
        else:
            graphpart2=""
            body2close=" } "
        if len(triples2[0])!=3:
            triples2=(triples1,)
        body2=""
        for line in triples2:
            body2+=formatQueryLine(line)
        if "insert_where"==method.lower():
            start2=" WHERE  "
            startB2=" { "
            querystring+=start2+startB2+graphpart2+body2+body2close+modifier2
    return querystring

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
        elif (term[0]=="?") or (term[:2]=="_:"):
            line+=" %s "%(term,)
        elif isinstance(term,str) and term[0]!="?":
             line+=' "%s" '%(term,)
        else:
            line+=' "%s" '%(term,)
    line+= " . "
    return line

def addToFusekiEndpoint(end_url,tfiles):
    aa=[]
    for tfile in tfiles:
        time.sleep(.1)
        tgraph=P.utils.urifyFilename(tfile)
        cmd="s-post {} {} {}".format(end_url, tgraph, tfile)
        aa+=[os.system(cmd)]




