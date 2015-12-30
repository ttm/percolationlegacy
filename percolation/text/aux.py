__doc__="auxiliary functions for text analysis routines"

def makeText_(ds,pr):
    """Get text in all sectors TTM"""
    foo=[P.utils.REPLACER.replace(i) for i in texts]
    texts_=[i[0] for i in foo]
    ncontractions=[i[1] for i in foo]
    return texts_,ncontractions, msg_ids
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

def textosParticipante(ds,authors=None):
    """Junta o texto de cada participante TTM"""
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
