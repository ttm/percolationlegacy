__doc__="functions for analysis of text by isolated functionalities \
        or analysis and rendering roadmaps"

def analyseAll(authors_texts,sectorialized_agents):
    """Overall text analysis routine, uses all resources

    Uses: P.text.aux.textFromAuthors()
          P.text.aux.textFromSectors()
    Used by: P.renderLegacy.topologicalTextualCharacterization.Analysis()
    """
    authors_texts=P.text.aux.textFromAuthors(authors_texts,self.topm_dict["sectorialized_agents"])
    authors_measures={}
    # análise de cada mensagem e de cada autor
    for author in authors_texts:
        authors_measures[author]={}
        texts=authors_texts[author]
        authors_measures[author]["raw_strings"]=P.text.raw.analyseAll(texts)
        authors_measures[author]["pos"]=     P.text.pos.analyseAll(authors_analysis[author]["raw_analysis"])
        authors_measures[author][ "wordnet" ]=P.text.wordnet.analyseAll(authors_analysis[author]["pos_analysis"])
        authors_measures[author]["tfIdf"]=P.text.tfIdf.tfIdf(texts)
    # análise de cada setor e da estrutura toda
#    sectors_texts=P.text.aux.textFromSectors(authors_text,sectorialized_agents)
    sectors_analysis={}
    for sector in sectorialized_agents:
        sectors_analysis[sector]["raw_strings"]=P.text.raw.sectorsAnalyseAll(authors_analysis,sectorialized_agents[sector])
        sectors_analysis[sector]["pos"]=        P.text.pos.sectorsAnalyseAll(authors_analysis,sectorialized_agents[sector])
        sectors_analysis[sector]["wordnet"]=    P.text.wordnet.sectorsAnalyseAll(authors_analysis,sectorialized_agents[sector])
        sectors_analysis[sector]["tfIdf"]=      P.text.tfIdf.sectorsAnalyseAll(authors_analysis,sectorialized_agents[sector])

#    texts=[sectors_texts[i] for i in ("peripherals","intermediaries","hubs")]
#    sectors_analysis["raw_strings"]=P.text.raw.analyseAll(texts)
#    sectors_analysis["pos"]=     P.text.pos.analyseAll(sectors_analysis["raw_analysis"])
#    sectors_analysis[ "wordnet" ]=P.text.wordnet.analyseAll(sectors_analysis["pos_analysis"])
#    sectors_analysis["tfIdf"]=P.text.tfIdf.tfIdf(texts)

    overall_analysis["raw_strings"]=P.text.raw.systemAnalysis(sectors_analysis)) # medias de toda a rede por mensagem, por autor e por setor
    overall_analysis["pos"]=P.text.raw.systemAnalysis(sectors_analysis)) # medias de toda a rede por mensagem, por autor e por setor
    overall_analysis["wordnet"]=P.text.raw.systemAnalysis(sectors_analysis)) # medias de toda a rede por mensagem, por autor e por setor
    overall_analysis["tfIdf"]=P.text.raw.systemAnalysis(texts)) # medias de toda a rede por mensagem, por autor e por setor

    del authors_texts,sectorialized_agents,texts,author
    return locals()





