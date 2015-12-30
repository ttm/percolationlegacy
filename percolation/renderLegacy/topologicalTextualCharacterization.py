import percolation as P, networkx as x, numpy as n, powerlaw
import os, re, random, sys, itertools
from scipy import stats
from SPARQLWrapper import SPARQLWrapper, JSON
c=P.utils.check
class Bootstrap:
    def __init__(self,endpoint_url,data_dir="/disco/data/",fdir="/root/r/repos/documentation/",update=False,write_tables=False):
        """If fdir=None, don't render latex tables"""
        self.res=[]
        self.trans={}
#        metafiles=P.utils.getFiles(data_dir)
#        #metafiles=[i for i in metafiles if ("_fb" in i) and ("gml" not in i)]
#        metafiles=[i for i in metafiles if "_fb" in i]
#        metafiles = random.sample(metafiles, 10)
#        metafiles=['/disco/data/fbEgoGML/VilsonVieira18022013_gml_fb/rdf/VilsonVieira18022013_gml_fbMeta.owl',
#                '/disco/data/fbEgoGML/RitaWu08042013_gml_fb/rdf/RitaWu08042013_gml_fbMeta.owl',
#                '/disco/data/fbGroups/DemocraciaPura06042013_fb/rdf/DemocraciaPura06042013_fbMeta.owl',
#                '/disco/data/fbEgo/MarceloSaldanha19112014_fb/rdf/MarceloSaldanha19112014_fbMeta.owl',
#                '/disco/data/fbEgo/PedroPauloRocha10032013_fb/rdf/PedroPauloRocha10032013_fbMeta.owl',
#                '/disco/data/fbEgo/VJPixel23052014_fb/rdf/VJPixel23052014_fbMeta.owl',
#                '/disco/data/fbGroups/Tecnoxamanismo15032014_fb/rdf/Tecnoxamanismo15032014_fbMeta.owl',
#                '/disco/data/fbGroups/PartidoPirata23032013_fb/rdf/PartidoPirata23032013_fbMeta.owl',
#                '/disco/data/fbEgo/RicardoPoppi18032014_fb/rdf/RicardoPoppi18032014_fbMeta.owl',
#                '/disco/data/fbEgoGML/LailaManuelle17012013_0258_gml_fb/rdf/LailaManuelle17012013_0258_gml_fbMeta.owl']
        metafiles=P.utils.getFiles(data_dir)
        #metafiles=metafiles[:1]+metafiles[-1:]
        #metafiles=[i for i in metafiles if "_tw" in i]
        #metafiles=[i for i in metafiles if (("_tw" not in i) and ("_fb" not in i) and ("gmane-" not in i))]
        # exclude IRC for now
        metafiles=[i for i in metafiles if (("_tw" in i) or ("_fb" in i) or ("gmane-" in i))]
        metafiles=metafiles[-2:-1]
        #metafiles=metafiles[:1]
        metagnames=[P.utils.urifyFilename(i) for i in metafiles]
        if update:
            foo=P.utils.addToEndpoint(endpoint_url,metafiles)
        oi=self.getOverallInfos(endpoint_url,metagnames)
        dirnames=[os.path.dirname(i) for i in metafiles]
        self.metagnames=metagnames
        self.metafiles=metafiles
        if write_tables:
            self.writeOverallTable()
            self.writeOverallEndpoint(endpoint_url)
        translates=self.loadTranslates(endpoint_url,update)
        self.endpoint_url=endpoint_url
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



    def loadTranslates(self,endpoint_url,update):
        """Load each of the translate files into appropriate graphs"""
        c("LT")
        for gname,fname in zip(self.metagnames,self.metafiles):
            c("LT %s %s"%(gname,fname))
            qq="SELECT "+"?{} "*2+"WHERE \
                 {{ GRAPH <"+ gname +"> {{            \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.interactionXMLFile)+">  ?if .}} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.rdfFile)+">  ?if .}} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.friendshipXMLFile)+">  ?ff .}} . \
                 }} }}"
            keys="if","ff"
            #vals=P.utils.mQuery(endpoint_url,qq,keys)[0]
            #vals=[i for i in vals if i]
            vals=P.utils.mQuery(endpoint_url,qq,keys)
            vals=list(itertools.chain(*vals))
            vals=[i for i in vals if i]
            dname=os.path.dirname(fname)
            vals_=[]
            for val in vals:
                if self.provenance in ("Gmane","IRC"):
                    files=os.listdir(dname)
                    files=[i for i in files if ("Translate" in i) and i.endswith(".owl")]
                    vals_+=files
            vals=[i for i in vals if "gmane" not in i]
            vals+=vals_
            for val in vals:
                c("LT val %s "%(val,))
                fname_=val.split("/")[-1]
                fname2="{}/{}".format(dname,fname_)
                guri=P.utils.urifyFilename(fname_)
                if update:
                    cmd="s-post {} {} {}".format(endpoint_url, guri, fname2)
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
            qq="SELECT ?{} ?{} ?{} WHERE {{ \
                        GRAPH <"+ gname +"> {{ \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.socialProtocol)+"> ?n .    }} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.gmane.gmaneID)+">  ?gid .      }} . \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.tw.nMessages)+">  ?twnmsgs .      }} . \
                    }} }}"
            plat,gid,twnmsgs=P.utils.mQuery(endpoint_url,qq,("n","gid","twnmsgs"))[0]
            #if gid or twnmsgs or plat.endswith("Facebook"):
            if gid:
                self.provenance="Gmane"
            elif twnmsgs:
                self.provenance="Twitter"
            elif plat and plat.endswith("Facebook"):
                self.provenance="Facebook"
            else:
                self.provenance="IRC"
            qq="SELECT "+"?{} "*13+"WHERE                                                \n \
                 {{ GRAPH <"+ gname +"> {{                                                   \n \
                           ?s <"+str(P.rdf.ns.po.createdAt)+">  ?ca .                        \n \
                           ?s <"+str(P.rdf.ns.rdfs.label)+">  ?label .                       \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.friendshipXMLFile)+">  ?ffile .   }} . # FB \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.rdfFile)+">  ?ffile .   }} . # GMANE        \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.po.interactionXMLFile)+">  ?ifile .  }} . # FB \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.ego)+">  ?ego .                   }} .      \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.friendship)+">  ?f .              }} .      \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.fAnon)+">  ?fa .                  }} .      \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.interaction)+">  ?i .             }} .      \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.iAnon)+">  ?ia .                  }} .      \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.nFriends)+"> ?nf .                }} .      \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.nFriendships)+">  ?nfs .          }} .      \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.nInteractions)+">  ?ni .          }} .      \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.fb.nFriendsInteracted)+">  ?nfi .    }} .      \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.gmane.nParticipants)+">  ?nfi .  }} .          \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.tw.nParticipants)+">  ?nfi .  }} .          \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.gmane.nCharacters)+">  ?nchars .  }} .         \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.gmane.nMessages)+">    ?nmsgs .  }} .          \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.tw.nMessages)+">    ?nmsgs .  }} .          \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.gmane.nResponses)+">   ?nresp .  }} .          \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.tw.nReplies)+">   ?nresp .  }} .          \n \
               OPTIONAL {{ ?s <"+str(P.rdf.ns.tw.nReTweets)+">   ?nretw .  }} .          \n \
                 }} }}"
            keys="nf","nfs","ni","nfi","ca","ego","f","fa","i","ia","ffile","ifile","label","nchars","nmsgs","nresp","nretw"
            vals=P.utils.mQuery(endpoint_url,qq,keys)[0]
            bdict={i:j for i,j in zip(keys,vals)}
            self.odict[gname]=bdict
