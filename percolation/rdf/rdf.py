import rdflib as r, percolation as P, pygraphviz as gv, os, datetime
check=P.utils.check
utf8=P.utils.utf8
from rdflib.plugins.sparql import prepareQuery

#bb=g.query(query,initBindings={"fid":ind})
#label=[i for i in bb][0][0].value

"""
para as URIs:
reserved    = gen-delims / sub-delims

gen-delims  = ":" / "/" / "?" / "#" / "[" / "]" / "@"

sub-delims  = "!" / "$" / "&" / "'" / "(" / ")"
            / "*" / "+" / "," / ";" / "="
https://tools.ietf.org/html/rfc3986#section-2

A URI também não é splitada com %
r.namespace.split_uri("http://purl.org/socialparticipation/irc/Participant#labMacambiraLaleniaLog1%2818")
"""
def LL_(literal,lang=None):
    if type(literal)==type(1123):
        ttype=NS.xsd.integer
    elif type(literal)==type(True):
        ttype=NS.xsd.boolean
    elif type(literal)==type(datetime.datetime.now()):
        ttype=NS.xsd.datetime
    elif type(literal)==type(datetime.date(2015,3,4)):
        ttype=NS.xsd.date
    else:
        ttype=NS.xsd.string
        literal=utf8(str(literal))
    if not lang:
        return r.Literal(literal,datatype=ttype)
    else:
        return r.Literal(literal,lang=lang,datatype=ttype)

COUNT=0
class NS:
    cm =     r.Namespace("http://purl.org/socialparticipation/cm/")   # caixa mágica
    obs =    r.Namespace("http://purl.org/socialparticipation/obs/") # ontology of the social library
    aa  =    r.Namespace("http://purl.org/socialparticipation/aa/")  # algorithmic autoregulation
    vbs =    r.Namespace("http://purl.org/socialparticipation/vbs/") # vocabulary of the social library
    opa =    r.Namespace("http://purl.org/socialparticipation/opa/") # participabr
    ops =    r.Namespace("http://purl.org/socialparticipation/ops/") # social participation ontology
    ocd =    r.Namespace("http://purl.org/socialparticipation/ocd/") # cidade democrática
    ore =    r.Namespace("http://purl.org/socialparticipation/ore/") # ontology of the reseach, for registering ongoing works, a RDF AA
    ot  =    r.Namespace("http://purl.org/socialparticipation/ot/")  # ontology of the thesis, for academic conceptualizations
    po=per = r.Namespace("http://purl.org/socialparticipation/po/") # percolation, this framework itself
    fb  =    r.Namespace("http://purl.org/socialparticipation/fb/")  # facebook
    tw  =    r.Namespace("http://purl.org/socialparticipation/tw/")  # twitter
    irc =    r.Namespace("http://purl.org/socialparticipation/irc/") # irc
    gmane =  r.Namespace("http://purl.org/socialparticipation/gmane/") # gmane
    ld  =    r.Namespace("http://purl.org/socialparticipation/ld/")  # linkedin 
    dbp  =    r.Namespace("http://dbpedia.org/resource/")
    rdf =    r.namespace.RDF
    rdfs =   r.namespace.RDFS
    owl =    r.namespace.OWL
    xsd =    r.namespace.XSD
    dc =     r.namespace.DC
    dct =    r.namespace.DCTERMS
    foaf =   r.namespace.FOAF
    doap =   r.namespace.DOAP
    void =   r.namespace.VOID
    U=   r.URIRef
query_=prepareQuery(
        "SELECT ?name WHERE {?fid fb:name ?name}"
        ,initNs={"fb":NS.fb})
a=NS.rdf.type
def makeDummyOntology():
    triples=(
            (NS.po.InteractionSnapshot, a, NS.rdfs.Class),
            (NS.po.GmaneSnapshot, a, NS.rdfs.Class),
            (NS.po.Snapshot, a, NS.rdfs.Class),
            (NS.po.InteractionSnapshot, NS.rdfs.subClassOf, NS.po.Snapshot), # fb, part, tw, irc, gmane, cidade
            (NS.po.GmaneSnapshot, NS.rdfs.subClassOf, NS.po.InteractionSnapshot),
            )
    return triples
def G(g,S,P,O):
    g.add((S,P,O))
def writeTriples(triples,filename,format_="turtle"):
    g=r.Graph()
    for triple in triples:
        if not isinstance(triple[2],r.URIRef):
            triple[2]=r.Literal(triple[2])
        g.add(triple)
    with open(filename,"wb") as f:
        f.write(g.serialize(format=format_))
