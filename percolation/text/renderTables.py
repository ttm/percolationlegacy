__doc__="rendering of latex tables"

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


