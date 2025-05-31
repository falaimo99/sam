# Import block
from lxml import etree
from rdflib import Graph, Literal, BNode, Namespace, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, OWL
from urllib.parse import urlparse
from modules.options import options

# this set up global variables for some useful URIs
globals = {
    "xml_id":"{http://www.w3.org/XML/1998/namespace}id",
    "base_data_URI": "https://github.com/falaimo99/sam/data/",
    }

# Namespace used by SAM
# for testing and readability purposes
datasam = Namespace(globals["base_data_URI"])
# actual ontologies
sam = Namespace("https://purl.org/samcore#")
wdt = Namespace("https://www.wikidata.org/wiki/")
wdp = Namespace("https://www.wikidata.org/wiki/Property:")
cwrc = Namespace("https://sparql.cwrc.ca/ontologies/cwrc.html#")
rel = Namespace("https://vocab.org/relationship/#")

# Simple extraction of the tree from the xml file
def extract_tree(path):
    tree = etree.parse(path)
    root = tree.getroot()  
    return root

# utils dictionary that get filled as the blocks connect themselves
utils_URI = {"story": "", "CharacterList": "", "referenceMaterial": ""}

# Function to set up the story element and the mandatory related items
# CharacterList and GroupOfScenes/Scenes
def extract_story(g, root):
    story = root.find("Story")
    story_URI = URIRef(globals["base_data_URI"] + story.attrib[globals["xml_id"]])
    try:
        for child in story.iterchildren():
            if child.tag.lower() == "trope":
                set_trope(g, child, story, story_URI)
    except:
        print("story has no trope or reference")
    utils_URI["story"] = story_URI

    character_list_URI = URIRef(story_URI + "_CharacterList")
    utils_URI["CharacterList"] = character_list_URI

    g.add((story_URI, wdp.P527, character_list_URI))

    if root.findall("SequenceOfScenes"):
        for SoS in root.findall("SequenceOfScenes"):
            SoS_URI = URIRef(story_URI + "_" + SoS.attrib[globals["xml_id"]])
            g.add((story_URI, wdp.P527, SoS_URI))

    for scene in root.findall("Scene"):
        scene_URI = URIRef(story_URI + f"_{scene.attrib[globals["xml_id"]]}")
        g.add((story_URI, wdp.P527, scene_URI))
        g.add((scene_URI, RDF.type, sam.Scene))
        set_scenes(g, scene, scene_URI, root)

    for setting in root.findall("Setting"):
        setting_URI = URIRef(
            utils_URI["story"] + f"_{setting.attrib[globals["xml_id"]]}"
        )
        setting_properties(g, setting, setting_URI)

    g.add((story_URI, RDF.type, sam.Story))
    g.add((character_list_URI, RDF.type, sam.CharacterList))

    set_characters(g, root)

    return g

# This function finds all the characters add them to the CharacterList
#  and adds all the relevant information to the graph
def set_characters(g, root):
    if root.find("CharacterList") != None:
        character_list = root.find("CharacterList")

        for character in character_list.findall("Character"):
            character_URI = URIRef(
                utils_URI["story"] + "_" + character.attrib[globals["xml_id"]]
            )
            g.add((utils_URI["CharacterList"], wdp.P527, character_URI))
            g.add((character_URI, RDF.type, wdt.Q95074))
            character_properties(g, character, character_URI)

        for group_of_characters in character_list.findall("CharacterGroup"):
            group_of_characters_URI = URIRef(
                utils_URI["story"] + "_" + group_of_characters.attrib[globals["xml_id"]]
            )
            if group_of_characters.tag.lower() == "organisation":
                g.add((group_of_characters_URI, RDF.type, wdt.Q43229))
            else:
                g.add((group_of_characters_URI, RDF.type, sam.GroupOfCharacters))
            g.add((utils_URI["CharacterList"], wdp.P527, group_of_characters_URI))
            character_properties(g, group_of_characters, group_of_characters_URI)

            # this part is a reiteration, it is possible to make it recursive
            # requires refactoring
            for child in group_of_characters.iterchildren():
                if child.tag.lower() == "trope":
                    set_trope(g, child, group_of_characters, group_of_characters_URI)

                if child.tag.lower() == "character":
                    character_URI = URIRef(
                        utils_URI["story"] + "_" + child.attrib[globals["xml_id"]]
                    )
                    g.add((utils_URI["CharacterList"], wdp.P527, character_URI))
                    g.add((character_URI, RDF.type, wdt.Q95074))
                    g.add((character_URI, wdp.P361, group_of_characters_URI))
                    character_properties(g, child, character_URI)
                if child.tag.lower() == "charactergroup" or "groupofcharacters":
                    if group_of_characters.tag.lower() == "organisation":
                        g.add((group_of_characters_URI, RDF.type, wdt.Q43229))
                    else:
                        g.add(
                            (group_of_characters_URI, RDF.type, sam.GroupOfCharacters)
                        )
                        g.add(
                            (
                                utils_URI["CharacterList"],
                                wdp.P527,
                                group_of_characters_URI,
                            )
                        )
                        character_properties(
                            g, group_of_characters, group_of_characters_URI
                        )
    return g


