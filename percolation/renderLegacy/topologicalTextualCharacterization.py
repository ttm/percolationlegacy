import percolation as P
c=P.utils.check
class Bootstrap:
    def __init__(self,endpoint_uri,data_dir="/disco/data/",fdir="/root/r/repos/documentation/"):
        """If fdir=None, don't render latex tables"""
        metafiles=P.utils.getFiles(datadir)
        foo=P.utils.addToEndpoint(metafiles)
        oi=self.getOverallInfos(metafiles)
        self.writeOverallTable(oi)
        # escrita de resumo no grafo de discovery principal
        self.writeOverallEndpoint(oi)
        # carrega translates nos grafos de nomes apropriados (tentar usar uris de snapshots)
        translates=self.loadTranslates(oi)
        # análise geral dos grafos, quais atributos, datas, etc
        analysis=self.overallAnalysis(translates)
        # ESCREVE TABELA
        self.writeOverallTable2(analysis)
        self.oi=oi
        self.translates=translates
        self.analysis=analysis
    def getOverallInfos(self,endpoint_url,metafiles):
        # analisa com os nomes, quantidades, proveniencias e demais infos do Meta
        pass
    def writeOverallTable(self,oi,fdir):
        pass
    def overallAnalysis(self,translates):
        pass
    def writeOverallTable2(self,analysis,fdir):
        pass
class Analyses:
    def __init__(self,bootstrap_instance,graphids):
        aa=[]
        for gid in graphids:
            aa+=Analysis(bootstrap,gid)
        self.aa=aa
    def overallMeasures(self,graphids):
        pass
class Analysis:
    def __init__(self,bootstrap_instance,graphid):
        self.boot=bootstrap
        # tudo para as estruturas totais:
        general_info=self.detailedGeneral()
        self.network=self.makeNetwork()
        self.users_sectors=self.getErdosSectorUsers()
        topological_info=self.topologicalMeasures()
        textual_info=self.textualMeasures()
        temporal_info=self.temporalMeasures()
        scalefree_info=self.scaleFreeTest()
        # explore different scales
    def detailedGeneral(self): pass
    def topologicalMeasures(self): pass
    def textualMeasures(self): pass
    def temporalMeasures(self): pass
    def scaleFreeTest(self): pass
class TimelineAnalysis:
    # make Analyses with input graphids
    # plot timelines
    # calculate unitary roots
    # make tables
    def unitaryRoot(self): pass
        unitary_info=self.unitaryRoot()
class MultiscaleAnalysis:
    # make Analyses with input graphids
    # find bet fit to scale free
    # plot some variables with respect to graphsize
    # render tables
    def multiScale(self): pass
        multiscale_info=self.multiScale()

def rdfUnitsTable(end_url,fdir="./tables/",fname="rdfUnits.tex",nrows=None):
    fname_=fdir+fname
    q="SELECT DISTINCT ?{} WHERE {{ GRAPH ?g {{ }} }}"; v="g"
    graphs=[i[0] for i in P.utils.mQuery(end_url,q,v)]
    if nrows:
        graphs=graphs[:nrows]
    graphs=sorted(graphs)
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

