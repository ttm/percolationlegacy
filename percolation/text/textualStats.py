import time, numpy as n, re, nltk as k, collections as c, string, pickle, os, langid, shutil
from nltk.corpus import wordnet as wn
import builtins as B

def generalMeasures(ds,np,ts):
    """Return overall measures from list datastructures and network partitioning"""
    # mensagens por setor TTM
    Ms=[sum([len(ds.author_messages[i]) for i in j])
        for j in np.sectorialized_agents__]
    Ms_=perc(Ms)
    NM=N/M # usuarios / mensagem TTM
    NM_=100*NM 
    NMs=[i/j if j!=0 else n.inf for i,j in zip(Ns,Ms)] # por setor TTM
    NMs_=perc(NMs)
    # Threads por setor TTM
    Gammas=[sum([len([i for i in ds.author_messages[aid] if i[1]==None])
           for aid in sa]) for sa in np.sectorialized_agents__]
    Gammas_=perc(Gammas)
    G_=[100*i/j for i,j in zip(Gammas,Ms)]

    # montante escrito por cada setor
    tlength_sectors=[]
    tlength_sector.append(lsector) # quantidade de texto nas mensagens de cada setor TTM

    mt=[n.mean(i) for i in tlength_sectors]
    st=[n.std(i) for i in tlength_sectors]
    tls=[i for j in tlength_sectors for i in j]
    mt_ =n.mean(tls)
    st_ =n.std(tls)
    vdict=locals()
    return vdict
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

def medidasTokens_(T,ncontract=None):
    """Make measures on tokens TTM"""
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
    vdict=locals()
    return vdict

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

def medidasLetras(T):
    """Medidas de letras TTM formatar para passagem como dicionário"""
    nc=len(T)
    ne=T.count(" ")
    nl=sum([t.isalpha() for t in T])
    nm=sum([t.isupper() for t in T])
    nv=sum([t in ("a","e","i","o","u") for t in T])
    np=sum([t in puncts for t in T])
    nd=sum([t.isdigit() for t in T]) # numerais
    return nc,ne/nc,np/(nc-ne),nd/(nc-ne),nl/(nc-ne),nv/nl,nm/nl
def medidasTamanhosTokens(medidas_tokens):
    """Medidas dos tamanhos dos tokens TTM"""
    tvars=("kw","kwnsw","kwssnsw","kwssnsw","kwsw","sw")
    return mediaDesvio(tids,medidas_tokens)
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
def medidasPOS(sentences_tokenized):
    """Measures of POS tags

    Receives a sequence of sentences,
    each as a sequence of tokens.
    Returns a set measures of POS tags,
    and the tagged sentences.

    Convention:
    VERB - verbs (all tenses and modes)
    NOUN - nouns (common and proper)
    PRON - pronouns 
    ADJ - adjectives
    ADV - adverbs
    ADP - adpositions (prepositions and postpositions)
    CONJ - conjunctions
    DET - determiners
    NUM - cardinal numbers
    PRT - particles or other function words
    X - other: foreign words, typos, abbreviations
    . - punctuation
    
    See "A Universal Part-of-Speech Tagset"
    by Slav Petrov, Dipanjan Das and Ryan McDonald
    for more details:
        http://arxiv.org/abs/1104.2086"""

    tags=brill_tagger.tag_sents(sentences_tokenized)
    tags_=[item for sublist in tags for item in sublist]
    tags__=[i[1] for i in tags_ if i[0].lower() in WL_]
    htags=c.Counter(tags__)
    htags__=c.OrderedDict()
    if htags:
       	factor=100.0/sum(htags.values())
        htags_={}
        for i in htags.keys(): htags_[i]=htags[i]*factor    
        htags__=c.OrderedDict(sorted(htags_.items(), key=lambda x: -x[1]))
    del tags_,tags__,htags,htags_,factor
    return locals()

def medidasWordnet2_POS(wn_measures,poss=("n","as","v","r")):
    """Make specific measures to each POS tag found TTM"""
    wn_measures2={}
    for pos in poss:
        wn_measures2[pos]=g.textUtils.medidasWordnet2_(wn_measures,pos)
    return wn_measures2
      
