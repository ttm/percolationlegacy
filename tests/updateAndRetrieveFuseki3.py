import rdflib
g = rdflib.ConjunctiveGraph('SPARQLUpdateStore')
#g.open("http://dbpedia.org/sparql")
#res=[i for i in g.query("SELECT ?s WHERE { ?s ?p ?o . } LIMIT 5")]

#g.open("http://200.144.255.210:8082/dsfoo/update")
#g.open("http://200.144.255.210:8082/dsfoo/data")
g.open("http://200.144.255.210:8082/dsfoo/sparql")
#g.open("http://200.144.255.210:8082/dsfoo")
#g.open("http://200.144.255.210:8082/dsfoo")
#res2=[i for i in g.query("SELECT ?s WHERE { ?s ?p ?o . } LIMIT 5")]
#q="SELECT DISTINCT ?g WHERE { GRAPH ?g { } }"
#res3=[i for i in g.query(q)]
#ql2="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/music_tw/master/rdf/music_twTranslate00015.owl> "
#ql2="INSERT DATA { LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl> }  "
#ql2="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl>  "
#res4=[i for i in g.update(ql2)]

#g.update("http://dbpedia.org/page/Mohall,_North_Dakota")
#g.update("LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl>")
#g.parse("http://dbpedia.org/page/Mohall,_North_Dakota")
#g.load("http://dbpedia.org/page/Mohall,_North_Dakota")
#g.load("https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl")
#g.store.update("https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl")
#g.store.update("LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl>")
g.store.query("LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl>")
#g.parse("https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl")
#g.store.commit()#"https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl")
#g.store.query("LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl>")#"https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl")
#g.open("http://dbpedia.org/page/Mohall,_North_Dakota")
#g.query("LOAD <http://dbpedia.org/page/Mohall,_North_Dakota>")
#ql2="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl>  "
#g.load("https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl")


gq = rdflib.ConjunctiveGraph('SPARQLStore')
gq.open("http://200.144.255.210:8082/dsfoo")
res2=[i for i in gq.query("SELECT ?s WHERE { ?s ?p ?o . } LIMIT 5")]
#g.update("LOAD <http://dbpedia.org/page/Mohall,_North_Dakota>")
