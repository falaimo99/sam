from lxml import etree
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL
from urllib.parse import urlparse
import os

# this set up globals for some useful URIs
globals = {
    "xml_id":"{http://www.w3.org/XML/1998/namespace}id",
    "base_data_URI": "https://github.com/falaimo99/sam/data/",
    "story_path": "./short_stories/Novellino_II.xml"
    }

# this function extract the tree from the well formed xml
def extract_tree(path):
    tree = etree.parse(path)
    root = tree.getroot()  
    return root

root = extract_tree(globals['story_path'])


# Namespaces used by SAM
# for testing and readability purposes
datasam = Namespace(globals['base_data_URI'])
# actual ontologies
sam = Namespace("https://purl.org/samcore#")
wdt = Namespace("https://www.wikidata.org/wiki/")
wdp = Namespace("https://www.wikidata.org/wiki/Property:")
cwrc = Namespace("https://sparql.cwrc.ca/ontologies/cwrc.html#")
rel = Namespace("https://vocab.org/relationship/#")

# Graph Instantiation
def setting_the_graph():
    g = Graph()

    g.bind("datasam", datasam)
    g.bind("sam", sam)
    g.bind("wdt", wdt)
    g.bind("wdp", wdp)
    g.bind("cwrc", cwrc)
    g.bind("rel", rel)
    
    return g

# utils dictionary that get filled as the blocks connect themselves
utils_URI = {}

# Function to set up the story element and the mandatory related items
# CharacterList and GroupOfScenes/Scenes
def set_base_story (g):
    
    story_URI = URIRef(
        globals["base_data_URI"] + root.find("Story").attrib[globals["xml_id"]]
        )
    utils_URI['story'] = story_URI
    character_list_URI = URIRef(
        story_URI + "_CharacterList"
    )
    utils_URI['CharacterList'] = character_list_URI

    if root.findall("SequenceOfScenes"):
        for SoS in root.findall("SequenceOfScenes"):
            SoS_URI = story_URI + "_" + SoS.attrib[globals["xml_id"]]
            g.add( (story_URI, wdp.P527, SoS_URI) )
    
    for scene in root.findall("Scene"):
        scene_URI = story_URI + "_" + scene.attrib[globals["xml_id"]]
        g.add( (story_URI, wdp.P527, scene_URI) )
        g.add( (scene_URI, RDF.type, sam.Scene))
        g.add( (scene_URI, RDF.type, sam.Scene))

    g.add ( (story_URI, RDF.type, sam.Story) )
    g.add ( (character_list_URI, RDF.type, sam.CharacterList) )

    return g

# This function finds all the characters add them to the CharacterList
#  and adds all the relevant information to the graph
def set_characters(g):
    character_list = root.find('CharacterList')

    for character in character_list.findall('Character'):
        character_URI = URIRef(
            utils_URI['story']+"_"+ character.attrib[globals['xml_id']]
            )
        g.add((utils_URI['CharacterList'], wdp.P527, character_URI))
        g.add((character_URI, RDF.type, wdt.Q95074))
        character_properties(character, character_URI)
        

    for character_group in character_list.findall('CharacterGroup'):
        character_group_URI = (
            utils_URI['story']+"_"+ character_group.attrib[globals['xml_id']]
        )
        g.add((utils_URI['CharacterList'], wdp.P527, character_group_URI))
        
    return g

# Ancillary function that attaches the properties to the characters
def character_properties(character, character_URI):
    # attributes analyzer. Some attributes are a shorthand for the literal part
    # of a character class

    if 'name' in character.attrib:
            character_name = URIRef(character_URI + "_name")
            g.add((character_name, RDF.type, wdt.Q82799))
            g.add((character_URI, wdp.P2561, character_name))
            g.add((
                character_name, sam.hasName, Literal(character.attrib['name']
                )))

    if 'occupation' in character.attrib:
        character_occupation = URIRef(character_URI + "_occupation")
        g.add((character_occupation, RDF.type, wdt.Q12737077))
        g.add((character_URI, wdp.P106, character_occupation))
        g.add((
            character_occupation,
            sam.hasTitle,
            Literal(character.attrib['occupation'])
            ))

    if 'descriptor' in character.attrib:
        g.add((
            character_URI,
            sam.descriptor,
            Literal(character.attrib['descriptor'])
            ))

    if 'gender' in character.attrib:
        try:
            url_parsed = urlparse(character.attrib['gender'])
            if url_parsed.netloc == "sparql.cwrc.ca":
                g.add((URIRef(character.attrib['gender']), RDF.type, URIRef("https://sparql.cwrc.ca/ontologies/cwrc.html#Gender")))
                g.add((
                    character_URI, wdp.P21, URIRef(character.attrib['gender'])
                    ))
        except:
            print(f"""{character.attrib[globals['xml_id']]
            } contains an invalid URL from sparql.cwrc.ca""")

    if 'narratorName' in character.attrib:
        g.add((
            character_URI,
            sam.narratorName,
            Literal(character.attrib['narratorName'])
            ))

    if 'partOf' in character.attrib:
        g.add((
            character_URI,
            wdp.P361,
            (utils_URI['story']+ f"_{character.attrib['partOf']}")
            ))

    # nested elements analyzer. Full reference where attributes are only used
    # when describing a data property


    for child in character.iterchildren():
        if child.tag.lower() == "trope":
            try:
                uri = URIRef(child.attrib['uri'])
                url_parsed = urlparse(uri)
                if url_parsed.netloc == "tvtropes.org":
                    trope_URI = URIRef(
                        globals['base_data_URI'] +
                        "trope_" + url_parsed.path.split("/")[-1]
                    )
                    g.add((character_URI, sam.hasTrope, trope_URI))
                    g.add((trope_URI, sam.tropeURI, uri))
            except:
                print(f"""{character.attrib[globals['xml_id']]
            } contains an invalid URI from tvtropes.org""")

        if child.tag.lower() == "relationship":
            try:
                uri = URIRef(child.attrib['uri'])
                url_parsed = urlparse(uri)
                if url_parsed.netloc == "vocab.org" and url_parsed.path == "/relationship/":
                    ref = URIRef(
            utils_URI['story']+"_"+ child.attrib['ref']
            )
                    g.add((character_URI, uri, URIRef(ref)))
            except:
                print(f"""{character.attrib[globals['xml_id']]
            } contains an invalid URI from vocab.org/relationship""")

        if child.tag.lower() == "occupation":
            try:
                character_occupation = URIRef(character_URI + "_occupation" + f"_{child.attrib['title']}")
                g.add((character_occupation, RDF.type, wdt.Q12737077))
                g.add((character_occupation, wdp.P1416, child.attrib['for']))
                g.add((character_occupation, sam.hasTitle, child.attrib['title']))
                g.add((character_URI, wdp.P106, character_occupation))
            except:
                print(f"""{character.attrib[globals['xml_id']]
            } occupation is not complete""")

        if child.tag.lower() == "name":
            try:
                character_name = URIRef(character_URI + "_name" + f"_{child.attrib['name']}")
                g.add((character_name, RDF.type, wdt.Q82799))
                g.add((character_URI, wdp.P2561, character_name))
                g.add((
                    character_name, sam.hasName, Literal(child.attrib['name']
                    )))
                g.add((
                    character_name,
                    wdp.P3938,
                    URIRef(utils_URI['story']+"_"+ child.attrib['by']
                    )))
            except:
                print(f"""{character.attrib[globals['xml_id']]
            } name is not complete""")


g = setting_the_graph()
set_base_story(g)
set_characters(g)
g.print()