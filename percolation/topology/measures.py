__doc__="for topological measures"
import networkx as x

def topologicalMeasures(gg=x.Graph()):
    """A detailed info about one and only graph.

    Information about date, number of friends, friendships,
    interactions, etc.
    Average degree, average clustering, etc.

    Input: networkx Graph
    Used by: P.renderLegacy.topologicalTextualCharacterization.Analysis()
    Uses: P.topology.measures.overallMeasures()
    ToDo: implement homophily
    """
    degrees=self.gg.degree()
    degrees_=list(degrees.values())
    strengths=self.gg.degree(weight="weight")
    strengths_=list(strengths.values())
    clustering=x.clustering( self.gg_ )
    clustering_=list(clustering.values())
    clustering_w=x.clustering( self.gg_,weight="weight" )
    clustering_w_=list(clustering_w.values())
    square_clustering=x.square_clustering( self.gg)
    square_clustering_=list(square_clustering.values())
    transitivity=x.transitivity(self.gg)
    transitivity_u=x.transitivity(self.gg_)
    closeness=x.closeness_centrality(self.gg)
    closeness_=list(closeness.values())
    eccentricity=x.closeness_centrality(self.gg_)
    eccentricity_=list(eccentricity.values())
    diameter=x.diameter(self.comp_)
    radius=x.radius(    self.comp_)
    nperiphery=len(x.periphery(self.comp_))
    ncenter=   len(x.center(self.comp_)   )
    size_component=self.comp_.number_of_nodes()
    ashort_path=x.average_shortest_path_length(   self.comp)
    ashort_path_w=x.average_shortest_path_length( self.comp,weight="weight")
    ashort_path_u=x.average_shortest_path_length( self.comp_)
    ashort_path_uw=x.average_shortest_path_length(self.comp_,weight="weight")
    nnodes=self.gg.number_of_nodes()
    nedges=self.gg.number_of_edges()

    # nodes_edge =100*nnodes/nedges # correlated to degree
    # fraction of participants in the largest component
    # and strongly connected components
    frac_weakly_connected=   100*self.comp.number_of_nodes()/nnodes
    frac_connected=100*self.comp_.number_of_nodes()/nnodes
    if self.gg.is_directed():
        weights=[i[2]["weight"] for i in self.gg.edges(data=True)]
        frac_strongly_connected=   100*x.strongly_connected_component_subgraphs(self.gg)[0].number_of_nodes()/nnodes
        frac_weakly_connected2=   100*x.weakly_connected_component_subgraphs(self.gg)[0].number_of_nodes()/nnodes
        # make weakly connected
    else:
        weights=[1]*nedges
        frac_strongly_connected=  frac_connected
    overall_measures=overallMeasures(locals())
    return locals()

def _overallMeasures(topm_dict):
    """Overall measures of a network.

    Used by: P.topology.measures.topologicalMeasures()"""
    return [
            #topm_dict["nodes_edge"], correlated to degree
            topm_dict["nnodes"], 
            topm_dict["nedges"],
            topm_dict["prob"], # anotar em ocorrências por mil ou milhões etc
            topm_dict["max_degree_empirical"],
            max(   topm_dict["strengths_"]),
            max(   topm_dict["weights"]),
            n.mean(topm_dict["degrees_"]),
            n.std( topm_dict["degrees_"]),
            n.mean(topm_dict["strengths_"]),
            n.std( topm_dict["strengths_"]),
            n.mean(topm_dict["weights"]),
            n.std( topm_dict["weights"]),
            n.mean(topm_dict["clustering_"]               ),
            n.std( topm_dict["clustering_"]               ),
            n.mean(topm_dict["clustering_w_"]             ),
            n.std( topm_dict["clustering_w_"]             ),
            n.mean(topm_dict["square_clustering_"]),
            n.std( topm_dict["square_clustering_"]),
            n.mean(topm_dict["closeness_"]                ),
            n.std( topm_dict["closeness_"]                ),
            n.mean(topm_dict["eccentricity_"]             ),
            n.std( topm_dict["eccentricity_"]             ),
            n.mean(topm_dict["sectorialized_degrees__"][0]), # periphery
            n.std( topm_dict["sectorialized_degrees__"][0]), # periphery
            n.mean(topm_dict["sectorialized_degrees__"][1]), # intermediary
            n.std( topm_dict["sectorialized_degrees__"][1]), # intermediary
            n.mean(topm_dict["sectorialized_degrees__"][2]), # hubs
            n.std( topm_dict["sectorialized_degrees__"][2]), # hubs

            topm_dict["sectorialized_nagents__"][0], # periphery
            topm_dict["sectorialized_nagents__"][1], # intermediary
            topm_dict["sectorialized_nagents__"][2], # hubs
            topm_dict["transitivity"],
            topm_dict["transitivity_u"],
            topm_dict["diameter"],
            topm_dict["radius"],
            topm_dict["frac_connected"],
            topm_dict["size_component"],
            topm_dict["ashort_path"],
            topm_dict["ashort_path_u"],
            topm_dict["ashort_path_w"],
            topm_dict["ashort_path_uw"],
            topm_dict["ncenter"],
            topm_dict["nperiphery"],
            topm_dict["sectorialized_agents__"],
            topm_dict["sectorialized_degrees__"],
            topm_dict["frac_strongly_connected"],
            topm_dict["frac_weakly_connected"],
        ]
