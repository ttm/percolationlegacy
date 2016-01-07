__doc__="auxiliary functions for text analysis routines"

this_dir, this_filename = os.path.split(__file__)
#DATA_PATH = os.path.join(this_dir, "data", "data.txt")
w=open(os.path.join(this_dir,"words.txt"),"r")
# https://raw.githubusercontent.com/dwyl/english-words/master/words.txt
w=w.read()
w=w.split()
KNOWN_WORDS=[i.lower() for i in w]
del w

labelsh=("","g.","p.","i.","h.")

def systemAnalysis(sectors_analysis):
    for sector in sectors_analysis:
        for measure_domain in sectors_analysis[sector]:
            for data_grouping in sectors_analysis[sector][measure_domain]:
                for data_group in sectors_analysis[sector][measure_domain]:
                    for measure_group in data_group:
                        for measure_type in data_group[measure_group]:
                            for measure_name in data_group[measure_group][measure_type]:
                                measure=data_group[measure_group][measure_type][measure_name]
                                if measure_type=="lengths_overall": # directly from tokens
                                    measure_type_="lengths_overall"
                                elif measure_type=="numeric_overall_low": # from messages from tokens
                                    measure_type_="numeric_overall_low_low"
                                elif measure_type=="numeric_overall": # from authors from tokens
                                    measure_type_="numeric_overall_low_high"


                                elif measure_type=="second_numeric_overall": # from authors from messages


                                elif measure_type=="numeric":
                                    measure_type_="numeric_overall"
                                elif measure_type=="second_numeric":
                                elif measure_type=="third_numeric":


def textFromAuthors(author_messages,sectorialized_agents):
    authors=set([i[0] for i in author_messages])
    authors_texts={}
    for author in authors:
        authors_texts[author]=[]
    for author,text in author_messages:
        authors_texts[author]+=[text]
    return authors_texts
def textFromSectors(authors_text,sectorialized_agents):
    sectors_texts={}
    for sector in sectorialized_agents:
        sectors_texts[sector]=[]
        for author in sectorialized_agents[sector]:
            for text in authors_text[author]:
                sectors_texts[sector]+=[text]
    return sectors_texts

def mediaDesvio2(adict={"stringkey":"strings_list"}):
    measures={"strings":adict,"numeric":{},"lengths":{}}
    keys=[key for key in adict if key[0]!="n"]
    for key in keys:
        lengths=[len(i) for i in adict[key]]
        measures["numeric"]["m"+key]=n.mean(lengths)
        measures["numeric"]["d"+key]=n.std(lengths)
        measures["lengths"][key]=lengths
    return measures

def mediaDesvio(adict={"stringkey":"strings_list"},tids=("astring","bstring")):
    """Calcula media e desvio dos tamanhos das strings"""
    if not tids:
        tids=tuple(adict.keys())
    measures_dict={}
    lengths_dict={}
    for tid in tids:
        lengths=[len(i) for i in adict[tid]]
        measures_dict["m"+tid]=n.mean(lengths)
        measures_dict["d"+tid]=n.std(lengths)
        lengths_dict["L"+tid]=lengths
    return measures_dict,lengths_dict

def mediaDesvioNumbers(adict={"stringkey":"strings_list"}):
    tdict={}
    for key in adict:
        tdict["m"+key]=n.mean(adict[key])
        tdict["d"+key]=n.tsd(adict[key])
    return tdict

def makeText_(ds,pr):
    """Get text in all sectors TTM"""
    foo=[P.utils.REPLACER.replace(i) for i in texts]
    texts_=[i[0] for i in foo]
    ncontractions=[i[1] for i in foo]
    return texts_,ncontractions, msg_ids
def filtro(pos_tagged_words_lowercase):
    """faz separação dos tokens para analise com wordnet TTM"""
    stopword_sem_synset=[]
    stopword_com_synset=[]
    word_com_synset=[]
    word_sem_synset=[]
    pontuacao=[]
    token_exotico=[]
    for pos_tagged_word in pos_tagged_words_lowercase:
        synset=wn.synsets(pos_tagged_word[0])
        if synset:
            if pos_tagged_word[0] in STOPWORDS:
                stopword_com_synset.append(pos_tagged_word)
            else:
                word_com_synset.append((pos_tagged_word[0],pos_tagged_word[1],synset))
        elif sum([tt in puncts for tt in pos_tagged_word[0]])==len(pos_tagged_word[0]):
            pontuacao.append(pos_tagged_word)
        elif pos_tagged_word[0] in STOPWORDS:
            stopword_sem_synset.append(pos_tagged_word)
        elif pos_tagged_word[0] in KNOWN_WORDS:
            word_sem_synset.append(pos_tagged_word)
        else:
            token_exotico.append(pos_tagged_word)
    del pos_tagged_word,synset,pos_tagged_words_lowercase
    return locals()
def traduzPOS(astring):
    """Traduz as POS tags usadas para a convenção do Wordnet"""
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
