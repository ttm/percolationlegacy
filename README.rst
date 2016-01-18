==================================================================
Percolate your social systems
==================================================================

This project delivers helper classes for the analysis of the GMANE
email database. Install with:

    $ pip install percolation

or

    $ python setup.py install

For greater control of customization (and debugging), clone the repo and install with pip with -e:

    $ git clone https://github.com/ttm/percolation.git

    $ pip install -e <path_to_repo>

This install method is especially useful with
reload function from IPython.lib.deepreload and the standard importlib.


Percolation unites Gmane, Participation, Social and MASS packages to enable anthropological physics experiments and social harnessing. Core features are:  

    - Ease percolation in social systems by processes such as collection and diffusion of information.

    - Enable knowledge about the networked self.

    - Make abstract animations from social data.                      

    - Make music from social data to fit animation as soundtrack.

    - Verification of expected stability and differentiation on the social structures.

    - Directions for agents and networks typologies, extending features from Gmane package.

    - Integration of resources through RDF data and OWL ontologies.  

    - Routines for representing data from social networks (tweets, Facebook data, IRC logs, LinkedIn, Gmane lists) as RDF.

    - Cross provenance resource recommendation, extending facilities from the Participation package.

    - Generation of activity reports.                                 


Plese check this PDF for further information:

    - https://github.com/ttm/percolation/raw/master/latex/percolation-article.pdf

Coding conventions:

    - A function name has a verb if t changes state of initialized objects, if it only "returns something", it is has no verb in name.

    - Classes, functions and variables are writen in CamelCase, headlessCamelCase and lowercase, respectively. Undeline is used only in variable names where the words in variable name make something unreadable (usualy because the resulting name is big).

    - Code should be very readable to avoid writing unecessary documentation and duplicating routine representations. The code is the documentation. This adds up to using docstrings to give context to the objects or omiting the docstrings.

    - The usual variables in scrits are: P for percolation, NS for P.rdf.NS for namespace, a for NS.rdf.type, c for P.utils.check, S for social, M for music, V for visuals, n for numpy, p for pylab, r for rdflib, x for networkx

    - The modules are: 
      
        a. start for the most canonical startup routine.
        b. legacy for usage outlines and standard analysis and media rendering routines
        a. rdf to ease add, save and navigation in rdflib graphs (all in rdf.io + rdf.ontology.makeOntolgy)
        b. rdf.ontology to organize ontology by parts and primarily in functions as they only return the triples or graph.
        h. text for statistics and analyses of text and making poetry # measures + pca
        i. topology for making networks, getting measures, making erdos sectorialization and getting meaningfull sequences of participants
        j. integrated for integrated analyses of text and topology # erdos sectorialization, KS and joint PCA
        x. analyses for analysis of individual snapshots an one measure to multiscale and timeline analyses # 
        k. statistics for Kolmogorov-Smirnov, PCA, circular measures, unit root tests and numeric utilites (import stats.ks .pca .urt .utils)
        c. utils.files for helpers in retrieving filenames and making names according to protocols
        d. utils.tables for rendering tabular data
        f. sparql for SparQL standard and legacy routines (imports only most useful objects from sparql.classes and sparql.functions)
        l. help for helper routines (e.g. wizard or steps to make something).


    - the file cureimport.py in newtests avoids cluttering the header of the percolation file while hacking framework. In using the Python interpreter, subsequent runs of scripts don't reload or raise error with importlib if the prior error was on load. Justo load it first: import cureimport, percolation as P, etc.

    - the variable P.percolation_graph is a ConjunctiveGraph with all execution state information metadata and translates and with each variable value as value, a bag (unordered, e.g. word sizes) or a collection (ordered, principal components, etc).

    - in the integrated measures, see if networks that have peculiar distribution of measures in erdos sectors also have smaller KS-distance between histograms of degrees and other topological measures. Generalizing, see if structures with an outlier os a measure is correlated with another measures characteristics, such as the correlation histogram.

    - every feature should be related to at least one outline.

    - routines should be oriented towards making or navigating percolation graph paths directly or through numeric computation and rendering of new triples or through navigating the local filesystem, legacy filesystem or connecting to an Open Linked Data sparql endpoint such as:
     .. _DBPedia: http://dbpedia.org/sparql

Usage example
=================

.. code:: python

    import percolation as P

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


