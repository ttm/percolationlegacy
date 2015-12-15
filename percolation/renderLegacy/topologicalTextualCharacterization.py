import percolation as P
c=P.utils.check

def rdfUnitsTable(end_url,fdir="./tables/",fname="rdfUnits.tex"):
    fname_=fdir+fname
    q="SELECT DISTINCT ?{} WHERE {{ GRAPH ?g {{ }} }}"; v="g"
    graphs=[i[0] for i in P.utils.mQuery(end_url,q,v)]
    mres=[]
    mress=[]
    mresp=[]
    mreso=[]
    for graph in graphs[:10]:
        c("check: " +graph)
        q='SELECT (COUNT(?s) as ?{{}})  WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'.format(graph)
        mres+=P.utils.mQuery(end_url,q,("cs",))[0]
        q='SELECT (COUNT(DISTINCT ?s) as ?{{}})  WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'.format(graph)
        mress+=P.utils.mQuery(end_url,q,("cs",))[0]
        q='SELECT (COUNT(DISTINCT ?p) as ?{{}})  WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'.format(graph)
        mresp+=P.utils.mQuery(end_url,q,("cs",))[0]
        q='SELECT (COUNT(DISTINCT ?o) as ?{{}})  WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'.format(graph)
        mreso+=P.utils.mQuery(end_url,q,("cs",))[0]
    labels=graphs[:10]
    labelsh="graph id","triples","subjects","predicates","objects"
    data=[[int(ii) for ii in [i,j,k,l]] for i,j,k,l in zip(mres,mress,mresp,mreso)]
    caption="count of RDF basic units"
    P.tableHelpers.lTable(labels,labelsh,data,caption,fname_,ttype="textGeral__")

