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
            for analysis in authors_analysis[author]["texts_measures"]["each_text"]:
                signals[sector]["texts_measures"]["chars"]=updateDict(signals[sector]["texts_measures"]["chars"],getSignals(authors_analysis[author]["chars"]))
                signals[sector]["texts_measures"]["tokens"]=updateDict(signals[sector]["texts_measures"]["tokens"],getSignals(authors_analysis[author]["tokens"]))
                signals[sector]["texts_measures"]["sentences"]=updateDict(signals[sector]["texts_measures"]["sentences"],getSignals(authors_analysis[author]["sentences"]))
            signals[sector]["texts_measures"]["all_texts"]=updateDict(signals[sector]["texts_measures"]["all_texts"],getSignals(authors_analysis[author]["texts_measures"]["all_texts"]))
            ########### DIV
            signals[sector]["text_measures"]["chars"]=updateDict(signals[sector]["text_measures"]["chars"],getSignals(authors_analysis[author]["text_measures"]["chars"]))
            signals[sector]["text_measures"]["tokens"]=updateDict(signals[sector]["text_measures"]["tokens"],getSignals(authors_analysis[author]["text_measures"]["tokens"]))
            signals[sector]["text_measures"]["sentences"]=updateDict(signals[sector]["text_measures"]["sentences"],getSignals(authors_analysis[author]["text_measures"]["sentences"]))
            # POS
            # Wordnet





