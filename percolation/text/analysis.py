__doc__="functions for analysis of text by isolated functionalities \
        or analysis and rendering roadmaps"

def analyseAll(authors_texts,sectorialized_agents):
    """Overall text analysis routine, uses all resources

    Uses: P.text.aux.textFromAuthors()
          P.text.aux.textFromSectors()
    Used by: P.renderLegacy.topologicalTextualCharacterization.Analysis()
    """
    authors_texts=P.text.aux.textFromAuthors(authors_texts,self.topm_dict["sectorialized_agents"])
    sectors_texts=P.text.aux.textFromSectors(authors_text,sectorialized_agents)
    authors_analysis={}
    # análise de cada mensagem e de cada autor
    for author in authors_texts:
        authors_analysis[author]={}
        texts=authors_texts[author]
        authors_analysis[author]["raw_metrics"]=P.text.raw.analyseAll(texts)
        authors_analysis[author]["pos_metrics"]=     P.text.pos.analyseAll(authors_analysis[author]["raw_analysis"])
        authors_analysis[author][ "wordnet_metrics" ]=P.text.wordnet.analyseAll(authors_analysis[author]["pos_analysis"])
        authors_analysis[author]["aux_metrics"]=P.text.tfIdf.tfIdf(texts)
    # análise de cada setor e da estrutura toda
    authors_analysis["ks_analysis"]=P.text.ks.analyseAll(authors_analysis,sectorialized_agents)
    sectors_analysis={}
    texts=[sectors_texts[i] for i in ("peripherals","intermediaries","hubs")]
    sectors_analysis["raw_analysis"]=P.text.raw.analyseAll(texts)
    sectors_analysis["pos_analysis"]=     P.text.pos.analyseAll(sectors_analysis["raw_analysis"])
    sectors_analysis[ "wordnet_analysis" ]=P.text.wordnet.analyseAll(sectors_analysis["pos_analysis"])
    sectors_analysis["aux_analysis"]=P.text.tfIdf.tfIdf(texts)
    del authors_texts,texts,erdos_sectorialization,author
    return locals()





