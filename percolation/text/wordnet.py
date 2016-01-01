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
    pos_tagged_words_lowercase=[(i[0].lower(),i[1]) for j in pos_tagged_sentences for i in j] #
    words_lists=P.text.aux.filtro(pos_tagged_words_lowercase) #
    words_pos_tagger_wordnet_ok=[] #
    words_pos_tagger_wordnet_not_ok=[] #
    for word in words_lists["word_com_synset"]s:
        synset=word[2]
        wordnet_pos_tag=[i.pos() for i in synset]
        pos_tag = P.text.aux.traduzPOS(word[1])
        found_ok_wordnet_pos_tag=[(pp in pos_tag) for pp in wordnet_pos_tag]
        if sum(found_ok_wordnet_pos_tag):
            tindex=found_ok_wordnet_pos_tag.index(True)
            words_pos_tagger_wordnet_ok.append((word[0],synset[tindex]))
        else:
            words_pos_tagger_wordnet_not_ok.append(word)
    # estatísticas sobre words_pos_tagger_wordnet_ok
    # quais as tags?
    wordnet_pos_tags_ok=[i[1].pos() for i in words_pos_tagger_wordnet_ok]
    wordnet_pos_tags_ok_histogram_normalized=[100*wordnet_pos_tags_ok.count(i)/len(posok_) for i in ('n', 's','a', 'r', 'v')]
    wordnet_pos_tags_ok_histogram_normalized[1]+=wordnet_pos_tags_ok_histogram_normalized[2]
    wordnet_pos_tags_ok_histogram_normalized=wordnet_pos_tags_ok_histogram_normalized[0:2]+wordnet_pos_tags_ok_histogram_normalized[3:] #
    del pos_tagged_sentences,word,synset,wordnet_pos_tag,pos_tag,found_ok_wordnet_pos_tag
    return locals()

def medidasWordnetPOS(wordnet_context,pos_tags=("n","as","v","r")):
    """Make specific measures to each POS tag found TTM"""
    wordnet_measures={}
    for pos_tag in pos_tags:
        wordnet_measures[pos]=g.textUtils.medidasWordnet(wordnet_context,pos_tag)
    return wordnet_measures

def medidasWordnet(wordnet_context,pos_tag=None):
    """Medidas das categorias da Wordnet sobre os verbetes TTM"""
    tagged_words=wordnet_context["words_pos_tagger_wordnet_ok"]
    if pos_tag:
        tagged_words_chosen=[i[1] for i in tagged_words if i[1].pos() in pos_tag]
    else:
        tagged_words_chosen=[i[1] for i in tagged_words]
    nlemmas=[len(i.lemmas()) for i in tagged_words_chosen] ###
    hyperpaths=[i.hypernym_paths() for i in tagged_words_chosen]
    nhyperpaths=[len(i) for i in hyperpaths]
    shyperpaths=[len(i) for j in hyperpaths for i in j]

    top_hypernyms=[i[0][:4] for i in hyperpaths] # fazer histograma por camada
    lexnames=[i.lexname().split(".")[-1] for i in tagged_words_chosen] # rever

    member_holonyms=[len(i.member_holonyms()) for i in tagged_words_chosen]
    part_holonyms=[len(i.part_holonyms()) for i in tagged_words_chosen]
    substance_holonyms=[len(i.substance_holonyms()) for i in tagged_words_chosen]
    nholonyms=[mhol[i]+phol[i]+shol[i] for i in range(len(tagged_words_chosen))] ###

    member_meronyms=[len(i.member_meronyms()) for i in tagged_words_chosen] #
    part_meronyms=[len(i.part_meronyms()) for i in tagged_words_chosen]
    substance_meronyms=[len(i.substance_meronyms()) for i in tagged_words_chosen]
    nmeronyms=[mmer[i]+pmer[i]+smer[i] for i in range(len(tagged_words_chosen))] ###

    nentailments=[len(i.entailments()) for i in tagged_words_chosen]

    nhypernyms=[len(i.hypernyms()) for i in tagged_words_chosen]
    ninstance_hypernyms=[len(i.instance_hypernyms()) for i in tagged_words_chosen]
    nhypernyms=[nhypernyms[i]+ninstance_hypernyms[i] for i in range(len(tagged_words_chosen))]

    nhyponyms=[len(i.hyponyms()) for i in tagged_words_chosen] ###
    ninstance_hyponyms=[len(i.instance_hyponyms()) for i in tagged_words_chosen]
    nhyponyms=[nhyponyms[i]+ninstance_hyponyms[i] for i in range(len(tagged_words_chosen))]

    max_depth=[i.max_depth() for i in tagged_words_chosen] ###
    min_ddepth=[i.min_depth() for i in tagged_words_chosen] ###

    nregion_domains=[len(i.region_domains()) for i in tagged_words_chosen] #
    ntopic_domains= [len(i.topic_domains())  for i in tagged_words_chosen]
    nusage_domains= [len(i.usage_domains())  for i in tagged_words_chosen]
    ndomains=[nregion_domains[i]+ntopic_domains[i]+nusage_domains[i]
            for i in range(len(tagged_words_chosen))] ###

    nsimilar=[    len(i.similar_tos()) for i in tagged_words_chosen]
    nverb_groups=[len(i.verb_groups()) for i in tagged_words_chosen]

    del wordnet_context,pos_tag,tagged_words
    locals_=locals()
    mvars_=[i for i in locals_.keys() if i not in ("tagged_words_chosen","hyperpaths","top_hypernyms","lexnames")]
    medidas=mediaDesvio(mvars,locals_)
    medidas.update(locals_)
    return medidas

