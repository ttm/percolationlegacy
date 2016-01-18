__doc__="""Usage outlines of the percolation package as python objects

Outlines:
    overall
    void
    topologicalAnalysis
    textualAnalysis
    integratedAnalysis
    detaiedTablesAndFigures
    music
    animation
    article
    game
    selfHarness
    tipMeCrazyMe # asks for a string (of words please, can make language detection)
                   # and performs random/arbitrary matches in participants names and texts,
                   # random/arbitrary data query,
                   # random/arbitrary media (animation/music/article) rendering
    motherfatherShip # connect to openlinkedsocialdata endpoint for direct harnessing
               # asks user if he wants to give his name for a demo media rendering
               # make some demo media, with found name, name silabes or parts or "intergalatic_mode"
               # maintain a status graph in endpoint for this mode
    helpMe # provides instructions on using percolation, social, music, audiovisual and openlinkedsocialdata.
    ontologyFramework # some operations on the ontology to exhibit knowledge represented and utility
    demo # a demo outline, can be tipMeCrazy, motherfatherShip or overall
    js # render js files, probably within rdf and d3 frameworks, possibly for use with meteor
    flask # start a flask server with minimum or user defined data, with sparql and other capabilities
    benchmarks # obtain benchmarks from simulations 
                        # Kolmogorov-Smirnov, circular min/max, pca test standards, unit root test, simulation from given context
               # obtain benchmarks from empirical data:
                        # OpenLinkedSocialData
    getData # guide user to get own data from fb, irc, twitter, etc.
            # other institutions, including ones in which the participant strives.
            # donate data raw or from gmane or netvizz, start own endpoint, 
            # use legacy on Social and OpenLinkedSocialData



Notes:
    Keep updating status graph in B.status_graph (a rdflib.Graph())

    Erdos setorialization should be applied with respect to all measures.
    Ideally, Erdos setorialization (the attribution of groups to data by comparison
    of data agains a binomial model) should be applied is all domains.
    (as participants vs degrees, do messages x size).
    Take measures to corroborate
    or refute the overly spoken hypothesis
    that empirical data values yield most often heavy tailed or even power-law distributions.
    
    Analyses should deliver quanlitative hypotheses.
    Type them as strong and weak hypotheses, with type related to the measures it is based upon.
    For example:
        if substantive token sizes in chars between intermediary and peripheral sectors
        exhibit KS distance and c measures
        are above \\alpha and \\beta in  are above x threshold, assume 

    
    """

import percolation as P, os, rdflib as r

def standardPercolationStartup2(percolationdir="~/.percolation/"):
    P.start()
def standardPercolationStartup(percolationdir="~/.percolation/"):
    percolationdir=os.path.expanduser(percolationdir)
    if not os.path.isdir(percolationdir):
        os.mkdir(percolationdir)
    dbdir=percolationdir+"sleepydb/"
    if not os.path.isdir(dbdir):
        os.mkdir(dbdir)
    percolation_graph=r.ConjunctiveGraph(store="Sleepycat")
    try:
        percolation_graph.open(dbdir, create=False)
    except:
        percolation_graph.open(dbdir, create=True)
        po=P.rdf.minimumOntology("triples")
        metadata=P.rdf.legacyMetadata("triples")
        percolation_graph.add(po+metadata)
    else:
        assert rt == VALID_STORE, 'The underlying store is corrupt'
    # add percolationdir and dbdir to percolation_graph
    return percolation_graph


def startupCustomPercolationGraph(custom_pg_path="./where/db/is/"):
    percolation_graph=r.ConjunctiveGraph("Sleepycat")
    rt = percolation_graph.open(custom_pg_path, create=False)
    P.percolation_graph=percolation_graph

def startupStandard():
    # import percolation as P
    # which starts the percolation graph with persistence
    pass

def FirstUsageOutline():
    """an example of a first usage"""
    P.statusStatistics()
    P.describeSnapshots()
    P.pickSnapshot()
    P.analyse()
    P.describeSnapshots()
    P.describeSnapshot()
    P.renderMedia("last")

def MinimizedOutline2():
    P.pickSnapshot()
    P.snapshotStatistics()
def MinimizedOutline():
    P.start()
    P.demo() # get some data statistics and make some media
def overallOutline():
    """The most simple but overall usage of percolation features
    
    ToDo:
    P.web.startMeteor()
    P.sparql.linkToEndpoint("http://dbpedia.org/sparql")
    P.web.linkToEndpoint("http://dbpedia.org/sparql")
    P.rdf.voidStatistics()
    P.rdf.voidStatistics(NS.dbp.AlbertCamus)"""

    po=P.rdf.ontology() # rdflib.Graph()
    metadata=P.rdf.legacyMetadata() # rdflib.Graph()
    percolation_graph=po+metadata # rdflib.Graph()
    snapshot=P.rdf.oneTranslate() # URI
    network=P.topology.makeNetwork(snapshot) # networx network
    topological_analysis=P.topology.analyse(network) # rdflib.Graph()
    textual_analysis=P.text.analyse(snapshot) # rdflib.Graph()
    integrated_analysis=P.integrated.analyse(snapshot) # rdflib.Graph()
    P.tables.make(integrated_analysis,"/tables/") # render latex, js and md tables
    P.audiovisuals.make(integrated_analysis,"/av/") # render sonification in sync with stopmotion animation from data
    user_uri=P.oneUser(integrated_analysis) # uri
    P.audiovisuals.makeMusic(integrated_analysis,"/av/",focus=user_uri) # render music
    P.web.startServer(port=5077) # start server in localhost:5077 or better specify