def set_trope(g, trope, scope, scope_URI):
    uri = trope.attrib["uri"]
    uri_parsed = urlparse(uri)
    if str(uri_parsed.hostname) == "tvtropes.org":
        trope_URI = URIRef(
            globals["base_data_URI"] + "trope_" + uri_parsed.path.split("/")[-1]
        )
        g.add((scope_URI, sam.hasTrope, trope_URI))
        g.add((trope_URI, sam.tropeURI, Literal(uri)))
    if "isPeriodic" in trope.attrib:
        g.add((trope_URI, RDF.type, sam.PeriodicTableTrope))
    else:
        g.add((trope_URI, RDF.type, sam.TVTropesTrope))
    
    if "participant" in trope.attrib:
        g.add((trope_URI, wdp.P710, URIRef(f"{utils_URI['story']}_{trope.attrib['participant']}")))
    try:
        for child in trope.iterchildren():
            if child.tag == "Character":
                g.add((trope_URI, wdp.P710, f"{utils_URI['story']}_{trope.attrib['ref']}"))
    except:
        print(f"{trope_URI} hasn't children")
    


#     print(
#         f"""{scope.attrib[globals['xml_id']]
# } contains an invalid URI from tvtropes.org"""
#     )


def set_scenes(g, scene, scene_URI, root):
    if options["uniqueManifestation"] == True:
        reference_material = root.find("referenceMaterial")
        excerpt_URI = URIRef(scene_URI + "_excerpt")
        g.add((excerpt_URI, RDF.type, wdt.Q1385610))
        g.add((scene_URI, sam.referenceMaterial, excerpt_URI))
        g.add((excerpt_URI, sam.excerpt_text, Literal(scene.xpath("string()").strip())))
        g.add(
            (
                scene_URI,
                sam.referenceMaterialSource,
                Literal(reference_material.attrib["uri"]),
            )
        )

    if "setting" in scene.attrib:
        try:
            setting_URI = URIRef(utils_URI["story"] + f"_{scene.attrib['setting']}")
            g.add((scene_URI, sam.hasSetting, setting_URI))
        except:
            print(f"{scene_URI} lacks setting")

    for child in scene.iterchildren():
        # child elements analyzer
        if child.tag.lower() == "participants":
            for character in child.iterchildren():
                character_URI = utils_URI["story"] + "_" + character.attrib["ref"]
                g.add((scene_URI, wdp.P710, character_URI))
                g.add((utils_URI["CharacterList"], wdp.P527, character_URI))
                # if character.tag.lower() == "charactergroup" or "groupofcharacters":
                #     g.add((character_URI, RDF.type, sam.GroupOfCharacters))
                # if character.tag.lower() == "character":
                #     g.add((character_URI, RDF.type, wdt.Q95074))
                character_properties(g, character, character_URI)

        if child.tag.lower() == ("transitionWord" or "transition"):
            transition = Literal(child.text)
            g.add((scene_URI, sam.transition, transition))

        if child.tag.lower() == "change":
            participant = child.attrib["participant"]
            change_URI = URIRef(f"{scene_URI}_{participant}_change")
            if child.text:
                g.add((change_URI, sam.changeExcerpt, Literal(child.text)))
            g.add((change_URI, RDF.type, sam.Change))
            g.add((scene_URI, sam.hasChange, change_URI))
            g.add((change_URI, wdp.P710, URIRef(f"{utils_URI["story"]}_{participant}")))
            character_properties(g, child, change_URI)

        if child.tag.lower() == "trope":
            set_trope(g, child, scene, scene_URI)

        if child.tag.lower() == "setting":
            setting_URI = URIRef(utils_URI["story"] + f"_{child.attrib['ref']}")
            g.add((scene_URI, sam.hasSetting, setting_URI))

    return g


