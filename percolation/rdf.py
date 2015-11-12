import rdflib as r, pygraphviz as gv, os
COUNT=0
class ns:
    obs = r.Namespace("http://purl.org/socialparticipation/obs/")
    aa = r.Namespace("http://purl.org/socialparticipation/aa/")
    vbs = r.Namespace("http://purl.org/socialparticipation/vbs/")
    opa = r.Namespace("http://purl.org/socialparticipation/opa/")
    ops = r.Namespace("http://purl.org/socialparticipation/ops/")
    ocd = r.Namespace("http://purl.org/socialparticipation/ocd/")
    ore = r.Namespace("http://purl.org/socialparticipation/ore/")
    ot = r.Namespace("http://purl.org/socialparticipation/ot/")
    per = r.Namespace("http://purl.org/socialparticipation/per/")
    rdf = r.namespace.RDF
    rdfs = r.namespace.RDFS
    owl = r.namespace.OWL
    xsd = r.namespace.XSD
def G(g,S,P,O):
    g.add((S,P,O))
LL=r.Literal
def writeAll(per_graph,sname="img_and_rdf",sdir="./"):
    nome_=sname
    g,A=per_graph
    for i in ("figs","dot","rdf"):
        if os.path.isdir(sdir+i):
            for afile in os.listdir(sdir+i):
                os.remove(sdir+i+"/"+afile)
            os.rmdir(sdir+i)
        os.mkdir(sdir+i)
    def mkName(tdir,tname,ttype): return "{}{}{}"
    nome=("figs/%s.png"%(nome_,))
    A.draw(nome,prog="dot")
    nome=("figs/%s_2.png"%(nome_,))
    A.draw(nome,prog="circo")
    nome=("figs/%s_3.png"%(nome_,))
    A.draw(nome,prog="fdp")

    A.write("dot/%s.dot"%(nome_,))

    f=open("rdf/%s.owl"%(nome_,),"wb")
    f.write(g.serialize())
    f.close()
    f=open("rdf/%s.ttl"%(nome_,),"wb")
    f.write(g.serialize(format="turtle"))
    f.close()


def makeBasicGraph(extra_namespaces=[],glabel="Ontologia da tese"):
    """each namespace a tuple (tag,URI)"""
    g,A=r.Graph(),gv.AGraph(directed=True,strict=False)
    A.graph_attr["label"]=glabel
    g.namespace_manager.bind("rdf", ns.rdf)    
    g.namespace_manager.bind("rdfs",ns.rdfs)    
    g.namespace_manager.bind("xsd", ns.xsd)    
    g.namespace_manager.bind("owl", ns.owl)    
    for tag, namespace in zip(*extra_namespaces):
        g.namespace_manager.bind(tag, namespace)
    return g,A
def startGraphs(ids=("mid1","mid2"),titles=("Ontology1","ConceptX"),extra_namespaces=[]):
    ags={}
    for iid,title in zip(ids,titles):
         ags[iid]=makeBasicGraph(extra_namespaces)
         ags[iid][1].graph_attr["label"]=title
    return ags
