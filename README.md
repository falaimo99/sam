# SAM

SAM (Story Abstract Metadata) is a model leveraging Semantic Web technologies to describe stories as abstract entities.

This repository represents the projectual output of my master's dissertation. It consists of a series of tools that are ready to use, and annotate data able to showcase a functioning example.

In particular the `script/` folder contains code able to transform a SAM annotated XML file into an RDF Knowledge Graph. The pieces of code responsible for this routine are `main.py` and a notebook name `xml_to_rdf.ipynb`.

The `short_stories/` folder contains the SAM XML annotated files, it will result evident that they're not using any standard XML namespace, and instead customized elements and attributes, specific to this project. The annotated stories come from the italian tradition of novella and folktale, that served as main study case for this project. Future developments involve other genres, in order to showcase more diverse SAM descriptions.

The ontology visualization is hosted on [Purl](https://purl.org/samcore), and uses [LODE](https://essepuntato.it/lode)