def writeAll(per_graph,sname="img_and_rdf",sdir="./",full=False,remove=False,dot=False,sizelimit=None):
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
    check("{} was rendered".format(nome_))
    if dot:
        A.write(sdir+"dot/%s.dot"%(nome_,))
        check("dot written")
    if sizelimit:
        i=0
        j=0
        g_=r.Graph()
        for sub, pred, obj in g:
            g_.add((sub,pred,obj))
            i+=1
            if i%sizelimit==0:
                f=open(sdir+"rdf/{}{:05d}.rdf".format(nome_,j),"wb")
                f.write(g_.serialize())
                f.close()
                check("rdf written")
                f=open(sdir+"rdf/{}{:05d}.ttl".format(nome_,j),"wb")
                f.write(g_.serialize(format="turtle"))
                f.close()
                check("ttl written")
                g_=r.Graph()
                j+=1
        f=open(sdir+"rdf/{}{:05d}.rdf".format(nome_,j),"wb")
        f.write(g_.serialize())
        f.close()
        check("rdf written")
        f=open(sdir+"rdf/{}{:05d}.ttl".format(nome_,j),"wb")
        f.write(g_.serialize(format="turtle"))
        f.close()
        check("ttl written")
    else:
        f=open(sdir+"rdf/%s.rdf"%(nome_,),"wb")
        f.write(g.serialize())
        f.close()
        check("rdf written")
        f=open(sdir+"rdf/%s.ttl"%(nome_,),"wb")
        f.write(g.serialize(format="turtle"))
        f.close()
        check("ttl written")


def makeBasicGraph(extra_namespaces=[],graphlabel=None):
    """each namespace a tuple (tag,URI) in extra_namespaces"""
    g,A=r.Graph(),gv.AGraph(directed=True,strict=False)
    g.namespace_manager.bind("rdf", NS.rdf)    
    g.namespace_manager.bind("rdfs",NS.rdfs)    
    g.namespace_manager.bind("xsd", NS.xsd)    
    g.namespace_manager.bind("owl", NS.owl)    
    for tag, namespace in zip(*extra_namespaces):
        g.namespace_manager.bind(tag, namespace)
    if graphlabel:
        gv.AGraph(directed=True,strict=False)
        A.graph_attr["label"]=graphlabel
    return g,A
def startGraphs(ids=("mid1","mid2"),titles=("Ontology1","ConceptX"),extra_namespaces=[]):
    ags={}
    for iid,title in zip(ids,titles):
         ags[iid]=makeBasicGraph(extra_namespaces)
         ags[iid][1].graph_attr["label"]=title
    return ags
def C(ag=[makeBasicGraph()],uri="foo",label="bar",superclass=None,comment=None,label_pt=None,comment_pt=None,color=None,graph_lang="en"):
    for gg in ag:
        g,A=gg
        G(g,uri,NS.rdf.type,NS.owl.Class)
        G(g,uri,NS.rdfs.label,LL_(label,lang="en"))
        if label_pt:
            G(g,uri,NS.rdfs.label,LL_(label_pt,lang="pt"))
        if graph_lang=="pt":
            A.add_node(label_pt,style="filled")
            nd=A.get_node(label_pt)
        else:
            A.add_node(label,style="filled")
            nd=A.get_node(label)
        if superclass:
            if type(superclass) in (type([1,2]),type((1,2))):
                for sp in superclass:
                    G(g,uri,NS.rdfs.subClassOf,sp)
                    #print([i for i in g.objects(sp,ns.rdfs.label)])
                    if graph_lang=="pt":
                        lsuperclass=[i for i in g.objects(sp,NS.rdfs.label) if i.language=="pt"][0].title()
