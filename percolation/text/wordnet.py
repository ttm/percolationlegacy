__doc__="text analysis with wordnet"
from nltk.corpus import wordnet as wn

def analyseAll(pos_analysis):
    """Make wordnet text analysis of all texts and of the merged text"""
    texts_measures=[]
    for each_pos_analysis in pos_analysis["texts_measures"]:
        texts_measures.append({})
        texts_measures[-1]["wordnet_context"]=\
                contextoWordnet(each_pos_analysis["tagged_sentences"])
        texts_measures[-1]["wordnet_measures"]=\
                medidasWordnetPOS(texts_measures[-1]["wordnet_context"])
    text_measures={}
    text_measures["wordnet_context"]=\
                contextoWordnet(pos_analysis["text_measures"]["tagged_sentences"])
    text_measures["wordnet_measures"]=\
                medidasWordnetPOS(text_measures["wordnet_context"])
    del pos_analysis,each_pos_analysis
    return locals()
def contextoWordnet(pos_tagged_sentences):
    """Medidas gerais sobre a aplicação da Wordnet TTM"""
    WT=pos_tagged_sentences
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

def medidasWordnetPOS(wn_measures,poss=("n","as","v","r")):
    """Make specific measures to each POS tag found TTM"""
    wn_measures={}
    for pos in poss:
        wn_measures[pos]=g.textUtils.medidasWordnet(wn_measures,pos)
    return wn_measures
def medidasWordnet(wndict,pos=None):
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

