__doc__="routines for selected Kolmogorov-Smirnov related statistics on text analysis"
def analyseAll(authors_analysis_dict,sectorialized_agents):
    """Return selected comparisons from overall text analysis"""
    samples_dict=collectSamples(authors_analysis_dict,sectorialized_agents)
    ks_measures=selectedComparisons(samples_dict)

def selectedComparisons(samples_dict):
    """Return selected comparisons from samples obtained from text analysis"""
    sectors="peripherals","intermediaries","hubs"
    ks_measures={}
    for analyses_type in samples_dict[sectors[0]]:
        ks_measures[analyses_type]={}
        for analysis_grouping in samples_dict[sectors[0]][analyses_type]:
            ks_measures[analyses_type][analysis_grouping]={}
            if samples_dict[sectors[0]][analyses_type][analysis_grouping]==dict:
                ks_measures[analyses_type][analysis_grouping]={}
                for analysis in samples_dict[sectors[0]][analyses_type][analysis_grouping]:
                    samples_peripherals=samples_dict[sectors[0]][analyses_type][analysis_grouping][analysis]
                    samples_intermediaries=samples_dict[sectors[1]][analyses_type][analysis_grouping][analysis]
                    samples_hubs=samples_dict[sectors[2]][analyses_type][analysis_grouping][analysis]
                    ks_measures[analysis]["peripherals_intermediaries"]=P.kolmogorovSmirnovTest(samples_peripherals,samples_intermediaries)
                    ks_measures[analysis]["peripherals_hubs"]=P.kolmogorovSmirnovTest(samples_peripherals,samples_hubs)
                    ks_measures[analysis]["hubs_intermediaries"]=P.kolmogorovSmirnovTest(samples_hubs,samples_intermediaries)

def collectSamples(authors_analysis_dict,sectorialized_agents):
    """Return selected samples from overall text analysis"""
    def returnSignals(keep_dict,analysis_dict):
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
        samples[sector]={"raw_analysis":{"texts_measures":{}, "text_measures":{}},
                         "pos_analysis":{"texts_measures":{}, "text_measures":{}},
                         "wordnet_analysis":{"texts_measures":{}, "text_measures":{}},
                        }
        for author in sectorialized_agents[sector]:
            for analysis in authors_analysis["raw_analysis"][author]["texts_measures"]["each_text"]:
                samples[sector]["raw_analysis"]["texts_measures"]["chars"]=updateDict(samples[sector]["raw_analysis"]["texts_measures"]["chars"],getSamples(authors_analysis["chars"]))
                samples[sector]["raw_analysis"]["texts_measures"]["tokens"]=updateDict(samples[sector]["texts_measures"]["tokens"],getSamples(authors_analysis["tokens"]))
                samples[sector]["raw_analysis"]["texts_measures"]["sentences"]=updateDict(samples[sector]["texts_measures"]["sentences"],getSamples(authors_analysis["sentences"]))

            samples[sector]["raw_analysis"]["texts_measures"]["all_texts"]=updateDict(samples[sector]["texts_measures"]["all_texts"],getSamples(authors_analysis[author]["texts_measures"]["all_texts"]))
            ########### DIV
            samples[sector]["raw_analysis"]["text_measures"]["chars"]=updateDict(samples[sector]["text_measures"]["chars"],getSamples(authors_analysis[author]["text_measures"]["chars"]))
            samples[sector]["raw_analysis"]["text_measures"]["tokens"]=updateDict(samples[sector]["text_measures"]["tokens"],getSamples(authors_analysis[author]["text_measures"]["tokens"]))
            samples[sector]["raw_analysis"]["text_measures"]["sentences"]=updateDict(samples[sector]["text_measures"]["sentences"],getSamples(authors_analysis[author]["text_measures"]["sentences"]))
            # POS
            for analysis in authors_analysis["pos_analysis"][author]["texts_measures"]:
                samples[sector]["pos_analysis"]["texts_measures"]=updateDict(samples[sector]["pos_analysis"]["texts_measures"],analysis["pos_measures"]["texts_measures"]))
            samples[sector]["pos_analysis"]["text_measures"]=updateDict(samples[sector]["pos_analysis"]["text_measures"],analysis))
            # Wordnet
            for analysis in authors_analysis["wordnet_analysis"][author]["texts_measures"]:
                samples[sector]["wordnet_analysis"]["texts_measures"]["wordnet_context"]=updateDict(samples[sector]["wordnet_analysis"]["texts_measures"]["wordnet_context"],analysis["wordnet_context"])
                samples[sector]["wordnet_analysis"]["texts_measures"]["wordnet_analysis"]=updateDict(samples[sector]["wordnet_analysis"]["texts_measures"]["wordnet_analysis"],analysis["wordnet_analysis"])
            samples[sector]["wordnet_analysis"]["text_measures"]["wordnet_context"]=updateDict(samples[sector]["wordnet_analysis"]["text_measures"]["wordnet_context"],authors_analysis["wordnet_analysis"][author]["text_measures"]["wordnet_context"])
            samples[sector]["wordnet_analysis"]["text_measures"]["wordnet_analysis"]=updateDict(samples[sector]["wordnet_analysis"]["text_measures"]["wordnet_analysis"],authors_analysis["wordnet_analysis"][author]["text_measures"]["wordnet_analysis"])
    return samples
