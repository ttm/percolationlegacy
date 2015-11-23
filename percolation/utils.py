import time, pickle
import builtins as B
TT=time.time()
# check
def check(amsg="string message"):
    global TT
    print(amsg, time.time()-TT); TT=time.time()
# pdumps aqui tb
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
def getAll(ggraph,uri):
    query="SELECT ?o WHERE {{?s {} ?o}}".format(uri)
    return list(set([i[0].value for i in ggraph.query(query)]))
