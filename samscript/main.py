from lxml import etree
from story import *
import os

options = {
    # option to accomodate the current state of the ontology
    # the manifestation will be uniquely determined in one place for all scenes
    # showcasing the possibility of adding more than one for each scene
    "uniqueManifestation": True,
}

# this function extract the tree from the well formed xml
def extract_tree(path):
    tree = etree.parse(path)
    root = tree.getroot()  
    return root


def main():
    g = story.setting_the_graph()

    for document in os.listdir("../short_stories"):
        print(document)
        root = extract_tree(document)
        set_base_story(g)
        set_characters(g)
        v = g.serialize()

    with open("dataset.ttl", "w") as f:
        f.write(v)

    return g
    
if __name__ == "main":
    main()