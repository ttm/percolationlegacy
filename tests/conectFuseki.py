from SPARQLWrapper import SPARQLWrapper, JSON
import rdflib as r, percolation as P
c=P.utils.check
# ./s-query --service http://200.144.255.210:8082/lau_gmane  'SELECT (COUNT(?s) as ?cs) WHERE {?s <http://purl.org/socialparticipation/gmane/sentAt> ?o}'
#sparql = SPARQLWrapper("http://200.144.255.210:8082/lau_gmane")
#sparql.setQuery("""
#    SELECT ?s ?o
#    WHERE {
#         ?s gmane:sentAt ?o .
#    } limit 5
#""")
#sparql.setReturnFormat(JSON)
#results = sparql.query().convert()
#
#for result in results["results"]["bindings"]:
#    print(result["s"]['value'], result["o"]['value'])
#
#sparql = SPARQLWrapper("http://api.talis.com/stores/bbc-backstage/services/sparql")
#sparql = SPARQLWrapper("http://pt.dbpedia.org/sparql")
#sparql.setQuery("""
#    SELECT *
#    WHERE {  ?s ?p ?o . } LIMIT 10
#""")
#sparql.setReturnFormat(JSON)
#results = sparql.query().convert()
#for result in results["results"]["bindings"]:
#    print(result["s"]['value'])

#sparql = SPARQLWrapper("http://data.digitalsocial.eu/sparql")
#sparql.setQuery("""
#    SELECT DISTINCT ?p
#    WHERE {  ?s ?p ?o . }
#""")
#sparql.setReturnFormat(JSON)
#results = sparql.query().convert()
#for result in results["results"]["bindings"]:
#    print(result["p"]['value'])
#sparql.setQuery("""
#    SELECT DISTINCT ?s ?o ?p
#    WHERE {  ?s <http://data.digitalsocial.eu/def/ontology/reach/members> ?o . ?s ?p ?o2 }
#""")
#sparql.setReturnFormat(JSON)
#results = sparql.query().convert()
#for result in results["results"]["bindings"]:
#    print(result["s"]['value'],result["o"]['value'],result["p"]['value'])
#sparql.setQuery("""
#    SELECT DISTINCT ?s ?o ?o2
#    WHERE {  ?s <http://data.digitalsocial.eu/def/ontology/reach/members> ?o . ?s <http://purl.org/linked-data/cube#dataSet> ?o2 }
#""")
#sparql.setReturnFormat(JSON)
#results = sparql.query().convert()
#for result in results["results"]["bindings"]:
#    print(result["s"]['value'],result["o"]['value'],result["o2"]['value'])

#sparql = SPARQLWrapper("http://vocabulary.semantic-web.at/PoolParty/sparql/semweb")
#sparql.setQuery("""
#    SELECT DISTINCT ?p
#    WHERE {  ?s ?p ?o . }
#""")
#sparql.setReturnFormat(JSON)
#results = sparql.query().convert()
##for result in results["results"]["bindings"]:
##    print(result["p"]['value'])
#
#sparql.setQuery("""
#    SELECT DISTINCT ?s ?o
#    WHERE {  ?s <http://xmlns.com/foaf/0.1/knows> ?o . }
#""")
#sparql.setReturnFormat(JSON)
#results2 = sparql.query().convert()
#
#sparql.setQuery("""
#    SELECT DISTINCT ?p ?o 
#    WHERE {  <http://vocabulary.semantic-web.at/semweb/1225> ?p ?o . }
#""")
#sparql.setReturnFormat(JSON)
#results3 = sparql.query().convert()
#
#
#sparql.setQuery("""
#    SELECT DISTINCT ?o 
#    WHERE {  <http://vocabulary.semantic-web.at/semweb/1225> a ?o . }
#""")
#sparql.setReturnFormat(JSON)
#results4 = sparql.query().convert()
#
#
#sparql.setQuery("""
#    SELECT DISTINCT ?s
#    WHERE {  ?s a <http://xmlns.com/foaf/0.1/Person> . }
#""")
#sparql.setReturnFormat(JSON)
#results5 = sparql.query().convert()
#
#
#sparql.setQuery("""
#    SELECT DISTINCT ?s
#    WHERE {  ?s a <http://xmlns.com/foaf/0.1/Agent> . }
#""")
#sparql.setReturnFormat(JSON)
#results6 = sparql.query().convert()
#
# há poucas amizades no: http://vocabulary.semantic-web.at/PoolParty/sparql/semweb
# mas pode resultar em alguma rede de interação

hh="""
prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
prefix dct: <http://purl.org/dc/terms/> 
prefix dce: <http://purl.org/dc/elements/1.1/> 
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix skos: <http://www.w3.org/2004/02/skos/core#> 
prefix bibo: <http://purl.org/ontology/bibo/> 
prefix foaf: <http://xmlns.com/foaf/0.1/> 
prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> 
prefix aiiso:<http://purl.org/vocab/aiiso/schema#>
prefix teach:<http://linkedscience.org/teach/ns#>  

 """ 
