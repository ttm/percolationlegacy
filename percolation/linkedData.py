import rdflib as r, pygraphviz as gv
obs = r.Namespace("http://purl.org/socialparticipation/obs/")
rdf = r.namespace.RDF
rdfs = r.namespace.RDFS
owl = r.namespace.OWL
xsd = r.namespace.XSD
def G(g,S,P,O):
    g.add((S,P,O))
L=r.Literal
def makeBasicGraph():
    g,A=r.Graph(),gv.AGraph(directed=True,strict=False)
    A.graph_attr["label"]="Ontologia da tese"
    g.namespace_manager.bind("ot", "http://purl.org/socialparticipation/ot/")    
    g.namespace_manager.bind("rdf", r.namespace.RDF)    
    g.namespace_manager.bind("rdfs", r.namespace.RDFS)    
    g.namespace_manager.bind("xsd", r.namespace.XSD)    
    g.namespace_manager.bind("owl", r.namespace.OWL)    



def C(ag=[ags["geral"]],uri="foo",label="bar",superclass=None,comment=None,color=None):
    for gg in ag:
        g,A=gg
        G(g,uri,rdf.type,owl.Class)
        G(g,uri,rdfs.label,L(label,lang="pt"))
        A.add_node(label,style="filled")
        nd=A.get_node(label)
        if superclass:
            if type(superclass) in (type([1,2]),type((1,2))):
                for sp in superclass:
                    G(g,uri,rdfs.subClassOf,sp)
                    lsuperclass=[i for i in g.objects(sp,rdfs.label)][0]
                    A.add_edge(  label, lsuperclass)
                    e=A.get_edge(label, lsuperclass)
                    e.attr["arrowhead"]="empty"
                    e.attr["arrowsize"]=2
            else:
                G(g,uri,rdfs.subClassOf,superclass)
                lsuperclass=[i for i in g.objects(superclass,rdfs.label)][0]
                A.add_edge(  label, lsuperclass)
                e=A.get_edge(label, lsuperclass)
                e.attr["arrowhead"]="empty"
                e.attr["arrowsize"]=2
        if comment:
            G(g,uri,rdfs.comment,L(comment,lang="pt"))
        if color:
            nd.attr['color']=color


