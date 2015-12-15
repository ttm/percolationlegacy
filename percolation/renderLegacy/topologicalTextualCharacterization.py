import percolation as P
c=P.utils.check

def rdfUnitsTable(end_url,fdir="./tables/",fname="rdfUnits.tex",nrows=None):
    fname_=fdir+fname
    q="SELECT DISTINCT ?{} WHERE {{ GRAPH ?g {{ }} }}"; v="g"
    graphs=[i[0] for i in P.utils.mQuery(end_url,q,v)]
    if nrows:
        graphs=graphs[:nrows]
    mres=[]
    mress=[]
    mresp=[]
    mreso=[]
    mresc=[]
    mresi=[]
    for graph in graphs:
        c("check: " +graph)
        q='''SELECT (COUNT(?s) as ?{{}}) (COUNT(DISTINCT ?s) as ?{{}})
                    (COUNT(DISTINCT ?p) as ?{{}}) (COUNT(DISTINCT ?o) as ?{{}})
                    WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'''.format(graph)
        mres_,mress_,mresp_,mreso_=P.utils.mQuery(end_url,q,("cs","ds","dp","do"))[0]
        q='''SELECT  (COUNT(DISTINCT ?c) as ?{{}}) (COUNT(DISTINCT ?i) as ?{{}})
                    WHERE {{{{ GRAPH <{}> {{{{ ?i a ?c }}}} }}}}'''.format(graph)
        mresc_,mresi_=P.utils.mQuery(end_url,q,("dc","di"))[0]
        mres+=[mres_]
        mress+=[mress_]
        mresp+=[mresp_]
        mreso+=[mreso_]
        mresc+=[mresc_]
        mresi+=[mresi_]
        #q='SELECT (COUNT(?s) as ?{{}})  WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'.format(graph)
        #mres+=P.utils.mQuery(end_url,q,("cs",))[0]
        #q='SELECT (COUNT(DISTINCT ?s) as ?{{}})  WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'.format(graph)
        #mress+=P.utils.mQuery(end_url,q,("cs",))[0]
        #q='SELECT (COUNT(DISTINCT ?p) as ?{{}})  WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'.format(graph)
        #mresp+=P.utils.mQuery(end_url,q,("cs",))[0]
        #q='SELECT (COUNT(DISTINCT ?o) as ?{{}})  WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'.format(graph)
        #mreso+=P.utils.mQuery(end_url,q,("cs",))[0]
    labels=[i.split("http://")[1][:-4] for i in graphs]
    labelsh="graph id","triples","subjects","predicates","objects", "classes","individuals"
    data=[[int(ii) for ii in [i,j,k,l,m,n]] for i,j,k,l,m,n in zip(mres,mress,mresp,mreso,mresc,mresi)]
    caption="count of RDF basic units"
    P.tableHelpers.lTable(labels,labelsh,data,caption,fname_,ttype="textGeral__")
    P.tableHelpers.doubleColumn(fname_)

