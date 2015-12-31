__doc__="analysis of chars, tokens, sentences and messages"
def analyseAll(texts_list):
    """Make raw text analysis of all texts and of the merged text"""
    # medidas por mensagem
    texts_measures=[]
    for text in texts_list:
        texts_measures.append({})
        texts_measures[-1]["chars"]=medidasChars(text)
        texts_measures[-1]["tokens"]=medidasTokens(string_text)
        texts_measures[-1]["sentences"]=medidasSentences(string_text)
        texts_measures[-1]["messages"]=medidasMessages(string_text)
    # medidas da lista toda
    text_measures={}
    text_measures["chars"]=medidasChars(text)
    text_measures["tokens"]=medidasTokens(string_text)
    text_measures["sentences"]=medidasSentences(string_text)
    text_measures["messages"]=medidasMessages(string_text)
    del text,texts_list
    return locals()
def medidasChars(T):
    """Medidas de letras TTM formatar para passagem como dicionário"""
    nchars=len(T)
    nspaces=T.count(" ")
    nletters=sum([t.isalpha() for t in T])
    nuppercase=sum([t.isupper() for t in T])
    nvowels=sum([t in ("a","e","i","o","u") for t in T])
    npuntuations=sum([t in puncts for t in T])
    ndigits=sum([t.isdigit() for t in T]) # numerais
    frac_espaces=nspaces/nchars
    frac_letters=nletters/(nchars-nspaces)
    frac_vowels=nvowels/nletters
    frac_uppercase=nuppercase/nletters
    frac_punctuations=npunctuations/(nchars-nspaces)
    frac_digits=ndigits/(nchars-nspaces)
    del T
    return locals()
def medidasTokens(T):
    """Medidas extensas sobre os tokens TTM"""
    atime=time.time()
    tokens=k.tokenize.wordpunct_tokenize(T)
    tokens_lowercase=[t.lower() for t in tokens]
    ntokens=len(tokens) #
    ntokens_diff=len(set(tokens)) # 
    # tokens que sao pontuacoes
    ntokens_punct=sum([sum([tt in puncts for tt in t])==len(t) for t in tokens]) #
    # known and unkown words
    known_words=[] #
    unknown_words=[] #
    punctuation_tokens=[]
    stopwords=[]
    for t in tokens_lowercase:
        if t in WORDLIST_UNIQUE:
            known_words.append(t)
        elif sum([tt in puncts for tt in t])==len(t):
            punctuation_tokens.append(t)
        else:
            unknown_words.append(t)
        if t in STOPWORDS:
            stopwords.append(t)
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
    tvars=("kw","kwnsw","kwssnsw","kwssnsw","kwsw","sw")
    token_sizes=mediaDesvio(tvars,medidas_tokens)
    del foo,foo_,t,tokens,tokens_lowercase,tvars,T
    return locals()

def medidasMensagens(ds,tids=None):
    """Medidas das mensagens em si TTM"""
    if not tids:
        mT=[ds.messages[i][3] for i in ds.message_ids]
    else:
        mT=[ds.messages[i][3] for i in tids]
    tokens_msgs=[k.tokenize.wordpunct_tokenize(t) for t in mT] # tokens
    knownw_msgs=[[i for i in toks if (i not in stopwords) and (i in WORDLIST_UNIQUE)] for toks in tokens_msgs]
    stopw_msgs=[[i for i in toks if i in stopwords] for toks in tokens_msgs]
    puncts_msgs=[[i for i in toks if
         (len(i)==sum([(ii in puncts) for ii in i]))]
         for toks in tokens_msgs] #
    sents_msgs=[k.sent_tokenize(t) for t in mT] # tokens
    nmsgs=len(mT)
    mvars="mT","tokens_msgs","knownw_msgs","stopw_msgs","puncts_msgs","sents_msgs"
    medidas=mediaDesvio(mvars,locals())
    medidas.update({"nmsgs":nmsgs,"tokens_msgs":tokens_msgs})
    return medidas
def medidasSentencas(T):
    """Medidas das sentenças TTM"""
    TS=k.sent_tokenize(T)
    tokens_sentences=[k.tokenize.wordpunct_tokenize(i) for i in TS] ### Para os POS tags
    knownw_sentences=[[i for i in ts if (i not in stopwords) and (i in WORDLIST_UNIQUE)] for ts in tokens_sentences]
    stopw_sentences =[[i for i in ts if i in stopwords] for ts in tokens_sentences]
    puncts_sentences=[[i for i in ts if
         (len(i)==sum([(ii in puncts) for ii in i]))]
         for ts in tokens_sentences] #
    mvars="TS","tokens_sentences","knownw_sentences","stopw_sentences","puncts_sentences"
    medidas=mediaDesvio(mvars,locals())
    medidas.update{"nsents":len(TS),"tokens_sentences":tokens_sentences}
    return medidas
def medidasTamanhosSentencas(T,medidas_tokens):
    """Medidas dos tamanhos das sentenças TTM"""
    TS=k.sent_tokenize(T)
    sTS=[k.tokenize.wordpunct_tokenize(i) for i in TS] ### Para os POS tags
    # numero de caracteres por sentenca
    tTS=[len(i) for i in TS]
    # tamanho das sentencas em tokens
    tsTS=[len(i) for i in sTS]
    # tamanho das sentencas em palavras conhecidas
    kw_=medidas_tokens["kw_"]
    tsTSkw=[len([ii for ii in i if ii in kw_]) for i in sTS]
    medidas=mediaDesvio(("tsTS","tTS","tsTSkw"),locals())
    medidas.update({"sTS",sTS})
    return medidas
def medidasTamanhosMensagens(mT, tids=None):
    tmT=[len(t) for t in mT] # chars
    ttmT=[len(k.tokenize.wordpunct_tokenize(t)) for t in mT] # tokens
    tsmT=[len(k.sent_tokenize(t)) for t in mT] # sentences
    return mediaDesvio(("tmT""ttmT""tsmT"),locals())


