import sys
keys=tuple(sys.modules.keys())
for key in keys:
    if "percolation" in key:
        print(key)
        del sys.modules[key]
import percolation as P, importlib
importlib.reload(P.tableHelpers)
importlib.reload(P.utils)
importlib.reload(P.renderLegacy)
importlib.reload(P.renderLegacy.topologicalTextualCharacterization)
importlib.reload(P.temporalStats)
c=P.utils.check
end_url="http://200.144.255.210:8082/dsfoo"
fdir="/root/repos/documentation/tables/"
ddir="/disco/data/"
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
c("preboot")
#boot=P.renderLegacy.topologicalTextualCharacterization.Bootstrap(end_url,ddir,fdir,update=False,write_tables=False)
boot=P.renderLegacy.topologicalTextualCharacterization.Bootstrap(end_url,ddir,fdir,update=True,write_tables=False,load_translates=True)
c("preanal")
#analysis=P.renderLegacy.topologicalTextualCharacterization.Analysis(boot)
#c("preanals")
analyses=P.renderLegacy.topologicalTextualCharacterization.Analyses(boot,graphids=[],tables=False,do_time=True)
##analyses=P.renderLegacy.topologicalTextualCharacterization.Analyses(boot,[],False)
#c("pretlanals")
#tl_analysis=P.renderLegacy.topologicalTextualCharacterization.TimelineAnalysis(boot)
#c("premsanals")
#ms_analysis=P.renderLegacy.topologicalTextualCharacterization.MultiscaleAnalysis(boot)
#c("finish")
