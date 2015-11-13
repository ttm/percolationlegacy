import rdflib as r, percolation as P, pygraphviz as gv, os, datetime
check=P.utils.check
from rdflib.plugins.sparql import prepareQuery

#bb=g.query(query,initBindings={"fid":ind})
#label=[i for i in bb][0][0].value

COUNT=0
class ns:
    obs = r.Namespace("http://purl.org/socialparticipation/obs/") # ontology of the social library
    aa  = r.Namespace("http://purl.org/socialparticipation/aa/")  # algorithmic autoregulation
    vbs = r.Namespace("http://purl.org/socialparticipation/vbs/") # vocabulary of the social library
    opa = r.Namespace("http://purl.org/socialparticipation/opa/") # participabr
    ops = r.Namespace("http://purl.org/socialparticipation/ops/") # social participation ontology
    ocd = r.Namespace("http://purl.org/socialparticipation/ocd/") # cidade democrática
    ore = r.Namespace("http://purl.org/socialparticipation/ore/") # ontology of the reseach, for registering ongoing works, a RDF AA
    ot  = r.Namespace("http://purl.org/socialparticipation/ot/")  # ontology of the thesis, for academic conceptualizations
    po=per = r.Namespace("http://purl.org/socialparticipation/po/") # percolation, this framework itself
    fb  = r.Namespace("http://purl.org/socialparticipation/fb/")  # facebook
    tw  = r.Namespace("http://purl.org/socialparticipation/tw/")  # twitter
    irc = r.Namespace("http://purl.org/socialparticipation/irc/") # irc
    ld  = r.Namespace("http://purl.org/socialparticipation/ld/")  # linkedin 
    rdf = r.namespace.RDF
    rdfs = r.namespace.RDFS
    owl = r.namespace.OWL
    xsd = r.namespace.XSD
query_=prepareQuery(
        "SELECT ?name WHERE {?fid fb:name ?name}"
        ,initNs={"fb":ns.fb})
def G(g,S,P,O):
    g.add((S,P,O))
LL=r.Literal
def writeAll(per_graph,sname="img_and_rdf",sdir="./",full=False,remove=False):
    nome_=sname
    g,A=per_graph
    if not os.path.isdir(sdir):
        os.mkdir(sdir)
    for i in ("figs","dot","rdf"):
        if os.path.isdir(sdir+i) and remove:
            for afile in os.listdir(sdir+i):
                os.remove(sdir+i+"/"+afile)
            os.rmdir(sdir+i)
        if not os.path.isdir(sdir+i):
            os.mkdir(sdir+i)
    if full=="True":
        nome=(sdir+"figs/%s.png"%(nome_,))
        A.draw(nome,prog="dot")
        nome=(sdir+"figs/%s_2.png"%(nome_,))
        A.draw(nome,prog="circo")
        nome=(sdir+"figs/%s_3.png"%(nome_,))
        A.draw(nome,prog="fdp")
        A.write("dot/%s.dot"%(nome_,))
    if full=="neato":
        print("on the draw")
        A.graph_attr["splines"]=True
        A.graph_attr["overlap"]=False
        A.graph_attr["size"]="39.5,32"
        nome=(sdir+"figs/%sN.png"%(nome_,))
        A.draw(nome,prog="neato")
    if full=="circo":
        print("on the circo draw")
#        A.graph_attr["splines"]=True
#        A.graph_attr["overlap"]=False
#        A.graph_attr["size"]="39.5,32"
        nome=(sdir+"figs/%sC.png"%(nome_,))
        A.draw(nome,prog="circo")
    elif full:
        nome=(sdir+"figs/%s.png"%(nome_,))
        A.draw(nome,prog="dot")
    check("drawed")
    A.write(sdir+"dot/%s.dot"%(nome_,))

    f=open(sdir+"rdf/%s.owl"%(nome_,),"wb")
    f.write(g.serialize())
    f.close()
    f=open(sdir+"rdf/%s.ttl"%(nome_,),"wb")
    f.write(g.serialize(format="turtle"))
    f.close()
    check("written")


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
def IC_(ga=None,uri="turiref",string="astringid",label="alabel"):
    ind=uri+"#"+str(string)
    if label and ga:
        for g,A in ga:
            G(g,ind,ns.rdf.type,uri)
            G(g,ind,ns.rdfs.label,LL(label))
            A.add_node(label,style="filled")
            nd=A.get_node(label)
            nd.attr['color']="#02F3DD"
    return ind


def IC(ga=None,uri="turiref",string="astringid",label="alabel"):
    ind=uri+"#"+str(string)
    if label and ga:
        for g,A in ga:
            G(g,ind,ns.rdf.type,uri)
            G(g,ind,ns.rdfs.label,LL(label))
            A.add_node(label,style="filled")
            nd=A.get_node(label)
            nd.attr['color']="#02F3DD"
    return ind

#def I(ga=[makeBasicGraph()],uri="turiref",string="astringid",label="alabel"):
#    global COUNT
#    ind=uri+"#"+str(string)
#    if label:
#        for g,A in ga:
#            G(g,ind,ns.rdf.type,uri)
#            A.add_node(COUNT,style="filled")
#            nd=A.get_node(COUNT)
#            nd.attr['color']="#A2F3D1"
#            nd.attr['label']=label
#    return ind

def link_(ga=[makeBasicGraph()],ind="uriref",label="alabel",props=["uri1","uri2"],objs=["uri1","uri2"]):
    """Link an instance with the object classes through the props"""
    query=prepareQuery(
            "SELECT ?name WHERE {?fid fb:name ?name}",
            initNs={"fb":ns.fb})
    for prop, obj in zip(props,objs):
        for g,A in ga:
            G(g,ind,prop,obj)
            bb=g.query(query,initBindings={"fid":obj})
            oname=[i for i in bb][0][0].value
            A.add_edge(label,oname)
            e=A.get_edge(label,oname)
            e.attr["label"]=prop.split("/")[-1]

def link(ga=[makeBasicGraph()],ind="uriref",label="alabel",props=["uri1","uri2"],vals=["val1","val2"]):
    """Link an instance with the vals through the props"""
    global COUNT
    # acha o name do uriref buscando no grafo
    for prop, val in zip(props,vals):
        for g,A in ga:
            if type(val)==type(datetime.datetime.now()):
                G(g,ind,prop,LL(val,datatype=ns.xsd.datetime))
            else:
                G(g,ind,prop,LL(val,datatype=ns.xsd.string))
            A.add_node(COUNT,style="filled")
            nd=A.get_node(COUNT)
            nd.attr["label"]=val
            nd.attr['color']="#02F3F1"
            A.add_edge(  label,COUNT)
            e=A.get_edge(label,COUNT); COUNT+=1
            e.attr["label"]=prop.split("/")[-1]


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
def L_(ga,sub,pred,obj):
    for g,A in ga:
        G(g,sub,pred,obj)
        # draw
        # get names
        # make edge
        bb=g.query(query_,initBindings={"fid":sub})
        sname=[i for i in bb][0][0].value
        bb=g.query(query_,initBindings={"fid":obj})
        oname=[i for i in bb][0][0].value
        A.add_edge(sname,oname)
        e=A.get_edge(sname,oname)
        e.attr["label"]=pred.split("/")[-1]

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

