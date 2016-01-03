__doc__="routines for selected Kolmogorov-Smirnov related statistics on text analysis"

def analyseAll(authors_analysis_dict,sectorialized_agents):
    """Return selected comparisons from overall text analysis"""
    samples_dict=collectSamplesUniform2(authors_analysis_dict,sectorialized_agents)
    ks_measures=selectedComparisonsUniform2(samples_dict)

def collectSamplesUniform2(authors_analysis_dict,sectorialized_agents):
    aa=author_analysis_dict
    numeric_samples={}
    for sector in sectorialized_agents:
        if sector not in numeric_samples.keys():
            numeric_samples[sector]={}
        for agent in sectorialized_agents[sector]:
            if agent not in numeric_samples.keys():
                numeric_samples[agent]={}
                for analysis in aa[agent]:
                    if analysis not in numeric_samples[agent]:
                        numeric_samples[agent][analysis]={}
                        numeric_samples[sector][analysis]={}
                    for data_grouping in aa[author][analysis]: # each text by author, of all text of the author and of the grouped text as one string.
                        if data_grouping not in numeric_samples[agent][analysis]:
                            numeric_samples[agent][ analysis][data_grouping]={}
                            numeric_samples[sector][analysis][data_grouping]={}
                        for data_group in aa[author][analysis][data_grouping]:
                            if data_group not in numeric_samples[agent][analysis][data_grouping]:
                                numeric_samples[agent][ analysis][data_grouping][data_group]={}
                                numeric_samples[sector][analysis][data_grouping][data_group]={}
                            for measures in aa[author][analysis][data_grouping][data_group]:
                                if data_group not in numeric_samples[agent][analysis][data_grouping][data_group]:
                                    numeric_samples[agent][ analysis][data_grouping][data_group][measures]={}
                                    numeric_samples[sector][analysis][data_grouping][data_group][measures]={}
                                for measure_name in aa[author][analysis][data_grouping][datagroup][measures]:
                                    if measure_name not in numeric_samples[agent][analysis][data_grouping][measures]:
                                        numeric_samples[agent][ analysis][data_grouping][data_group][measures][measure_name]=[]
                                        numeric_samples[sector][analysis][data_grouping][data_group][measures][measure_name]=[]
                                    measure=aa[author][analysis][data_grouping][datagroup][measures][measure_name]
                                    if isinstance(measure,numbers.Number):
                                        # usually starts with m d n frac
                                        numeric_values=[aa[author][analysis][data_grouping][datagroup][measures]]
                                    elif isinstance(measure,(list,tuple)):
                                        if isinstance(measure[0],str):
                                            numeric_values=[len(i) for i in aa[author][analysis][data_grouping][datagroup][measures]]
                                        else:
                                            raise TypeError("expected iterator to have strings as elements")
                                    else:
                                        raise TypeError("expected a number or an iterator wth string elements")
                                    if len(numeric_values)>1 and sum([numeric_values[0]==i for i in numeric_values])==len(numeric_values):
                                        c("all equal {sector} {agent} {analysis} {data_grouping} {data_group} {measures} {measure} {numeric_values}".format(**locals()))
                                    numeric_samples[agent][analysis][data_grouping][datagroup][measures][measure] +=numeric_values
                                    numeric_samples[sector][analysis][data_grouping][datagroup][measures][measure]+=numeric_values
                                        
############# OLD
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
                    for var in samples_dict[sectors[0]][analyses_type][analysis_grouping][analysis]:
                        samples_peripherals=samples_dict[sectors[0]][analyses_type][analysis_grouping][analysis]
                        samples_intermediaries=samples_dict[sectors[1]][analyses_type][analysis_grouping][analysis]
                        samples_hubs=samples_dict[sectors[2]][analyses_type][analysis_grouping][analysis]
                        ks_measures[analysis]["peripherals_intermediaries"]=P.kolmogorovSmirnovTest(samples_peripherals,samples_intermediaries)
                        ks_measures[analysis]["peripherals_hubs"]=P.kolmogorovSmirnovTest(samples_peripherals,samples_hubs)
                        ks_measures[analysis]["hubs_intermediaries"]=P.kolmogorovSmirnovTest(samples_hubs,samples_intermediaries)
            else:
                for var in samples_dict[sectors[0]][analyses_type][analysis_grouping]:
                    samples_peripherals=samples_dict[sectors[0]][analyses_type][analysis_grouping]
                    samples_intermediaries=samples_dict[sectors[1]][analyses_type][analysis_grouping]
                    samples_hubs=samples_dict[sectors[2]][analyses_type][analysis_grouping]



                samples[sector][analyses][analysis_grouping]=updateDict(samples[sector][analyses][analysis_grouping],getSamples(authors_analysis[analyses][author][analysis_grouping]))

def collectSamples(authors_analysis_dict,sectorialized_agents):
    """Return selected samples from overall text analysis"""
    def returnSignals(keep_dict,analysis_dict):
    def updateDict(dict_keep,new_dict)
        for var in new_dict:
            if var not in dict_keep:
                dict_keep[var]=new_dict[var]
            else:
                dict_keep[var]+=new_dict[var]
    samples={"raw_analysis":{"texts_measures":{}, "text_measures":{}},
                     "pos_analysis":{"texts_measures":{}, "text_measures":{}},
                     "wordnet_analysis":{"texts_measures":{}, "text_measures":{}},
                    }
    for sector in sectorialized_agents:
        for author in sectorialized_agents[sector]:
            for analyses in authors_analysis:
                for analysis_grouping in authors_analysis[analyses][author]:
                    if type(authors_analysis[analyses][author][analysis_grouping])==dict:
                        for analysis in authors_analysis[analyses][author][analysis_grouping]:
                            samples[sector][analyses][analysis_grouping][analysis]=updateDict(samples[sector][analyses][analysis_grouping][analysis],getSamples(authors_analysis[analyses][author][analysis_grouping][analysis]))
                    else:
                        samples[sector][analyses][analysis_grouping]=updateDict(samples[sector][analyses][analysis_grouping],authors_analysis[analyses][author][analysis_grouping])
            ############ OLD IMPLEMENTATION
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
