import percolation as P
c=P.utils.check

class Analysis:
    def __init__(self,endpoint_url,data_dir,final_dir):
        general_info,endpoint=P.config.boostrap(end_url,fdir)
        # tudo para as estruturas totais:
        general_info=self.detailedGeneral(end_url,general_info)
        topological_info=self.topologicalMeasures(end_url,general_info)
        textual_info=self.textualMeasures(end_url,general_info, topological_info)
        temporal_info=self.temporalMeasures(end_url,general_info, topological_info)
        unitary_info=self.unitaryRoot(end_url,general_info, topological_info)
        scalefree_info=self.scaleFreeTest(end_url,general_info, topological_info)
        # explore different scales
        multiscale_info=self.multiScale(end_url,general_info)
    def detailedGeneral(self): pass
    def topologicalMeasures(self): pass
    def textualMeasures(self): pass
    def temporalMeasures(self): pass
    def unitaryRoot(self): pass
    def scaleFreeTest(self): pass
    def bootstrapFuseki(endpoint_url,data_dir="/disco/data/",fdir="/root/r/repos/documentation/"):
        """If fdir=None, don't render latex tables"""
        # varre arquivos procurando "Meta"
        metafiles=getMetas(datadir)
        # adiciona ao endpoint grafo com nome via regra de formacao de URI ou URI de snapshot
        addToEndpoint(metafiles)
        # analisa com os nomes, quantidades, proveniencias e demais infos do Meta
        oi=getOverallInfos(metafiles)
        # ESCREVE TABELA
        writeOverallTable(oi)
        # escrita de resumo no grafo de discovery principal
        writeOverallEndpoint(oi)
        # carrega translates nos grafos de nomes apropriados (tentar usar uris de snapshots)
        translates=writeOverallEndpoint(oi)
        # análise geral dos grafos, quais atributos, datas, etc
        analysis=overallAnalysis(oi)
        # ESCREVE TABELA
        writeOverallTable2(analysis)
        # TERMINA BOOTSTRAP
        # mais um resumo total?
        return general_info, endpoint
        # análise de estabilidade e texto
        # teste de raiz unitária, medida de proximidade da livre de escala, expansão do pca, casos com múltiplas escalas


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

