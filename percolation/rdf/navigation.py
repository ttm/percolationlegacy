__doc__="""utilities for navigating rdflib graphs in Percolation (usually a/the percolation_graph))
useful rdflib builtin functions (avoid reimplementation):
    rdflib.Graph().add(triples)
masks written:
    L(literal_value) for probing value/data type and language. Also extended to accept lists and dictionaries"""

import percolation as P

def triplesScafolding(subjects,predicates,objects,context=None):
    """Link subject(s) through predicate(s) to subject(s).
    
    Accepts any combination of one and N triples in inputs, eg:
      triplesScafolding(participants,NS.po.name,names) # N 1 N
      triplesScafolding(participants,name_props,name) # N N 1
      triplesScafolding(participant,name_pros,names) # 1 N N

      triplesScafolding(participant, names_props,name) # 1 N 1
      triplesScafolding(participant, NS.po.name,names) # 1 1 N
      triplesScafolding(participants,NS.po.name,name) # N 1 1

    Might be useful for rearanging lists into triples:
      triplesScafolding(participants,name_props,names) # N N N
      triplesScafolding(participant,NS.po.name,names) # 1 1 1"""

    N=max(len(subjects),len(predicates),len(objects))
    check=sum([((len(i)==N) or isinstance(i,(r.URIRef,r.Namespace))) for i in (subjects,predicates,objects)])==3
    if not check:
        raise ValueError("input should be a combination of loose URIs and lists of same size ")
    triples=[]
    if check==3:
        for i, subject in enumerate(subjects):
            predicate=predicates[i]
            object_=objects[i]
            triples+=[(subject,predicate,object_)]
    else:
        if isinstance(subjects,(r.URIRef,r.Namespace)):
            subjects=[subjects]
        if isinstance(predicates,(r.URIRef,r.Namespace)):
            predicates=[predicates]
        if isinstance(objects,(r.URIRef,r.Namespace)):
            objects=[objects]
        for subject in subjects:
            for predicate in predicates:
                for object_ in objects:
                    triples+=[(subject, predicate, object_)]
    if context=="return_triples":
        return triples
    P.rdf.io.add(triples,context=context)

def add(triples, context): # should be in io
    for triple in triples:
        if not isinstance(triple[2],(r.Namespace,r.URIRef,r.Literal)):
            triple=(triple[0],triple[1],L(triple[2]))



def C(classname,stringid,context=None):
    """Adds the individual classname+stringid a classname and returns individual"""
    uri=classname+"#"+stringid
    if context:
        triples=[
                uri, a, classname
                ]
        P.io.add(triples,context_id=context)
    return uri

def L(literal,lang=None,datatype=None):
    if language=1:
        language="en"
    elif language=2:
        language="pt"
    elif language=3:
        language="es"
    return r.Literal(literal,lang=language,datatype)

