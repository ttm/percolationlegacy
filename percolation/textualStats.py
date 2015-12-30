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
def makeText_(ds,pr):
    """Get text in all sectors TTM"""
    foo=[P.utils.REPLACER.replace(i) for i in texts]
    texts_=[i[0] for i in foo]
    ncontractions=[i[1] for i in foo]
    return texts_,ncontractions, msg_ids
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
    mkw=n.mean(kw)
    dkw=n.std(kw)
    msw=n.mean(sw)
    dsw=n.std(sw)
    mvars=("mkw","dkw","msw","dsw")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
def makeSentencesTable(medidasSentencas_dict, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="sentencesInline.tex",tag=None):
    """Tabela de medidas de sentencas TTM"""
    sms=medidasSentencas_dict
    mvars=("nsents",
            "Mchars_sents","Schars_sents",
            "Mtoks_sents","Stoks_sents",
            "Mknownw_sents","Sknownw_sents",
            "Mstopw_sents","Sstopw_sents",
            "Mpuncts_sents","Spuncts_sents",)
    sms_=[[sms[j][i] for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=(r"$sents$",r"$sents_{\%}$",
            r"$\mu_S(chars)$", r"$\sigma_S(chars)$",
            r"$\mu_S(tokens)$",r"$\sigma_S(tokens)$",
            r"$\mu_S(knownw)$",r"$\sigma_S(knownw)$",
            r"$\mu_S(stopw)$", r"$\sigma_S(stopw)$",
            r"$\mu_S(puncts)$",r"$\sigma_S(puncts)$",
            )
    caption=r"""Sentences sizes in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs)."""
    #data=list(map(list, zip(*tms_)))
    data=sms_
    nsents=data[0]
    nsents_=perc_(nsents)
    data=n.array(data[1:])
    data=n.vstack((nsents,nsents_,data))
    fname_=mkName(table_dir,fname,tag)
    g.lTable(labels,labelsh,data,caption,fname_,"textGeral")
    ME(fname_[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(fname_[:-4]+"_",[1],[1],[2,4,6,8,10,12])

def makeTokenSizesTable(medidasTokens__instance, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="tokenSizesInline.tex",tag=None):
    """Tabela de medidas de tamanhos de tokens TTM"""
    tms=medidasTokens__instance
    mvars=("Mtoken","Stoken","Mknownw","Sknownw",
            "Mknownw_diff","Sknownw_diff",
            "Mstopw","Sstopw")
    tms_=[[tms[j][i] for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=( r"$\mu(\overline{tokens})$",r"$\sigma(\overline{tokens})$",
            r"$\mu(\overline{knownw})$",r"$\sigma(\overline{knownw})$",
            r"$\mu(\overline{knownw \neq})$",r"$\sigma(\overline{knownw \neq})$",
            r"$\mu(\overline{stopw})$",r"$\sigma(\overline{stopw})$")
    caption=r"""Token sizes in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs)."""
    data=tms_
    fname_=mkName(table_dir,fname,tag)
    g.lTable(labels,labelsh,data,caption,fname_,"textGeral_")
    ME(fname_[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(fname_[:-4]+"_",[1],[1],[2,4,6,8])
def makeTokensTable(medidasTokens__instance, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="tokensInline.tex",tag=None):
    """Tabela de medidas de tokens TTM"""
    tms=medidasTokens__instance
    mvars=("tokens",
            "tokens_diff",
            "knownw",
            "knownw_diff",
            "stopw",
            "punct",
            "contract")
    tms_=[[tms[j][i] for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=(r"$tokens$",
            r"$tokens_{\%}$",
            r"$tokens \neq$",
            r"$\frac{knownw}{tokens}$",
            r"$\frac{knownw \neq}{knownw}$",
            r"$\frac{stopw}{knownw}$",
            r"$\frac{punct}{tokens}$",
            r"$\frac{contrac}{tokens}$",
            )
    caption=r"""tokens in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, 
    {{\bf h.}} for hubs)."""
    data=tms_
    ntoks=data[0]
    ntoks_=perc_(ntoks)
    data=n.array(data[1:])
    data=n.vstack((ntoks,ntoks_,data*100))
    fname_=mkName(table_dir,fname,tag)
    g.lTable(labels,labelsh,data,caption,fname_,"textGeral")
    ME(fname_[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(fname_[:-4]+"_",[1],[1],[2,3,5,7,8])

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

def makeKSTables(dists,table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fnames=None,tags=None,tag=None):
    """Make ks tables with the cstatistics TTM"""
    ldists=[]
    for dists_meas in dists:
        l=[]
        for sect1_meas in dists_meas:
            calphas=[]
            dnns=[]
            for sect2_val in sect1_meas:
               calpha,dnn=sect2_val 
               calphas+=[calpha]
               dnns+=[dnn]
            l+=[calphas,dnns]
        ldists.append(l) # new table
    dists=ldists 
    labels=labelsh[1:]
    labels_=[(l,"") for l in labels]
    labels__=[i for j in labels_ for i in j]
    caption="KS distances on {}."
    count=0
    if not fnames:
        fnames=[str(i) for i in range(len(dists))]
    if not tags:
        tags=[str(i) for i in range(len(dists))]
    for meas,fname,tag_ in zip(dists,fnames,tags):
        fname_=mkName(table_dir,fname+".tex",tag)
        g.lTable(labels__,labelsh,meas,caption.format(tag_),
                fname_,"ksDistances")
        ME(fname_[:-4],"\\bf",[(0,i) for i in range(1,5)]+[(i,0) for i in range(1,9)])
        DL(fname_[:-4]+"_",[1],[1],[2,4,6,8])
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

def makeCharTable(charsMeasures_instance, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="charsInline.tex",tag=None):
    """Table of characters measures TTM"""
    cms=charsMeasures_instance
    labelsh=("","g.","p.","i.","h.")
    labels=(r"$chars$",
            r"$chars_{\%}$",
            r"$\frac{spaces}{chars}$",
            r"$\frac{punct}{chars-spaces}$",
            r"$\frac{digits}{chars-spaces}$",
            r"$\frac{letters}{chars-spaces}$",
            r"$\frac{vogals}{letters}$",
            r"$\frac{uppercase}{letters}$",
            )

    caption=r"""Characters in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, 
    {{\bf h.}} for hubs)."""
    data=list(map(list, zip(*cms)))
    nchars=data[0]
    nchars_=perc_(nchars)
    data=n.array(data[1:])
    data=n.vstack((nchars,nchars_,data*100))
    fname_=mkName(table_dir,fname,tag)
    g.lTable(labels,labelsh,data,caption,fname_,"textGeral")
    ME(fname_[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(fname_[:-4]+"_",[1],[1],[2,4,5,7,8])
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

def mediaDesvio(tids=("astring","bstring"),adict={"stringkey":"tokens"}):
    """Para facilitar nas medidas de média e desvio TTM"""
    fdict={}
    for tid in tids:
        tid_=tid+"_"
        toks=[len(i) for i in adict[tid]]
        mtid=n.mean(toks)
        dtid=n.std(toks)
        fdict["m"+tid]=mtid
        fdict["d"+tid]=dtid
        if tid_ in adict.keys():
            toks_=[len(i) for i in adict[tid_]]
            mtid_=n.mean(toks_)
            dtid_= n.std(toks_)
            fdict["m"+tid_]=mtid_
            fdict["d"+tid_]=dtid_
    return fdict
def medidasTamanhosTokens(medidas_tokens):
    """Medidas dos tamanhos dos tokens TTM"""
    tvars=("kw","kwnsw","kwssnsw","kwssnsw","kwsw","sw")
    return mediaDesvio(tids,medidas_tokens)
def makeCorrelationTable_(measures_pca, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="correlationInline.tex",tag=None):
    """Make table of correlation values from PCA TTM"""
    mp=measures_pca
    cors=[i["pca"].C for i in mp]
    cors_=[]
    for secn in range(len(cors[0])):
        for cor in cors: # cor correlation measure
            cors_.append(cor[secn])
    data=cors_
    labels=mp[0]["vlabels"]
    labelsh=[""]+labels
    labels_=[(i,"","","") for i in labels]
    labels__=[i for j in labels_ for i in j]
    labels__[1:4]=["(p.)","(i.)","(h.)"]
    caption="Pierson correlation coefficient for the topological and textual measures."
    fname_=mkName(table_dir,fname,tag)
    g.lTable(labels__,labelsh,data,caption,fname_,"textCorr")
    # renderiza matriz como tabela
    #ME(table_dir+fname[:-4],"\\bf",[(0,i) for i in range(1,5)])
    nz=(n.abs(n.array(data))>.6).nonzero()
    ii=nz[0]
    jj=nz[1]
    #pts=[(i,j) for i,j in zip(ii,jj)]
    pts=[(i+1,j+1) for i,j in zip(ii,jj)]
    B.thing=nz,data,pts
    ME(fname_[:-4],"\\bf",pts)
    DL(fname_[:-4]+"_",[1],[1],[2,3,4,
                                         6,7,8,
                                         10,11,12,
                                         14,15,16,
                                         18,19,20,
                                         22,23,24,
                                         26,27,28,
                                         30,31,32,
                                         34,35,36])
def makeMessagesTable(medidasMensagens_dict, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="messagesInline.tex",tag=None):
    """Make table of messages statistics"""
    mms=medidasMensagens_dict
    mvars=("nmsgs",
            "Msents_msgs","Ssents_msgs",
            "Mtokens_msgs","Stokens_msgs",
            "Mknownw_msgs","Sknownw_msgs",
            "Mstopw_msgs","Sstopw_msgs",
            "Mpuncts_msgs","Spuncts_msgs",
            "Mchars_msgs","Schars_msgs",
            )
    mms_=[[mms[j][i] for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=(r"$msgs$",r"$msgs_{\%}$",
            r"$\mu_M(sents)$", r"$\sigma_M(sents)$",
            r"$\mu_M(tokens)$",r"$\sigma_M(tokens)$",
            r"$\mu_M(knownw)$",r"$\sigma_M(knownw)$",
            r"$\mu_M(stopw)$", r"$\sigma_M(stopw)$",
            r"$\mu_M(puncts)$",r"$\sigma_M(puncts)$",
            r"$\mu_M(chars)$", r"$\sigma_M(chars)$",
            )

    caption=r"""Messages sizes in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs)."""
    #data=list(map(list, zip(*tms_)))
    data=mms_
    nmsgs=data[0]
    nmsgs_=perc_(nmsgs)
    data=n.array(data[1:])
    data=n.vstack((nmsgs,nmsgs_,data))
    fname_=mkName(table_dir,fname,tag)
    g.lTable(labels,labelsh,data,caption,fname_,"textGeral")
    ME(fname_[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(fname_[:-4]+"_",[1],[1],[2,4,6,8,10,12,14,16])

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

def auxWnTb(tt,level,tabfname,wn_dict_list):
    """Make table of the counted wordnet synsets TTM"""
    def S(acounter):
        return sorted(acounter.items(),key=lambda x: -x[1])
    tt_=[S(i) for i in tt]
    labels=[i[0] for i in tt_[0][:12]]
    if labels:
        wms_=[[tt[i][j] for i in range(4)] for j in labels]
        labels=[i.replace("_","\_") for i in labels]
        if level=="root":
            caption=r"""Counts for the most incident synsets at the semantic roots in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs). Yes.""".format(level)
        else:
            caption=r"""Counts for the most incident synsets {} step from the semantic roots in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs).""".format(level)
        # normalizar este data com relação às colunas
        data=n.array(wms_)
        data=100*data/data.sum(axis=0)
        data=data[:12]
        data=n.vstack((data,data.sum(axis=0)))
        labels+=[r"{{\bf total}}"]
        g.lTable(labels,labelsh,data,caption,tabfname,"textGeral_")
        ME(tabfname[:-4],"\\bf",[(0,i) for i in range(1,5)])
        DL(tabfname[:-4]+"_",[1,-3],[1])
    else:
        print(tabfname.split("/")[-1], "No labels:",labels,
                "\nProbably no hypernyms:",
              len(wn_dict_list[0]["top_hypernyms"]))
def makeWordnetTable2a(wn_dict_list, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="wnInline2a.tex"):
    """Table about the most incident roots TTM"""
    t0=[c.Counter([i[0].name() for i in j["top_hypernyms"]]) for j in wn_dict_list]
    auxWnTb(t0,"root",table_dir+fname,wn_dict_list)
def makeWordnetTable2b(wn_dict_list, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="wnInline2b.tex"):
    """Table about the most incident synsets a step from root TTM"""
    t1=[c.Counter([i[1].name() for i in j["top_hypernyms"] if len(i)>1]) for j in wn_dict_list]
    #auxWnTb(labels,labelsh,data,level,tabfname)
    auxWnTb(t1,"one",table_dir+fname,wn_dict_list)
def makeWordnetTable2c(wn_dict_list, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="wnInline2c.tex"):
    """Table about the most incident synsets three steps from root TTM"""
    t2=[c.Counter([i[2].name() for i in j["top_hypernyms"] if len(i)>2]) for j in wn_dict_list]
    auxWnTb(t2,"two",table_dir+fname,wn_dict_list)
def makeWordnetTable2d(wn_dict_list, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="wnInline2d.tex"):
    """Table about the most incident synsets four steps from root TTM"""
    t3=[c.Counter([i[3].name() for i in j["top_hypernyms"] if len(i)>3]) for j in wn_dict_list]
    auxWnTb(t3,"three",table_dir+fname,wn_dict_list)
def makeWordnetPOSTable(wn_dict_list, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="wnPOSInline.tex",tag=None):
    """Make table of counted wordnet POS tags TTM"""
    wms=wn_dict_list
    labels=["N","ADJ","VERB","ADV","POS","POS!"]
    data=[[wms[i]["ftags"][j] for i in range(4)] for j in range(4)]
    data+=[[100*len(wms[i]["posok"])/len(wms[i]["WT_"]) for i in range(4)]]
    data+=[[100*(len(wms[i]["posok"])/(len(wms[i]["posok"])+len(wms[i]["posnok"]))) for i in range(4)]]
    caption=r"""Percentage of synsets with each of the POS tags used by Wordnet. The last lines give the percentage of words considered from all of the tokens (POS) and from the words with synset (POS!). The tokens not considered are punctuations, unrecognized words, words without synsets, stopwords and words for which Wordnet has no synset  tagged with POS tags . Values for each Erd\"os sectors are in the columns {{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs."""
    labelsh=("","g.","p.","i.","h.")
    fname_=mkName(table_dir,fname,tag)
    g.lTable(labels,labelsh,data,caption,fname_,"textGeral_")
    ME(fname_[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(fname_[:-4]+"_",[1,-4],[1])
def medidasWordnet2_POS(wn_measures,poss=("n","as","v","r")):
    """Make specific measures to each POS tag found TTM"""
    wn_measures2={}
    for pos in poss:
        wn_measures2[pos]=g.textUtils.medidasWordnet2_(wn_measures,pos)
    return wn_measures2
def makeWordnetTables2_POS(wn_dict_pos, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="wnPOSInline2",poss=("n","as","v","r"),tag=None):
    """Make wordnet tables of each pos tag TTM"""
    TDIR=table_dir
    for pos in poss:
        wn_measures2=wn_dict_pos[pos]
        g.textUtils.makeWordnetTable(  wn_measures2,TDIR  ,fname="{}-{}-{}tag.tex". format(fname,pos,tag)) # medias e desvios das incidencias dos atributos
        g.textUtils.makeWordnetTable2a(wn_measures2,TDIR,  fname="{}a-{}-{}tag.tex".format(fname,pos,tag)) # contagem dos synsets raiz
        g.textUtils.makeWordnetTable2b(wn_measures2,TDIR,  fname="{}b-{}-{}tag.tex".format(fname,pos,tag)) # contagem dos synsets raiz
        g.textUtils.makeWordnetTable2c(wn_measures2,TDIR,  fname="{}c-{}-{}tag.tex".format(fname,pos,tag)) # contagem dos synsets raiz
        g.textUtils.makeWordnetTable2d(wn_measures2,TDIR,  fname="{}d-{}-{}tag.tex".format(fname,pos,tag)) # contagem dos synsets raiz
    # make one file from all 20 (max) tables
    names="{}-{}_.tex","{}a-{}_.tex","{}b-{}_.tex","{}c-{}_.tex","{}d-{}_.tex"
    tx=""
    for pos in poss:
        tx+="\n\n% POS -> "+pos
        for name in names:
            name_=TDIR+name.format(fname,pos,tag)
            if os.path.isfile(name_):
                tx+="\n% fname -> "+name_+"\n"
                tx+=open(name_).read()
    g.writeTex(tx,TDIR+fname+".tex")
def makeWordnetTable(wn_dict_list, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="wnInline.tex"):
    """Make wordnet measures table TTM"""
    wms=wn_dict_list
    mvars=("mmind","dmind",
           "mmaxd","dmaxd",
           "mnhol_","dnhol_",
           "mnmer_","dnmer_",
           "mndomains","dndomains",
           "mnsimilar","dnsimilar",
           "mnverb_groups","dnverb_groups",
           "mnlemmas","dnlemmas",
           "mnentailments","dnentailments",
           "mnhypo_","dnhypo_",
           "mnhyper_","dnhyper_",
           )

    wms_=[[wms[j][i] for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=("$\mu(min\,depth)$","$\sigma(min\,depth)$",
            "$\mu(max\,depth)$",r"$\sigma(max\,depth)$",
            "$\mu(holonyms)$",    "$\sigma(holonyms)$",
            "$\mu(meronyms)$",    "$\sigma(meronyms)$",
            "$\mu(domains)$",     "$\sigma(domains)$",
            "$\mu(similar)$",     "$\sigma(similar)$",
            "$\mu(verb\,groups)$","$\sigma(verb\,groups)$",
            "$\mu(lemmas)$",      "$\sigma(lemmas)$",
            "$\mu(entailments)$", "$\sigma(entailments)$",
            "$\mu(hyponyms)$",    "$\sigma(hyponyms)$",
            "$\mu(hypernyms)$",   "$\sigma(hypernyms)$",
        )
    caption=r"""Measures of wordnet features in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs)."""
    data=wms_
    g.lTable(labels,labelsh,data,caption,table_dir+fname,"textGeral_")
    ME(table_dir+fname[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(table_dir+fname[:-4]+"_",[1],[1],[2,4,6,8,10,12,14,16,18,20,22])

def makePOSTable(posMensagens_dict, table_dir="/home/r/repos/artigoTextoNasRedes/tables/",fname="posInline.tex",tag=None):
    """Make POS tags measures table TTM"""
    pms=posMensagens_dict
    mvars=['NOUN', 'X', 'ADP', 'DET', 'VERB', 'ADJ', 'ADV', 'PRT', 'PRON', 'NUM', 'CONJ',"."]
    pms__=[[pms[j]["htags__"][i] if (i in pms[j]["htags__"].keys()) else 0 for j in range(4)] for i in mvars]
    labelsh=("","g.","p.","i.","h.")
    labels=mvars[:-1]+["PUNC"]
    caption=r"""POS tags in each Erd\"os sector ({{\bf p.}} for periphery, {{\bf i.}} for intermediary, {{\bf h.}} for hubs).
    Universal POS tags~\cite{{petrov}}:
    VERB - verbs (all tenses and modes);
    NOUN - nouns (common and proper);
    PRON - pronouns;
    ADJ - adjectives;
    ADV - adverbs;
    ADP - adpositions (prepositions and postpositions);
    CONJ - conjunctions;
    DET - determiners;
    NUM - cardinal numbers;
    PRT - particles or other function words;
    X - other: foreign words, typos, abbreviations;
    PUNCT - punctuation.
"""
    data=pms__
    fname_=mkName(table_dir,fname,tag)
    g.lTable(labels,labelsh,data,caption,fname_,"textGeral_")
    ME(fname_[:-4],"\\bf",[(0,i) for i in range(1,5)])
    DL(fname_[:-4]+"_",[1],[1],[2,4,7,9,10,11,12])
def filtro(wt_):
    """faz separação dos tokens para analise com wordnet TTM"""
    sword_sem_synset=[]
    sword_com_synset=[]
    word_com_synset=[]
    word_sem_synset=[]
    pontuacao=[]
    token_exotico=[]
    for wt in wt_:
        ss=wn.synsets(wt[0])
        if ss:
            if wt[0] in stopwords:
                sword_com_synset.append(wt)
            else:
                word_com_synset.append((wt[0],wt[1],ss))
        elif sum([tt in puncts for tt in wt[0]])==len(wt[0]):
            pontuacao.append(wt)
        elif wt[0] in stopwords:
            sword_sem_synset.append(wt)
        elif wt[0] in WL_:
            word_sem_synset.append(wt)
        else:
            token_exotico.append(wt)
    del wt,ss,wt_
    return locals()
def traduzPOS(astring):
    """Traduz as POS tags usadas para a convenção do Wordnet TTM"""
    if astring in ("NOUN","NNS","NN","NUM"):
        return wn.NOUN
    elif astring in ("VERB","VBG"):
        return wn.VERB
    elif astring in ("ADJ","JJ","ADP"):
        return wn.ADJ+wn.ADJ_SAT
    elif astring in ("ADV","RB","PRT"):
        return wn.ADV
    else:
        return "NOPOS"
        
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

def medidasPCA2_(ds,nm,authors_lists=None):
    mall=medidasPCA2(ds,nm)
    return [mall]+[medidasPCA2(ds,nm,authors) for authors in authors_lists]
def medidasPCA2(ds,nm,authors=None):
    """PCA para as medidas de cada participante TTM"""
    textosP= textosParticipante(ds,authors)
    medidasP=medidasParticipante(textosP)
    medidas_autor=g.textUtils.medidasPCA(medidasP,nm)

    vkeys=["clustering","degree","strength","Mpuncts_sents","Spuncts_sents","Mknownw_sents","Sknownw_sents","Mstopw_sents","Sstopw_sents"]
    pca=g.textUtils.tPCA(medidas_autor,vkeys)
    vlabels=[r"$cc$",r"$d$",r"$s$",r"$\mu_S(p)$",r"$\sigma_S(p)$",r"$\mu_S(kw)$",r"$\sigma_S(kw)$",r"$\mu_S(sw)$",r"$\sigma_S(sw)$"]
    mvars=("vlabels","pca","vkeys","medidas_autor","medidasP","textosP")
    vdict={}
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    return vdict
def medidasPCA(medidas_participante_dict,network_measures):
    """PCA simples para as medidas de cada participante TTM"""
    nm,mp=network_measures,medidas_participante_dict
    for author in mp:
        mp[author]["degree"]=nm.degrees[author]
        mp[author]["strength"]=nm.strengths[author]
        mp[author]["clustering"]=nm.clusterings[author]
    return mp
def textosParticipante(ds,authors=None):
    """Medidas de texto de cada participante TTM"""
    texts={}
    if not authors:
        authors=ds.author_messages
    for author in authors:
        texts[author]=""
        for msg in ds.author_messages[author]:
            msgid=msg[0]
            text=ds.messages[msgid][-1]
            texts[author]+=text
            B.LANG+=[langid.classify(text)]
    return texts
def makePCATable_(medidas_pca,table_dir,fname="pcaInline.tex",tag=None):
    """Faz tabela com as medidas do PCA TTM"""
    vecs=[i["pca"].feature_vec_.real for i in medidas_pca]
    vals=[i["pca"].eig_values_.real for i in medidas_pca]
    labelsh=[""]+["PC{}".format(i+1) for i in range(vecs[0].shape[1])]
    labels=medidas_pca[0]["vlabels"]
    labels=labels+[r"$\lambda$"]
    data=[]
    for secn in range(len(vecs[0])):
        for vec in vecs:
            data.append(vec[secn])
    caption="PCA formation"
    data=n.vstack(data+[val[:vecs[0].shape[1]] for val in vals])
    labels_=[(i,"","","") for i in labels]
    labels__=[i for j in labels_ for i in j]
    labels__[1:4]=["(p.)","(i.)","(h.)"]
    fname_=mkName(table_dir,fname,tag)
    g.lTable(labels__,labelsh,data,caption,fname_,"textPCA")
    ME(fname_[:-4],"\\bf",[(0,i) for i in range(1,6)]+[(i,0) for i in range(1,11)])
    DL(fname_[:-4]+"_",[1,-6],[1],[2,3,4,
                                         6,7,8,
                                         10,11,12,
                                         14,15,16,
                                         18,19,20,
                                         22,23,24,
                                         26,27,28,
                                         30,31,32,
                                         34,35,36,
                                         38,39,40])

from sklearn.feature_extraction.text import TfidfVectorizer
def tfIdf(texts):
    """Returns distance matrix for the texts TTM"""
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform([tt.lower() for tt in texts])
    aa=(tfidf * tfidf.T).A
    return aa
def kolmogorovSmirnovDistance(seq1,seq2,bins=300):
    """Calculate distance between histograms
    
    Adapted from the Kolmogorov-Smirnov test TTM"""
    amin=min(min(seq1),min(seq2))
    amax=max(max(seq1),max(seq2))
    bins=n.linspace(amin,amax,bins+1,endpoint=True)
    h1=n.histogram(seq1,bins,density=True)[0]
    h2=n.histogram(seq2,bins,density=True)[0]
    space=bins[1]-bins[0]
    cs1=n.cumsum(h1*space)
    cs2=n.cumsum(h2*space)

    dc=n.abs(cs1-cs2)
    Dnn=max(dc)
    n1=len(seq1)
    n2=len(seq2)
    fact=((n1+n2)/(n1*n2))**0.5
    calpha=Dnn/fact
    return calpha
def uniteTables3(TDIR,tag):
    """junta cada POS tag da wn em uma tabelona TTM"""
    tt="wnPOSInline2a","wnPOSInline2b","wnPOSInline2c","wnPOSInline2d",
    fnames=[]
    for pos in ("n","as","v","r"):
    #for pos in ("n",):
        fname=TDIR+"wnPOSInline2-{}-{}".format(pos,tag)
        fnames=[]
        for ttt in tt:
            fnames+=[TDIR+ttt+"-{}-{}tag_".format(pos,tag)]
        if os.path.isfile(fnames[1]+".tex"):
            g.tableHelpers.vstackTables_(fnames[0],fnames[1],fname)
        else:
            shutil.copyfile(fnames[0]+".tex",fname+".tex")
        if os.path.isfile(fnames[2]+".tex"):
            g.tableHelpers.vstackTables_(fname,fnames[2],fname)
        if os.path.isfile(fnames[3]+".tex"):
            g.tableHelpers.vstackTables_(fname,fnames[3],fname)
def uniteTables2(TDIR,tag):
    """vtstack tables TTM Deprecated?"""
    foo=TDIR+"posMerged{}".format(tag)
    g.tableHelpers.vstackTables_(TDIR+"posInline{}_".format(tag),
            TDIR+"wnPOSInline{}_".format(tag),foo)

def uniteTables(TDIR,tag):
    """vstack tables TTM Deprecated?"""
    t1="geral"#"geralInline0_"
    t2="chars"
    t3="tokensMerged"
    t4="sentences"
    t5="messages"
    def makeN(ss):
        if ss==t3:
            return ss+"Inline{}".format(tag)
        return ss+"Inline{}_".format(tag)
    tt=[TDIR+makeN(i) for i in (t1,t2,t3,t4,t5)]
    foo=TDIR+"mergedA{}".format(tag)
    g.tableHelpers.vstackTables(tt[0],tt[1],foo)
    g.tableHelpers.vstackTables(foo,tt[2],foo)
    g.tableHelpers.vstackTables(foo,tt[3],foo)
    g.tableHelpers.vstackTables(foo,tt[4],foo)

def makeTables_(lids,TOTAL,TDIR,FDIR,tags=None,offset=0,start_from=0,basedir="~./gmane3/"):
    """General outline of a text analysis and tables rendering TTM"""
    if not tags:
        tags=[str(i) for i in range(len(lids))]
    for lid,tag in zip(lids,tags):
        es=g.EmailStructures(lid,TOTAL,offset=offset,basedir=basedir)
        if sum([len(i)>4 for i in es.structs[-1].sectorialized_agents__])<3:
            B.degen.append(lid)
            continue
        makeTable(lid,es,TOTAL,TDIR,FDIR,tag)
def makeTable(lid,es,TOTAL,TDIR,FDIR,tag,offset=0):
    #TDIR="/home/r/repos/artigoTextoNasRedes/tables/"
    #TDIRf="/home/r/repos/artigoTextoNasRedes/figs/"
    ds=es.structs[1]
    timest=es.structs[2]
    pr=es.structs[-1]
    nm=es.structs[4]
    B.LANG=[]
    B.tag=tag

    gmeasures=g.generalMeasures(ds,pr,timest)
    g.makeGeneralTable(gmeasures,TDIR,tag=tag)

    ts,ncontractions,msg_ids=g.textUtils.makeText_(ds,pr); check("make text")
    B.LANG+=[langid.classify(ts[0])]

    char_measures=g.textUtils.medidasLetras_(ts); check("medidas letras")
    g.textUtils.makeCharTable(char_measures,TDIR,tag=tag)
    
    tok_measures=g.textUtils.medidasTokens__(ts,ncontractions); check("medidas tokens")
    g.textUtils.makeTokensTable(tok_measures,TDIR,tag=tag)
    g.textUtils.makeTokenSizesTable(tok_measures,TDIR,tag=tag)
    g.tableHelpers.vstackTables(TDIR+"tokensInline{}_".format(tag),TDIR+"tokenSizesInline{}_".format(tag),TDIR+"tokensMergedInline{}".format(tag))
    
    sent_measures=g.textUtils.medidasSentencas_(ts); check("medidas sentenças")
    g.textUtils.makeSentencesTable(sent_measures,TDIR,tag=tag)
    
    msg_measures=g.textUtils.medidasMensagens_(ds,msg_ids); check("medidas mensagens")
    g.textUtils.makeMessagesTable(msg_measures,TDIR,tag=tag)

    g.textUtils.uniteTables(TDIR,tag)
    
    pos_measures=g.textUtils.medidasPOS_([i["tokens_sentences"] for i in sent_measures]); check("medidas POS")
    g.textUtils.makePOSTable(pos_measures,TDIR,tag=tag)

    def medidasWordnet2_(list_wn_stuff,pos):
        return [medidasWordnet2(i,pos) for i in list_wn_stuff]
    def medidasWordnet_(list_words_with_pos_tags):
        return [medidasWordnet(i) for i in list_words_with_pos_tags]
    wn_measures=g.textUtils.medidasWordnet_([i["tags"] for i in pos_measures]); check("medidas wordnet")
    g.textUtils.makeWordnetPOSTable(wn_measures,TDIR ,tag=tag) # medias e desvios das incidencias dos atributos

    g.textUtils.uniteTables2(TDIR,tag)
    
    wn_measures2_pos=g.textUtils.medidasWordnet2_POS(wn_measures); check("medidas wordnet 2")
    g.textUtils.makeWordnetTables2_POS(wn_measures2_pos,TDIR,tag=tag) # escreve arquivo com todas as 5 tabelas para cada pos

    g.textUtils.uniteTables3(TDIR,tag)

    sinais=g.textUtils.medidasSinais_(ts); check("medidas sinais")
    dists=g.textUtils.ksAll(sinais,mkeys=["lens_tok","lens_word","lens_sent"]); check("ks sinais")
    g.textUtils.makeKSTables(dists,TDIR,
            fnames=("ksTokens","ksWords","ksSents"),
        =("size of tokens","size of known words","size of sentences"),tag=tag)

    sinais2=g.textUtils.medidasSinais2_(pos_measures,msg_measures); check("medidas sinais 2")
    dists2=g.textUtils.ksAll(sinais2,mkeys=["adj","sub","pun","verb","chars"]); check("ks sinais 2")
    g.textUtils.makeKSTables(dists2,TDIR,
            fnames=("ksAdjs","ksSubs","ksPuns","ksVerbs","ksChars"),
            tags=("use of adjectives on sentences","use of substantives on sentences","use of punctuations on sentences","use of verbs in each 100 tokens","use of number of characters in messages"),tag=tag)



    # correlação pierson e spearman (tem necessidade das duas?)
    medidas_pca=g.textUtils.medidasPCA2_(ds,nm,pr.sectorialized_agents__); check("medidas pca") # retorna medidas para plotar e tabelas
    g.textUtils.makeCorrelationTable_(medidas_pca,TDIR,"correlationInline.tex",tag=tag)
    g.textUtils.makePCATable_(medidas_pca,TDIR,tag=tag)
    medidas_pca[0]["pca"].plot("plot_pca-{}.png".format(tag),pr,labels="sym",tdir=FDIR)
    es.structs=es.structs[1:]
    ftags=[i["ftags"] for i in wn_measures]
    LANG=B.LANG
    mvars=("es","gmeasures","ts","ncontractions","msg_ids",
            "char_measures","tok_measures","sent_measures",
            "msg_measures","pos_measures","ftags",
            "sinais","sinais2","dists2","medidas_pca","LANG","tag")
    vdict={}; check("antes da escrita do pickle")
    for mvar in mvars:
        vdict[mvar] = locals()[mvar]
    pDump(vdict,TDIR+"vdict-{}.pickle".format(tag))
    check("escrito pickle, {}, {}".format(lid, TDIR))
    del B.tag