#                        lsuperclass=[i for i in g.objects(sp,ns.rdfs.label) if i.lang=="pt"][0].title()
                        A.add_edge(  label_pt, lsuperclass)
                        e=A.get_edge(label_pt, lsuperclass)
                    else:
                        lsuperclass=[i for i in g.objects(sp,NS.rdfs.label) if i.language=="en"][0].title()
                        A.add_edge(  label, lsuperclass)
                        e=A.get_edge(label, lsuperclass)
                    e.attr["arrowhead"]="empty"
                    e.attr["arrowsize"]=2
            else:
                G(g,uri,NS.rdfs.subClassOf,superclass)
                #lsuperclass=[i for i in g.objects(superclass,rdfs.label)][-1]
                if graph_lang=="pt":
                    lsuperclass=[i for i in g.objects(superclass,NS.rdfs.label) if i.language=="pt"][0]
                    A.add_edge(  label_pt, lsuperclass)
                    e=A.get_edge(label_pt, lsuperclass)
                else:
                    lsuperclass=[i for i in g.objects(superclass,NS.rdfs.label) if i.language=="en"][0]
                    A.add_edge(  label, lsuperclass)
                    e=A.get_edge(label, lsuperclass)
                e.attr["arrowhead"]="empty"
                e.attr["arrowsize"]=2
        if comment:
            if type(comment) in (type([1,2]),type((1,2))):
                for co in comment:
                    G(g,uri,NS.rdfs.comment,LL_(co,lang="en"))
            else:
                G(g,uri,NS.rdfs.comment,LL_(comment,lang="en"))
        if comment_pt:
            if type(comment_pt) in (type([1,2]),type((1,2))):
                for co in comment_pt:
                    G(g,uri,NS.rdfs.comment,LL_(co,lang="pt"))
            else:
                G(g,uri,NS.rdfs.comment,LL_(comment_pt,lang="pt"))
        if color:
            nd.attr['color']=color
def IC(ga=None,uri=r.URIRef("http://foo.bar"),string="astringid",label=None,draw=False):
    ind=uri+"#"+str(string)
    if ga:
        for g,A in ga:
            G(g,ind,NS.rdf.type,uri)
            if label:
                G(g,ind,NS.rdfs.label,LL_(label))
            if label and draw:
                A.add_node(label,style="filled")
                nd=A.get_node(label)
                nd.attr['color']="#02F3DD"
            elif draw:
                raise ValueError("draw=True but no label")
    return ind

def linkClasses(ga=[makeBasicGraph()],ind=r.URIRef("http://foo.bar"),\
        props=["uri1","uri2"],objs=["uri1","uri2"],draw=False):
    """Link ind subject instance with the objs classes through the props"""
    if draw:
        labels=[0]*len(props)
    for prop, obj, label in zip(props,objs,labels):
        for g,A in ga:
            G(g,ind,prop,obj)
            if draw:
                g.query("SELECT ?s WHERE { <%s> rdfs.label ?label }"%(obj,))
                slabel_=subject_label.replace("%","")
                A.add_edge(  slabel_,label)
                e=A.get_edge(slabel_,label)
                e.attr["label"]=prop.split("/")[-1]

def linkData(ga=[makeBasicGraph()],ind="uriref",props=[NS.po.foo,NS.po.bar],vals=["val1","val2"],label=None):
    """Link an instance with the vals through the props"""
    global COUNT
    # acha o name do uriref buscando no grafo
    for prop, val in zip(props,vals):
        for g,A in ga:
            G(g,ind,prop,LL_(val))
            if label:
                A.add_node(COUNT,style="filled")
                nd=A.get_node(COUNT)
                nd.attr["label"]=val
                nd.attr['color']="#02F3F1"
                label=label.replace("%","FOO")
                A.add_edge(  label,COUNT)
                e=A.get_edge(label,COUNT); COUNT+=1
                e.attr["label"]=prop.split("/")[-1]

def P(ag=[makeBasicGraph()],uri="foo",label="bar",label_pt=None,comment=None):
    """Add object property to RDF graph"""
    for gg in ag:
        g=gg[0]
        G(g,uri,NS.rdf.type,NS.owl.ObjectProperty)
        G(g,uri,NS.rdfs.label,LL_(label,lang="en"))
        if label_pt:
            G(g,uri,NS.rdfs.label,LL_(label_pt,lang="pt"))
        if comment:
            G(g,uri,NS.rdfs.comment,LL_(comment,lang="en"))

def D(ag=[makeBasicGraph()],uri="foo",label="bar",dtype=NS.xsd.string,comment=None,label_pt=None):
    """Add data property to RDF graph"""
    for gg in ag:
        g=gg[0]
        G(g,uri,NS.rdf.type,NS.owl.DatatypeProperty)
        G(g,uri,NS.rdfs.label,LL_(label,lang="pt"))
        G(g,uri,NS.rdfs.range,dtype)
        if comment:
            G(g,uri,NS.rdfs.comment,LL_(comment,lang="en"))
        if label_pt:
            G(g,uri,NS.rdfs.label,LL_(label_pt,lang="pt"))
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

