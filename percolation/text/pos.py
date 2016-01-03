__doc__="text analysis with POS tags"
def analyseAll(raw_analysis):
    """Make POS tags analysis of all texts and of merged text"""
    texts_measures={"each_text":[]} #
    for each_raw_analysis in raw_analysis["texts_measures"]["each_text"]:
        texts_measures["each_text"].append({})
        texts_measures["each_text"][-1]["pos"]=
          medidasPOS(each_raw_analysis["sentences"]["sentences"])
    text_measures=medidasPOS(
            raw_analysis["text_measures"]["sentences"]["sentences"]) #
    del each_raw_analysis, raw_analysis
    return locals()

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

    tagged_sentences=brill_tagger.tag_sents(sentences_tokenized) #
    tagged_words=[item for sublist in tagged_sentences for item in sublist]
    tags=[i[1] for i in tags_ if i[0].lower() in P.text.aux.KNOWN_WORDS]
    tags_histogram=c.Counter(tags)
    tags_histogram_normalized=c.OrderedDict() #
    if htags:
       	factor=100.0/sum(htags.values())
        htags_={}
        for i in tags_histogram.keys(): tags_histogram_normalized[i]=tags_histogram[i]*factor    
        tags_histogram_normalized_ordered=c.OrderedDict(sorted(htags_.items(), key=lambda x: -x[1])) #
    del tagged_words,tags,tags_histogram,htags_,factor,i,sentences_tokenized,tags_histogram_normalized
    return locals()