class Analyses:
    """Calculate unit roots, PCA averages and deviations and best fit to scale-free"""
    def __init__(self,bootstrap_instance,graphids=[],tables=False,do_network=False, \
                 do_topology=False,do_power=False, \
                 do_text=False,do_time=False,write_back=False):
        if not graphids:
            graphids=list(bootstrap_instance.trans.keys())
        self.options=locals()
        aa=[]
        for gid in graphids:
            aa+=[Analysis(bootstrap_instance,gid,self.options)]
        self.aa=aa
        if tables:
            self.renderTables()
    def renderTables(self):
        for analysis in self.aa:
            # make a line for the table or for each table
            # a table for powelaw fits
            # a table for the topological measures
            pass
        if self.options["do_power"]:
            self.renderPowerlawTable()
        if self.options["do_topology"]:
            self.renderTopologicalTable()
        if self.options["do_text"]:
            self.renderTextTable()
        if self.options["do_time"]:
            self.renderTimeTable()
    def renderPowerlawTable(self):
        #labels=[i.graphid for i in self.aa]
        labelsh=["id","alpha","xmin","D","sigma","noisy"]
        labelsh+=["R","p"]*5
        labels=[]
        dists=list(self.aa[0].power_res.supported_distributions.keys())
        dists.remove("power_law")
        lines=[]
        for anal in self.aa:
            labels.append(anal.graphid)
            c("power: "+labels[-1])
            data=[anal.power_res.alpha,anal.power_res.xmin,anal.power_res.D,anal.power_res.sigma,anal.power_res.noise_flag]
            dcomp=[]
            for dist in dists:
                c("plaw compare: "+ dist)
                dcomp+=list(anal.power_res.distribution_compare("power_law",dist))
            data+=dcomp
            lines.append(data)
            if anal.gg.is_directed():
                labels.append(anal.graphid+"*")
                data=[anal.power_res.alpha,anal.power_res.xmin,anal.power_res.D,anal.power_res.sigma,anal.power_res.noise_flag]
                dcomp=[]
                for dist in dists:
                    dcomp+=list(anal.power_res_.distribution_compare("power_law",dist))
                data+=dcomp
                lines.append(data)
        caption="Fit of network connectivity to power-law distributions"
        fname_="aqui.tex"
        P.tableHelpers.lTable(labels,labelsh,lines,caption,fname_,ttype="allFloat")
        P.tableHelpers.doubleColumn(fname_)
        self.labels=labels
    def renderTopologicalTable(self):
        # self.labels tem os labels
        lines=[]
        labels=[]
        for anal in self.aa:
            labels+=[anal.graphid]
            # tem as medidas topologicas, organizar em 1 ou + tabelas
            # renderizar em paisagem ou nem assim?
            # fazer papel grande, deixar que de zoom pq eh digital
            line=[
                    anal.topm_dict["nnodes"], 
                    anal.topm_dict["nedges"],
                    #anal.topm_dict["nodes_edge"], correlated to degree
                    anal.topm_dict["prob"], # anotar em ocorrências por mil ou milhões etc
                    anal.topm_dict["max_degree_empirical"],
                    max(anal.topm_dict["strengths_"]),
                    max(anal.topm_dict["weights"]),
                    n.mean(anal.topm_dict["degrees_"]),
                    n.std(anal.topm_dict["degrees_"]),
                    n.mean(anal.topm_dict["strengths_"]),
                    n.std(anal.topm_dict["strengths_"]),
                    n.mean(anal.topm_dict["weights"]),
                    n.std(anal.topm_dict["weights"]),
                    n.mean(anal.topm_dict["clustering_"]               ),
                    n.std(anal.topm_dict["clustering_"]               ),
                    n.mean(anal.topm_dict["clustering_w_"]             ),
                    n.std(anal.topm_dict["clustering_w_"]             ),
                    n.mean(anal.topm_dict["square_clustering_"]),
                    n.std( anal.topm_dict["square_clustering_"]),
                    n.mean(anal.topm_dict["closeness_"]                ),
                    n.std(anal.topm_dict["closeness_"]                ),
                    n.mean(anal.topm_dict["eccentricity_"]             ),
                    n.std(anal.topm_dict["eccentricity_"]             ),
                    n.mean(anal.topm_dict["sectorialized_degrees__"][0]), # periphery
                    n.std(anal.topm_dict["sectorialized_degrees__"][0]), # periphery
                    n.mean(anal.topm_dict["sectorialized_degrees__"][1]), # intermediary
                    n.std(anal.topm_dict["sectorialized_degrees__"][1]), # intermediary
                    n.mean(anal.topm_dict["sectorialized_degrees__"][2]), # hubs
                    n.std(anal.topm_dict["sectorialized_degrees__"][2]), # hubs

                    anal.topm_dict["sectorialized_nagents__"][0], # periphery
                    anal.topm_dict["sectorialized_nagents__"][1], # intermediary
                    anal.topm_dict["sectorialized_nagents__"][2], # hubs
                    anal.topm_dict["transitivity"],
                    anal.topm_dict["transitivity_u"],
                    anal.topm_dict["diameter"],
                    anal.topm_dict["radius"],
                    anal.topm_dict["frac_connected"],
                    anal.topm_dict["size_component"],
                    anal.topm_dict["ashort_path"],
                    anal.topm_dict["ashort_path_u"],
                    anal.topm_dict["ashort_path_w"],
                    anal.topm_dict["ashort_path_uw"],
                    anal.topm_dict["ncenter"],
                    anal.topm_dict["nperiphery"],
#                    anal.topm_dict["sectorialized_agents__"],
#                    anal.topm_dict["sectorialized_degrees__"],
                    anal.topm_dict["frac_strongly_connected"],
                    anal.topm_dict["frac_weakly_connected"],
                ]
            lines+=[line]
        labelsh=["$N$","$E$","$p$","$k_{max}$","$s_{max}$","$w_{max}$",
                 "$\mu(k)$","$\sigma(k)$","$\mu(s)$","$\std(s)$","$\mu(w)$","$\std(w)$",
                 "$\mu(cc)$","$\std(cc)$","$\mu(cc_w)$","$\std(cc_w)$","$\mu(sc)$","$\std(sc)$",
                 "$\mu(cl)$","$\std(cl)$","$\mu(ec)$","$\std(ec)$",
                 "$\mu(k_P)$","$\std(k_P)$","$\mu(k_I)$","$\std(k_I)$","$\mu(k_H)$","$\std(k_H)$",
                 "$P$","$I$","$H$","$t$","$t_u$","$D$","$R$","$con$","$comp$",
                 "$\mu(sp)$","$\mu(sp_u)$","$\mu(sp_w)$","$\mu(sp_{uw})$",
                 "$C*$","$P*$","$W$","$S$"]
        caption="Fit of network connectivity to power-law distributions"
        fname_="aqui2.tex"
        P.tableHelpers.lTable(labels,labelsh,lines,caption,fname_,ttype="allFloat")
        P.tableHelpers.doubleColumn(fname_)
    def renderTextTable(self):
        pass
    def renderTimeTable(self):
        c("IMPORTANT ::: make Time tables TTM")
        pass