# Ancillary function that attaches the properties to the characters
def character_properties(g, character, character_URI):
    # attributes analyzer. Some attributes are a shorthand for the literal part
    # of a character class
    if "name" in character.attrib:
        character_name = URIRef(character_URI + "_name")
        g.add((character_name, RDF.type, wdt.Q82799))
        g.add((character_URI, wdp.P2561, character_name))
        g.add((character_name, sam.hasName, Literal(character.attrib["name"])))

    if "occupation" in character.attrib:
        character_occupation = URIRef(character_URI + "_occupation")
        g.add((character_occupation, RDF.type, wdt.Q12737077))
        g.add((character_URI, wdp.P106, character_occupation))
        g.add(
            (
                character_occupation,
                sam.hasTitle,
                Literal(character.attrib["occupation"]),
            )
        )

    if "descriptor" in character.attrib:
        g.add((character_URI, sam.descriptor, Literal(character.attrib["descriptor"])))

    if "gender" in character.attrib:
        try:
            url_parsed = urlparse(character.attrib["gender"])
            if url_parsed.netloc == "sparql.cwrc.ca":
                g.add(
                    (
                        URIRef(character.attrib["gender"]),
                        RDF.type,
                        URIRef("https://sparql.cwrc.ca/ontologies/cwrc.html#Gender"),
                    )
                )
                g.add((character_URI, wdp.P21, URIRef(character.attrib["gender"])))
        except:
            print(
                f"""{character.attrib[globals['xml_id']]
            } contains an invalid URL from sparql.cwrc.ca"""
            )

    if "narratorName" in character.attrib:
        g.add(
            (character_URI, sam.narratorName, Literal(character.attrib["narratorName"]))
        )

    if "partOf" in character.attrib:
        g.add(
            (
                character_URI,
                wdp.P361,
                (utils_URI["story"] + f"_{character.attrib['partOf']}"),
            )
        )

    # nested elements analyzer. Full reference where attributes are only used
    # when describing a data property

    for child in character.iterchildren():
        if child.tag.lower() == "trope":
            set_trope(g, child, character, character_URI)

        if child.tag.lower() == "relationship":
            try:
                uri = child.attrib["uri"]
                url_parsed = urlparse(uri)
                if (
                    url_parsed.netloc == "vocab.org"
                    and url_parsed.path == "/relationship/"
                ):
                    ref = URIRef(utils_URI["story"] + "_" + child.attrib["ref"])
                    g.add((character_URI, URIRef(uri), URIRef(ref)))
            except:
                print(
                    f"""{character.attrib[globals['xml_id']]
            } contains an invalid URI from vocab.org/relationship"""
                )

        if child.tag.lower() == "occupation":
            try:
                character_occupation = URIRef(
                    character_URI + "_occupation" + f"_{child.attrib['title']}"
                )
                ref = URIRef(utils_URI["story"] + "_" + child.attrib["for"])
                g.add((character_occupation, RDF.type, wdt.Q12737077))
                g.add((character_occupation, wdp.P1416, ref))
                g.add(
                    (character_occupation, sam.hasTitle, Literal(child.attrib["title"]))
                )
                g.add((character_URI, wdp.P106, character_occupation))
            except:
                print(
                    f"""{character.attrib[globals['xml_id']]
            } occupation is not complete"""
                )

        if child.tag.lower() == "name":
            try:
                character_name = URIRef(
                    character_URI + "_name" + f"_{child.attrib['name']}"
                )
                g.add((character_name, RDF.type, wdt.Q82799))
                g.add((character_URI, wdp.P2561, character_name))
                g.add((character_name, sam.hasName, Literal(child.attrib["name"])))
                g.add(
                    (
                        character_name,
                        wdp.P3938,
                        URIRef(f"{utils_URI["story"]}_{child.attrib["by"]}"),
                    )
                )
            except:
                print(
                    f"""{character.attrib[globals['xml_id']]
            } name is not complete"""
                )


def setting_properties(g, setting, setting_URI):
    g.add((setting_URI, RDF.type, sam.Setting))

    # children elements analyzer
    for child in setting.iterchildren():
        if child.tag.lower() == "trope":
            set_trope(g, child, setting, setting_URI)
            
        if child.tag.lower() == "place":
            place_URI = URIRef(
                utils_URI["story"] + f"_{child.attrib[globals['xml_id']]}"
            )
            g.add((setting_URI, sam.hasPlace, place_URI))
            g.add((place_URI, RDF.type, wdt.Q17334923))
            if child.text:
                g.add((place_URI, sam.placeDescriptor, Literal(child.text)))
            if "uri" in child.attrib:
                g.add((place_URI, wdp.P625, URIRef(child.attrib["uri"])))

        if child.tag == "diegeticTime":
            diegeticTime_URI = URIRef(f"{setting_URI}_time")
            g.add((setting_URI, sam.diegeticTime, diegeticTime_URI))
            g.add((diegeticTime_URI, RDF.type, wdt.Q12322185))
            if "date" in child.attrib:
                g.add(
                    (
                        diegeticTime_URI,
                        sam.date,
                        Literal(child.attrib["date"]),
                        datatype == XSD.dateTime,
                    )
                )
            if "stringDate" in child.attrib:
                g.add(
                    (
                        diegeticTime_URI,
                        sam.stringDate,
                        Literal(child.attrib["stringDate"]),
                    )
                )