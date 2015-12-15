import rdflib as r, percolation as P, os, select, sys, time
c=P.utils.check
datadir="/disco/data/"
end_url="http://200.144.255.210:8082/dsfoo"

#q='SELECT (COUNT(?s) as ?{{}})  WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'.format(tgraph)
#            check(q)
#            res1=mQuery(end_url,q,("cs",))
#
#q='SELECT DISTINCT ?{{}} WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}} LIMIT 5'.format(tgraph)
#

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

# write as latex tables for the article
# migrate text latexHelpers to percolation
labels=graphs[:10]
labelsh="graph id","triples","subjects","predicates","objects"
data=[[int(ii) for ii in [i,j,k,l]] for i,j,k,l in zip(mres,mress,mresp,mreso)]
caption="count of RDF basic units"
filename="fooTableHere.tex"
P.tableHelpers.lTable(labels,labelsh,data,caption,filename,ttype="textGeral__")
#P.tableHelpers.lTable(labels,labelsh,data,caption,filename,ttype="kolmNull"):





sys.exit()
dirs=os.listdir(datadir)
aa=[]
for tdir in dirs:
    umbrelladir=datadir+tdir
    datasetdirs=os.listdir(umbrelladir)
    datasetdirs_=[i for i in datasetdirs if os.path.isdir("{}/{}".format(umbrelladir,i))]
    datasetdirs_=[i for i in datasetdirs_ if not i.startswith(".")]
    for datasetdir in datasetdirs_:
        rdfdir="{}/{}/rdf/".format(umbrelladir,datasetdir)
        files=os.listdir(rdfdir)
        for tfile in files:
            time.sleep(0.1)
            #c("typein 'qq' to quit loop")
            #key, o, e =select.select([sys.stdin],[],[],0.1)
            #if key=="qq":
            #    break
            if tfile.endswith(".owl"):
                tfile_=rdfdir+tfile 
                c(tfile_)
                # pegar do Meta o nome do snapshot para o tgraph
                tgraph="http://{}".format(tfile.replace("_","").lower())
#                cmd="s-put {} {} {}".format(end_url, tgraph, tfile_)
#                c(cmd)
                aa+=[os.system(cmd)]; c("pos")
#        else:
#            continue
#        break
#    else:
#        continue
#    break