class Analysis:
    """The analysis of one and only network.

    The rendering of tables and figures is left for the Analyses class,
    which can be directly called and calls initializes many of this class.
    """
    def __init__(self,bootstrap_instance,graphid=None,options={}):
        if graphid==None:
            graphid=list(bootstrap_instance.trans.keys())[0]
        self.graphid=graphid
        self.boot=bootstrap_instance
        if options.get("do_network"):
            self.makeNetwork()
        if options.get("do_topology"):
            self.topologicalMeasures()
        if options.get("do_sectors"):
            self.getErdosSectorsUsers()
        if options.get("do_time"):
            self.temporalMeasures()
        if options.get("do_text"):
            self.textualMeasures()
        if options.get("do_power"):
            self.scaleFreeTest()
        if options.get("do_pca"):
            self.pcaAnalysis()
        if options.get("write_back"):
            scalefree_info=self.writeBack()
        # explore different scales

    def pcaAnalysis(self):
        # choose some case collections of measures with wich to make PCA analysis
        # at least one for topological measures
        # another for textual measures
        # another with both
        raise NotImplementedError("PCA analysis must be implemented")
    def textualMeasures(self):
        # get textual content related to each user
        query= "SELECT ?{} ?{} WHERE \
                {{ GRAPH <"+ self.graphid +"> {{                 }} .   \
                   OPTIONAL {{  ?s tw:author ?from .             }} .   \
                   OPTIONAL {{  ?s gmane:author ?from .          }} .   \
                   OPTIONAL {{  ?s tw:messageContent ?text .     }} .   \
                   OPTIONAL {{  ?s gmane:body ?text .            }} .   \
                }} }}"
        author_texts=P.utils.mQuery(self.boot.endpoint_url,query,("from","text")))
        texts=P.text.aux.textFromSectors(author_texts,self.topm_dict["sectorialized_agents"])
        sector_text_analysis=P.text.analysis.analyseAll(texts)
        author_text_analysis=P.text.analysis.analyseAll(texts)
        del query, texts
        self.topm_dict.update(locals())
        raise NotImplementedError("Text processing must be implemented")
    def writeBack(self):
        """Write analysis info back to the endpoint"""
        raise NotImplementedError("Write back must be implemented")
    def makeNetwork(self):
        """Build network from endpoint through simple criteria."""
        # see what procedence: FB, TW, IRC, Email, etc
