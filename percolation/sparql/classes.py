from functions import *

class SparQL(SparQLEndpoint,SparQLQueries):
    """Class that holds sparql endpoint connection and convenienves for query"""
    def __init__(self,endpoint_url):
        SparQLEndpoint.__init__(self,endpoint_url)
class SparQLLegacy(SparQLEndpoint,SparQLQueries,SparQLLegacy):
    """Class that holds sparql endpoint connection and convenienves for query and renderind analysis strictures, tables and figures"""
    def __init__(self,endpoint_url):
        SparQLEndpoint.__init__(self,endpoint_url)


class SparQLEndpoint:
    """Fuseki connection maintainer through rdflib"""
    def __init__(self,endpoint_url):
        pass
class SparQLQueries:
    """Covenience class for inheritance with SparQLEndpoint and SparQLLegacy"""
    pass
class SparQLLegacyConvenience:
    """Convenience class for query and renderind analysis strictures, tables and figures"""
    pass
