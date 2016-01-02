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
    def updateDict(dict_keep,new_dict)
        for var in new_dict:
            if var not in dict_keep:
                dict_keep[var]=new_dict[var]
            else:
                dict_keep[var]+=new_dict[var]
    for sector in sectorialized_agents:
        signals[sector]={}
        for author in sectorialized_agents[sector]:
            for analysis in authors_analysis["raw_analysis"][author]["texts_measures"]["each_text"]:
                signals[sector]["raw_analysis"]["texts_measures"]["chars"]=updateDict(signals[sector]["raw_analysis"]["texts_measures"]["chars"],getSignals(authors_analysis["chars"]))
                signals[sector]["raw_analysis"]["texts_measures"]["tokens"]=updateDict(signals[sector]["texts_measures"]["tokens"],getSignals(authors_analysis["tokens"]))
                signals[sector]["raw_analysis"]["texts_measures"]["sentences"]=updateDict(signals[sector]["texts_measures"]["sentences"],getSignals(authors_analysis["sentences"]))

            signals[sector]["raw_analysis"]["texts_measures"]["all_texts"]=updateDict(signals[sector]["texts_measures"]["all_texts"],getSignals(authors_analysis[author]["texts_measures"]["all_texts"]))
            ########### DIV
            signals[sector]["raw_analysis"]["text_measures"]["chars"]=updateDict(signals[sector]["text_measures"]["chars"],getSignals(authors_analysis[author]["text_measures"]["chars"]))
            signals[sector]["raw_analysis"]["text_measures"]["tokens"]=updateDict(signals[sector]["text_measures"]["tokens"],getSignals(authors_analysis[author]["text_measures"]["tokens"]))
            signals[sector]["raw_analysis"]["text_measures"]["sentences"]=updateDict(signals[sector]["text_measures"]["sentences"],getSignals(authors_analysis[author]["text_measures"]["sentences"]))
            # POS
            for analysis in authors_analysis["pos_analysis"][author]["texts_measures"]:
                signals[sector]["pos_analysis"]["texts_measures"]=updateDict(signals[sector]["pos_analysis"]["texts_measures"],analysis["pos_measures"]["texts_measures"]))
            signals[sector]["pos_analysis"]["text_measures"]=updateDict(signals[sector]["pos_analysis"]["text_measures"],analysis))
            # Wordnet
            for analysis in authors_analysis["wordnet_analysis"][author]["texts_measures"]:
                signals[sector]["wordnet_analysis"]["texts_measures"]["wordnet_context"]=updateDict(signals[sector]["wordnet_analysis"]["texts_measures"]["wordnet_context"],analysis["wordnet_context"])
                signals[sector]["wordnet_analysis"]["texts_measures"]["wordnet_analysis"]=updateDict(signals[sector]["wordnet_analysis"]["texts_measures"]["wordnet_analysis"],analysis["wordnet_analysis"])
            signals[sector]["wordnet_analysis"]["text_measures"]["wordnet_context"]=updateDict(signals[sector]["wordnet_analysis"]["text_measures"]["wordnet_context"],authors_analysis["wordnet_analysis"][author]["text_measures"]["wordnet_context"])
            signals[sector]["wordnet_analysis"]["text_measures"]["wordnet_analysis"]=updateDict(signals[sector]["wordnet_analysis"]["text_measures"]["wordnet_analysis"],authors_analysis["wordnet_analysis"][author]["text_measures"]["wordnet_analysis"])