#        ftype=re.findall(r"\d+[gml]*fb(friendship|interaction)",self.graphid)
#        if ftype:
#            plat="Facebook"
        if self.boot.provenance=="Facebook":
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
        #ftype=re.findall(r"//(gmane)-.*",self.graphid)
        #if ftype:
        if self.boot.provenance=="Gmane":
            query= "SELECT ?from ?to (COUNT(DISTINCT ?m2) as ?weight) WHERE \
             {{ GRAPH <"+ self.graphid +"> {{            \
             ?m2 gmane:responseTo ?m1 .        \
             ?m1 gmane:author ?from .        \
             ?m2 gmane:author ?to .        \
             }} }} GROUP BY ?from ?to"
            keys="from","to","weight"
        ftype=re.findall(r"//(gmane)-.*",self.graphid)
        if self.boot.provenance=="Twitter":
            query= "SELECT ?from ?to (COUNT(DISTINCT ?m2) as ?weight) WHERE \
             {{ GRAPH <"+ self.graphid +"> {{            \
             ?m2 tw:retweetOf ?m1 .        \
             ?m1 tw:author ?from .        \
             ?m2 tw:author ?to .        \
             }} }} GROUP BY ?from ?to"
            keys="from","to","weight"
        if self.boot.provenance=="IRC":
            query= "SELECT ?from ?to (COUNT(DISTINCT ?m1) as ?weight) WHERE \
             {{ GRAPH <"+ self.graphid +"> {{            \
             ?m1 irc:author ?from2 .        \
             ?m1 irc:directedTo ?to2 .        \
             ?from2 irc:nick ?from .        \
             ?to2 irc:nick ?to .        \
             }} }} GROUP BY ?from ?to"
            keys="from","to","weight"
        vals=P.utils.mQuery(self.boot.endpoint_url,query,keys)
        c([i[2] for i in vals])
        if vals and (len(vals[0])==3):
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
    def topologicalMeasures(self):
        """A detailed info about one and only graph.

        Information about date, number of friends, friendships,
        interactions, etc.
        Average degree, average clustering, etc.
        ToDo: implement homophily
        """
        degrees=self.gg.degree()
        degrees_=list(degrees.values())
        strengths=self.gg.degree(weight="weight")
        strengths_=list(strengths.values())
        clustering=x.clustering( self.gg_ )
        clustering_=list(clustering.values())
        clustering_w=x.clustering( self.gg_,weight="weight" )
        clustering_w_=list(clustering_w.values())
        square_clustering=x.square_clustering( self.gg)
        square_clustering_=list(square_clustering.values())
        transitivity=x.transitivity(self.gg)
        transitivity_u=x.transitivity(self.gg_)
        closeness=x.closeness_centrality(self.gg)
        closeness_=list(closeness.values())
        eccentricity=x.closeness_centrality(self.gg_)
        eccentricity_=list(eccentricity.values())
        diameter=x.diameter(self.comp_)
        radius=x.radius(    self.comp_)
        nperiphery=len(x.periphery(self.comp_))
        ncenter=   len(x.center(self.comp_)   )
        size_component=self.comp_.number_of_nodes()
        ashort_path=x.average_shortest_path_length(   self.comp)
        ashort_path_w=x.average_shortest_path_length( self.comp,weight="weight")
        ashort_path_u=x.average_shortest_path_length( self.comp_)
        ashort_path_uw=x.average_shortest_path_length(self.comp_,weight="weight")
        nnodes=self.gg.number_of_nodes()
        nedges=self.gg.number_of_edges()

        # nodes_edge =100*nnodes/nedges # correlated to degree
        # fraction of participants in the largest component
        # and strongly connected components
        frac_weakly_connected=   100*self.comp.number_of_nodes()/nnodes
        frac_connected=100*self.comp_.number_of_nodes()/nnodes
        if self.gg.is_directed():
            weights=[i[2]["weight"] for i in self.gg.edges(data=True)]
            frac_strongly_connected=   100*x.strongly_connected_component_subgraphs(self.gg)[0].number_of_nodes()/nnodes
            frac_weakly_connected2=   100*x.weakly_connected_component_subgraphs(self.gg)[0].number_of_nodes()/nnodes
            # make weakly connected
        else:
            weights=[1]*nedges
            frac_strongly_connected=  frac_connected
        self.topm_dict=locals()
    def getErdosSectorsUsers(self,minimum_incidence=2):
        t=self.topm_dict
        max_degree_empirical=max(t["degrees_"])
        prob=t["nedges"]/(t["nnodes"]*(t["nnodes"]-1)) # edge probability
        self.max_degree_possible=2*(t["nnodes"]-1) # max d given N
        d_=list(set(t["degrees_"]))
        d_.sort()
        sectorialized_degrees__= self.newerSectorializeDegrees(
                                      self.makeEmpiricalDistribution(
                                        t["degrees_"], d_, t["nnodes"] ),
              stats.binom(self.max_degree_possible,prob),
              d_,
              max_degree_empirical,
              minimum_incidence,t["nnodes"])
        sectorialized_agents__= self.sectorializeAgents(
             sectorialized_degrees__, t["degrees"])
        sectorialized_nagents__=[len(i) for i in sectorialized_agents__]
        #mvars=("prob","max_degree_empirical","sectorialized_degrees__","sectorialized_agents__")
        del t
        self.topm_dict.update(locals())
    def sectorializeAgents(self,sectorialized_degrees,agent_degrees):
        periphery=[x for x in agent_degrees
                     if agent_degrees[x] in sectorialized_degrees[0]]
        intermediary=[x for x in agent_degrees
                     if agent_degrees[x] in sectorialized_degrees[1]]
        hubs=[x for x in agent_degrees
                     if agent_degrees[x] in sectorialized_degrees[2]]
        return locals()
    def newerSectorializeDegrees(self,empirical_distribution,binomial,incident_degrees_,max_degree_empirical,minimum_count,num_agents):
        # compute bins [start, end]
        prob_min=minimum_count/num_agents
        llimit=0
        rlimit=0
        self.bins=bins=[]
        self.empirical_probs=empirical_probs=[]
        while (rlimit < len(incident_degrees_)):
            if (sum(empirical_distribution[llimit:])>prob_min):
                prob_empirical=0
                while True:
                    prob_empirical=sum(
                         empirical_distribution[llimit:rlimit+1] )
                    if prob_empirical >= prob_min:
                        break
                    else:
                        rlimit+=1
                bins.append((llimit,rlimit))
                empirical_probs.append(prob_empirical)
                rlimit+=1
                llimit=rlimit
            else: # last bin
                print("last bin less probable than prob_min")
                rlimit=len(incident_degrees_)-1
                bins.append((llimit,rlimit))
                prob_empirical=sum(
                     empirical_distribution[llimit:rlimit+1] )
                empirical_probs.append(prob_empirical)
                rlimit+=1

        binomial_probs=[]
        for i, bin_ in enumerate(bins):
            llimit=bin_[0]
            rlimit=bin_[1]
            ldegree=incident_degrees_[llimit]-1
            rdegree=incident_degrees_[rlimit]
            binomial_prob=binomial.cdf(rdegree)-binomial.cdf(ldegree)
            binomial_probs.append(binomial_prob)

        # calcula probabilidades em cada bin
        # compara as probabilidades
        distribution_compare = list(n.array(empirical_probs) < n.array(binomial_probs))
        self.binomial_probs=binomial_probs
        self.distribution_compare0=distribution_compare
        if sum(distribution_compare):
            tindex= distribution_compare.index(True)
            tindex2=distribution_compare[::-1].index(True)
            periphery_degrees=incident_degrees_[:tindex]
            intermediary_degrees=incident_degrees_[tindex:-tindex2]
            hub_degrees=         incident_degrees_[-tindex2:]
        else:
            periphery_degrees=incident_degrees_[:]
            intermediary_degrees=[]
            hub_degrees=[]

        return periphery_degrees, intermediary_degrees, hub_degrees

    def makeEmpiricalDistribution(self, incident_degrees, incident_degrees_, N):
        empirical_distribution=[]
        for degree in incident_degrees_:
            empirical_distribution.append(incident_degrees.count(degree)/N)
        return empirical_distribution
    def temporalMeasures(self):
        if self.boot.provenance == "Facebook":
            print("Try making RDF of .tab so to render temporal measures")
            return
        query= "SELECT ?mdatetime WHERE \
         {{ GRAPH <"+ self.graphid +"> {{            \
           OPTIONAL {{ ?s <"+str(P.rdf.ns.gmane.sentAt)+">    ?mdatetime .  }} .          \n \
           OPTIONAL {{ ?s <"+str(P.rdf.ns.tw.sentAt)+">       ?mdatetime .  }} .          \n \
         }} }}"
        keys=("mdatetime",)
        vals=[i[0]for i in P.utils.mQuery(self.boot.endpoint_url,query,keys)]
        self.time_statistics=P.temporalStats.TemporalStatistics(datetimestrings=vals)

    def scaleFreeTest(self):
        """Under the framework developed at: http://arxiv.org/abs/1305.0215"""
        self.power_res=powerlaw.Fit(self.topm_dict["degrees_"],discrete=True)
        c("degree fit of" + self.graphid)
        if self.gg.is_directed():
            self.power_res_=powerlaw.Fit(self.topm_dict["strengths_"],discrete=True)
            c("strength fit of " + self.graphid)
        else:
            self.power_res_=self.power_res
class TimelineAnalysis(Analyses):
    # make Analyses with input graphids
    # plot timelines
    # calculate unit roots
    # http://conference.scipy.org/proceedings/scipy2011/pdfs/statsmodels.pdf
    # http://arch.readthedocs.org/en/latest/unitroot/tests.html
    # https://pypi.python.org/pypi/arch/
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

