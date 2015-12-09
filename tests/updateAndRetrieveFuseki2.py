import percolation as P
import  importlib
importlib.reload(P.utils)

mq=P.utils.mQuery
u= "http://200.144.255.210:8082/dsfoo/query"
u2="http://200.144.255.210:8082/dsfoo/update"
u3="http://200.144.255.210:8082/dsfoo"
u4="http://200.144.255.210:8082/dsfoo/upload"
u5="http://200.144.255.210:8082/dsfoo/data"
u6="http://200.144.255.210:8082/dsfoo/sparql"
q="SELECT DISTINCT ?{} WHERE {{ GRAPH ?g {{ }} }}"
v="g"
#r=mq(u3,q,v)
##r2=mq(u2,"CREATE GRAPH <http://graphTa.foo>")
##r3=mq(u,q)
#
#
#qt="""SELECT (COUNT(?s) as ?{}) WHERE {{ ?s <http://purl.org/socialparticipation/irc/sentAt> ?o }} """
#v="cs",
#rt_=mq(u3,qt,v)
#qt="""SELECT (COUNT(?s) as ?{}) WHERE {{ GRAPH <http://banana.com> {{ ?s <http://purl.org/socialparticipation/tw/sentAt> ?o }} }} """
#rt=mq(u3,qt,v)
#
##ql="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/music_tw/master/rdf/music_twTranslate00000.owl> INTO GRAPH <http://graphTa.foo>  "
##rl=mq(u2,ql)
#
#
##r2=mq(u2,"CREATE GRAPH <http://graphTa2.foo>")
##r3=mq(u,q)
#
#r2=mq(u2,"CREATE GRAPH <http://pitchuca.nenem>")
##r2=mq(u2,"DROP GRAPH <http://pitchuca.nenem>")
#v="g"
#r3=mq(u3,q,v)

ql2="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/music_tw/master/rdf/music_twTranslate00000.owl> INTO GRAPH <http://pitchuca.nenem>  "
ql2="LOAD <file:/home/r/repos/social/tests/publishing/tw/music_tw/rdf/music_twTranslate00015.owl> INTO GRAPH <http://pitchuca.nenem>  "
ql2="LOAD <file:/home/r/repos/social/tests/publishing/tw/music_tw/rdf/music_twTranslate00015.owl>  "
ql2="LOAD <http://raimond.me.uk/void/jamendo_example.n3> "
ql2="LOAD <http://dbpedia.org/page/Mohall,_North_Dakota> "
ql2="LOAD <http://vocab.org/relationship/> "
ql2="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/music_tw/master/rdf/music_twTranslate00015.owl> "
q4="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/bundle_tw/master/python_tw/rdf/python_twTranslate00000.owl> INTO GRAPH <http://AuAuAu.foo> . "
ql2="LOAD <http://dbpedia.org/page/Mohall,_North_Dakota> INTO GRAPH <http://AuAuAu.foo> . "
#ql2="LOAD <file:/home/r/repos/social/tests/publishing/tw/music_tw/rdf/music_twTranslate00015.owl> INTO GRAPH <http://pitchuca.nenem> \n "
ql2="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/music_tw/master/rdf/music_twTranslate00015.owl> "
ql2="LOAD <https://raw.githubusercontent.com/OpenLinkedSocialData/labMacambiraLaleniaLog2/master/rdf/labMacambiraLaleniaLog2Translate.owl> INTO GRAPH <http://pitchuca.nenem> "

r4=mq(u2,ql2)
#rl2=mq(u3,q4)



#qq="""PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#INSERT DATA
#{
#      GRAPH <http://AuAuAu.foo> { <https://raw.githubusercontent.com/OpenLinkedSocialData/bundle_tw/master/python_tw/rdf/python_twTranslate00000.owl> foaf:name "dev" . }
#      }"""
#rl2=mq(u2,qq)
#
#v="cs",
#qt="""SELECT (COUNT(?s) as ?{}) WHERE {{ GRAPH <http://AuAuAu.foo> {{ ?s <http://purl.org/socialparticipation/tw/sentAt> ?o }} }} """
#rt=mq(u,qt,v)


