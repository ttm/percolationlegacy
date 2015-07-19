import rdflib as r, pygraphviz as gv
obs = r.Namespace("http://purl.org/socialparticipation/obs/")
rdf = r.namespace.RDF
rdfs = r.namespace.RDFS
owl = r.namespace.OWL
xsd = r.namespace.XSD
def G(g,S,P,O):
    g.add((S,P,O))
LL=r.Literal
def makeBasicGraph():
    g,A=r.Graph(),gv.AGraph(directed=True,strict=False)
    A.graph_attr["label"]="Ontologia da tese"
    g.namespace_manager.bind("ot", "http://purl.org/socialparticipation/ot/")    
    g.namespace_manager.bind("rdf", r.namespace.RDF)    
    g.namespace_manager.bind("rdfs", r.namespace.RDFS)    
    g.namespace_manager.bind("xsd", r.namespace.XSD)    
    g.namespace_manager.bind("owl", r.namespace.OWL)    
    return g,A
def C(ag=[makeBasicGraph()],uri="foo",label="bar",superclass=None,comment=None,color=None,label_en=None):
    for gg in ag:
        g,A=gg
        G(g,uri,rdf.type,owl.Class)
        G(g,uri,rdfs.label,LL(label,lang="pt"))
        if label_en:
            G(g,uri,rdfs.label,LL(label_en,lang="en"))
        A.add_node(label,style="filled")
        nd=A.get_node(label)
        if superclass:
            if type(superclass) in (type([1,2]),type((1,2))):
                for sp in superclass:
                    G(g,uri,rdfs.subClassOf,sp)
                    print([i for i in g.objects(sp,rdfs.label)])
                    lsuperclass=[i for i in g.objects(sp,rdfs.label) if i.language=="pt"][0].title()
                    A.add_edge(  label, lsuperclass)
                    e=A.get_edge(label, lsuperclass)
                    e.attr["arrowhead"]="empty"
                    e.attr["arrowsize"]=2
            else:
                G(g,uri,rdfs.subClassOf,superclass)
                #lsuperclass=[i for i in g.objects(superclass,rdfs.label)][-1]
                lsuperclass=[i for i in g.objects(superclass,rdfs.label) if i.language=="pt"][0]
                print(lsuperclass)
                A.add_edge(  label, lsuperclass)
                e=A.get_edge(label, lsuperclass)
                e.attr["arrowhead"]="empty"
                e.attr["arrowsize"]=2
        if comment:
            G(g,uri,rdfs.comment,LL(comment,lang="pt"))
        if color:
            nd.attr['color']=color

def P(ag=[makeBasicGraph()],uri="foo",label="bar",label_en=None):
    """Add object property to RDF graph"""
    for gg in ag:
        g=gg[0]
        G(g,uri,rdf.type,owl.ObjectProperty)
        G(g,uri,rdfs.label,LL(label,lang="pt"))
        if label_en:
            G(g,uri,rdfs.label,LL(label_en,lang="en"))

def D(ag=[makeBasicGraph()],uri="foo",label="bar",dtype="baz"):
    """Add data property to RDF graph"""
    for gg in ag:
        g=gg[0]
        G(g,uri,rdf.type,owl.DatatypeProperty)
        G(g,uri,rdfs.label,LL(label,lang="pt"))
        G(g,uri,rdfs.range,dtype)
def L(ag=[makeBasicGraph()],olabel="foo",llabel="bar",dlabel="baz"):
    """Add object property link with labels for origin, link, destination"""
    for gg in ag:
        A=gg[1]
        A.add_edge(  olabel,dlabel)
        e=A.get_edge(olabel,dlabel)
        e.attr["label"]=llabel
def LD(ag=[makeBasicGraph()],olabel="foo",llabel="bar",dlabel="baz"):
    """Add data property link with labels for origin, link, destination"""
    global COUNT
    for gg in ag:
        A=gg[1]
        A.add_node(COUNT,style="filled")
        nd=A.get_node(COUNT)
        nd.attr["label"]=dlabel
        nd.attr['color']="#A2F3D1"
        A.add_edge(  olabel,COUNT)
        e=A.get_edge(olabel,COUNT); COUNT+=1
        e.attr["label"]=llabel


