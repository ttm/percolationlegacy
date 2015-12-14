import time, pickle, os, zipfile
import builtins as B
from SPARQLWrapper import SPARQLWrapper, JSON
TT=time.time()

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
    #if "update" in se: # or if not mvars
    if not mvars: # or if not mvars
        return spql_endpoint.query().convert()
    else:
        results = spql_endpoint.query().convert()
        res=[]
        for result in results["results"]["bindings"]:
            res.append([result[i]['value'] for i in mvars])
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

def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
# pdumps aqui tb
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
