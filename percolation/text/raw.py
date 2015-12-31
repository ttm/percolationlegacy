__doc__="analysis of chars, tokens, sentences and messages"
def analyseAll(texts_list):
    """Make raw text analysis of all texts and of the merged text"""
    # medidas por mensagem
    texts_measures=[]
    for text in texts_list:
        texts_measures.append({})
        texts_measures[-1]["chars"]=medidasChars(text)
        texts_measures[-1]["tokens"]=medidasTokens(string_text)
        texts_measures[-1]["sentences"]=medidasSentences(string_text)
        texts_measures[-1]["messages"]=medidasMessages(string_text)
    # medidas da lista toda
    text_measures={}
    text_measures["chars"]=medidasChars(text)
    text_measures["tokens"]=medidasTokens(string_text)
    text_measures["sentences"]=medidasSentences(string_text)
    text_measures["messages"]=medidasMessages(string_text)
    del text,texts_list
    return locals()
def medidasChars(T):
    """Medidas de letras TTM formatar para passagem como dicionário"""
    nc=len(T)
    ne=T.count(" ")
    nl=sum([t.isalpha() for t in T])
    nm=sum([t.isupper() for t in T])
    nv=sum([t in ("a","e","i","o","u") for t in T])
    np=sum([t in puncts for t in T])
    nd=sum([t.isdigit() for t in T]) # numerais
    return nc,ne/nc,np/(nc-ne),nd/(nc-ne),nl/(nc-ne),nv/nl,nm/nl
def medidasTokens(T):
    """Medidas extensas sobre os tokens TTM"""
    atime=time.time()
    wtok=k.tokenize.wordpunct_tokenize(T)
    wtok_=[t.lower() for t in wtok]
    nt=len(wtok) #
    ntd=len(set(wtok)) # 
    # tokens que sao pontuacoes
    ntp=sum([sum([tt in puncts for tt in t])==len(t) for t in wtok]) #
    # known and unkown words
    kw=[] #
    ukw=[] #
    tp=[]
    sw=[]
    for t in wtok_:
        if t in WL_:
            kw.append(t)
        elif sum([tt in puncts for tt in t])==len(t):
            tp.append(t)
        else:
            ukw.append(t)
        if t in stopwords:
            sw.append(t)
    sw_=set(sw)
    kw_=set(kw)
    ukw_=set(ukw)
    kwss=[i for i in kw if wn.synsets(i)] #
    kwss_=set(kwss) #
    # known words that does not have synsets
    kwnss=[i for i in kw if i not in kwss_]; c("MT2:")
    kwnss_=set(kwnss) #
    # words that are stopwords
    kwsw=[i for i in kw if i in stopwords] #
    kwsw_=set(kwsw); c("MT3:")
    # known words that are not stopwords
    kwnsw=[i for i in kw if i not in stopwords] #
    kwnsw_=set(kwnsw) #
    # unknown words that are stopwords
    ukwsw=[i for i in ukw if i in stopwords]; c( "MT4:")
    # known words that return synsets and are stopwords
    kwsssw=[i for i in kwss if i in stopwords]; c("MT5:")
    # known words that dont return synsets and are stopwords
    kwnsssw=[i for i in kwnss if i in stopwords]; c("MT6:")
    # words that are known, are not stopwords and do not return synset
    foo_=kwnss_.difference(stopwords)
    kwnssnsw=[i for i in kw if i in foo_]; c("MT7:")
    foo_=kwss_.difference(stopwords) 
    kwssnsw=[i for i in kw if i in foo_] #
    kwssnsw_=set(kwssnsw); c("MT8:")
    del foo, foo_,t,wtok,wtok_
    return locals()

def medidasTamanhosTokens(medidas_tokens):
    """Medidas dos tamanhos dos tokens TTM"""
    tvars=("kw","kwnsw","kwssnsw","kwssnsw","kwsw","sw")
    return mediaDesvio(tvars,medidas_tokens)
