import percolation as P, networkx as x, os, re
from SPARQLWrapper import SPARQLWrapper, JSON
c=P.utils.check
class Bootstrap:
    def __init__(self,endpoint_url,data_dir="/disco/data/",fdir="/root/r/repos/documentation/"):
        """If fdir=None, don't render latex tables"""
        self.res=[]
        self.trans={}
        metafiles=P.utils.getFiles(data_dir)[:1]
        metagnames=[P.utils.urifyFilename(i) for i in metafiles]
        foo=P.utils.addToEndpoint(endpoint_url,metafiles)
        oi=self.getOverallInfos(endpoint_url,metagnames)
        dirnames=[os.path.dirname(i) for i in metafiles]
        self.metagnames=metagnames
        self.metafiles=metafiles
        self.writeOverallTable()
        self.writeOverallEndpoint(endpoint_url)
        translates=self.loadTranslates(endpoint_url)
        self.endpoint_url=endpoint_url
#        analysis=self.overallAnalysis(endpoint_url)
    def extra(self):
        # ESCREVE TABELA
        self.writeOverallTable2(analysis)
        self.oi=oi
        self.translates=translates
        self.analysis=analysis
    def overallAnalysis(self,endpoint_url):
        """Withour use for now"""
        # análise geral dos grafos, quais atributos, datas, etc
        qq="SELECT "+"(COUNT(?s) as ?{}) (COUNT(DISTINCT ?s) as ?{}) (COUNT(DISTINCT ?p) as ?{}) (COUNT(DISTINCT ?o) as ?{}) WHERE \
         {{ GRAPH <"+ gname +"> {{            \
                ?s ?p ?o .        \
         }} }}"
        keys="ntrip","nsubj","npred","nobj"
        vals=P.utils.mQuery(endpoint_url,qq,keys)[0]
        bdict={i:j for i,j in zip(keys,vals)}



    def loadTranslates(self,endpoint_url):
        """Load each of the translate files into appropriate graphs"""
        c("LT")
        for gname,fname in zip(self.metagnames,self.metafiles):
            c("LT %s %s"%(gname,fname))
            qq="SELECT "+"?{} "*2+"WHERE \
                 {{ GRAPH <"+ gname +"> {{            \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.interactionXMLFile)+">  ?if .}} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.friendshipXMLFile)+">  ?ff .}} . \
                 }} }}"
            keys="if","ff"
            vals=P.utils.mQuery(endpoint_url,qq,keys)[0]
            vals=[i for i in vals if i]
            for val in vals:
                c("LT val %s "%(val,))
                fname_=val.split("/")[-1]
                dname=os.path.dirname(fname)
                fname2="{}/{}".format(dname,fname_)
                guri=P.utils.urifyFilename(fname_)
                cmd="s-put {} {} {}".format(endpoint_url, guri, fname2)
                c(cmd)
                os.system(cmd)
                if guri in self.trans.keys():
                    self.trans[guri]+=[val]
                else:
                    self.trans[guri]=[val]
    def writeOverallEndpoint(self,endpoint_url):
        """Write to po:discovery graph"""
        # faz query dos snapshots, pega os TranslationXML
        # cgt
        disc_graph=P.rdf.ns.po.DiscoveryGraph+"#"+"Foo"
        for gname,fname in zip(self.metagnames,self.metafiles):
            # insert the metafile in the discovery foo
            cmd="s-put {} {} {}".format(endpoint_url, disc_graph, fname)
            os.system(cmd)
            snapshot=P.rdf.ns.po.Snapshot+"#"+fname.split("/rdf/")[0].split("/")[-1]
            # link snapshot to local adresses of discovery and translation
            # and to the smaller preffered label
            # add totals to the sparql discovery
            fdir=os.path.dirname(fname)
            files=os.listdir(fdir)
            files=["{}/{}".format(fdir,i) for i in files if ((("Interaction" in i) or ("Friendship" in i) or ("Translate" in i)) and i.endswith(".owl"))]
            tgnames=[]
            for tfile in files:
                tgname=P.utils.urifyFilename(tfile,digits=False)
                cmd="s-put {} {} {}".format(endpoint_url, tgname, tfile)
                os.system(cmd)
                tgnames+=[tgname]
            ss=""
            for afile in files:
                ss+='<%s> <%s> "%s" . '%(snapshot,P.rdf.ns.po.localTranslationFile,afile)
            for tgname in tgnames:
                ss+='<%s> <%s> "%s" . '%(snapshot,P.rdf.ns.po.translationGraph,tgname)
            queryString = 'INSERT DATA { GRAPH <%s> { \
                           <%s> <%s> "%s" . \
                           <%s> <%s> "%s" . \
                             %s \
                            } }'%(
                                    disc_graph,
                                   snapshot,P.rdf.ns.po.localDiscoveryFile,fname,
                                   snapshot,P.rdf.ns.po.discoveryGraph,gname,
                                   ss
                                 )
            sparql = SPARQLWrapper(endpoint_url)

            sparql.setQuery(queryString) 
            sparql.method = 'POST'
            sparql.query()
            # adicionar o proprio meta no discovery
    def writeOverallTable(self):
        labels=[self.odict[i]["label"].split(" ")[-1].replace("_","\_") for i in self.metagnames]+["TOTAL"]
        labelsh="label","participants","iparticipants","interactions","relations","from","ego","friendship","anon","interaction","anon"
        data=[[self.odict[i][avar] for avar in ("nf","nfi","ni","nfs","ca","ego","f","fa","i","ia")] for i in self.metagnames]
        total=[0,0,0,0,0,0,0,0,0,0]
        for dt in data:
            for i in range(4):
                total[i]+=int(dt[i])
            for i in range(5,10):
                total[i]+=(dt[i]=="true")
        data+=[[str(i) for i in total[:4]]+["-"]+["{}/{}".format(i,len(data)) for i in total[5:]]]
        caption="overview of social datasets"
        P.tableHelpers.lTable(labels,labelsh,data,caption,"tryMe2TT.tex",ttype="strings")
        P.tableHelpers.doubleColumn("tryMe2TT.tex")


    def getOverallInfos(self,endpoint_url,metagnames):
        """analisa com os nomes, quantidades, proveniencias e demais infos do Meta"""
        self.odict={}
        for gname in metagnames:
            # faz query para saber a proveniencia
            # pega alguns dados basicos
            # pega endereco dos translates
            if "gmane" in gname:
                plat="Gmane"
            else:
                qq="SELECT ?{}  WHERE {{ GRAPH <"+ gname +"> {{ ?s <"+str(P.rdf.ns.po.socialProtocol)+"> ?n . }} }}"
                plat=P.utils.mQuery(endpoint_url,qq,("n",))[0][0]
            if plat.endswith("Facebook"):
                qq="SELECT "+"?{} "*13+"WHERE \
                 {{ GRAPH <"+ gname +"> {{            \
                        ?s <"+str(P.rdf.ns.po.createdAt)+">  ?ca .        \
                        ?s <"+str(P.rdf.ns.fb.ego)+">  ?ego .        \
                        ?s <"+str(P.rdf.ns.fb.friendship)+">  ?f .        \
                        ?s <"+str(P.rdf.ns.fb.fAnon)+">  ?fa .        \
                        ?s <"+str(P.rdf.ns.fb.interaction)+">  ?i .        \
                        ?s <"+str(P.rdf.ns.fb.iAnon)+">  ?ia .        \
                        ?s <"+str(P.rdf.ns.rdfs.label)+">  ?label .        \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.nFriends)+"> ?nf .            }} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.nFriendships)+">  ?nfs .      }} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.nInteractions)+">  ?ni .     }} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.nFriendsInteracted)+">  ?nfi .}} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.nFriendsInteracted)+">  ?nfi .}} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.friendshipXMLFile)+">  ?ffile .}} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.interactionXMLFile)+">  ?ifile .}} . \
                 }} }}"
                keys="nf","nfs","ni","nfi","ca","ego","f","fa","i","ia","ffile","ifile","label"
                vals=P.utils.mQuery(endpoint_url,qq,keys)[0]
                bdict={i:j for i,j in zip(keys,vals)}
                self.odict[gname]=bdict

    def writeOverallTable2(self,analysis,fdir):
        pass
