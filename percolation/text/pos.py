__doc__="text analysis with POS tags"
def analyseAll(raw_analysis):
    """Make POS tags analysis of all texts and of merged text"""
    texts_measures={"each_text":[]} #
    for each_raw_analysis in raw_analysis["texts_measures"]["each_text"]:
        texts_measures["each_text"].append({})
        texts_measures["each_text"][-1]["pos"]=[medidasPOS(each_raw_analysis["sentences"]["sentences"])]
    text_measures["texts_overall"]=[medidasMensagens2(texts_measures)]
    del each_raw_analysis, raw_analysis
    return locals()

def medidasMensagens2(texts_measures):
    all_texts_measures={}
    for data_group in texts_measures: # each_text
        for metric_group in data_group: # chars, tokens, sents
            for measure_type in metric_group[metric_group]: # numeric or list/tuple of strings
                for measure_name in metric_group[metric_group][measure_type]: # nchars, frac_x, known_words, etc
                    if measure_type=="numeric":
                        measure=[data_group[metric_group][measure_type][measure_name]]
                    elif measure_type=="lengths":
                        measure=data_group[metric_group][measure_type][measure_name]
                    elif measure_type=="tagged_tokens":
                        measure=[i[1] for i in data_group[metric_group][measure_type][measure_name]]
                    else:
                        raise KeyError("unidentified measute_type")

                    all_texts_measures[metric_group][measure_type][measure_name]+=measure
    texts_overall={}
    for metric_group in all_texts_measures: # chars, tokens, sents
        texts_overall[metric_group]={}
        for measure_type in all_texts_measures[metric_group]: # numeric or list/tuple of strings
            texts_overall[metric_group][measure_type]={}
            if measure_type=="tagged_tokens":
                texts_overall[metric_group][measure_type]=pos_histogram
                tags_histogram=c.Counter(texts_overall[metric_group][measure_type]["the_tagged_tokens"])
                tags_histogram_normalized={} #
                if tags_histogram:
                    factor=100.0/sum(tags_histogram.values())
                    htags_={}
                    for i in tags_histogram.keys():
                        tags_histogram_normalized[i]=tags_histogram[i]*factor    
                    tags_histogram_normalized=c.OrderedDict(sorted(tags_histogram_normalized.items(), key=lambda x: -x[1])) 
                texts_overall[metric_group][measure_type]=tags_histogram_normalized
                continue
            for measure_name in all_texts_measures[metric_group][measure_type]: # nchars, frac_x, known_words, etc
                vals=all_texts_measures[metric_group][measure_type][measure_name]
                mean_name="M{}".format(measure_name)
                std_name="M{}".format(measure_name)
                texts_overall[metric_group][measure_type][mean_name]=n.mean(vals)
                texts_overall[metric_group][measure_type][std_name]=n.std(vals)
    return all_texts_measures, texts_overall

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

    # metric_type: tagged_sentences # metric_name: the_tagged_sentences, measure: `the tag sentences`
    tagged_sentences=brill_tagger.tag_sents(sentences_tokenized)
    tagged_tokens=[item for sublist in tagged_sentences for item in sublist] #
    tags=[i[1] for i in tagged_tokens if i[0].lower() in P.text.aux.KNOWN_WORDS]
    tags_histogram=c.Counter(tags)
    # metric_type: numeric metric_name: `the pos tag`, measure: percentage of usage

    tags_histogram_normalized={} #
    if tags_histogram:
       	factor=100.0/sum(htags.values())
        htags_={}
        for i in tags_histogram.keys():
            tags_histogram_normalized[i]=tags_histogram[i]*factor    
        tags_histogram_normalized=c.OrderedDict(sorted(tags_histogram_normalized.items(), key=lambda x: -x[1])) 

    measures={"tagged_tokens":{},"numeric":{}}
    measures["tagged_tokens"]["the_tagged_tokens"]=tagged_tokens
    measures["numeric"]=tags_histogram_normalized
    return measures




