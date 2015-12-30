__doc__="functions for analysis of text by isolated functionalities \
        or analysis and rendering roadmaps"
from sklearn.feature_extraction.text import TfidfVectorizer
def tfIdf(texts):
    """Returns distance matrix for the texts TTM"""
    vect = TfidfVectorizer(min_df=1)
    tfidf = vect.fit_transform([tt.lower() for tt in texts])
    aa=(tfidf * tfidf.T).A
    return aa
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
    """Overall textual analysis with rendering of tables"""
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
