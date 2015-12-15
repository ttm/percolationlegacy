import percolation as P, importlib
importlib.reload(P.renderLegacy)
importlib.reload(P.renderLegacy.topologicalTextualCharacterization)
end_url="http://200.144.255.210:8082/dsfoo"
fdir="./tables/"
P.renderLegacy.topologicalTextualCharacterization.rdfUnitsTable(end_url,fdir)
