import percolation as P
import  importlib
from IPython.lib.deepreload import reload as dreload
#importlib.reload(P)
importlib.reload(P.rdf)
#importlib.reload(g.listDataStructures)
#importlib.reload(g.interactionNetwork)
#importlib.reload(pe.linkedData)
##dreload(pe,exclude="pytz")
#dreload(pe)




tg=P.rdf.makeBasicGraph([["per"],[P.rdf.ns.per]],"The percolation ontology")
P.rdf.C([tg],P.rdf.ns.per.Dataset,"Dataset",
        comment="A collection of data typically in a computer readable format.",
        label_pt="Dataset")

P.rdf.C([tg],P.rdf.ns.per.Sequence,"Sequence",superclass=P.rdf.ns.per.Dataset,
        comment="A sequence of data snapshots, possibly ordered with respect to time or another reference.",
        label_pt="Sequência")

P.rdf.C([tg],P.rdf.ns.per.Snapshot,"Snapshot",
        superclass=P.rdf.ns.per.Dataset,color="#F29999",
        comment="a collection of data taken together as a unit of analysis.",
        label_pt="Snapshot")

P.rdf.C([tg],P.rdf.ns.per.Analysis,"Analysis",superclass=P.rdf.ns.per.Dataset,
        comment="A quantitative analysis expressed by numbers, datastructures and interpretations.",
        label_pt="Análise")

P.rdf.C([tg],P.rdf.ns.per.SequenceAnalysis,"Sequence Analysis",superclass=P.rdf.ns.per.Analysis,
        comment="A sequence of data snapshots, possibly ordered with respect to time or another reference.",
        label_pt="Análise de Sequência")

P.rdf.C([tg],P.rdf.ns.per.SnapshotAnalysis,"Snapshot Analysis",superclass=P.rdf.ns.per.Analysis,
        color="#F29999", comment="a collection of data taken together as a unit of analysis.",
        label_pt="Análise de Snapshot")

P.rdf.C([tg],P.rdf.ns.per.Provenance,"Provenance",
        comment="A class for whatever informations about the provenance of the data.",
        label_pt="Proveniência")


P.rdf.P([tg],P.rdf.ns.per.provenance,"provenance","proveniência")
P.rdf.L([tg],"Snapshot","provenance","Provenance")

P.rdf.D([tg],P.rdf.ns.per.createdAt,"created at",P.rdf.ns.xsd.datetime)
P.rdf.LD([tg],"Provenance","created at","xsd:datetime")

P.rdf.D([tg],P.rdf.ns.per.donatedBy,"donated by",P.rdf.ns.xsd.string)
P.rdf.LD([tg],"Provenance","donated by","xsd:string")

P.rdf.D([tg],P.rdf.ns.per.availableAt,"available at",P.rdf.ns.xsd.string,
        "an instance where the data can be found, preferably a URL where the data is publicly available")
P.rdf.LD([tg],"Provenance","available at","xsd:string")

P.rdf.P([tg],P.rdf.ns.per.meronym,"meronym","meronímia")
P.rdf.P([tg],P.rdf.ns.per.holonym,"holonym","holonímia")
#P.rdf.L([tg],"Sequence","meronym","Snapshot")
P.rdf.L([tg],"Snapshot","holonym","Sequence")
#P.rdf.L([tg],"Sequence","meronym","Snapshot")

P.rdf.D([tg],P.rdf.ns.per.platform,"platform",P.rdf.ns.xsd.string,
"a name or identifier for the social media platform from which the data was collected","plataforma")
P.rdf.LD([tg],"Snapshot","platform","xsd:string")

P.rdf.P([tg],P.rdf.ns.per.enables,"enables","enables")
P.rdf.L([tg],"Snapshot","enables","Snapshot Analysis")
P.rdf.L([tg],"Sequence","enables","Sequence Analysis")

P.rdf.writeAll(tg,"PO","./",True)

