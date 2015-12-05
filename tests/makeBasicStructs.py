import percolation as P
import rdflib as r, networkx as x
c=P.utils.check

#rdf_file="/home/r/repos/social/tests/publishing/fb/AntonioAnzoategui18022013/rdf/AntonioAnzoategui18022013Translate.ttl"
#rdf_file_="/home/r/repos/social/tests/publishing/fb/AntonioAnzoategui18022013/rdf/AntonioAnzoategui18022013Translate.owl"
#rdf_file= "/home/r/repos/social/tests/publishing/fb/AntonioAnzoategui18022013/irc/.ttl"
#rdf_file_="/home/r/repos/social/tests/publishing/fb/AntonioAnzoategui18022013/irc/.owl"
#rdf_file=  "/home/r/repos/social/tests/publishing/irc/wikimedia-dev/rdf/wikimedia-devTranslate.ttl"
#rdf_file_= "/home/r/repos/social/tests/publishing/irc/wikimedia-dev/rdf/wikimedia-devTranslate.owl"
rdf_file=  "/home/r/repos/social/tests/publishing/irc/labMacambiraLaleniaLog2/rdf/labMacambiraLaleniaLog2Translate.ttl"
rdf_file_=  "/home/r/repos/social/tests/publishing/irc/labMacambiraLaleniaLog2/rdf/labMacambiraLaleniaLog2Translate.owl"

##ruri=P.rdf.ns.fb.friend
#ruri=P.rdf.ns.irc.directMessage
#ruri1_="irc:author"
#ruri2_="irc:directedTo"
##luri=P.rdf.ns.fb.name
#luri="irc:nick"
## id_uri nao existe, pode pegar do id .split("#")[-1]
#c("aler")
#g=r.Graph()
#g.load(rdf_file_)
#c("lido")
#q1=r"SELECT ?i1 ?l1 ?i2 ?l2 WHERE {{ ?m {} ?i1 . ?i1 {} ?l1 . ?m {} ?i2 . ?i2 {} ?l2 . }}".format(ruri1_,luri,ruri2_,luri )
#res=[i for i in g.query(q1)]
#c("queriado")
#
#dg=x.DiGraph()
#for rel in res:
#    id1,l1,id2,l2=rel
#    if dg.has_node(id1): dg.node[id1]["weight"]+=1.
#    else:       dg.add_node(id1,label=l1,weight=1.)
#
#    if dg.has_node(id2): dg.node[id2]["weight"]+=1.
#    else:       dg.add_node(id2,label=l2,weight=1.)
#
#    if dg.has_edge(id1,id2): dg[id1][id2]["weight"]+=1.
#    else:       dg.add_edge(id1,id2,weight=2.)
#c("feito grafo")
## resolver os alias arbitrarios

#rdf_file=  "/home/r/repos/social/tests/publishing/tw/god_tw/rdf/god_twTranslate00002.ttl"
#rdf_file0_=  "/home/r/repos/social/tests/publishing/tw/god_tw/rdf/god_twTranslate00000.owl"
#rdf_file_=  "/home/r/repos/social/tests/publishing/tw/god_tw/rdf/god_twTranslate00001.owl"
#rdf_file2_=  "/home/r/repos/social/tests/publishing/tw/god_tw/rdf/god_twTranslate00002.owl"
##q1=r"""SELECT ?i1 ?l1 ?i2 ?l2 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1 .  ?i1 tw:name ?l1 .  ?m2 tw:author ?i2 .  ?i2 tw:name ?l2 . }}"""
##q1=r"""SELECT ?i1 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1  }}"""
##q1=r"""SELECT ?i1 ?l1 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1 .  ?i1 tw:name ?l1  }}"""
#q1=r"""SELECT ?i1 ?l1 ?i2 ?l2 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1 .  ?i1 tw:name ?l1 .  ?m2 tw:author ?i2 .  ?i2 tw:name ?l2 . }}"""
#g=r.Graph()
#g.load(rdf_file0_)
#c("lido")
#g.load(rdf_file_)
#c("lido")
#g.load(rdf_file2_)
#c("lido")
#res=[i for i in g.query(q1)]
#c("queriado")
#dg=x.DiGraph()
#for rel in res:
#    id1,l1,id2,l2=rel
#    if dg.has_node(id1): dg.node[id1]["weight"]+=1.
#    else:       dg.add_node(id1,label=l1,weight=1.)
#
#    if dg.has_node(id2): dg.node[id2]["weight"]+=1.
#    else:       dg.add_node(id2,label=l2,weight=1.)
#
#    if dg.has_edge(id1,id2): dg[id1][id2]["weight"]+=1.
#    else:       dg.add_edge(id1,id2,weight=2.)
#c("feito grafo")


#P.basicStructures.makeNetwork(rdf_file_,ruri,luri,None)


