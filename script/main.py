import os
import modules.graph
import modules.functions
from modules.options import options

if __name__ == "__main__":
    g = modules.graph.setting_the_graph()
    for document in os.listdir(options['xml_path']):
        full_path = os.path.join(options['xml_path'], document)
        root = modules.functions.extract_tree(os.path.join(options['xml_path'], document))
        modules.functions.extract_story(g, root)

    v = g.serialize()
    with open("./dataset.ttl", "w") as f:
        f.write(v)