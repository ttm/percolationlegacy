__doc__="most of the following routines are deprecated \
        in favor of better or more complete analyses \
        in the percolation.text module"
 
def medidasParticipante(dict_auth_text):
    """Medidas de texto por autor TTM"""
    medidas_autor={}
    for author in dict_auth_text:
        text=dict_auth_text[author]
        if text:
            text_,ncontract=R(text)
            medidas=medidasSentencas(text_)
            medidas2=medidasPOS(medidas["tokens_sentences"])
            medidas.update(medidas2)
            medidas_autor[author]=medidas
    return medidas_autor


def medidasSinais2_(medidas_pos_list,medidas_mensagens):
    return [medidasSinais2(post,mmU)
            for post,mmU in zip(medidas_pos_list,medidas_mensagens)]
def medidasSinais2(post,medidas_mensagensU):
    """Get POS measures from Wordnet tagging"""
    sinal=[[i[1] for i in j] for j in post["tags"]]
    sinal_=chunks([i[1] for j in post["tags"] for i in j],100)
    sinais={}
    sinais["adj"]=[j.count("ADJ") for j in sinal]
    sinais["sub"]=[j.count("NOUN") for j in sinal]
    sinais["pun"]=[j.count(".") for j in sinal]
    sinais["verb"]=[j.count("VERB") for j in sinal_]
    sinais["chars"]=medidas_mensagensU["toks_msgs"]
    return sinais

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


