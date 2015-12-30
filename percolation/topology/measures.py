__doc__="for topological measures"
def topologicalMeasures(self):
    """A detailed info about one and only graph.

    Information about date, number of friends, friendships,
    interactions, etc.
    Average degree, average clustering, etc.
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
    self.topm_dict=locals()
