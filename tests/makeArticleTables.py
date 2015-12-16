import percolation as P, importlib
importlib.reload(P.tableHelpers)
importlib.reload(P.renderLegacy)
importlib.reload(P.renderLegacy.topologicalTextualCharacterization)
end_url="http://200.144.255.210:8082/dsfoo"
fdir="/root/repos/documentation/tables/"
ddit="/disco/data/"
#P.renderLegacy.topologicalTextualCharacterization.rdfUnitsTable(end_url,fdir,nrows=20)
#P.renderLegacy.topologicalTextualCharacterization.rdfUnitsTable(end_url,fdir)

#general_info=P.config.boostrap(end_url,fdir)
## tudo para as estruturas totais:
#general_info=P.renderLegacy.topologicalTextualCharacterization.detailedGeneral(end_url,general_info)
#topological_info=P.renderLegacy.topologicalTextualCharacterization.topologicalMeasures(end_url,general_info)
#textual_info=P.renderLegacy.topologicalTextualCharacterization.textualMeasures(end_url,general_info, topological_info)
#temporal_info=P.renderLegacy.topologicalTextualCharacterization.temporalMeasures(end_url,general_info, topological_info)
#unitary_info=P.renderLegacy.topologicalTextualCharacterization.unitaryRoot(end_url,general_info, topological_info)
#scalefree_info=P.renderLegacy.topologicalTextualCharacterization.scaleFreeTest(end_url,general_info, topological_info)
## explore different scales
#multiscale_info=P.renderLegacy.topologicalTextualCharacterization.multiScale(end_url,general_info)

# ou 
analysis=P.renderLegacy.topologicalTextualCharacterization.Analysis(end_url,ddir,fdir)

