import time, pickle, os, zipfile, string, networkx as x, re
import builtins as B
import percolation as P
from SPARQLWrapper import SPARQLWrapper, JSON
TT=time.time()
import pdb

nestedDict = lambda: collections.defaultdict(nestedDict)
PROVENANCE_IDS="gmane-", "_fb", "_tw"

def createAAUser(nick=None,email=None,name=None,comment=None,context="aa"):
    default_percolation_session=P.get("per:currentState per:currentSession ?foosession. ?foosession per:user ?user . ?user a per:DefaultParticipant")
    if not default_percolation_session:
        while 1:
            try:
                percolation_equivalence=input("use percolation profile data (y/n)? ")
                if percolation_equivalence not in ("y","n"):
                    raise ValueError
            except ValueError:
                if percolation_equivalence=="y":
                    # get nick, email, name and comment from percolation or set equivalence between sets
                    current_user_uri=P.get(NS.per.currentUser)
                    nick=P.get(current_user_uri,NS.per.nick)
                    name=P.get(current_user_uri,NS.per.name)
                    email=P.get(current_user_uri,NS.per.email)
                    comment=P.get(current_user_uri,NS.per.coment)
                    c("got nick: {}\nname: {}\nemail: {}\ncomment: {}\nfrom uri: {}".format(
                        nick, name, email, comment, current_user_uri)
                continue
            break
    if not nick:
        nick=input("please write your preferred nick (if any): ")
    if not email:
        email=input("please write your preferred email (if any): ")
    if not name:
        name=input("please write your name (if any): ")
    if not comment:
        comment=input("please write any comment for the user that you are creating (if any): ")

    if not nick:
        nick=randomNick()
    now=datetime.datetime.now()
    user_uri=P.rdf.timestampedURI(NS.per.participant,nick,now)
    triples=[
            (user_uri, a, NS.per.Participant),
            (user_uri, NS.aa.nick, nick),
            (user_uri, NS.aa.registered, now),
            ]

    if email:
        triples+=[(user_uri,NS.aa.email,email)]
    if name:
        triples+=[(user_uri,NS.aa.name,name)]
    if comment:
        triples+=[(user_uri,NS.aa.comment,comment)]
    return P.add(triples,context=context)


def createUser(nick=None,email=None,name=None,comment=None,context="session"):
    if not nick:
        nick=input("please write your preferred nick (if any): ")
    if not email:
        email=input("please write your preferred email (if any): ")
    if not name:
        name=input("please write your name (if any): ")
    if not comment:
        comment=input("please write any comment for the user that you are creating (if any): ")

    if not nick:
        nick=randomNick()
    now=datetime.datetime.now()
    user_uri=P.rdf.timestampedURI(NS.per.participant,nick,now)
    triples=[
            (user_uri, a, NS.per.Participant),
            (user_uri, NS.per.nick, nick),
            (user_uri, NS.per.registered, now),
            ]

    if email:
        triples+=[(user_uri,NS.per.email,email)]
    if name:
        triples+=[(user_uri,NS.per.name,name)]
    if comment:
        triples+=[(user_uri,NS.per.comment,comment)]
    return P.add(triples,context=context)

def startSession(context="session"):
    current_user_uri=P.get(NS.per.currentUser)
    now=datetime.datetime.now()
    if not current_user_uri:
        nick=P.utils.randomNick()
        current_user_uri=P.rdf.timestampedURI(NS.per.Participant,nick,now)
        triples=[
                (current_user_uri, a, NS.per.DefaultParticipant),
                (current_user_uri, NS.per.nick, nick),
                (current_user_uri, NS.per.registered, now),
                ]
        c("Please create a user with P.utils.createUser() ASAP. Registered for now as {} with URI: {}".format(nick,current_user_uri))
    else:
        triples=[]

    session_uri=P.rdf.timestampedURI(NS.per.Session)
    current_state_uri=NS.per.CurrentState # shout be in ontology
    triples+=[
             (current_state_uri,NS.per.currentSession,session_uri),
             (session_uri,NS.per.started,now),
             (session_uri,NS.per.user,current_user_uri),
             (current_state_uri,NS.per.currentUser,current_user_uri),
             ]

    P.add(triples,context=context)
    P.rdf.minimumOntology()
    P.rdf.legacyMetadata()
    P.rdf.rdfsInference("minimum_ontology","legacy_metadata","session_legacy_metadata")
    # by this point, one should have the named graphs/contexts:
    # session, minimum_ontology, legacy_metadata, session_legacy_metadata

def shout(message_string,context="aa"):
    participant_uri=P.get(NS.per.percolationParticipant)

    nick=P.get(participant_uri,NS.nick)
    now=datetime.datetime.now()
    shout_uri=P.rdf.timestampedURI(NS.aa.Shout,nick,now)

    triples=[
            (shout_uri,aa.user,participant_uri)
            (shout_uri,aa.shoutText,shout),
            (shout_uri,aa.created,now)
            ]

    is_percolation_session=P.get(NS.per.trueSession)
    if is_percolation_session:
        percolation_session_uri=P.get(NS.per.Session)
        triples+=[(shout_uri,NS.aa.percolationSession,percolation_session_uri)]
    shout_status="current shout timestamp: {}\ncurrent shout text: {}".format(now.isoformat(),message_string)
    session_uri=P.get(NS.aa.currentSession)
    if session_uri:
        triples+=[(aa_session,NS.aa.hasShout,shout_uri)]

        session_started_timestamp=P.get(aa_session,NS.aa.started)
        session_status="aa user: {}\nyour session started at {}.".format(nick,session_started_timestamp)

        last_shout_text, last_shout_timestamp=P.get("<%s> aa:hasShout ?shoutfoo . \
                ?shoutfoo aa:shoutText ?shouttext .\
                ?shoutfoo aa:created ?shouttime",context,aa_session,"ORDER BY DESC(?shouttime) LIMIT 1")
        last_message_status="last shout at: {},\nlast shout is: {}".format(last_shout_timestamp,last_shout_text)
        help_codeta="see P.utils.aaSesion() to start and manage sessions and {} context/named graph.".format(context)
        c("{}\n{}\n{}\n{}\n".format(session_status,last_shout_status,shout_status,help_codeta))
    else:
        c("{}\nNo aa session active. Manage with P.utils.aaSession() if shouts should be associated to a session.".format(shout_status))
    return P.add(triples,context=context)




def objectFromDict(adict):
    class aobj:
        pass
    for key in adict:
        exec("aobj.{}={}".format(key,adict[key]))
    return aobj
def fileProvenanceDict(files):
    gmane=sorted([i for i in files if PROVENANCE_IDS[0] in i])
    fb=   sorted([i for i in files if PROVENANCE_IDS[1] in i]) # FB
    tw=   sorted([i for i in files if PROVENANCE_IDS[2] in i]) # TW
    dummy2=gmane[8:12]
    dummy_diversified=gmane[3:4] +fb[3:4]+tw[3:4]
    dummy=gmane[-10:-9]
    dummyfb=fb[10:11]
    all_ok=gmane+fb+tw
    all_=files
    del files
    return locals()
def callDebugger():
    """Helper function to call interpreter or debugger in the midle of execution for testing and debugging"""
    pdb.set_trace()
# use with tdict=nestedDict(); tdict["akey1"]["akey2"]="anything"
def uniqueItems(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
def min3(narray):
    narray_=n.array(narray)
    args=narray_.argsort()
    return narray_[args[:3]]
def max3(narray):
    narray_=n.array(narray)
    args=narray_.argsort()
    return narray_[args[-3:]]
def toUndirected(xgraph):
    gg=x.Graph()
    gg.add_edges_from(xgraph.edges_iter(), weight=0)

    for u, v, d in xgraph.edges_iter(data=True):
            gg[u][v]['weight'] += d['weight']
    return gg
def getFiles(datadir,ext=".owl"):
    dirs=os.listdir(datadir)
    aa=[]
    for tdir in dirs:
        umbrelladir=datadir+tdir
        datasetdirs=os.listdir(umbrelladir)
        datasetdirs_=[i for i in datasetdirs if os.path.isdir("{}/{}".format(umbrelladir,i))]
        datasetdirs_=[i for i in datasetdirs_ if not i.startswith(".")]
        for datasetdir in datasetdirs_:
            rdfdir="{}/{}/rdf/".format(umbrelladir,datasetdir)
            files=os.listdir(rdfdir)
            files=[i for i in files if "Meta" in i]
            files=[i for i in files if i.endswith(".owl")]
            for tfile in files:
                tfile_=rdfdir+tfile
                aa+=[tfile_]
    return aa
def urifyFilename(fname,digits=True):
    if digits:
        fname="".join(i for i in fname if i not in string.digits)
    return "http://{}".format(fname.split("/")[-1].replace("_","").lower())
def testRdfs(path,end_url,do_query=True,write_back=True):
    files=os.listdir(path)
    for afile in files:
        afile_=path+afile
        tgraph="http://{}".format(afile.lower())
        tgraph="".join(i for i in tgraph if not i.isdigit()).replace("_","")
        #"s-put http://200.144.255.210:8082/dsfoo http://adorno.enfeite.ttl AdornoNaoEhEnfeiteTranslate.ttl"
        cmd="s-put {} {} {}".format(end_url, tgraph, afile_)
        os.system(cmd); check(cmd)
        if do_query:
            q='SELECT (COUNT(?s) as ?{{}})  WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}}'.format(tgraph)
            check(q)
            res1=mQuery(end_url,q,("cs",))
            check(res1)
            q='SELECT DISTINCT ?{{}} WHERE {{{{ GRAPH <{}> {{{{ ?s ?p ?o }}}} }}}} LIMIT 5'.format(tgraph)
            res2=mQuery(end_url,q,("s",))
            check(res2); print("\n")

#        q="SELECT DISTINCT ?{} WHERE {{ GRAPH ?g {{ }} }}"
#        v="g"
#        graphs=[i[0] for i in mQuery(end_url,q,v)]
#        if "http://discovery.info" not in graphs:
#            success=mQuery(end_url,"CREATE GRAPH <http://discovery.info>")
#        # build query to insert
#        uquery="""WITH GRAPH <http://discovery.info>
#             INSERT DATA {
## endpoint
## networktype
## basic info: nparticipants, nedges, date snapshot
## original
#             }
#        """

#        cmd="s-query --service {}  'SELECT (COUNT(?s) as ?cs)  WHERE {{ GRAPH <{}> {{ ?s ?p ?o }} }}'".format(end_url,tgraph)
#        os.system(cmd); check(cmd)
#        cmd="s-query --service {}  'SELECT ?s WHERE {{ GRAPH <{}> {{ ?s ?p ?o }} }} LIMIT 1'".format(end_url,tgraph)
#        os.system(cmd); check(cmd)

def getGraphs(path,end_url):
    files=os.listdir(path)
    for afile in files:
        afile_=path+afile
        #"s-put http://200.144.255.210:8082/dsfoo http://adorno.enfeite.ttl AdornoNaoEhEnfeiteTranslate.ttl"
        cmd="s-put {} http://{} {}".format(end_url,afile,afile_)
        os.system(cmd)
        check(cmd)


def utf8(astring):
    """Ensure string is utf8"""
    return astring.strip().encode("utf-8").decode("utf-8","ignore")
hh="""
prefix xsd: <http://www.w3.org/2001/XMLSchema#> 
prefix dct: <http://purl.org/dc/terms/> 
prefix dce: <http://purl.org/dc/elements/1.1/> 
prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
prefix owl: <http://www.w3.org/2002/07/owl#>
prefix skos: <http://www.w3.org/2004/02/skos/core#> 
prefix bibo: <http://purl.org/ontology/bibo/> 
prefix foaf: <http://xmlns.com/foaf/0.1/> 
prefix geo: <http://www.w3.org/2003/01/geo/wgs84_pos#> 
prefix aiiso:<http://purl.org/vocab/aiiso/schema#>
prefix teach:<http://linkedscience.org/teach/ns#>
prefix cm: <http://purl.org/socialparticipation/cm/>
prefix obs: <http://purl.org/socialparticipation/obs/>
prefix aa: <http://purl.org/socialparticipation/aa/>
prefix vbs: <http://purl.org/socialparticipation/vbs/>
prefix opa: <http://purl.org/socialparticipation/opa/>
prefix ops: <http://purl.org/socialparticipation/ops/>
prefix ocd: <http://purl.org/socialparticipation/ocd/>
prefix ore: <http://purl.org/socialparticipation/ore/>
prefix ot: <http://purl.org/socialparticipation/ot/>
prefix po: <http://purl.org/socialparticipation/po/>
prefix fb: <http://purl.org/socialparticipation/fb/>
prefix tw: <http://purl.org/socialparticipation/tw/>
prefix irc: <http://purl.org/socialparticipation/irc/>
prefix gmane: <http://purl.org/socialparticipation/gmane/>
prefix ld: <http://purl.org/socialparticipation/ld/>\n""" 
def mQuery(spql_endpoint,query,mvars=None):
    se=spql_endpoint[:]
    spql_endpoint=SPARQLWrapper(spql_endpoint)
    if mvars:
        query=query.format(*mvars)
        query=hh+query
        spql_endpoint.setQuery(query)
        spql_endpoint.setReturnFormat(JSON)
    else:
        #spql_endpoint.method = 'POST'
        spql_endpoint.method = 'PUT'
        spql_endpoint.setQuery(query)
        return spql_endpoint.query().convert()
    #if "update" in se: # or if not mvars
    if mvars:
        results = spql_endpoint.query().convert()
        res=[]
        for result in results["results"]["bindings"]:
            res+=[[]]
            for i in mvars:
                rr=result.get(i)
                if rr:
                    res[-1]+=[rr["value"]]
                else:
                    res[-1]+=[0]
#            print(res)
            #res.append([result[i]['value'] for i in mvars])
        #for result in results["results"]["bindings"]:
        #    res.append([result[i]['value'] for i in mvars])
        return res
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
def zipDir(odirpath,dpath="./afilename.zip"):
    zipf = zipfile.ZipFile(dpath, 'w')
    zipdir(odirpath, zipf)
    zipf.close()
def zipDir2(odirpath,dpath="./afilename"):
    i=0
    zipf = zipfile.ZipFile("{}{}.zip".format(dpath,"00000"), 'w')
    for root, dirs, files in os.walk(odirpath):
        for file in files:
            zipf.write(os.path.join(root, file))
            i+=1
            if i%5000==0:
                zipf.close()
                zipf = zipfile.ZipFile("{}{}.zip".format(dpath,i), 'w')
    zipf.close()

#
#if __name__ == '__main__':
#    zipf = zipfile.ZipFile('Python.zip', 'w')
#    zipdir('tmp/', zipf)
#    zipf.close()

def check(*args):
    global TT
    prompt=0
    if args[0]==1:
        prompt=1
        args=args[1:]
    if args and isinstance(args[0],str) and (len(args[0])==args[0].count("\n")):
        print("{}{:.3f}".format(args[0],time.time()-TT),*args[1:]); TT=time.time()
    else:
        print("{:.3f}".format(time.time()-TT),*args); TT=time.time()
    if prompt:
        input("ANY KEY TO CONTINUE")
# pdumps aqui tb
def identifyProvenance(astring):
    if "gmane-" in astring:
        return P.rdf.NS.po.GmaneSnapshot
    elif "_fb" in astring:
        return P.rdf.NS.po.FacebookSnapshot
    elif "_tw" in astring:
        return P.rdf.NS.po.TwitterSnapshot

class Dumper:
    def __init__(self,tfilename):
        if os.path.isfile(tfilename):
            self.f=open(tfilename,"ab")
        else:
            self.f=open(tfilename,"wb")
    def dump(self,tobj):
        pickle.dump(tobj,self.f)
    def close(self):
        self.f.close()
def pRead3(tfilename,tweets,fopen=None):
    """pickle read for the Dumper class"""
    if not fopen:
        f=open(tfilename,"rb")
    else:
        f=fopen
    #while len(tweets)<9900:
    while len(tweets)<5000:
        try:
            tweets+=pickle.load(f)
        except EOFError:
            break
    return tweets,f

def pRead2(tfilename):
    """pickle read for the Dumper class"""
    objs=[]
    with open(tfilename,"rb") as f:
        while 1:
            try:
                objs.append(pickle.load(f))
            except EOFError:
                break
    return objs
def pDump(tobject,tfilename):
    with open(tfilename,"wb") as f:
        pickle.dump(tobject,f,-1)
def pRead(tfilename):
    with open(tfilename,"rb") as f:
        tobject=pickle.load(f)
    return tobject
# e o das strings
strange="Ã¡","Ã ","Ã¢","Ã£","Ã¤","Ã©","Ã¨","Ãª","Ã«","Ã­","Ã¬","Ã®","Ã¯","Ã³","Ã²","Ã´","Ãµ","Ã¶","Ãº","Ã¹","Ã»","Ã¼","Ã§","Ã","Ã€","Ã‚","Ãƒ","Ã„","Ã‰","Ãˆ","ÃŠ","Ã‹","Ã","ÃŒ","ÃŽ","Ã","Ã“","Ã’","Ã”","Ã•","Ã–","Ãš","Ã™","Ã›","Ãœ","Ã‡","Ã"
correct="á", "à", "â", "ã", "ä", "é", "è", "ê", "ë", "í", "ì", "î", "ï", "ó", "ò", "ô", "õ", "ö", "ú", "ù", "û", "ü", "ç", "Á", "À", "Â", "Ã", "Ä", "É", "È", "Ê", "Ë", "Í", "Ì", "Î", "Ï", "Ó", "Ò", "Ô", "Õ", "Ö", "Ú", "Ù", "Û", "Ü", "Ç","Ú"
def utf8Fix(string):
    # https://berseck.wordpress.com/2010/09/28/transformar-utf-8-para-acentos-iso-com-php/
    for st, co in zip(strange,correct):
        string=string.replace(st,co)
    return string

def countMe(ggraph,uri,o="?o"):
    query=r"SELECT (COUNT(?o) as ?count) WHERE {{   ?s {} {}}}".format(uri,o)
    return [i for i in ggraph.query(query)][0][0].value
def countMe2(ggraph,uri):
    query=r"SELECT (COUNT(?s) as ?count) WHERE {{?s a {}}}".format(uri)
    return [i for i in ggraph.query(query)][0][0].value
def getAll(ggraph,uri):
    query="SELECT ?o WHERE {{?s {} ?o}}".format(uri)
    return list(set([i[0].value for i in ggraph.query(query)]))
def getAll2(ggraph,uri):
    query="SELECT ?o WHERE {{?s {} ?o}}".format(uri)
    return list(set([i[0] for i in ggraph.query(query)]))
def cred(twc_class):
    t=twc_class
    return [t.tak,t.taks,t.tat,t.tats]
def breakMe():
    a=oasijdaoisjdoiasjdoiasjdoiajsdoiajsdoiajsd
def perc(alist):
    if type(alist) in (type([1,2]), type((2,4))):
        return [100*i/sum(alist) for i in alist]
    else:
        return 100*alist/alist.sum()
def mkName(tdir,fname,tag):
    return tdir+fname.replace(".tex","{}.tex".format(tag))

class RegexpReplacer(object):
    """Replaces contractions with full words"""
    replacement_patterns = [
    (r'won\'t', 'will not'),
    (r'can\'t', 'can not'),
    (r'i\'m', 'i am'),
    (r'ain\'t', 'is not'),
    (r'(\w+)\'ll', '\g<1> will'),
    (r'(\w+)n\'t', '\g<1> not'),
    (r'(\w+)\'ve', '\g<1> have'),
    (r'(\w+)\'s', '\g<1> is'),
    (r'(\w+)\'re', '\g<1> are'),
    (r'(\w+)\'d', '\g<1> would')
    ]
    patterns = [(re.compile(regex), repl) for (regex, repl) in replacement_patterns]
    def replace(self, text):
        s = text
        count_=0
        for (pattern, repl) in self.patterns:
            (s, count) = re.subn(pattern, repl, s)
            count_+=count
        return s, count_
REPLACER=RegexpReplacer()
del RegexpReplacer
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    ll=[]
    for i in range(0, len(l), n):
        ll.append(l[i:i+n])
    return ll
