import rdflib as r, percolation as P, pygraphviz as gv, os, datetime
check=P.utils.check
utf8=P.utils.utf8
from rdflib.plugins.sparql import prepareQuery

#bb=g.query(query,initBindings={"fid":ind})
#label=[i for i in bb][0][0].value

"""
para as URIs:
reserved    = gen-delims / sub-delims

gen-delims  = ":" / "/" / "?" / "#" / "[" / "]" / "@"

sub-delims  = "!" / "$" / "&" / "'" / "(" / ")"
            / "*" / "+" / "," / ";" / "="
https://tools.ietf.org/html/rfc3986#section-2

A URI também não é splitada com %
r.namespace.split_uri("http://purl.org/socialparticipation/irc/Participant#labMacambiraLaleniaLog1%2818")
"""
def LL_(literal,lang=None):
    if type(literal)==type(1123):
        ttype=NS.xsd.integer
    elif type(literal)==type(True):
        ttype=NS.xsd.boolean
    elif type(literal)==type(datetime.datetime.now()):
        ttype=NS.xsd.datetime
    elif type(literal)==type(datetime.date(2015,3,4)):
        ttype=NS.xsd.date
    else:
        ttype=NS.xsd.string
        literal=utf8(str(literal))
    if not lang:
        return r.Literal(literal,datatype=ttype)
    else:
        return r.Literal(literal,lang=lang,datatype=ttype)

COUNT=0
class NS:
    cm =     r.Namespace("http://purl.org/socialparticipation/cm/")   # caixa mágica
    obs =    r.Namespace("http://purl.org/socialparticipation/obs/") # ontology of the social library
    aa  =    r.Namespace("http://purl.org/socialparticipation/aa/")  # algorithmic autoregulation
    vbs =    r.Namespace("http://purl.org/socialparticipation/vbs/") # vocabulary of the social library
    opa =    r.Namespace("http://purl.org/socialparticipation/opa/") # participabr
    ops =    r.Namespace("http://purl.org/socialparticipation/ops/") # social participation ontology
    ocd =    r.Namespace("http://purl.org/socialparticipation/ocd/") # cidade democrática
    ore =    r.Namespace("http://purl.org/socialparticipation/ore/") # ontology of the reseach, for registering ongoing works, a RDF AA
    ot  =    r.Namespace("http://purl.org/socialparticipation/ot/")  # ontology of the thesis, for academic conceptualizations
    po=per = r.Namespace("http://purl.org/socialparticipation/po/") # percolation, this framework itself
    fb  =    r.Namespace("http://purl.org/socialparticipation/fb/")  # facebook
    tw  =    r.Namespace("http://purl.org/socialparticipation/tw/")  # twitter
    irc =    r.Namespace("http://purl.org/socialparticipation/irc/") # irc
    gmane =  r.Namespace("http://purl.org/socialparticipation/gmane/") # gmane
    ld  =    r.Namespace("http://purl.org/socialparticipation/ld/")  # linkedin 
    dbp  =    r.Namespace("http://dbpedia.org/resource/")
    rdf =    r.namespace.RDF
    rdfs =   r.namespace.RDFS
    owl =    r.namespace.OWL
    xsd =    r.namespace.XSD
    dc =     r.namespace.DC
    dct =    r.namespace.DCTERMS
    foaf =   r.namespace.FOAF
    doap =   r.namespace.DOAP
    void =   r.namespace.VOID
    U=   r.URIRef
query_=prepareQuery(
        "SELECT ?name WHERE {?fid fb:name ?name}"
        ,initNs={"fb":NS.fb})