def C(ag=[makeBasicGraph()],uri="foo",label="bar",superclass=None,comment=None,label_pt=None,comment_pt=None,color=None):
    for gg in ag:
        g,A=gg
        G(g,uri,ns.rdf.type,ns.owl.Class)
        G(g,uri,ns.rdfs.label,LL(label,lang="en"))
        if label_pt:
            G(g,uri,ns.rdfs.label,LL(label_pt,lang="pt"))
        A.add_node(label,style="filled")
        nd=A.get_node(label)
        if superclass:
            if type(superclass) in (type([1,2]),type((1,2))):
                for sp in superclass:
                    G(g,uri,ns.rdfs.subClassOf,sp)
                    print([i for i in g.objects(sp,ns.rdfs.label)])
                    lsuperclass=[i for i in g.objects(sp,ns.rdfs.label) if i.language=="en"][0].title()
                    A.add_edge(  label, lsuperclass)
                    e=A.get_edge(label, lsuperclass)
                    e.attr["arrowhead"]="empty"
                    e.attr["arrowsize"]=2
            else:
                G(g,uri,ns.rdfs.subClassOf,superclass)
                #lsuperclass=[i for i in g.objects(superclass,rdfs.label)][-1]
                lsuperclass=[i for i in g.objects(superclass,ns.rdfs.label) if i.language=="en"][0]
                print(lsuperclass)
                A.add_edge(  label, lsuperclass)
                e=A.get_edge(label, lsuperclass)
                e.attr["arrowhead"]="empty"
                e.attr["arrowsize"]=2
        if comment:
            if type(comment) in (type([1,2]),type((1,2))):
                for co in comment:
                    G(g,uri,ns.rdfs.comment,LL(co,lang="en"))
            else:
                G(g,uri,ns.rdfs.comment,LL(comment,lang="en"))
        if comment_pt:
            if type(comment_pt) in (type([1,2]),type((1,2))):
                for co in comment_pt:
                    G(g,uri,ns.rdfs.comment,LL(co,lang="pt"))
            else:
                G(g,uri,ns.rdfs.comment,LL(comment_pt,lang="pt"))
        if color:
            nd.attr['color']=color

def P(ag=[makeBasicGraph()],uri="foo",label="bar",label_pt=None,comment=None):
    """Add object property to RDF graph"""
    for gg in ag:
        g=gg[0]
        G(g,uri,ns.rdf.type,ns.owl.ObjectProperty)
        G(g,uri,ns.rdfs.label,LL(label,lang="en"))
        if label_pt:
            G(g,uri,ns.rdfs.label,LL(label_pt,lang="pt"))
        if comment:
            G(g,uri,ns.rdfs.comment,LL(comment,lang="en"))

def D(ag=[makeBasicGraph()],uri="foo",label="bar",dtype=ns.xsd.string,comment=None,label_pt=None):
    """Add data property to RDF graph"""
    for gg in ag:
        g=gg[0]
        G(g,uri,ns.rdf.type,ns.owl.DatatypeProperty)
        G(g,uri,ns.rdfs.label,LL(label,lang="pt"))
        G(g,uri,ns.rdfs.range,dtype)
        if comment:
            G(g,uri,ns.rdfs.comment,LL(comment,lang="en"))
        if label_pt:
            G(g,uri,ns.rdfs.label,LL(label_pt,lang="pt"))
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

def namespaces(ids=[]):
    """Declare namespace URIs in RDF graph and return a dictionary of them.
    
    input: list of ids. Use tuple for (idstring, URIString) of
    benefint from RDFLib and particpatory IDs 
    throughtput: declare RDF in graph g
    output: dictionary of {key=id, value=URI} as declared
    
    Deals automaticaly with namespaces from RDFlib and selected
    participatory libs"""
    idict={}
    for tid in ids:
        # findig URIRef 
        if type(tid)!=type("fooString"): # tuple (tid,iuri)
            idict[tid[0]]=r.Namespace(tid[1])
        elif tid in [fooString.lower() for fooString in dir(r.namespace)]: # rdflib shortcut
            if tid in dir(r.namespace):
                idict[tid]=eval("r.namespace."+tid)
            else:
                idict[tid]=eval("r.namespace."+tid.upper())
        else: # participatory shortcut
            idict[tid]=r.Namespace("http://purl.org/socialparticipation/{}/".format(tid))
        # adding to RDF Graph
        if type(tid)!=type("fooString"): # tuple (tid,iuri)
            g.namespace_manager.bind(tid[0], idict[tid[0]])    
        else:
            g.namespace_manager.bind(tid, idict[tid])    
    return idict
def ID_GEN(namespace,tid):
    ind=namespace+"#"+tid
    G(ind,ns["rdf"].type,namespace)
    return ind

