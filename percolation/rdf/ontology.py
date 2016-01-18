__doc__="primary source of the participation ontology by parts in triples and functions.

ToDo:
    write the Fuseki configuration file as triples in a function here.
"
def minimumOntology(context=None):
    triples=rdfsTriples()
    if context=="triples":
        return triples
    P.percolation_graph.add(triples)
def rdfsTriples():
    """Sub Class/Property and range domain assertions"""
    # about snapshots:
    # about ?? (take alook below or wait for need)

def localFiles(): pass
def localFilesVM(): pass
def onlineFiles(): pass


def externalSparQLConfiguration():
    triples=[
            (NS.po.SparqlEndpoint+"#DBPedia",NS.void.sparqlEndpoint,"http://localhost:9082/RTDB"),
            (NS.po.Percolation, NS.po.sparqlEndpoint, NS.po.SparqlEndpoint+"#DBPedia"),
            ]
    return triples
def developmentSparQLConfiguration():
    triples=[
            (NS.po.Percolation, NS.po.sparqlEndpoint, NS.po.SparqlEndpoint+"#DEV2"),
            (NS.po.SparqlEndpoint+"#DEV2",NS.void.sparqlEndpoint,"http://localhost:9082/RTDB"),
            (NS.po.SparqlEndpoint+"#DEV2",NS.rdfs.comment,"for local development in the VM with Fuseki"),
            (NS.po.SparqlEndpoint+"#DEV2",NS.rdfs.label,"dev2"),
            ]
    return triples
def publishingSparqlConfiguration():
            (NS.po.SparqlEndpoint["#sparql"], NS.void.sparqlEndpoint, "http://openlinkedsocialdata.org/sparql"),
            (NS.po.SparqlEndpoint+"#DEVAA",NS.void.sparqlEndpoint,"http://openlinkedsocialdata/AA/"),
            (NS.po.SparqlEndpoint+"#AA",   NS.void.sparqlEndpoint,"http://openlinkedsocialdata/AA/"),
            (NS.po.SparqlEndpoint+"#AA",   NS.void.sparqlEndpoint,"for using AA, i.e. for sharing frfr"),
            (NS.po.SparqlEndpoint+"#AA",   NS.void.sparqlEndpoint,"dev1"),
            (NS.po.Percolation, NS.po.sparqlEndpoint, NS.po.SparqlEndpoint+"#AA"),

