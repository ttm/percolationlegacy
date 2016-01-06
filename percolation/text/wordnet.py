__doc__="text analysis with wordnet"
from nltk.corpus import wordnet as wn

def analyseAll(pos_analysis):
    """Make wordnet text analysis of all texts and of the merged text"""
    #texts_measures=[]
    texts_measures={"each_text":[]}
    for each_pos_analysis in pos_analysis["texts_measures"]["each_text"]:
        texts_measures.append({})
        texts_measures[-1]["wordnet_context"]=\
                contextoWordnet(each_pos_analysis["tagged_tokens"]["the_tagged_tokens"])
        #texts_measures[-1]["wordnet_measures"]=\
        texts_measures[-1]=\
                medidasWordnetPOS(texts_measures[-1]["wordnet_context"])
    del each_pos_analysis
    texts_measures["texts_overall"]=[medidasMensagens2(texts_measures)]
    #text_measures={}
    #text_measures["wordnet_context"]=\
    #            contextoWordnet(pos_analysis["text_measures"]["tagged_sentences"])
    #text_measures["wordnet_measures"]=\
    #            medidasWordnetPOS(text_measures["wordnet_context"])
    #del pos_analysis,each_pos_analysis
    return locals()

def contextoWordnet(pos_tagged_tokens):
    """Medidas gerais sobre a aplicação da Wordnet TTM"""
    pos_tagged_tokens_lowercase=[(i[0].lower(),i[1]) for i in pos_tagged_tokens] #
    tokens_lists=P.text.aux.filtro(pos_tagged_tokens_lowercase) #
    tokens_pos_tagger_wordnet_ok=[] #
    tokens_pos_tagger_wordnet_not_ok=[] #
    for token in tokens_lists["word_com_synset"]:
        synset=token[2]
        wordnet_pos_tag=[i.pos() for i in synset]
        pos_tag = P.text.aux.traduzPOS(token[1])
        found_ok_wordnet_pos_tag=[(pp in pos_tag) for pp in wordnet_pos_tag]
        if sum(found_ok_wordnet_pos_tag):
            tindex=found_ok_wordnet_pos_tag.index(True)
            words_pos_tagger_wordnet_ok.append((token[0],synset[tindex]))
        else:
            tokens_pos_tagger_wordnet_not_ok.append(token)
    # estatísticas sobre words_pos_tagger_wordnet_ok
    # quais as tags?
    wordnet_pos_tags_ok=[i[1].pos() for i in words_pos_tagger_wordnet_ok]
    wordnet_pos_tags_ok_histogram_normalized=[100*wordnet_pos_tags_ok.count(i)/len(posok_) for i in ('n', 's','a', 'r', 'v')]
    wordnet_pos_tags_ok_histogram_normalized[1]+=wordnet_pos_tags_ok_histogram_normalized[2]
    wordnet_pos_tags_ok_histogram_normalized=wordnet_pos_tags_ok_histogram_normalized[0:2]+wordnet_pos_tags_ok_histogram_normalized[3:] #
    wordnet_pos_tags_ok_histogram_normalized=c.OrderedDict(sorted(wordnet_pos_tags_ok_histogram_normalized.items(), key=lambda x: -x[1])) 
    measures={"strings":{},"numeric":{}}
    measures["numeric"]=wordnet_pos_tags_ok_histogram_normalized
    measures["strings"]["tokens_pos_tagger_wordnet_ok"]=tokens_pos_tagger_wordnet_ok
    measures["strings"]["tokens_pos_tagger_wordnet_not_ok"]=tokens_pos_tagger_wordnet_not_ok
    measures["numeric"].update({"frac_pos_tagger_wordnet_ok":len(tokens_pos_tagger_wordnet_ok)/len(pos_tagged_tokens)})
    return measures

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
    hyperpaths_word=[i.hypernym_paths() for i in tagged_words_chosen]
    hyperpaths=[i for j in hyperpaths_words for i in j]
    lemmas=[i.lemmas() for i in tagged_words_chosen] ###

    tmember_holonyms  =[i.member_holonyms() for i in tagged_words_chosen]
    part_holonyms     =[i.part_holonyms() for i in tagged_words_chosen]
    substance_holonyms=[i.substance_holonyms() for i in tagged_words_chosen]
    holonyms=[i+j+l for i,j,l in zip(tmember_holonyms,part_holonyms,substance_holonyms)]


    tmember_meronyms=   [i.member_meronyms() for i in tagged_words_chosen] #
    part_meronyms=     [i.part_meronyms() for i in tagged_words_chosen]
    substance_meronyms=[i.substance_meronyms() for i in tagged_words_chosen]
    meronyms=[i+j+l for i,j,l in zip(tmember_meronyms,part_meroyms,substance_meronyms)]

    region_domains=[i.region_domains() for i in tagged_words_chosen] #
    topic_domains= [i.topic_domains()  for i in tagged_words_chosen]
    usage_domains= [i.usage_domains()  for i in tagged_words_chosen]
    domains=[i+j+l for i,j,l in zip(region_domains,topic_domains,usage_domains)]

    hypernyms=[i.hypernyms() for i in tagged_words_chosen]
    instance_hypernyms=[i.instance_hypernyms() for i in tagged_words_chosen]
    hypernyms_all=[i+j for i,j in zip(hypernyms,instance_hypernyms)]

    hyponyms=[i.hyponyms() for i in tagged_words_chosen] ###
    instance_hyponyms=[i.instance_hyponyms() for i in tagged_words_chosen]
    hyponyms_all=[i+j for i,j in zip(hyponyms,instance_hyponyms)]

    entailments=[i.entailments() for i in tagged_words_chosen]
    similar=[    i.similar_tos() for i in tagged_words_chosen]
    verb_groups=[i.verb_groups() for i in tagged_words_chosen]

    measures=P.text.aux.mediaDesvio2(locals())
    max_depth=[i.max_depth() for i in tagged_words_chosen] ###
    min_ddepth=[i.min_depth() for i in tagged_words_chosen] ###
    tdict={"tmax_depth":max_depth,"tmin_depth":min_depth}
    measures["lengths"].update(tdict)
    measures["numeric"].update(P.text.aux.mediaDesvioNumbers(tdict))
    top_hypernyms=[i[0][:4] for i in hyperpaths] # fazer histograma por camada
    lexnames=[i.lexname().split(".")[-1] for i in tagged_words_chosen] # rever
    measures["strings"]["top_hypernyms"]=top_hypernyms
    measures["strings"]["lexnames"]=lexnames

    return measures

