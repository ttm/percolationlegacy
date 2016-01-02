__doc__="routines for selected Kolmogorov-Smirnov related statistics on text analysis"
def selectedComparisons(authors_analysis_dict,sectorialized_agents):
    """Return selected comparisons from overall text analysis"""
    def returnSignals(analysis_dict):
        keep_dict={}
        if var.startswith("m") or var.startswith("d") or var.startswith("n") or var.startswith("frac"):
            keep_dict[var]+= [analysis_dict[var]]
        else:
            keep_dict[var]+= [len(i) for i in analysis_dict[var]]
        return keep_dict


    # ao menos 2 raw, 2 pos, 2 wn
    # o sinal é medições por mensagem ou por chunck ou por autor?
    # cada autor pertence a um dos setores, então:
    # vira pegar as medidas de cada mensagem de cada autor
    # e usar de sinal.
    # É necessário receber a setorialização de Erdos junto aas análises do dicionário
    for sector in sectorialized_agents:
        signals[sector]={}
        for author in sectorialized_agents[sector]:
            signals[sector]["all_texts"]=getSignals(authors_analysis[author]["all_texts"])
            for analysis in authors_analysis[author]["texts_measures"]["each_text"]:
                signals[sector]["chars"]=getSignals(authors_analysis[author]["chars"])
                signals[sector]["tokens"]=getSignals(authors_analysis[author]["tokens"])
                signals[sector]["sentences"]=getSignals(authors_analysis[author]["sentences"])

                signals[sector]["chars"]["frac_punctuations"]+=[analysis["chars"]["frac_punctuations"]]
                signals[sector]["chars"]["frac_letter"]+=[analysis["chars"]["frac_punctuations"]]
                signals[sector]["chars"]["frac_digits"]+=[analysis["chars"]["frac_punctuations"]]
                signals[sector]["chars"]["frac_uppercase"]+=[analysis["chars"]["frac_punctuations"]]
                signals[sector]["chars"]["nchars"]+=[analysis["chars"]["nchars"]]

                signals[sector]["tokens"]["frac_punctuations"]+=[analysis["tokens"]["frac_punctuations"]]
                signals[sector]["tokens"]["frac_known_words"]+=[analysis["tokens"]["frac_known_words"]]
                signals[sector]["tokens"]["frac_stopwords"]+=[analysis["tokens"]["frac_stopwords"]]
                signals[sector]["tokens"]["lexical_diversity"]+=[analysis["tokens"]["lexical_diversity"]]
                signals[sector]["tokens"]["ntokens"]+=[analysis["tokens"]["ntokens"]]
                signals[sector]["tokens"]["ntokens_diff"]+=[analysis["tokens"]["ntokens_diff"]]

                signals[sector]["tokens"]["mknown_words"]+=[analysis["tokens"]["mknown_words"]]
                signals[sector]["tokens"]["dknown_words"]+=[analysis["tokens"]["dknown_words"]]
                signals[sector]["tokens"]["mstopwords"]+=[analysis["tokens"]["mstopwords"]]
                signals[sector]["tokens"]["dstopwords"]+=[analysis["tokens"]["dstopwords"]]

                signals[sector]["tokens"]["len_known_words"]+=[len(i) for i in analysis["tokens"]["known_words"]]
                signals[sector]["tokens"]["len_stopwords"]+=[  len(i) for i in analysis["tokens"]["stopwords"]]

                signals[sector]["sentences"]["len_sentences_chars"]+=[  len(i) for i in analysis["sentences"]["sentences"]]
                signals[sector]["sentences"]["len_sentences_tokens"]+=[  len(i) for i in analysis["sentences"]["tokens_sentences"]]
                signals[sector]["sentences"]["len_sentences_known_words_not_stopwords"]+=[  len(i) for i in analysis["sentences"]["known_words_not_stopwords_sentences"]]
                signals[sector]["sentences"]["len_sentences_stopwords"]+=[  len(i) for i in analysis["sentences"]["stopwords_sentences"]]
                signals[sector]["sentences"]["len_sentences_punctuations"]+=[  len(i) for i in analysis["sentences"]["punctuations_sentences"]]

                signals[sector]["sentences"]["mknown_words_not_stopwords"]+=[analysis["sentences"]["mknown_words_not_stopwords"]]
                signals[sector]["sentences"]["dknown_words_not_stopwords"]+=[analysis["sentences"]["dknown_words_not_stopwords"]]
                signals[sector]["sentences"]["mstopwords"]+=[analysis["sentences"]["mstopwords"]]
                signals[sector]["sentences"]["dstopwords"]+=[analysis["sentences"]["dstopwords"]]

                signals[sector]["sentences"]["nsentences"]+=[analysis["sentences"]["nsentences"]]
            for analysis in authors_analysis[author]["text_measures"]:
            # medidas gerais para cada autor no authors_analysis["texts_measures"]["messages"] e no author_analysis["text_measures"]


    raw_analyses=analysis_dict["raw_analysis"]["texts_measures"]["each_text"]
    [i["chars"] for i in raw_analyses]
    pass