def medidasMensagens(ds,tids=None):
    """Medidas das mensagens em si TTM"""
    if not tids:
        mT=[ds.messages[i][3] for i in ds.message_ids]
    else:
        mT=[ds.messages[i][3] for i in tids]
    tokens_msgs=[k.tokenize.wordpunct_tokenize(t) for t in mT] # tokens
    knownw_msgs=[[i for i in toks if (i not in stopwords) and (i in WL_)] for toks in tokens_msgs]
    stopw_msgs=[[i for i in toks if i in stopwords] for toks in tokens_msgs]
    puncts_msgs=[[i for i in toks if
         (len(i)==sum([(ii in puncts) for ii in i]))]
         for toks in tokens_msgs] #
    sents_msgs=[k.sent_tokenize(t) for t in mT] # tokens
    nmsgs=len(mT)
    mvars="mT","tokens_msgs","knownw_msgs","stopw_msgs","puncts_msgs","sents_msgs"
    medidas=mediaDesvio(mvars,locals())
    medidas.update({"nmsgs":nmsgs,"tokens_msgs":tokens_msgs})
    return medidas
def medidasSentencas(T):
    """Medidas das sentenças TTM"""
    TS=k.sent_tokenize(T)
    tokens_sentences=[k.tokenize.wordpunct_tokenize(i) for i in TS] ### Para os POS tags
    knownw_sentences=[[i for i in ts if (i not in stopwords) and (i in WL_)] for ts in tokens_sentences]
    stopw_sentences =[[i for i in ts if i in stopwords] for ts in tokens_sentences]
    puncts_sentences=[[i for i in ts if
         (len(i)==sum([(ii in puncts) for ii in i]))]
         for ts in tokens_sentences] #
    mvars="TS","tokens_sentences","knownw_sentences","stopw_sentences","puncts_sentences"
    medidas=mediaDesvio(mvars,locals())
    medidas.update{"nsents":len(TS),"tokens_sentences":tokens_sentences}
    return medidas
def medidasTamanhosSentencas(T,medidas_tokens):
    """Medidas dos tamanhos das sentenças TTM"""
    TS=k.sent_tokenize(T)
    sTS=[k.tokenize.wordpunct_tokenize(i) for i in TS] ### Para os POS tags
    # numero de caracteres por sentenca
    tTS=[len(i) for i in TS]
    # tamanho das sentencas em tokens
    tsTS=[len(i) for i in sTS]
    # tamanho das sentencas em palavras conhecidas
    kw_=medidas_tokens["kw_"]
    tsTSkw=[len([ii for ii in i if ii in kw_]) for i in sTS]
    medidas=mediaDesvio(("tsTS","tTS","tsTSkw"),locals())
    medidas.update({"sTS",sTS})
    return medidas
def medidasTamanhosMensagens(mT, tids=None):
    tmT=[len(t) for t in mT] # chars
    ttmT=[len(k.tokenize.wordpunct_tokenize(t)) for t in mT] # tokens
    tsmT=[len(k.sent_tokenize(t)) for t in mT] # sentences
    return mediaDesvio(("tmT""ttmT""tsmT"),locals())
def medidasTokensQ(T,lang="en"):
    """Medidas de tokens TTM"""
    atime=time.time()
    wtok=k.tokenize.wordpunct_tokenize(T)
    wtok_=[t.lower() for t in wtok]
    if lang=="en":
        kw=[len(i) for i in wtok_ if i in WL_]
        sw=[len(i) for i in wtok_ if i in stopwords]
    else:
        kw=[len(i) for i in wtok_ if i in WLP_]
        sw=[len(i) for i in wtok_ if i in stopwordsP]
    return P.utils.mediaDesvio(("kw","sw"),locals())

def medidasTokens_(T,ncontract=None):
    """Make measures on tokens, one should favor medidasTokens() if doing a thorough analysis"""
    wtok=k.tokenize.wordpunct_tokenize(T)
    wtok_=[t.lower() for t in wtok]
    tokens=len(wtok) #
    tokens_=set(wtok)
    tokens_diff=len(tokens_)/tokens # 
    punct=sum([sum([tt in puncts for tt in t])==len(t) for t in wtok_])
    punct/=tokens
    known=[i for i in wtok_ if (i not in stopwords) and (i in WL_)]
    knownw=len(known)
    known_=set(known)
    knownw_diff=len(known_)/knownw
    stop=[i for i in wtok_ if i in stopwords]
    stopw=len(stop)/knownw
    knownw/=tokens
    contract=ncontract/tokens

    Mtoken,Stoken=mediaDesvio_(wtok_)
    Mknownw,Sknownw=mediaDesvio_(known)
    Mknownw_diff,Sknownw_diff=mediaDesvio_(known_)
    Mstopw,Sstopw=mediaDesvio_(stop)
    del wtok, wtok_,known,known_,stop
    return locals()


