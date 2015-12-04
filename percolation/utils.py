import time, pickle, os
import builtins as B
TT=time.time()
# check
import zipfile

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
