==================================================================
Percolate your social systems
==================================================================

This project delivers helper classes for the analysis of Linked Open Social Data.
Install with:

    $ pip install percolation

or

    $ python setup.py install

For greater control of customization (and debugging), clone the repo and install with pip with -e:

    $ git clone https://github.com/ttm/percolation.git

    $ pip install -e <path_to_repo>

This install method is especially useful while reloading modified module in subsequent runs of percolation
usually with the standard importlib.

Percolation unites Social, Music and Visuals packages to enable anthropological physics experiments and social harnessing.

Core features
=============

    - Ease percolation in social systems by processes such as collection and diffusion of information.
    - Enable knowledge about the networked self.
    - Generation of activity reports.                                 
    - Make abstract animations from social data.                      
    - Make standalone music from social data or to fit animation as soundtrack.

    - Integration of resources through RDF data and OWL ontologies.  

    - Directions for agents and networks typologies.
    - Verification of expected stability and differentiation on the social structures.

    - Cross provenance resource recommendation, extending facilities from the Participation package.


Plese check this PDF for further information:

    - https://github.com/ttm/percolation/raw/master/latex/percolation-article.pdf

Coding conventions:

    - A function name has a verb if t changes state of initialized objects, if it only "returns something", it is has no verb in name.

    - Classes, functions and variables are writen in CamelCase, headlessCamelCase and lowercase, respectively. Underline is used only in variable names where the words in variable name make something unreadable (usually because the resulting name is big).

    - Code should be very readable to avoid writing unnecessary documentation and duplicating routine representations. The code is the documentation. This adds up to using docstrings to give context to the objects or omitting the docstrings.

    - The usual variables in scripts are: P for percolation, NS for P.rdf.NS for namespace, a for NS.rdf.type, c for P.utils.check, S for social, M for music, V for visuals, n for numpy, p for pylab, r for rdflib, x for networkx

    - The modules are: 
      
        - bootstrap for bootstrapping percolation server and session (startup() is the canonic startup routine)
        - legacy for usage outlines and standard analyses and media rendering routines of tables and with music and visuals
        - rdf to ease add, save and navigation in rdflib graphs (all in rdf.io + rdf.ontology.makeOntolgy + rdf.utils)

                - rdf.ontology to organize ontology by parts and primarily in functions as they only return the triples or graph
                - rdf.sparql for SparQL standard and legacy routines (imports only most useful objects from sparql.classes and sparql.functions)

        - text for measures of text
        - topology for making networks, getting measures, making erdos sectorialization and meaningful sequences of participants
        - time for circular statistics and other measures from timestamps
        - integrated for integrated measures of text, topology and time measures # erdos sectorialization, KS and joint PCA

                - integrated.timeline
                - integrated.multiscale

        - analyses for rendering knowledge from text, topology, time and integrated measures.

        - statistics for obtaining statistics from measures:
          
                - statistics.kolmogorov_smirnov for measures of KS distance and the c statistic
                - statistics.pca for principal component analysis statistics
                - statistics.unit_root_tests for e.g. the augmented Dickey–Fuller test
                - statistics.outliers for detection of outliers in data
                - statistics.power_law for measures from optimal power-law fit to data
                - statistics.numeric_utilities (e.g. creating mean and standard deviation variables from array of arrays)

        - utils for small utilities in using percolation

                - utils.files for helpers in retrieving filenames and making names according to protocols
                - utils.utils for general purpose utilities (e.g. get unique values from sequence without modifying its order)
                - utils.poetry for making poetry from text
                - utils.tables for rendering latex and html tables

        - web for integration to the WWW through flask, js and meteor.

        - help for helper routines (e.g. wizard or steps to make something).

    - The modules can be classified with respect to its functionalities:

        - System administration: startup, legacy, help. These modules ease use of percolation with startup and usage routines.
        - Information architecture: rdf, utils. These modules ease accessing and modifying informational structure of percolation.
        - Measuring: text, topology, time. These modules take measures and build basic structures for so.
        - Knowledge achievement: integrated, statistics and analyses.

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

