__doc__="""generic routines that don't require a sparql connection"""

def buildQuery(triples1,graph1=None,triples2=None,graph2=None):
    """The general query builder from fields and respective triples or uris"""
    pass




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

def addToFusekiEndpoint(end_url,tfiles):
    aa=[]
    for tfile in tfiles:
        time.sleep(.1)
        tgraph=P.utils.urifyFilename(tfile)
        cmd="s-post {} {} {}".format(end_url, tgraph, tfile)
        aa+=[os.system(cmd)]