#rdf_file=  "/home/r/repos/opa/participaTriplestore.ttl"
#rdf_file_=  "/home/r/repos/opa/participaTriplestore.rdf"
##q1=r"""SELECT ?i1 ?l1 ?i2 ?l2 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1 .  ?i1 tw:name ?l1 .  ?m2 tw:author ?i2 .  ?i2 tw:name ?l2 . }}"""
##q1=r"""SELECT ?i1 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1  }}"""
##q1=r"""SELECT ?i1 ?l1 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1 .  ?i1 tw:name ?l1  }}"""
#g=r.Graph()
#g.load(rdf_file_)
#c("lido")
#q1=r"""SELECT ?i1 ?l1 ?i2 ?l2 WHERE  {{ ?i1 opa:knows ?i2 .  ?i1 opa:name ?l1 .  ?i2 opa:name ?l2 . }}"""
#res=[i for i in g.query(q1)]
#c("queriado")
#dg=x.Graph()
#for rel in res:
#    id1,l1,id2,l2=rel
#    if dg.has_node(id1): dg.node[id1]["weight"]+=1.
#    else:       dg.add_node(id1,label=l1,weight=1.)
#
#    if dg.has_node(id2): dg.node[id2]["weight"]+=1.
#    else:       dg.add_node(id2,label=l2,weight=1.)
#
#    if dg.has_edge(id1,id2): dg[id1][id2]["weight"]+=1.
#    else:       dg.add_edge(id1,id2,weight=2.)
#c("feito grafo")
#gg=dg.copy()
#q2="""SELECT DISTINCT ?i1 ?l2 ?i2 ?l2
#       WHERE {
#           ?artigo opa:hasReply ?comentario .
#           ?artigo opa:publisher ?i1 .
#           ?i1 opa:name ?l1 .
#           ?comentario opa:creator ?i2 .
#           ?i2 opa:name ?l2 .
#       }"""
#res=[i for i in g.query(q2)]
#c("queriado")
#dg=x.DiGraph()
#for rel in res:
#    id1,l1,id2,l2=rel
#    if dg.has_node(id1): dg.node[id1]["weight"]+=1.
#    else:       dg.add_node(id1,label=l1,weight=1.)
#
#    if dg.has_node(id2): dg.node[id2]["weight"]+=1.
#    else:       dg.add_node(id2,label=l2,weight=1.)
#
#    if dg.has_edge(id1,id2): dg[id1][id2]["weight"]+=1.
#    else:       dg.add_edge(id1,id2,weight=2.)
#c("feito grafo")


#rdf_file=  "/home/r/repos/ocd2/cdTriplestore.ttl"
#rdf_file_=  "/home/r/repos/ocd2/cdTriplestore.rdf"
###q1=r"""SELECT ?i1 ?l1 ?i2 ?l2 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1 .  ?i1 tw:name ?l1 .  ?m2 tw:author ?i2 .  ?i2 tw:name ?l2 . }}"""
###q1=r"""SELECT ?i1 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1  }}"""
###q1=r"""SELECT ?i1 ?l1 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1 .  ?i1 tw:name ?l1  }}"""
#q1=r"""SELECT ?i1 ?i2 WHERE  {{ ?m1 a ocd:Post . ?m2 ocd:topic ?m1 .  ?m1 ocd:author ?i1 .  ?m2 ocd:author ?i2 . }}"""
#c("aler")
#g=r.Graph()
#g.load(rdf_file_)
#c("lido")
#res=[i for i in g.query(q1)]
#c("queriado")
#dg=x.DiGraph()
#for rel in res:
#    id1,id2=rel
#    if dg.has_node(id1): dg.node[id1]["weight"]+=1.
#    else:       dg.add_node(id1,weight=1.)
#
#    if dg.has_node(id2): dg.node[id2]["weight"]+=1.
#    else:       dg.add_node(id2,weight=1.)
#
#    if dg.has_edge(id1,id2): dg[id1][id2]["weight"]+=1.
#    else:       dg.add_edge(id1,id2,weight=1.)
#c("feito grafo")


rdf_file=  "/home/r/repos/aa01/rdf/aaTriplestore.ttl"
rdf_file_=  "/home/r/repos/aa01/rdf/aaTriplestore.rdf"
##q1=r"""SELECT ?i1 ?l1 ?i2 ?l2 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1 .  ?i1 tw:name ?l1 .  ?m2 tw:author ?i2 .  ?i2 tw:name ?l2 . }}"""
##q1=r"""SELECT ?i1 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1  }}"""
##q1=r"""SELECT ?i1 ?l1 WHERE  {{ ?m1 tw:retweetOf ?m2 . ?m1 tw:author ?i1 .  ?i1 tw:name ?l1  }}"""
q1=r"""SELECT ?i1 ?l1 WHERE  {{ ?m1 a aa:Shout . ?m1 aa:user ?i1 .  ?i1 aa:nick ?l1 . }}"""
c("aler")
g=r.Graph()
g.load(rdf_file_)
c("lido")
res=[i for i in g.query(q1)]
c("queriado")
# faz contagem de atividade
# assume correlação com grau/força e admite erro (q não existe, pois não existe uma rede propriamente)
from collections import Counter
pg=Counter(res)
c("feito pseudo-grafo")

# faz rede de revisao das sessoes
q1=r"""SELECT ?i1 ?l1 ?i2 ?l2 WHERE  {{ ?m a aa:Session . ?m aa:user ?i1 .  ?m aa:checker ?i2 . ?i1 aa:nick ?l1 . ?i2 aa:nick ?l2 . }}"""
c("lido")
res=[i for i in g.query(q1)]
dg=x.DiGraph()
for rel in res:
    id1,l1,id2,l2=rel
    if dg.has_node(id1): dg.node[id1]["weight"]+=1.
    else:       dg.add_node(id1,label=l1,weight=1.)

    if dg.has_node(id2): dg.node[id2]["weight"]+=1.
    else:       dg.add_node(id2,label=l2,weight=1.)

    if dg.has_edge(id1,id2): dg[id1][id2]["weight"]+=1.
    else:       dg.add_edge(id1,id2,weight=2.)
c("feito grafo")


# makenetwork estah pronto para fb
# todos os outros precisam fazer

