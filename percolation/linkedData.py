import rdflib as r, pygraphviz as gv
COUNT=0
obs = r.Namespace("http://purl.org/socialparticipation/obs/")
rdf = r.namespace.RDF
rdfs = r.namespace.RDFS
owl = r.namespace.OWL
xsd = r.namespace.XSD
def G(g,S,P,O):
    g.add((S,P,O))
LL=r.Literal
def makeBasicGraph(extra_namespaces=[]):
    """each namespace a tuple (tag,URI)"""
    g,A=r.Graph(),gv.AGraph(directed=True,strict=False)
    A.graph_attr["label"]="Ontologia da tese"
    #g.namespace_manager.bind("ot", "http://purl.org/socialparticipation/ot/")    
    g.namespace_manager.bind("rdf", r.namespace.RDF)    
    g.namespace_manager.bind("rdfs", r.namespace.RDFS)    
    g.namespace_manager.bind("xsd", r.namespace.XSD)    
    g.namespace_manager.bind("owl", r.namespace.OWL)    
    for tag, namespace in zip(*extra_namespaces):
        g.namespace_manager.bind(tag, namespace)    

    return g,A
def startGraphs(ids=("mid1","mid2"),titles=("Ontology1","ConceptX"),extra_namespaces=[]):
    ags={}
    for iid,title in zip(ids,titles):
         ags[iid]=makeBasicGraph(extra_namespaces)
         ags[iid][1].graph_attr["label"]=title
    return ags
def C(ag=[makeBasicGraph()],uri="foo",label="bar",superclass=None,comment=None,comment_pt=None,color=None,label_en=None):
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
            if type(comment) in (type([1,2]),type((1,2))):
                for co in comment:
                    G(g,uri,rdfs.comment,LL(co,lang="en"))
            else:
                G(g,uri,rdfs.comment,LL(comment,lang="en"))
        if comment_pt:
            if type(comment_pt) in (type([1,2]),type((1,2))):
                for co in comment_pt:
                    G(g,uri,rdfs.comment,LL(co,lang="pt"))
            else:
                G(g,uri,rdfs.comment,LL(comment_pt,lang="pt"))
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