a=NS.rdf.type
def makeDummyOntology():
    triples=(
            (NS.po.InteractionSnapshot, a, NS.rdfs.Class),
            (NS.po.GmaneSnapshot, a, NS.rdfs.Class),
            (NS.po.Snapshot, a, NS.rdfs.Class),
            (NS.po.InteractionSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # fb, part, tw, irc, gmane, cidade
            (NS.po.GmaneSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),
            )
    return triples
def makeExtradata():
    triples=(
            (NS.po.Resource+"#PythonSparQLServer1",NS.po.url,"https://projects.bigasterisk.com/sparqlhttp/"),
            (NS.po.Resource+"#PythonSparQLServer2",NS.po.url,"https://github.com/RDFLib/rdflib-web"),
            (NS.po.Resource+"#PythonSparQLServer2",NS.po.url,"http://rdflib-web.readthedocs.org/en/latest/"),
            (NS.po.Resource+"#DocumentCollection1",NS.po.url,"https://www.w3.org/DesignIssues/"),
            (NS.po.Resource+"#DocumentCollection1",NS.rdfs.comment,"Tim Berners-Lee's outline of architectural principles for thinking specifications."),
            (NS.po.Resource+"#BFO",NS.po.url,"https://raw.githubusercontent.com/BFO-ontology/BFO/master/releases/2.0/bfo.owl"),
            (NS.po.Resource+"#BFO",NS.rdfs.comment,"BFO 2.0"),
            (NS.po.Resource+"#BFO",NS.rdfs.label,"bfo"),
            (NS.po.Resource+"#BFO",NS.doap.repository,"https://github.com/bfo-ontology/BFO/"),
            (NS.po.Resource+"#BFO",NS.foaf.homepage,"http://ifomis.uni-saarland.de/bfo/"),
            (NS.po.Note+"#1",NS.po.url,"leave Fuseki a little bit and start making a Flask interface for dealing with RDF data"),
            )
def makeMetadata():
    triples=(
            (NS.po.po+".owl", a, NS.owl.Ontology),
            (NS.po.po+".owl", NS.dct.title, "The Participation Ontology"),
            (NS.po.po+".owl", NS.dct.description, "The Participation Ontology eases integration of social data\
                                                for scientific research and harnessing by the participants/integrants of the social structures"),
            (NS.po.po+".owl", NS.dct.creator, "Renato Fabbri"),
            (NS.po.po+".owl", NS.doap.maintainer, NS.po.Participant+"#RenatoFabbri"),
            (NS.po.po+".owl", NS.doap.developer ,NS.po.Participant+"#RenatoFabbri"),
            (NS.po.po+".owl", NS.foaf.maker,NS.po.Participant+"#RenatoFabbri"),
            (NS.po.po+".owl", NS.doap.mailing+"-list","listamacambira@googlegroups.com"),
            (NS.po.po+".owl", NS.dc.license, r.URIRef("http://www.opendatacommons.org/licenses/odbl/")),
            (NS.po.po+".owl", NS.rdfs.seeAlso, NS.po.Percolation),
            (NS.po.po+".owl", NS.rdfs.seeAlso, NS.po.Social),
            (NS.po.po+".owl", NS.rdfs.seeAlso, NS.po.Music),
            (NS.po.po+".owl", NS.rdfs.seeAlso, NS.po.Visuals),
            (NS.po.po+".owl", NS.rdfs.seeAlso, ),
            (NS.po.po+".owl", NS.foaf.homepage, "https://github.com/ttm/percolation"),
            (NS.po.po+".owl", NS.foaf.mbox, "mailto:renato.fabbri@gmail.com"),

            (NS.po.Participant+"#RenatoFabbri", a, NS.po.Participant),
            (NS.po.Participant+"#RenatoFabbri", NS.foaf.name, "Renato Fabbri"),
            (NS.po.Participant+"#RenatoFabbri",NS.foaf.mbox,"mailto:renato.fabbri@gmail.com"),

            (NS.po.Percolation, a, NS.po.PythonPackage),
            (NS.po.Percolation, NS.po.homeRepo, NS.U("https://github.com/ttm/percolation")),
            (NS.po.Percolation, NS.rdfs.comment, "The Percolation Python package for social harnessing"),
            (NS.po.Percolation, NS.po.sparqlEndpoint, NS.po.SparqlEndpoint+"#DEV1"),
            (NS.po.SparqlEndpoint+"#DEV1",NS.po.url,"http://200.144.255.210:8082/RTDB"),
            (NS.po.SparqlEndpoint+"#DEV1",NS.rdfs.comment,"for remote development"),
            (NS.po.SparqlEndpoint+"#DEV1",NS.rdfs.label,"dev1"),
            (NS.po.Percolation, NS.dct.subject, NS.dbp.Social_network_analysis),
            (NS.po.Percolation, NS.dct.subject, NS.dbp.Social_networks),
            (NS.po.Percolation, NS.dct.subject, NS.dbp.Linked_data),
            (NS.po.Percolation, NS.dct.subject, NS.dbp.Semantic_web),
            (NS.po.Percolation, NS.dct.subject, NS.dbp.Complex_systems_theory),
            (NS.po.Percolation, NS.dct.subject, NS.dbp.Complex_networks),
            (NS.po.Percolation, NS.dct.subject, NS.dbp.Physics),




            (NS.po.Percolation, NS.void.sparqlEndpoint, "http://openlinkedsocialdata.org/sparql"),

            (NS.po.Percolation, NS.po.sparqlEndpoint, NS.po.SparqlEndpoint+"#DEV2"),
            (NS.po.Percolation, NS.po.sparqlEndpoint, NS.po.SparqlEndpoint+"#DEV2"),
            (NS.po.SparqlEndpoint+"#DEV2",NS.po.url,"http://localhost:9082/RTDB"),
            (NS.po.SparqlEndpoint+"#DEV2",NS.rdfs.comment,"for local development in the VM with Fuseki"),
            (NS.po.SparqlEndpoint+"#DEV2",NS.rdfs.label,"dev2"),

            (NS.po.Percolation, NS.po.sparqlEndpoint, NS.po.SparqlEndpoint+"#1"),
            (NS.po.Percolation, NS.po.sparqlEndpoint, NS.po.SparqlEndpoint+"#2"),
            (NS.po.Percolation, NS.po.sparqlEndpoint, NS.po.SparqlEndpoint+"#3"),
            (NS.po.Percolation, NS.po.sparqlEndpoint, NS.po.SparqlEndpoint+"#AA"),
            (NS.po.SparqlEndpoint+"#AA",NS.po.url,"http://openlinkedsocialdata/AA/"),
            (NS.po.SparqlEndpoint+"#AA",NS.rdfs.comment,"for using AA, i.e. for sharing frfr"),
            (NS.po.SparqlEndpoint+"#AA",NS.rdfs.label,"dev1"),

            (NS.po.SparqlEndpoint+"#DEVAA",NS.po.url,"http://openlinkedsocialdata/AA/"),

            (NS.po.onlineMetaXMLFile, NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.onlineMetaTTLFile, NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.MetaXMLFilename,   NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.MetaTTLFilename    NS.rdfs.subPropertyOf, NS.void.dataDump),
                       
            (NS.po.onlineInteractionXMLFile,NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.onlineinteractionTTLFile,NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.interactionXMLFilename,  NS.rdfs.subPropertyOf, NS.void.dataDump),
            (NS.po.interactionTTLFilename,  NS.rdfs.subPropertyOf, NS.void.dataDump),

            (NS.po.OpenLinkedSocialData, NS.subClassOf, NS.po.PercolationRelated), # for the primary topics
            (NS.po.OpenLinkedSocialData, NS.po.emphasis, NS.dbp.Linked_data),
            (NS.po.OpenLinkedSocialData, NS.void.subset, NS.facebook),
            (NS.po.OpenLinkedSocialData, NS.void.subset, NS.twitter),
            (NS.po.OpenLinkedSocialData, NS.void.subset, NS.irc),
            (NS.po.OpenLinkedSocialData, NS.void.subset, NS.gmane),
            (NS.po.OpenLinkedSocialData, NS.void.subset, NS.participation),
            (NS.po.OpenLinkedSocialData, NS.void.subset, NS.po.Linkset1),
            (NS.po.Linkset1, a,NS.po.Linkset),
            (NS.void.Linkset, NS.rdfs.subClassOf, NS.po.Linkset),
            (NS.po.Linkset1, NS.void.linkPredicate,NS.owl.sameAs),
            (NS.po.linkset, NS.rdfs.comment,"void:Linkset only accepts two targets. the class po:Linkset can have any number of targes"),
            (NS.po.linkset, NS.rdfs.comment,"The link set for matching between the datasets: renatogk==renato.fabbri@gmail==renato.fabbri==hybrid..."),
            (NS.linksets.Linkset1
            (NS.po.linkset, NS.void.subset,NS.OpenLinedSocialData),
            (NS.po.linkset, NS.void.target,NS.facebook),
            (NS.po.linkset, NS.void.target,NS.twitter),
            (NS.po.linkset, NS.void.target,NS.irc),
            (NS.po.linkset, NS.void.target,NS.gmane),
            (NS.po.linkset, NS.void.target,NS.aa),
            (NS.po.linkset, NS.void.target,NS.participabr),
            (NS.po.linkset, NS.void.target,NS.cidadedemocratica),
            (NS.po.OpenLinkedSocialData+"#Participation", NS.void.subset, NS.participabr),
            (NS.po.OpenLinkedSocialData+"#Participation", NS.void.subset, NS.cidadedemocratica),
            (NS.po.OpenLinkedSocialData+"#Participation", NS.void.subset, NS.aa),

            (NS.po.OpenLinkedSocialData, NS.void.classPartition, NS.po.VoidPartition+"#Participants"),
            (NS.po.OpenLinkedSocialData, NS.void.classPartition, NS.po.VoidPartition+"#Messages"),
            (NS.po.OpenLinkedSocialData, NS.void.classPartition, NS.po.VoidPartition+"#Friendships"),
            (NS.po.OpenLinkedSocialData, NS.void.classPartition, NS.po.VoidPartition+"#Interactions"),
            (NS.po.OpenLinkedSocialData, NS.void.classPartition, NS.po.VoidPartition+"#Texts"),
            (NS.po.OpenLinkedSocialData, NS.void.classPartition, NS.po.VoidPartition+"#Texts"),
            (NS.po.OpenLinkedSocialData, NS.void.propertyPartition, NS.po.VoidPartition+"#Linked"),
            (NS.po.OpenLinkedSocialData, NS.void.propertyPartition, NS.po.VoidPartition+"#Names"),
            (NS.po.VoidPartition+"#Participants", NS.void.class, NS.po.Participant),
            (NS.po.VoidPartition+"#Messages", NS.void.class, NS.po.Messages),
            (NS.po.VoidPartition+"#Interactions", NS.void.class, NS.po.Interaction),
            (NS.po.VoidPartition+"#Friendships", NS.void.class, NS.po.Friendship),
            (NS.po.VoidPartition+"#Texts", NS.void.class, NS.po.Text),
            (NS.po.VoidPartition+"#Linked", NS.void.property, NS.po.text),
            (NS.po.VoidPartition+"#Names", NS.void.property, NS.po.name),
                       
            (NS.po.Social, a,                NS.po.PythonPackage),
            (NS.po.Social, NS.po.homeRepo, NS.U("https://github.com/ttm/social")),
            (NS.po.Social, NS.rdfs.comment, "The Social Python package for accessing data from social platforms and rendering linked data"),
            (NS.po.Social, NS.po.standardDataPath, "../data/"),
            (NS.po.Social, NS.po.standardFacebookDataPath, "../data/fb/"),
            (NS.po.Social, NS.po.standardTwitterDataPath, "../data/tw/"),
            (NS.po.Social, NS.po.standardIRCDataPath, "../data/irc/"),
            (NS.po.Social, NS.po.standardGmaneDataPath, "../data/gmane/"),

            (NS.po.Music, a,                NS.po.PythonPackage),
            (NS.po.Music, NS.po.homeRepo, NS.U("https://github.com/ttm/music")),
            (NS.po.Music, NS.rdfs.comment, "The Music Python package making music with sample-based methods"),

            (NS.po.Visuals, a,                NS.po.PythonPackage),
            (NS.po.Visuals, NS.po.homeRepo, NS.U("https://github.com/ttm/visuals")),
            (NS.po.Visuals, NS.rdfs.comment, "The Visuals Python package making image and video data visualizations"),


            (NS.po.OpenLinkedSocialData, a,                NS.po.PythonPackage),
            (NS.po.OpenLinkedSocialData, NS.foaf.homepage, NS.U("https://github.com/OpenLinkedSocialData")),
            (NS.po.OpenLinkedSocialData, NS.rdfs.comment, "Linked RDF data rendered through participatory packages"),
            (NS.po.OpenLinkedSocialData, a, NS.void.Dataset),
            (NS.po.OpenLinkedSocialData, NS.void.feature, NS.U("http://www.w3.org/ns/formats/Turtle")),
            (NS.po.OpenLinkedSocialData, NS.void.feature, NS.U("http://www.w3.org/ns/formats/RDF_XML")),

            (NS.po.subject, NS.rdfs.subPropertyOf, NS.dct.subject ),
            (NS.po.subject, NS.rdfs.subPropertyOf, NS.foaf.topic  ),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Social_network_analysis),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Social_networks),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Linked_data),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Semantic_web),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Complex_systems_theory),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Complex_networks),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Physics),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Art),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Music),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Internet_art),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Data_visualization),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Stop_motion),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Percolation),
            (NS.po.PercolationRelated, NS.po.subject, NS.dbp.Empowerment),
            (NS.dbp.Empowerment,NS.rdfs.comment, "Empowerment refers to increasing the economic, political, social, educational, gender, or spiritual strength of an entity or entities."), # from dbpedia

            (NS.po.OpenLinkedSocialData, NS.rdfs.subClassOf, NS.po.PercolationRelated),
            (NS.po.Percolation, NS.rdfs.subClassOf, NS.po.PercolationRelated),
            (NS.po.Social, NS.rdfs.subClassOf, NS.po.PercolationRelated),
            (NS.po.Music, NS.rdfs.subClassOf, NS.po.PercolationRelated),
            (NS.po.Visuals, NS.rdfs.subClassOf, NS.po.PercolationRelated),

            (NS.po.emphasys, NS.rdfs.subClassOf, NS.foaf.primaryTopic),
            (NS.po.Visuals, NS.po.emphasys, NS.dbp.Stop_motion),
            (NS.po.Visuals, NS.po.emphasys, NS.dbp.Image),
            (NS.po.Music, NS.po.emphasys, NS.dbp.Music),
            (NS.po.Music, NS.po.emphasys, NS.dbp.Sound),
            (NS.po.Music, NS.po.emphasys, NS.po.SampleBasedDAW),
            (NS.po.OpenLinkedSocialData, NS.po.emphasys, NS.void.Dataset),
            (NS.po.Social, NS.po.emphasis, NS.dbp.Semantic_web),
            (NS.po.Social, NS.po.emphasis, NS.dbp.Linked_data),

            (NS.po.Percolation, NS.po.uses, NS.po.Social),
            (NS.po.Percolation, NS.po.uses, NS.po.Music),
            (NS.po.Percolation, NS.po.uses, NS.po.Visuals),
            (NS.po.Percolation, NS.po.uses, NS.po.OpenLinkedSocialData),

            (NS.po.Social , NS.po.dependsOn,  , NS.po.Percolation),
            (NS.po.Music  , NS.po.dependsOn,  , NS.po.Percolation),
            (NS.po.Visuals, NS.po.dependsOn,  , NS.po.Percolation),
            (NS.po.Percolation, NS.po.uses, NS.po.OpenLinkedSocialData),


            (NS.po.Social, NS.po.sythesizes, NS.po.OpenLinkedSocialData),
            (NS.po.Percolation, NS.po.analyzes, NS.po.OpenLinkedSocialData),
            (NS.po.Percolation, NS.po.makesArtWith, NS.po.OpenLinkedSocialData),

            (NS.po.Percolation, NS.po.enables, NS.dbp.Empowerment),
            (NS.po.Percolation, NS.po.enables, NS.dbp.Benchmarking),
            (NS.po.OpenLinkedSocialData, NS.po.enables, NS.dbp.Benchmarking),
            (NS.po.OpenLinkedSocialData, NS.po.enables, NS.dbp+".Self-knowledge_(psychology)",

            (NS.po.Percolation, NS.po.usesTechnique, NS.po.SocialPercolationProcess),
            (NS.po.Percolation, NS.po.usesTechnique, NS.po.ErdosSectorialization),
            (NS.po.ErdosSectorialization, NS.rdfs.comment, "The sectorialization of a social structure, \
                    with respect to its participants, in hub, intermediary and periphery sectors, \
                    through the comparison of the in, out and total degrees and strengths histograms against the Erdos-Renyi model."),
            (NS.po.Percolation, NS.po.usesTechnique, NS.po.MultiscaleAnalysis),
            (NS.po.Percolation, NS.po.usesTechnique, NS.po.TimelineAnalysis),
            (NS.po.Percolation, NS.po.usesTechnique, NS.po.Audiovisualization),
            (NS.po.Audiovisualization,NS.rdfs.comment,"the projection of data through sound or light for research and artistic goals"),
            (NS.po.TimelineAnalysis,NS.rdfs.comment,"Analysis of topological and textual features of social structures along a timeline"),
            (NS.po.MultiscaleAnalysis,NS.rdfs.comment,"Analysis of topological and textual features of social structures in various scales"),
            (NS.po.Percolation, NS.po.usesTechnique, NS.dbp.Kolmogorov_smirnov_test),
            (NS.po.Percolation, NS.po.usesTechnique, NS.dbp.Principal_component_analysis),
            (NS.po.Percolation, NS.po.usesTechnique, NS.dbp.Unit_root_test),
            (NS.po.Percolation, NS.po.usesTechnique, NS.dbp.CorrelationMatrix),
            (NS.po.Percolation, NS.po.usesTechnique, NS.dbp.Bag_of_Words),
            (NS.po.Percolation, NS.po.usesTechnique, NS.po.BagOfSizes),
            (NS.po.Percolation, NS.po.usesTechnique, NS.po.POSCounting),
            (NS.po.Percolation, NS.po.usesTechnique, NS.po.AlphabetCounting),
            (NS.po.Percolation, NS.po.usesTechnique, NS.po.SynsetCounting),

            (NS.po.BagOfSizes,NS.rdfs.comment,"Counting of sizes of words, sentences, paragraphs by types (e.g. stopwords)."),
            (NS.po.AlphabetCounting,NS.rdfs.comment,"Counting of alphabet like vowels and consonants."),
            (NS.po.SynsetCounting,NS.rdfs.comment,"Counting of wordnet synsets features, e.g. number of holonyms or hypernyms."),
            (NS.po.SynsetCounting,NS.rdfs.comment,"To enhance result qualities, the most occurent wordnet synset (by wordnet standards) which matches the POS tagger tag (>95% of true positives) is chosen "),
            (NS.po.SynsetCounting,NS.po.dependsOn,NS.po.POSCounting),

            (NS.po.POSCounting,NS.rdfs.comment,"Counting of POS tags, e.g. number of substantives or adjectves."),
            (NS.po.POSCounting,NS.rdfs.comment,"Bag of sizes delivers appropriate tokenization of sentences."),
            (NS.po.POSCounting,NS.po.uses,NS.po.BagOfSizes),

            )

    return triples
