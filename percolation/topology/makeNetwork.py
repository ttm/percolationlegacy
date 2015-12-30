__doc__="rendering of network structures from proper data"
def makeNetwork(relational_data):
    if relational_data and (len(relational_data[0])==3):
        gg=x.DiGraph()
        for val in relational_data:
            gg.add_edge(val[0],val[1],weight=int(val[2]))
        gg_=P.utils.toUndirected(gg)
        comp=x.weakly_connected_component_subgraphs(gg)[0]
        comp_=x.connected_component_subgraphs(gg_)[0]
    elif relational_data:
        gg=x.Graph()
        for val in relational_data:
            gg.add_edge(val[0],val[1])
        comp=x.connected_component_subgraphs(gg)[0]
        gg_=gg
        comp_=comp
    return locals()