qq="""
  SELECT DISTINCT ?p (COUNT(?p) AS ?count ) {
    ?s ?p ?o .
    } 
    GROUP BY ?p
    ORDER BY ?count
    """
sparql = SPARQLWrapper("http://data.aalto.fi/sparql")
#sparql.setQuery(hh+qq)
#sparql.setReturnFormat(JSON)
#results9 = sparql.query().convert()
#for result in results9["results"]["bindings"]:
#    print(result["p"]['value'],result["count"]['value'])
def mQuery(query,mvars):
    query_=query.format(*mvars)
    sparql.setQuery(hh+query_)
    sparql.setReturnFormat(JSON)
    results9 = sparql.query().convert()
    res=[]
    for result in results9["results"]["bindings"]:
        res.append([result[i]['value'] for i in mvars])
    return res
#qq=r"""
#  SELECT DISTINCT ?{} (COUNT(?p) AS ?{} ) {{
#    ?s ?p ?o .
#    }} 
#    GROUP BY ?p
#    ORDER BY ?count
#    """; mvars="p","count"
#mres=mQuery(qq,mvars)
#c("primeira query")
#qq=r"""
#  SELECT ?{} (COUNT(?o) AS ?{} ) {{
#    ?s a ?o .
#    }} 
#    GROUP BY ?o
#    ORDER BY ?count
#    """; mvars="o","count"
#mres2=mQuery(qq,mvars)
#c("segunda query")
#qq=r"""
#  SELECT ?{} (COUNT(?p) AS ?{} ) {{
#    ?s a bibo:Article .
#    ?s ?p ?o .
#    }} 
#    GROUP BY ?p
#    ORDER BY ?count
#    """; mvars="p","count"
#mres3=mQuery(qq,mvars)
#c("query 3")
#qq=r"""
#  SELECT ?{} ?{} {{
#    ?s a bibo:Article .
#    ?s dce:contributor ?o .
#    }} 
#    LIMIT 10
#    """; mvars="s","o"
#mres4=mQuery(qq,mvars)
#c("query 4")
## se admitirmos o nome separado por ; como id,
## vira fazer a rede de interacao com a string
## que retorna o contributor
#qq=r"""
#  SELECT ?{} ?{} ?{} {{
#    ?s a bibo:Article .
#    ?s bibo:authorList ?o .
#    ?s dce:contributor ?o2 .
#    }} 
#    LIMIT 10
#    """; mvars="s","o","o2"
#mres5=mQuery(qq,mvars)
#c("query 5")
#
#aa=mres5[-2]
#acount=aa[-1].count(";")+1
#qq=r"""
#  SELECT ?{} ?{} ?{} ?{} ?{} ?{} {{"""+\
#r"""    <{}> rdf:first ?a1 .
#    ?a1 foaf:name ?l1 .
#    <{}> rdf:rest ?foo .
#    ?foo rdf:first ?a2 .
#    ?a2 foaf:name ?l2 .
#    ?foo rdf:rest ?bar .
#    ?bar rdf:first ?a3 .
#    ?a3 foaf:name ?l3 .
#    }}}} """.format(aa[1],aa[1]); mvars="a1","l1","a2","l2","a3","l3"
#mres6=mQuery(qq,mvars)
#c("query 6")
#
#qq=r"""
#SELECT ?{} ?{} """+\
#r"""WHERE {{{{
#  <{}> rdf:rest*/rdf:first ?person . ?person foaf:name ?name .
#  }}}}
#""".format(aa[1]); mvars="person","name"
#mres7=mQuery(qq,mvars)
#c("query 7")
# puxa artigos com
# contributor, conta número de ; +1 é o número de autores
# puxado tb authorList, faz a query certa para obter
# as ids e labels com relação a cada Artigo.
# Estes são clicks, monta rede
qq=r"""
  SELECT ?{} ?{} {{
    ?s a bibo:Article .
    ?s bibo:authorList ?o .
      ?o rdf:rest*/rdf:first ?person .
      ?person foaf:name ?name .
    }} LIMIT 5000 
    """; mvars="name", "s"
c("antes query 8")
mres8=mQuery(qq,mvars)
c("query 8")
dd={}
for res in mres8:
    if res[-1] in dd.keys():
        dd[res[-1]]+=[res[0]]
    else:
        dd[res[-1]]=[res[0]]
# dd tem os cliques
import networkx as x
gg=x.Graph()
for key in dd:
    i=1
    for id1 in dd[key]:
        if gg.has_node(id1): gg.node[id1]["weight"]+=1.
        else:       gg.add_node(id1,weight=1.)
    for id1 in dd[key]:
        for id2 in dd[key][i:]:
            if gg.has_edge(id1,id2): gg[id1][id2]["weight"]+=1.
            else:       gg.add_edge(id1,id2,weight=1.)
        i+=1




# http://data.uni-muenster.de/sparql


# creator maker name members attendees individualMembers clients
# http://data.digitalsocial.eu/def/ontology/twitterAccount