def makeMetadataOntology():
    makeMetadata()
    makeMetadataStructure()

"https://github.com/OpenLinkedSocialData"
def makeMetadataStructure():
    triples=(
            (NS.po.Participant, NS.rdfs.subClassOf, NS.foaf.Person),
            (NS.po.PythonPackage, NS.rdfs.subClasOf, NS.doap.Project),
            (NS.po.PythonPackage, NS.doap.programming+"-language", "Python"),
            (NS.po.homeRepo, NS.rdfs.subPropertyOf, NS.doap.location),
            (NS.po.homeRepo, NS.rdfs.subPropertyOf, NS.doap.repository),
            (NS.po.homeRepo, NS.rdfs.subPropertyOf, NS.foaf.homepage),
            (NS.po.homeRepo, NS.rdfs.range, NS.doap.Repository),
            )
    return triples

def makeOntology():
    triples=(
            #(NS.po.InteractionSnapshot, a, NS.rdfs.Class),
            #(NS.po.GmaneSnapshot, a, NS.rdfs.Class),
            #(NS.po.Snapshot, a, NS.rdfs.Class),

            (NS.po.InteractionSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # fb, part, tw, irc, gmane, cidade
            (NS.po.FriendshipSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # fb, part
            (NS.po.ReportSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # aa

            (NS.po.FacebookSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot),
            (NS.po.FacebookInteractionSnapshot, NS.rdfs.subClassOf, NS.po.FacebookSnapshot),
            (NS.po.FacebookInteractionSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

            (NS.po.FacebookFriendshipSnapshot, NS.rdfs.subClassOf, NS.po.FacebookSnapshot),
            (NS.po.FacebookFriendshipSnapshot, NS.rdfs.subClassOf, NS.po.FriendshipSnapshot),

            (NS.po.TwitterSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

            (NS.po.GmaneSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

            (NS.po.IRCSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

            (NS.po.AASnapshot, NS.rdfs.subClassOf, NS.po.ReportSnapshot),

            (NS.po.ParticipaSnapshot, NS.rdfs.subClassOf, NS.po.CompleteSnapshot),

            (NS.po.CidadeDemocraticaSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),

            (NS.gmane.gmaneID, NS.rdfs.subPropertyOf, NS.po.auxID),
            (NS.fb.groupID, NS.rdfs.subPropertyOf, NS.po.auxID),

            (NS.po.interactionXMLFile, NS.rdfs.subPropertyOf,NS.po.defaultXML), # fb
            (NS.po.rdfFile           , NS.rdfs.subPropertyOf,NS.po.defaultXML), # twitter, gmane
            (NS.po.friendshipXMLFile , NS.rdfs.subPropertyOf,NS.po.defaultXML), # fb

            (NS.po.MetaNamedGraph, NS.rdfs.subClassOf,NS.po.NamedGraph), 
            (NS.po.TranslationNamedGraph, NS.rdfs.subClassOf, NS.po.NamedGraph),

            (NS.po.metaGraph , NS.rdfs.subPropertyOf,NS.po.namedGraph), # fb
            (NS.po.metaGraph , NS.rdfs.range,NS.po.MetaNamedGraph), # fb
            (NS.po.translationGraph , NS.rdfs.subPropertyOf,NS.po.namedGraph), # fb
            (NS.po.translationGraph , NS.rdfs.range,NS.po.TranslationNamedGraph), # fb

            (NS.gmane.Message,NS.rdfs.subClassOf,NS.po.Message), 
            (NS.tw.Message,NS.rdfs.subClassOf,NS.po.Message), 
            (NS.po.Message,NS.rdfs.subClassOf,NS.po.InteractionInstance), 
            (NS.fb.Interaction,NS.rdfs.subClassOf,NS.po.InteractionInstance), 

            (NS.gmane.Participant,NS.rdfs.subClassOf,NS.po.Participant), 
            (   NS.fb.Participant,NS.rdfs.subClassOf,NS.po.Participant), 
            (   NS.tw.Participant,NS.rdfs.subClassOf,NS.po.Participant),  

            (NS.fb.friend,a,NS.owl.SymmetricProperty), 
            # ADD IRC and other instances
            
            (NS.fb.ID, NS.rdfs.subPropertyOf,NS.po.ID),
            (NS.po.numericID, NS.rdfs.subPropertyOf,NS.po.ID),
            (NS.po.stringID, NS.rdfs.subPropertyOf,NS.po.ID),


            (NS.fb.nRelations, NS.rdfs.subPropertyOf,NS.po.nRelations),
            (NS.fb.nInterations, NS.rdfs.subPropertyOf,NS.fb.nRelations),
            (NS.fb.nFriendships, NS.rdfs.subPropertyOf,NS.fb.nRelations),


            (NS.fb.anonymized, NS.rdfs.subPropertyOf,NS.po.anonymized),
            (NS.fb.friendshipsAnonymized, NS.rdfs.subPropertyOf,NS.fb.anonymized),
            (NS.fb.interactionssAnonymized, NS.rdfs.subPropertyOf,NS.fb.anonymized),

            (NS.fb.numericID,NS.rdfs.subPropertyOf,NS.fb.ID),
            (NS.fb.numericID,NS.rdfs.subPropertyOf,NS.po.numericID),
            (NS.fb.stringID, NS.rdfs.subPropertyOf,NS.fb.ID),
            (NS.fb.stringID, NS.rdfs.subPropertyOf,NS.po.stringID),

            (NS.gmane.stringID,NS.rdfs.subPropertyOf,NS.po.stringID),
            (NS.gmane.email,   NS.rdfs.subPropertyOf,NS.gmane.stringID),

            # TW IRC AA Part CD
            (NS.tw.stringID,NS.rdfs.subPropertyOf,NS.po.stringID),
            (NS.tw.email,   NS.rdfs.subPropertyOf,NS.tw.stringID),

            # User ID somente, na msg a ID eh a URI pois nao diferem em listas/grupos diferentes
            # Mas IDs podem existir para grupos e pessoas, pois se repetem em datasets diferentes

            # type of relation retrievement: 1, 2 or 3

            # labels equivalence: irc, etc
            # date equivalence
            # interaction/relation uris equivalence
            # textual content equivalence

            # if text is available
           )
    return triples
def renderOntology(triples_dir="/disco/triplas/",dummy=False):
    if dummy:
        triples=makeDummyOntology()
    else:
        triples=makeOntology()
    P.rdf.writeTriples(triples,"{}po.ttl".format(triples_dir))
    c("po ttl written")
def G(g,S,P,O):
    g.add((S,P,O))
def writeTriples(triples,filename,format_="turtle"):
    g=r.Graph()
    for triple in triples:
        if not isinstance(triple[2],r.URIRef):
            triple[2]=r.Literal(triple[2])
        g.add(triple)
    with open(filename,"wb") as f:
        f.write(g.serialize(format=format_))
def writeAll(per_graph,sname="img_and_rdf",sdir="./",full=False,remove=False,dot=False,sizelimit=None):
    nome_=sname
    g,A=per_graph
    if not os.path.isdir(sdir):
        os.mkdir(sdir)
    for i in ("figs","dot","rdf"):
        if os.path.isdir(sdir+i) and remove:
            for afile in os.listdir(sdir+i):
                os.remove(sdir+i+"/"+afile)
            os.rmdir(sdir+i)
        if not os.path.isdir(sdir+i):
            os.mkdir(sdir+i)
    if full=="True":
        nome=(sdir+"figs/%s.png"%(nome_,))
        A.draw(nome,prog="dot")
        nome=(sdir+"figs/%s_2.png"%(nome_,))
        A.draw(nome,prog="circo")
        nome=(sdir+"figs/%s_3.png"%(nome_,))
        A.draw(nome,prog="fdp")
        A.write("dot/%s.dot"%(nome_,))
    if full=="neato":
        print("on the draw")
        A.graph_attr["splines"]=True
        A.graph_attr["overlap"]=False
        A.graph_attr["size"]="39.5,32"
        nome=(sdir+"figs/%sN.png"%(nome_,))
        A.draw(nome,prog="neato")
    if full=="circo":
        print("on the circo draw")
#        A.graph_attr["splines"]=True
#        A.graph_attr["overlap"]=False
#        A.graph_attr["size"]="39.5,32"
        nome=(sdir+"figs/%sC.png"%(nome_,))
        A.draw(nome,prog="circo")
    elif full:
        nome=(sdir+"figs/%s.png"%(nome_,))
        A.draw(nome,prog="dot")
    check("{} was rendered".format(nome_))
    if dot:
        A.write(sdir+"dot/%s.dot"%(nome_,))
        check("dot written")
    if sizelimit:
        i=0
        j=0
        g_=r.Graph()
        for sub, pred, obj in g:
            g_.add((sub,pred,obj))
            i+=1
            if i%sizelimit==0:
                f=open(sdir+"rdf/{}{:05d}.rdf".format(nome_,j),"wb")
                f.write(g_.serialize())
                f.close()
                check("rdf written")
                f=open(sdir+"rdf/{}{:05d}.ttl".format(nome_,j),"wb")
                f.write(g_.serialize(format="turtle"))
                f.close()
                check("ttl written")
                g_=r.Graph()
                j+=1
        f=open(sdir+"rdf/{}{:05d}.rdf".format(nome_,j),"wb")
        f.write(g_.serialize())
        f.close()
        check("rdf written")
        f=open(sdir+"rdf/{}{:05d}.ttl".format(nome_,j),"wb")
        f.write(g_.serialize(format="turtle"))
        f.close()
        check("ttl written")
    else:
        f=open(sdir+"rdf/%s.rdf"%(nome_,),"wb")
        f.write(g.serialize())
        f.close()
        check("rdf written")
        f=open(sdir+"rdf/%s.ttl"%(nome_,),"wb")
        f.write(g.serialize(format="turtle"))
        f.close()
        check("ttl written")


def makeBasicGraph(extra_namespaces=[],graphlabel=None):
    """each namespace a tuple (tag,URI) in extra_namespaces"""
    g,A=r.Graph(),gv.AGraph(directed=True,strict=False)
    g.namespace_manager.bind("rdf", NS.rdf)    
    g.namespace_manager.bind("rdfs",NS.rdfs)    
    g.namespace_manager.bind("xsd", NS.xsd)    
    g.namespace_manager.bind("owl", NS.owl)    
    for tag, namespace in zip(*extra_namespaces):
        g.namespace_manager.bind(tag, namespace)
    if graphlabel:
        gv.AGraph(directed=True,strict=False)
        A.graph_attr["label"]=graphlabel
    return g,A
def startGraphs(ids=("mid1","mid2"),titles=("Ontology1","ConceptX"),extra_namespaces=[]):
    ags={}
    for iid,title in zip(ids,titles):
         ags[iid]=makeBasicGraph(extra_namespaces)
         ags[iid][1].graph_attr["label"]=title
    return ags
def C(ag=[makeBasicGraph()],uri="foo",label="bar",superclass=None,comment=None,label_pt=None,comment_pt=None,color=None,graph_lang="en"):
    for gg in ag:
        g,A=gg
        G(g,uri,NS.rdf.type,NS.owl.Class)
        G(g,uri,NS.rdfs.label,LL_(label,lang="en"))
        if label_pt:
            G(g,uri,NS.rdfs.label,LL_(label_pt,lang="pt"))
        if graph_lang=="pt":
            A.add_node(label_pt,style="filled")
            nd=A.get_node(label_pt)
        else:
            A.add_node(label,style="filled")
            nd=A.get_node(label)
        if superclass:
            if type(superclass) in (type([1,2]),type((1,2))):
                for sp in superclass:
                    G(g,uri,NS.rdfs.subClassOf,sp)
                    #print([i for i in g.objects(sp,ns.rdfs.label)])
                    if graph_lang=="pt":
                        lsuperclass=[i for i in g.objects(sp,NS.rdfs.label) if i.language=="pt"][0].title()
#                        lsuperclass=[i for i in g.objects(sp,ns.rdfs.label) if i.lang=="pt"][0].title()
                        A.add_edge(  label_pt, lsuperclass)
                        e=A.get_edge(label_pt, lsuperclass)
                    else:
                        lsuperclass=[i for i in g.objects(sp,NS.rdfs.label) if i.language=="en"][0].title()
                        A.add_edge(  label, lsuperclass)
                        e=A.get_edge(label, lsuperclass)
                    e.attr["arrowhead"]="empty"
                    e.attr["arrowsize"]=2
            else:
                G(g,uri,NS.rdfs.subClassOf,superclass)
                #lsuperclass=[i for i in g.objects(superclass,rdfs.label)][-1]
                if graph_lang=="pt":
                    lsuperclass=[i for i in g.objects(superclass,NS.rdfs.label) if i.language=="pt"][0]
                    A.add_edge(  label_pt, lsuperclass)
                    e=A.get_edge(label_pt, lsuperclass)
                else:
                    lsuperclass=[i for i in g.objects(superclass,NS.rdfs.label) if i.language=="en"][0]
                    A.add_edge(  label, lsuperclass)
                    e=A.get_edge(label, lsuperclass)
                e.attr["arrowhead"]="empty"
                e.attr["arrowsize"]=2
        if comment:
            if type(comment) in (type([1,2]),type((1,2))):
                for co in comment:
                    G(g,uri,NS.rdfs.comment,LL_(co,lang="en"))
            else:
                G(g,uri,NS.rdfs.comment,LL_(comment,lang="en"))
        if comment_pt:
            if type(comment_pt) in (type([1,2]),type((1,2))):
                for co in comment_pt:
                    G(g,uri,NS.rdfs.comment,LL_(co,lang="pt"))
            else:
                G(g,uri,NS.rdfs.comment,LL_(comment_pt,lang="pt"))
        if color:
            nd.attr['color']=color
def IC(ga=None,uri=r.URIRef("http://foo.bar"),string="astringid",label=None,draw=False):
    ind=uri+"#"+str(string)
    if ga:
        for g,A in ga:
            G(g,ind,NS.rdf.type,uri)
            if label:
                G(g,ind,NS.rdfs.label,LL_(label))
            if label and draw:
                A.add_node(label,style="filled")
                nd=A.get_node(label)
                nd.attr['color']="#02F3DD"
            elif draw:
                raise ValueError("draw=True but no label")
    return ind

def linkClasses(ga=[makeBasicGraph()],ind=r.URIRef("http://foo.bar"),\
        props=["uri1","uri2"],objs=["uri1","uri2"],draw=False):
    """Link ind subject instance with the objs classes through the props"""
    if draw:
        labels=[0]*len(props)
    for prop, obj, label in zip(props,objs,labels):
        for g,A in ga:
            G(g,ind,prop,obj)
            if draw:
                g.query("SELECT ?s WHERE { <%s> rdfs.label ?label }"%(obj,))
                slabel_=subject_label.replace("%","")
                A.add_edge(  slabel_,label)
                e=A.get_edge(slabel_,label)
                e.attr["label"]=prop.split("/")[-1]

def linkData(ga=[makeBasicGraph()],ind="uriref",props=[NS.po.foo,NS.po.bar],vals=["val1","val2"],label=None):
    """Link an instance with the vals through the props"""
    global COUNT
    # acha o name do uriref buscando no grafo
    for prop, val in zip(props,vals):
        for g,A in ga:
            G(g,ind,prop,LL_(val))
            if label:
                A.add_node(COUNT,style="filled")
                nd=A.get_node(COUNT)
                nd.attr["label"]=val
                nd.attr['color']="#02F3F1"
                label=label.replace("%","FOO")
                A.add_edge(  label,COUNT)
                e=A.get_edge(label,COUNT); COUNT+=1
                e.attr["label"]=prop.split("/")[-1]

def P(ag=[makeBasicGraph()],uri="foo",label="bar",label_pt=None,comment=None):
    """Add object property to RDF graph"""
    for gg in ag:
        g=gg[0]
        G(g,uri,NS.rdf.type,NS.owl.ObjectProperty)
        G(g,uri,NS.rdfs.label,LL_(label,lang="en"))
        if label_pt:
            G(g,uri,NS.rdfs.label,LL_(label_pt,lang="pt"))
        if comment:
            G(g,uri,NS.rdfs.comment,LL_(comment,lang="en"))

def D(ag=[makeBasicGraph()],uri="foo",label="bar",dtype=NS.xsd.string,comment=None,label_pt=None):
    """Add data property to RDF graph"""
    for gg in ag:
        g=gg[0]
        G(g,uri,NS.rdf.type,NS.owl.DatatypeProperty)
        G(g,uri,NS.rdfs.label,LL_(label,lang="pt"))
        G(g,uri,NS.rdfs.range,dtype)
        if comment:
            G(g,uri,NS.rdfs.comment,LL_(comment,lang="en"))
        if label_pt:
            G(g,uri,NS.rdfs.label,LL_(label_pt,lang="pt"))
def L_(ga,sub,pred,obj):
    for g,A in ga:
        G(g,sub,pred,obj)
        # draw
        # get names
        # make edge
        bb=g.query(query_,initBindings={"fid":sub})
        sname=[i for i in bb][0][0].value
        bb=g.query(query_,initBindings={"fid":obj})
        oname=[i for i in bb][0][0].value
        A.add_edge(sname,oname)
        e=A.get_edge(sname,oname)
        e.attr["label"]=pred.split("/")[-1]

def L(ag=[makeBasicGraph()],olabel="foo",llabel="bar",dlabel="baz"):
    """Add object property link with labels for origin, link, destination"""
    for gg in ag:
        A=gg[1]
        A.add_edge(  olabel,dlabel)
        e=A.get_edge(olabel,dlabel)
        e.attr["label"]=llabel
def LD(ag=[makeBasicGraph()],olabel="foo",llabel="bar",dlabel="baz"):
    """Add data property link with labels for origin, link, destination"""
    global COUNT
    for gg in ag:
        A=gg[1]
        A.add_node(COUNT,style="filled")
        nd=A.get_node(COUNT)
        nd.attr["label"]=dlabel
        nd.attr['color']="#A2F3D1"
        A.add_edge(  olabel,COUNT)
        e=A.get_edge(olabel,COUNT); COUNT+=1
        e.attr["label"]=llabel

def namespaces(ids=[]):
    """Declare namespace URIs in RDF graph and return a dictionary of them.
    
    input: list of ids. Use tuple for (idstring, URIString) of
    benefint from RDFLib and particpatory IDs 
    throughtput: declare RDF in graph g
    output: dictionary of {key=id, value=URI} as declared
    
    Deals automaticaly with namespaces from RDFlib and selected
    participatory libs"""
    idict={}
    for tid in ids:
        # findig URIRef 
        if type(tid)!=type("fooString"): # tuple (tid,iuri)
            idict[tid[0]]=r.Namespace(tid[1])
        elif tid in [fooString.lower() for fooString in dir(r.namespace)]: # rdflib shortcut
            if tid in dir(r.namespace):
                idict[tid]=eval("r.namespace."+tid)
            else:
                idict[tid]=eval("r.namespace."+tid.upper())
        else: # participatory shortcut
            idict[tid]=r.Namespace("http://purl.org/socialparticipation/{}/".format(tid))
        # adding to RDF Graph
        if type(tid)!=type("fooString"): # tuple (tid,iuri)
            g.namespace_manager.bind(tid[0], idict[tid[0]])    
        else:
            g.namespace_manager.bind(tid, idict[tid])    
    return idict
def ID_GEN(namespace,tid):
    ind=namespace+"#"+tid
    G(ind,ns["rdf"].type,namespace)
    return ind