def medidasWordnet(words_with_pos_tags):
    """Medidas gerais sobre a aplicação da Wordnet TTM"""
    WT=words_with_pos_tags
    WT_=[(i[0].lower(),i[1]) for j in WT for i in j] #
    wlists=filtro(WT_) #
    wl=wlists["word_com_synset"]
    posok=[] #
    posnok=[] #
    for ww in wl:
        pos = traduzPOS(ww[1])
        ss=ww[2]
        # procura nos nomes dos synsets o pos e numeracao mais baixa
        poss=[i.pos() for i in ss]
        fposs=[pp in pos for pp in poss]
        if sum(fposs):
            tindex=fposs.index(True)
            posok.append((ww[0],ss[tindex]))
        else:
            posnok.append(ww)
    # estatísticas sobre posok
    # quais as tags?
    posok_=[i[1].pos() for i in posok]
    ftags_=[100*posok_.count(i)/len(posok_) for i in ('n', 's','a', 'r', 'v')]
    ftags=ftags_[0:2]+ftags_[3:] #
    ftags[1]+=ftags_[2]
    del WT,wl,ww,pp,pos,ss,poss,fposs,tindex,posok_,ftags_
    return locals()

def medidasWordnet2(wndict,pos=None):
    """Medidas das categorias da Wordnet sobre os verbetes TTM"""
    sss=wndict["posok"]
    if pos:
        sss_=[i[1] for i in sss if i[1].pos() in pos]
    else:
        sss_=[i[1] for i in sss]
    hyperpaths=[i.hypernym_paths() for i in sss_]
    top_hypernyms=[i[0][:4] for i in hyperpaths] # fazer histograma por camada
    lexnames=[i.lexname().split(".")[-1] for i in sss_] # rever

    mhol=[len(i.member_holonyms()) for i in sss_]
    phol=[len(i.part_holonyms()) for i in sss_]
    shol=[len(i.substance_holonyms()) for i in sss_]
    nhol_=[mhol[i]+phol[i]+shol[i] for i in range(len(sss_))] ###

    mmer=[len(i.member_meronyms()) for i in sss_] #
    pmer=[len(i.part_meronyms()) for i in sss_]
    smer=[len(i.substance_meronyms()) for i in sss_]
    nmer_=[mmer[i]+pmer[i]+smer[i] for i in range(len(sss_))] ###

    nlemmas=[len(i.lemmas()) for i in sss_] ###
    nhyperpaths=[len(i) for i in hyperpaths]
    shyperpaths=[len(i) for j in hyperpaths for i in j]

    nentailments=[len(i.entailments()) for i in sss_]

    nhypernyms=[len(i.hypernyms()) for i in sss_]
    nihypernyms=[len(i.instance_hypernyms()) for i in sss_]
    nhyper_=[nhypernyms[i]+nihypernyms[i] for i in range(len(sss_))]

    nhypo=[len(i.hyponyms()) for i in sss_] ###
    nihypo=[len(i.instance_hyponyms()) for i in sss_]
    nhypo_=[nhypo[i]+nihypo[i] for i in range(len(sss_))]

    maxd=[i.max_depth() for i in sss_] ###
    mind=[i.min_depth() for i in sss_] ###

    nregion_domains=[len(i.region_domains()) for i in sss_] #
    ntopic_domains= [len(i.topic_domains())  for i in sss_]
    nusage_domains= [len(i.usage_domains())  for i in sss_]
    ndomains=[nregion_domains[i]+ntopic_domains[i]+nusage_domains[i]
            for i in range(len(sss_))] ###

    nsimilar=[    len(i.similar_tos()) for i in sss_]
    nverb_groups=[len(i.verb_groups()) for i in sss_]

    del wndict
    mvars_=[i for i in locals.keys() if i not in ("sss","sss_","top_hypernyms","pos","hyperpaths","lexnames")]
    locals_=locals()
    medidas=mediaDesvio(mvars_,locals_)
    for mvar in mvars:
        del locals_[mvar]
    medidas.update(locals_)
    return medidas