def developmentLiterature():
    triples=[
            (NS.po.Literature+"#Document1",NS.po.url,"https://www.w3.org/2005/04/fresnel-info/manual/"),
            (NS.po.Literature+"#Document1",NS.rdfs.comment,"Fresnel Lens for specification of which structures are in each view and is which format"),
            (NS.po.Literature+"#PythonSparQLServer1",NS.po.url,"https://projects.bigasterisk.com/sparqlhttp/"),
            (NS.po.Literature+"#PythonSparQLServer2",NS.po.url,"https://github.com/RDFLib/rdflib-web"),
            (NS.po.Literature+"#PythonSparQLServer2",NS.po.url,"http://rdflib-web.readthedocs.org/en/latest/"),
            (NS.po.Literature+"#DocumentCollection1",NS.po.url,"https://www.w3.org/DesignIssues/"),
            (NS.po.Literature+"#DocumentCollection1",NS.rdfs.comment,"Tim Berners-Lee's outline of architectural principles for thinking specifications."),
            (NS.po.Literature+"#BFO",NS.po.url,"https://raw.githubusercontent.com/BFO-ontology/BFO/master/releases/2.0/bfo.owl"),
            (NS.po.Literature+"#BFO",NS.rdfs.comment,"BFO 2.0"),
            (NS.po.Literature+"#BFO",NS.rdfs.label,"bfo"),
            (NS.po.Literature+"#BFO",NS.doap.repository,"https://github.com/bfo-ontology/BFO/"),
            (NS.po.Literature+"#BFO",NS.foaf.homepage,"http://ifomis.uni-saarland.de/bfo/"),

            (NS.po.Literature+"#MusicPlug",NS.po.url,"https://www.youtube.com/watch?v=noL0qY48gug"),
            (NS.po.Literature+"#MusicPlug",NS.rdfs.comment,"Get from before 33m until 42m. Use attack (note onset), BPM and spectral analysers to make music.\n\
                    Use chokurei and other symbles as tracks for some sections.
                    Show sections of the network chosen by walks in measures or geometric walks."),
            NS.po.Note+"#ContagionGame", rdfs.comment,"think on contagion just as in plague inc (steam games).\n\
                    Data can be taken from dbpedia, randomized to make other world or be set by user.\n\
                    Percolation techniques ease adoptors of world transcendence,\n\
                    these fertilize/infect/influence others, game is won when world transcends.
                    Make text-mode demo with continents. Translate into D3js (or Netlogo)."


            ]
    return triples



def handNotes():
    """Triples obtained from anotation 'by hand', i.e. triples are direct anotation of a participant"""
    triples=handFabbriNotes()
    triples+=handSomeoneFoo()
    return triples
def handNotesSomeoneFoo(): pass
def handNotesFabbri():
    linkstring="Raul para quando/onde ele vai tocar\
                Markun/Capi para raspagem e criações diversas\
                Vilson p js/lm/vida\
                Marilia p Teoria Crítica/Filosofia/Antropologia/Psicanálise/Cranio/percolação\
                Penalva p física/matemática/percolação\
                Rita p vestíveis/percolação/arte/cranio/arquitetura\
                Savazone p literatura/arte\
                Thata p igreja/arte/música/percolação\
                Alfaix p música/arte/stockhausen\
                Priscila p antonio/campo grange/antropologia/mobilizacao pela causa indígena\
                Chu p VM/doc/Nilc/publicacoes/polimeros\
                Joioso p VM\
                LM p comunicado/convocação/compartilhamento/ideia\
                Iwao p música/percolação\
                Besouro p percolação/arte\
                PrLeandro p percolação/bíblia\
                Wanilton p percolação/bíblia\
                Elbio p rio/daime/percolacao\
                VGrilo p ceará/daime/percolacao\
                Yonashiro p música/arte/transcendência\
                Jorge Antunes p música/arte\
                Deborah Antunes p personalidade autoritária\
                Júlia Tygel p música/antropologia\
                Renata de Paula p espiritismo/percolação\
                Nitai p dados ligados/minc\
                Boechat p bíblia/ipc\
                Luis Henrique p jornalismo/filosofia/arte contemporânea/vida\
                Rogério Lourenço p antropologia/transcendencia\
                Pablo Pascale p labic/percolação\
                Massom p artes plásticas\
                Marta p daime/video/gamarra\
                Camila p daime/sociologia/gamarra/percolação\
                Ligia p daime/transcendência/percolação\
                Ricardo Fabbri p vida/transcendência/percolação/computação/matemática\
                Maurício Fabbri p vida/computação/matemática\
                Cláudia Lopes p matemática/tangran/vida/culinária\
                Oda p trancendencia/móveis montessori/imagens/processing/dengue\
                Gilberto Macruz p transcendência/artes plásticas\
                Sandra Leão p transcendência/música/rádio/dj\
                Lunhani p transcendência/música/rádio/composição\
                Fernando Gularte p transcendência/música/literatura/matematica\
                Fabib p transcendência/psicologia/esquizoanálise/submidialogia/tecnoxamanismo\
                Goa p transcendência/computação/cultura livre/juntadados\
                Marcelo Soares p computação/cultura livre/juntadados\
                Canevacci p antropologia/transcendência\
                Silvio Carneiro p filosofia/cautela\
                Henrique Xavier p filosofia/estética/arte/música\
                Porres p música/pd/percolação\
                Mario Nunzuo p música/basquete\
                Ivan Marin p física/computação/matemática\
                SPA p física/computação/matemática\
                Cristiane Godoy p física/computação/matemática\
                Sérgio Amadeu p cultura livre/sociologia\
                Chico Simões p tambores/maracatu/transcendência\
                Daniel Teixeira p java/bíblia\
                Caleb Luporini p processing/diy/\
                Leo Maia p física/matemática/percolação\
                Pedro Rocha para arte/transcendência/percolação\
                "
    triples=P.rdf.linkstringToTriples(NS.po.Participant+"#RenatoFabbri",linkstring)
    triples+=[
            (NS.po.Participant+"#RenatoFabbri", a, NS.po.Participant),
            (NS.po.Participant+"#RenatoFabbri", NS.po.personToContact, NS.po.Participant+"#Raul"),
            (NS.po.Participant+"#RenatoFabbri", NS.po.contactNotes, ),
            (NS.po.Participant+"#RenatoFabbri", NS.foaf.name, "Renato Fabbri"),
            (NS.po.Participant+"#RenatoFabbri",NS.foaf.mbox,"mailto:renato.fabbri@gmail.com"),
            ]
    return triples
def notes():
    notesFabbri()
    notesSomeoneFoo
def notesSomeoneFoo(): pass
def notesFabbri():
    triples=(
            (NS.po.Note+"#1",NS.po.text,"leave Fuseki a little bit and start making a Flask interface for dealing with RDF data"),
            (NS.po.Note+"#2",NS.po.text,"take mean and std of correlation matrix as a measure of coherence in the system."),
            (NS.po.Question+"#1",NS.po.text,"why declare owl:Class if only using rdfs:subClassOf,subClassOf,range,domain?"),
            (NS.po.Note+"#3",NS.po.text,"make reasoning by loop at least for benchmarking. Just iterate triples and add them to a aux graph."),
            )
    return triples
def poMetadata():
    triples=(
            (NS.po.po+".owl", a, NS.owl.Ontology),
            (NS.po.po+".owl", NS.dct.title, "The Participation Ontology"),
            (NS.po.po+".owl", NS.dct.title, "The Percolation Ontology"),
            (NS.po.po+".owl", NS.dct.title, "The Participation/Percolation Ontology"),
            (NS.po.po+".owl", NS.dct.description, "The Participation/Percolation Ontology eases integration of social data\
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



def po():
    triples=[
            (NS.po.Question, NS.rdfs.subClassOf, NS.po.Note),
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
            (NS.po.Percolation, NS.po.note, "Percolations.outlines misturam contexto e roteiro","pt"),
            (NS.po.Percolation, NS.po.note, "Percolation.outlines merge context and script","en"),
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

