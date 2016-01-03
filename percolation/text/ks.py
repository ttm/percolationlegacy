__doc__="routines for selected Kolmogorov-Smirnov related statistics on text analysis"

def analyseAll(authors_analysis_dict,sectorialized_agents):
    """Return selected comparisons from overall text analysis"""
    samples_dict=collectSamplesUniform2(authors_analysis_dict,sectorialized_agents)
    ks_sectors_comparisons=ksSectorsComparisonsUniform2(samples_dict)

def selectedComparisonsUniform2(samples_dict):
    sector_samples_dict=samples_dict["numeric_samples_sectors"]
#    for sector in sector_samples_dict["numeric_samples_sectors"]:
    sector="peripherals"
    ks_sectors_comparisons={}
    for analysis in sector_samples_dict[sector]:
        if analysis not in ks_sectors_comparisons:
            ks_sectors_comparisons[analysis]={}
        for data_grouping in sector_samples_dict[sector][analysis]:
            if data_grouping not in ks_sectors_comparisons[analysis]:
                ks_sectors_comparisons[analysis][data_grouping]={}
            for data_group in sector_samples_dict[sector][analysis][data_grouping]:
                if data_group not in ks_sectors_comparisons[analysis][data_grouping]:
                    ks_sectors_comparisons[analysis][data_grouping][data_group]={}
                for measures_type in sector_samples_dict[sector][analysis][data_grouping][data_group]:
                    if measures_type not in ks_sectors_comparisons[analysis][data_grouping][data_group]:
                        ks_sectors_comparisons[analysis][data_grouping][data_group][measures_type]={}
                    for measure_name in sector_samples_dict[sector][analysis][data_grouping][data_group][measures_type]:
                        peripherals_values=sector_samples_dict["peripherals"][analysis][data_grouping][data_group][measure_name]
                        intermeriaries_values=sector_samples_dict["intermediaries"][analysis][data_grouping][data_group][measure_name]
                        hubs_values=sector_samples_dict["hubs"][analysis][data_grouping][data_group][measure_name]
                        foo["p_i"]=P.kolmogorovSmirnov.kolmogorovSmirnovTest(peripherals_values,intermediaries_values)
                        foo["p_h"]=P.kolmogorovSmirnov.kolmogorovSmirnovTest(peripherals_values,hubs_values)
                        foo["i_h"]=P.kolmogorovSmirnov.kolmogorovSmirnovTest(intermediaries_values,hubs_values)
                        ks_sectors_comparisons[analysis][data_grouping][data_group][measure_name]=foo
    return ks_sectors_comparisons

def collectSamplesUniform2(samples_dict):
    aa=author_analysis_dict
    numeric_samples_sectors={}
    numeric_samples_agents={}
    indistinct_measures=[]
    for sector in sectorialized_agents:
        if sector not in numeric_samples_sectors.keys():
            numeric_samples_sectors[sector]={}
        for agent in sectorialized_agents[sector]:
            if agent not in numeric_samples_agents.keys():
                numeric_samples_agents[agent]={}
            for analysis in aa[agent]:
                if analysis not in numeric_samples_agents_[agent]:
                    numeric_samples_agents[agent][analysis]={}
                    numeric_samples_sectors[sector][analysis]={}
                for data_grouping in aa[agent][analysis]: # each text by author, of all text of the author and of the grouped text as one string.
                    if data_grouping not in numeric_samples_agents[agent][analysis]:
                        numeric_samples_agents[agent][ analysis][data_grouping]={}
                        numeric_samples_sectors[sector][analysis][data_grouping]={}
                    for data_group in aa[agent][analysis][data_grouping]:
                        if data_group not in numeric_samples_agents[agent][analysis][data_grouping]:
                            numeric_samples_agents[agent][ analysis][data_grouping][data_group]={}
                            numeric_samples_sectors[sector][analysis][data_grouping][data_group]={}
                        for measures_type in aa[agent][analysis][data_grouping][data_group]:
                            if measures_type not in numeric_samples_agents[agent][analysis][data_grouping][data_group]:
                                numeric_samples_agents[agent][ analysis][data_grouping][data_group][ measures_type]={}
                                numeric_samples_sectors[sector][analysis][data_grouping][data_group][measures_type]={}
                            for measure_name in aa[agent][analysis][data_grouping][datagroup][measures_type]:
                                if measure_name not in numeric_samples_agents[agent][analysis][data_grouping][measures_type]:
                                    numeric_samples_agents[agent][ analysis][data_grouping][data_group][ measures_type][measure_name]=[]
                                    numeric_samples_sectors[sector][analysis][data_grouping][data_group][measures_type][measure_name]=[]
                                measure=aa[agent][analysis][data_grouping][datagroup][measures_type][measure_name]
                                if isinstance(measure,numbers.Number):
                                    # usually starts with m d n frac
                                    numeric_values=[measure]
                                elif isinstance(measure,(list,tuple)):
                                    if isinstance(measure[0],str):
                                        numeric_values=[len(i) for i in measure]
                                    else:
                                        raise TypeError("expected iterator to have strings as elements")
                                else:
                                    raise TypeError("expected a number or an iterator wth string elements")
                                if len(numeric_values)>1 and sum([numeric_values[0]==i for i in numeric_values])==len(numeric_values):
                                    all_equal="all equal {sector} {agent} {analysis} {data_grouping} {data_group} {measures_type} {measure_name} {numeric_values}".format(**locals())
                                    c(all_equal)
                                    indistinct_measures.append(all_equal)
                                numeric_samples_agents[agent][analysis][data_grouping][datagroup][  measures_type][measure_name] +=numeric_values
                                numeric_samples_sectors[sector][analysis][data_grouping][datagroup][measures_type][measure_name]+=numeric_values
                                        
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