class Analyses:
    """Calculate unit roots, PCA averages and deviations and best fit to scale-free"""
    def __init__(self,bootstrap_instance,graphids=[]):
        if not graphids:
            graphids=list(bootstrap_instance.trans.keys())
        aa=[]
        for gid in graphids:
            aa+=[Analysis(bootstrap_instance,gid)]
        self.aa=aa
    def overallMeasures(self,graphids):
        pass
class Analysis:
    """The analysis of one and only network.
    The rendering of tables and figures is left for the Analyses class
    """
    def __init__(self,bootstrap_instance,graphid=None):
        if graphid==None:
            graphid=list(bootstrap_instance.trans.keys())[0]
        self.graphid=graphid
        self.boot=bootstrap_instance
        # tudo para as estruturas totais:
        self.network=self.makeNetwork()
        general_info=self.detailedGeneral()
        self.users_sectors=self.getErdosSectorsUsers()
        topological_info=self.topologicalMeasures()
        textual_info=self.textualMeasures()
        temporal_info=self.temporalMeasures()
        scalefree_info=self.scaleFreeTest()
        # explore different scales
    def makeNetwork(self):
        """Build network from endpoint through simple criteria."""
        # see what procedence: FB, TW, IRC, Email, etc
        ftype=re.findall(r"\d+fb(friendship|interaction)",self.graphid)
        if ftype:
            plat="Facebook"
            if ftype[0]=="interaction":
                query= "SELECT ?{} ?{} ?{} WHERE \
                 {{ GRAPH <"+ self.graphid +"> {{            \
                 ?s fb:iFrom ?from .        \
                 ?s fb:iTo ?to .        \
                 ?s fb:weight ?weight .        \
                 }} }}"
                keys="from","to","weight"

            if ftype[0]=="friendship":
                query= "SELECT ?{} ?{} WHERE \
                 {{ GRAPH <"+ self.graphid +"> {{            \
                 ?f1 fb:friend ?f2 .        \
                 }} }}"
                keys="f1","f2"
        vals=P.utils.mQuery(self.boot.endpoint_url,query,keys)
        if len(vals[0])==3:
            gg=x.DiGraph()
            for val in vals:
                gg.add_edge(val[0],val[1],weight=int(val[2]))
            gg_=P.utils.toUndirected(gg)
            comp=x.weakly_connected_component_subgraphs(gg)[0]
            comp_=x.connected_component_subgraphs(gg_)[0]
        else:
            gg=x.Graph()
            for val in vals:
                gg.add_edge(val[0],val[1])
            comp=x.connected_component_subgraphs(gg)[0]
            gg_=gg
            comp_=comp
        self.gg=gg
        self.gg_=gg_
        self.comp=comp
        self.comp_=comp_
    def detailedGeneral(self):
        """A detailed info about one and only graph.

        Information about date, number of friends, friendships,
        interactions, etc.
        Average degree, average clustering, etc.
        ToDo: implement homophily
        """
        # clustering, weighted clustering (ou só transitivity)
        # average clustering e square clustering
        degrees=self.gg.degree()
        strengths=self.gg.degree(weight="weight")
        aclustering=x.average_clustering(self.gg_)
        aclustering_w=x.average_clustering(self.gg_,weight="weight")
        square_clustering=x.square_clustering( self.gg)
        transitivity=x.transitivity(self.gg)
        transitivity_u=x.transitivity(self.gg_)
        closeness=x.closeness_centrality(self.gg)
        # eccentricity
        eccentricity=x.closeness_centrality(self.gg_)
        # diameter/radius
        diameter=x.diameter(self.comp_)
        radius=x.radius(    self.comp_)
        # nperiphery ncenter
        nperiphery=x.periphery(self.comp_)
        ncenter=x.center(self.comp_)
        size_component=self.comp_.number_of_nodes()
        # average shortest path
        ashort_path=x.average_shortest_path_length(   self.comp)
        ashort_path_w=x.average_shortest_path_length( self.comp,weight="weight")
        ashort_path_u=x.average_shortest_path_length( self.comp_)
        ashort_path_uw=x.average_shortest_path_length(self.comp_,weight="weight")
        # nnodes, nedges, frac nodes/edges, frac edge_weight/edge
        nnodes=self.gg.number_of_nodes()
        nedges=self.gg.number_of_edges()

        nodes_edge =100*nnodes/nedges
        # fraction of participants in the largest component
        # and strongly connected components
        frac_weakly_connected=   100*self.comp.number_of_nodes()/nnodes
        frac_connected=100*self.comp_.number_of_nodes()/nnodes
        if self.gg.is_directed():
            total_weight=sum([i[2]["weight"] for i in self.gg.edges(data=True)])
            frac_strongly_connected=   100*x.strongly_connected_component_subgraphs(self.gg)[0].number_of_nodes()/nnodes
        else:
            total_weight=nedges
            frac_strongly_connected=  frac_connected
        weight_edge=100*total_weight/nedges
        mvars=("frac_connected","frac_strongly_connected","weight_edge",
              "nodes_edge","nnodes","nedges",
              "ashort_path","ashort_path_u","ashort_path_w","ashort_path_uw",
              "nperiphery","ncenter","diameter","radius","eccentricity",
              "closeness","square_clustering","aclustering","aclustering_w",
              "strengths","degrees","transitivity","transitivity_u","size_component")
        self.topm_dict={}
        ll=locals()
        for mvar in mvars:
            self.topm_dict[mvar] = ll[mvar]
    def getErdosSectorsUsers(self): pass
    def topologicalMeasures(self): pass
    def textualMeasures(self): pass
    def temporalMeasures(self): pass
    def scaleFreeTest(self): pass
class TimelineAnalysis(Analyses):
    # make Analyses with input graphids
    # plot timelines
    # calculate unitary roots
    # make tables
    def init():
        unitary_info=self.unitaryRoot()
    def unitaryRoot(self): pass
class MultiscaleAnalysis(Analyses):
    # make Analyses with input graphids
    # find bet fit to scale free
    # plot some variables with respect to graphsize
    # render tables
    def init():
        multiscale_info=self.multiScale()
    def multiScale(self): pass

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

