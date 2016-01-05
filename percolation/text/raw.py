__doc__="analysis of chars, tokens, sentences and messages"

def analyseAll(texts_list):
    """Make raw text analysis of all texts and of the merged text"""
    # medidas por mensagem
    texts_measures={"each_text":[]}
    for text in texts_list:
        texts_measures["each_text"].append({})
        texts_measures["each_text"][-1]["chars"]=medidasChars(text)
        texts_measures["each_text"][-1]["tokens"]=medidasTokens(text)
        texts_measures["each_text"][-1]["sentences"]=medidasSentencasParagrafos(text,texts_measures[-1]["tokens"]["known_words_unique"])
    del text
    texts_measures["texts_overall"]=[medidasMensagens2(texts_measures)]
    return locals()

def medidasMensagens2(texts_measures):
    #measure_types=("chars","tokens","sentences")
    ## tirar medias e desvios das medidas,
    # ou dos tamanhos dos seus componentes
    # parece ser a única coisa a fazer
    all_texts_measures={}
    for data_group in texts_measures: # each_text
        for metric_group in data_group: # chars, tokens, sents
            for measure_type in metric_group[metric_group]: # numeric or list/tuple of strings
                for measure_name in metric_group[metric_group][measure_type]: # nchars, frac_x, known_words, etc
                    if measure_type=="numeric":
                        measure=[data_group[metric_group][measure_type][measure_name]]
                    elif measure_type=="lengths":
                        measure=data_group[metric_group][measure_type][measure_name]]

                    all_texts_measures[metric_group][measure_type][measure_name]+=measure
    texts_overall={}
    for metric_group in all_texts_measures: # chars, tokens, sents
        texts_overall[metric_group]={}
        for measure_type in all_texts_measures[metric_group]: # numeric or list/tuple of strings
            texts_overall[metric_group][measure_type]={}
            for measure_name in all_texts_measures[metric_group][measure_type]: # nchars, frac_x, known_words, etc
                vals=all_texts_measures[metric_group][measure_type][measure_name]
                mean_name="M{}".format(measure_name)
                std_name="M{}".format(measure_name)
                texts_overall[metric_group][measure_type][mean_name]=n.mean(vals)
                texts_overall[metric_group][measure_type][std_name]=n.std(vals)
    return all_texts_measures, texts_overall

def medidasChars(T):
    """Medidas de letras TTM formatar para passagem como dicionário"""
    nchars=len(T) #
    nspaces=T.count(" ")
    nletters=sum([t.isalpha() for t in T])
    nuppercase=sum([t.isupper() for t in T])
    nvowels=sum([t in ("a","e","i","o","u") for t in T])
    npunctuations=sum([t in puncts for t in T])
    ndigits=sum([t.isdigit() for t in T]) # numerais
    frac_spaces=nspaces/nchars #
    frac_letters=nletters/(nchars-nspaces) #
    frac_vowels=nvowels/nletters #
    frac_uppercase=nuppercase/nletters #
    frac_punctuations=npunctuations/(nchars-nspaces) #
    frac_digits=ndigits/(nchars-nspaces) #
    del T,nspaces,nletters,nuppercase,nvowels,npunctuations,ndigits
    measures={"numeric":locals()}
    return measures

def medidasTokens(T):
    """Medidas extensas sobre os tokens TTM"""
    atime=time.time()
    T=T.lower()
    tokens=k.tokenize.wordpunct_tokenize(T); del T
    tokens=[t.lower() for t in tokens]
    # known and unkown words
    known_words=[] #
    unknown_words=[] #
    punctuation_tokens=[]
    stopwords=[] #
    for t in tokens:
        if t in WORDLIST_UNIQUE:
            known_words.append(t)
        elif sum([tt in puncts for tt in t])==len(t):
            punctuation_tokens.append(t)
        else:
            unknown_words.append(t)
        if t in STOPWORDS:
            stopwords.append(t)
    del t
    stopwords_unique=set(stopwords)
    known_words_unique=set(known_words)
    unknown_words_unique=set(uknown_words)
    known_words_has_wnsynset=[i for i in known_words if wn.synsets(i)]
    known_words_has_wnsynset_unique=set(known_words_has_wnsynset)
    known_words_no_wnsynset=[i for i in known_words if i not in known_words_has_wnsynset_unique]
    known_words_no_wnsynset_unique=set(known_words_without_wnsynset)
    known_words_stopwords=[i for i in known_words if i in stopwords_unique]
    known_words_stopwords_unique=set(known_words_stopwords)
    known_words_not_stopwords=[i for i in known_words if i not in stopwords_unique]
    known_words_not_stopwords_unique=set(known_words_not_stopwords)
    unknown_words_stopwords=[i for i in unknown_words if i in stopwords_unique]
    known_words_stopwords_has_wnsynset=[i for i in kwss if i in stopwords_unique]
    # known words that dont return synsets and are stopwords
    known_words_stopwords_no_wnsynset=[i for i in kwnss if i in stopwords_unique]; c("MT6:")
    # words that are known, are not stopwords and do not return synset
    foo_=known_words_no_synset_unique.difference(stopwords_unique)
    known_words_not_stopword_no_synset=[i for i in kw if i in foo_]; c("MT7:")
    # known words with synset that are not stopwords
    foo_=known_words_has_wnsynset_unique.difference(stopwords_unique) 
    known_words_not_stopword_has_synset=[i for i in kw if i in foo_] #
    known_words_not_stopword_has_synset_unique=set(known_words_not_stopword_has_synset)
    del foo_
    measures=P.text.aux.mediaDesvio2(locals())
    measures["numeric"].update(tokensFracs(measures["strings"]}))
    return measures

