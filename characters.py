from lxml import etree
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL
from urllib.parse import urlparse
import os



# Ancillary function that attaches the properties to the characters
def character_properties(g, character, character_URI):
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