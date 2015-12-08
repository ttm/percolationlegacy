# this file should exemplify data upload and retrieval in a Jena/Fuseki instance
# both named graphs and to default graph should be addressed
from SPARQLWrapper import SPARQLWrapper, JSON

# ./s-put http://200.144.255.210:8082/dsfoo <http://banana.com> /disco/repos/music_tw/rdf/music_twTranslate00000.owl
# ./s-query --service http://200.144.255.210:8082/dsfoo  'SELECT (COUNT(?s) as ?cs)  WHERE { GRAPH <http://banana.com> { ?s <http://purl.org/socialparticipation/tw/sentAt> ?o } }'
# ./s-put http://200.144.255.210:8082/dsfoo default /disco/repos/labMacambiraLaleniaLog2/rdf/labMacambiraLaleniaLog2Translate.owl


# query both default and named
eurl="http://200.144.255.210:8082/dsfoo/query"
eurl2="http://200.144.255.210:8082/dsfoo/update"
sparql = SPARQLWrapper(eurl)
sparql2 = SPARQLWrapper(eurl2)
q1="""SELECT (COUNT(?s) as ?cs) WHERE {?s <http://purl.org/socialparticipation/irc/sentAt> ?o}"""

sparql.setQuery(q1)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

q2="""SELECT (COUNT(?s) as ?cs) WHERE { GRAPH <http://banana.com> { ?s <http://purl.org/socialparticipation/tw/sentAt> ?o} } """

sparql.setQuery(q2)
sparql.setReturnFormat(JSON)
results2 = sparql.query().convert()
# upload to a new named
# query it

q1_="""SELECT (COUNT(?s) as ?cs) WHERE {?s <http://purl.org/socialparticipation/tw/sentAt> ?o}"""
q2_="""SELECT (COUNT(?s) as ?cs) WHERE { GRAPH <http://banana.com> { ?s <http://purl.org/socialparticipation/irc/sentAt> ?o} } """

sparql.setQuery(q1_)
sparql.setReturnFormat(JSON)
results_ = sparql.query().convert()

sparql.setQuery(q2_)
sparql.setReturnFormat(JSON)
results2_ = sparql.query().convert()

#q3="LOAD <file:https://raw.githubusercontent.com/OpenLinkedSocialData/bundle_tw/master/python_tw/rdf/python_twTranslate00000.owl> INTO GRAPH <http://graph.foo>"
#sparql.addParameter("named-graph-uri","<http://graph.foo>")
q3="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/bundle_tw/master/python_tw/rdf/python_twTranslate00000.owl> INTO <http://graph.foo>  "
sparql.setQuery(q3)
#sparql.setReturnFormat(JSON)
#results3 = sparql.query().convert()
q3_="""SELECT (COUNT(?s) as ?cs) WHERE {GRAPH <http://graph.foo> { ?s <http://purl.org/socialparticipation/tw/sentAt> ?o } }"""
sparql.setQuery(q3_)
sparql.setReturnFormat(JSON)
results3_ = sparql.query().convert()

q4="""SELECT (COUNT(?s) as ?cs) WHERE {GRAPH <http://graph.foo> { ?s <http://purl.org/socialparticipation/tw/sentAt> ?o } }"""
q4_="""CREATE GRAPH <http://graphBARLOBO.foo>"""
q5="SELECT DISTINCT ?g WHERE { GRAPH ?g { } }"
sparql2.setQuery(q4_)
sparql2.setReturnFormat(JSON)
res=sparql2.query().convert()

#q5="SELECT DISTINCT ?g WHERE { GRAPH ?g { } }"
q4="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/bundle_tw/master/python_tw/rdf/python_twTranslate00000.owl> INTO GRAPH <http://graphBARLOBO.foo>  "
sparql2.setQuery(q4)
sparql2.setReturnFormat(JSON)
res2=sparql2.query().convert()
#sparql.addNamedGraph("named-graph-uri","http://graph.foo")
#sparql.addNamedGraph("http://graph.foo")
#sparql.addNamedGraph("http://graph.foo")
##sparql.setReturnFormat(JSON)
##sparql.query()
sparql.setQuery(q5)
sparql.setReturnFormat(JSON)
results5 = sparql.query().convert()
# agora uploadar para algum named graph
#from rdflib.plugins.stores import sparqlstore
#store = sparqlstore.SPARQLUpdateStore()
#store.open((endpoint, endpoint))

#q3="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/bundle_tw/master/python_tw/rdf/python_twTranslate00000.owl> INTO <http://graph.foo>"







# PREFIX dc: <http://purl.org/dc/elements/1.1/>
# PREFIX ns: <http://example.org/ns#>
# INSERT DATA
# { GRAPH <http://example/bookStore> { <http://example/book1>  ns:price  42 } }