def tokensFracs(strings):
    ntokens=len(strings["tokens"])
    frac_punctuations=len(strings["punctuations"])/len(strings["tokens"])
    frac_known_words =len(strings["known_words"])/len( strings["tokens"])
    frac_stopwords   =len(strings["stopwords"])/len(   strings["known_words"])
    lexical_diversity=len(strings["known_words"])/len( strings["known_words_unique"])
    token_diversity=  len(strings["tokens_unique"])/ntokens
    del strings
    return locals()

def medidasSentencasParagrafos(T,known_words_unique):
    """Medidas das sentenças TTM"""
    paragraphs=[i.strip() for i in T.split("\n")]
    nparagraphs_empty=len([i for i in paragraphs if not i])
    paragraphs=[i for i in paragraphs if i]

    sentences_paragraphs=[k.sent_tokenize(j) for j in paragraphs]
    tokens_paragraphs=[k.tokenize.wordpunct_tokenize(j) for j in paragraphs] ### Para os POS tags
    known_words_paragraphs=[[ii for ii in i if ii in known_words_unique] for i in tokens_paragraphs]
    known_words_not_stopwords_paragraphs=[[i for i in ts if (i not in STOPWORDS) and (i in WORDLIST_UNIQUE)] for ts in tokens_paragraphs]
    stopwords_paragraphs=[[i for i in ts if i in STOPWORDS] for ts in tokens_paragraphs]
    punctuations_paragraphs=[[i for i in ts if
         (len(i)==sum([(ii in puncts) for ii in i]))]
         for ts in tokens_paragraphs] #
    sentences=k.sent_tokenize(T); del T
    nsentences_empty=len([i for i in sentences if not i])
    sentences=[i for i in sentences if i]
    tokens_sentences=[k.tokenize.wordpunct_tokenize(i) for i in sentences] ### Para os POS tags
    known_words_sentences=[[ii for ii in i if ii in known_words_unique] for i in tokens_sentences]
    known_words_not_stopwords_sentences=[[i for i in ts if (i not in STOPWORDS) and (i in WORDLIST_UNIQUE)] for ts in tokens_sentences]
    stopwords_sentences =[[i for i in ts if i in STOPWORDS] for ts in tokens_sentences]
    punctuations_sentences=[[i for i in ts if
         (len(i)==sum([(ii in puncts) for ii in i]))]
         for ts in tokens_sentences] #

    measures=P.text.aux.mediaDesvio2(locals())
    measures["numeric"].update(sentenceFracs(measures["strings"]}))
    return measures

def sentenceFracs(strings):
    frac_sentences_paragraph=len(strings["sentences"])/len(strings["paragraphs"])
    del strings
    return locals()

def medidasMensagens(texts_list):
    """Medidas das mensagens em si"""
    tokens_messages=[k.tokenize.wordpunct_tokenize(t) for t in texts_list] # tokens
    known_words_messages=[[i for i in toks if (i not in stopwords) and (i in WORDLIST_UNIQUE)] for toks in tokens_messages]
    stopwords_messages=[[i for i in toks if i in stopwords] for toks in tokens_messages]
    punctuations_messages=[[i for i in toks if
         (len(i)==sum([(ii in puncts) for ii in i]))]
         for toks in tokens_messages] #
    sentences_msgs=[k.sent_tokenize(t) for t in texts_list] # tokens
    chars_messages=texts_list[:]
    del texts_list
    locals_=locals()
    mvars=tuple(locals_.keys())
    medidas=mediaDesvio(mvars,locals())
    medidas.update({nmessages=len(texts_list)})
    medidas.update(locals_)
    return medidas
