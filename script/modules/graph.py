from rdflib import Graph, Namespace
from modules.functions import globals

# Namespace used by SAM
# for testing and readability purposes
datasam = Namespace(globals["base_data_URI"])
# actual ontologies
sam = Namespace("https://purl.org/samcore#")
wdt = Namespace("https://www.wikidata.org/wiki/")
wdp = Namespace("https://www.wikidata.org/wiki/Property:")
cwrc = Namespace("https://sparql.cwrc.ca/ontologies/cwrc.html#")
rel = Namespace("https://vocab.org/relationship/#")


# Graph Instantiation
def setting_the_graph():
    g = Graph()

    # Namespace used by SAM
    # for testing and readability purposes
    datasam = Namespace(globals["base_data_URI"])
    # actual ontologies
    sam = Namespace("https://purl.org/samcore#")
    wdt = Namespace("https://www.wikidata.org/wiki/")
    wdp = Namespace("https://www.wikidata.org/wiki/Property:")
    cwrc = Namespace("https://sparql.cwrc.ca/ontologies/cwrc.html#")
    rel = Namespace("https://vocab.org/relationship/#")

    g.bind("datasam", datasam)
    g.bind("sam", sam)
    g.bind("wdt", wdt)
    g.bind("wdp", wdp)
    g.bind("cwrc", cwrc)
    g.bind("rel", rel)

    return g