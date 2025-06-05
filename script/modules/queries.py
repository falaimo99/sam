character_suggested = {
    "suggested_query1": "datasam:Novella_V_Giornata_II_Decameron_Boccaccio",
    "suggested_query2": "datasam:Petrosinella_CuntodeliCunti_Basile_orca",
    "suggested_query3": " datasam:Novella_del_Grasso_Legnaiuolo_anonimo_ManettoAmmattini",
    "suggested_query4": " datasam:Novella_del_Grasso_Legnaiuolo_anonimo_ManettoAmmattini",
    "suggested_query5": " datasam:Petrosinella_CuntodeliCunti_Basile_orca",
    "suggested_query6": " datasam:novellino_II_anonimo_lapidario",
    "suggested_query7": " datasam:novellino_II_anonimo_lapidario",
    "suggested_query8": " datasam:Novella_V_Giornata_II_Decameron_Boccaccio_andreuccioDiPietro",
    "suggested_query10": " datasam:Novella_V_Giornata_II_Decameron_Boccaccio_andreuccioDiPietro",
    "suggested_query11": " datasam:Novella_V_Giornata_II_Decameron_Boccaccio_andreuccioDiPietro",
    "suggested_query12": " datasam:Novella_V_Giornata_II_Decameron_Boccaccio_andreuccioDiPietro",
}

character_queries = {
    "query_1": """
    SELECT DISTINCT ?story (COUNT (*) AS ?character_number) WHERE{
            BIND(uri(% s) AS ?story)
		% s wdp:P527 ?cl .
		?cl rdf:type sam:CharacterList .
		?cl wdp:P527 ?cn .
		?cn rdf:type wdt:Q95074
}
    """
    % (
        character_suggested["suggested_query1"],
        character_suggested["suggested_query1"],
    ),
    "query_2": """
    SELECT ?character ?character_group ?character_group_trope WHERE {
            BIND(uri(% s) AS ?character)
            % s wdp:P361 ?character_group .
            ?character_group sam:hasTrope ?character_group_trope .
    }"""
    % (
        character_suggested["suggested_query2"],
        character_suggested["suggested_query2"],
    ),
    "query_3": """
    SELECT ?character ?name_class ?name WHERE {
            BIND(uri(% s) AS ?character)
            % s wdp:P2561 ?name_class .
            ?name_class sam:hasName ?name .
    }
"""
    % (
        character_suggested["suggested_query3"],
        character_suggested["suggested_query3"],
    ),
    "query_4": """
    SELECT ?character ?name ?named_by WHERE {
            BIND(uri(% s) AS ?character)
            % s wdp:P2561 ?name_class .
            ?name_class sam:hasName ?name .
            ?name_class wdp:P3938 ?named_by .
    }
"""
    % (
        character_suggested["suggested_query4"],
        character_suggested["suggested_query4"],
    ),
    "query_5": """
    SELECT ?character ?character_group WHERE {
            BIND(uri(% s) AS ?character)
            % s wdp:P361 ?character_group
    }"""
    % (
        character_suggested["suggested_query5"],
        character_suggested["suggested_query5"],
    ),
    "query_6": """
    SELECT ?character ?character_gender WHERE {
            BIND(uri(% s) AS ?character)
            % s wdp:P21 ?character_gender
    }
"""
    % (
        character_suggested["suggested_query6"],
        character_suggested["suggested_query6"],
    ),
    "query_7": """
    SELECT ?character ?occupation ?for ?title WHERE {
            BIND(uri(% s) AS ?character)
            % s wdp:P106 ?occupation .
            ?occupation sam:hasTitle ?title .
    OPTIONAL{?occupation wdp:P1416 ?for}
    }
"""
    % (
        character_suggested["suggested_query7"],
        character_suggested["suggested_query7"],
    ),
    "query_8": """
    SELECT ?character ?change ?change_type ?changed_value ?scene WHERE {
            BIND(uri(% s) AS ?character)
            ?scene sam:hasChange ?change .
            ?change wdp:P710 % s .
    OPTIONAL{?change ?change_type ?changed_value}
    }
"""
    % (
        character_suggested["suggested_query8"],
        character_suggested["suggested_query8"],
    ),
    "query_9": """
    SELECT ?character ?definition WHERE {
            wdt:Q95074 rdfs:label ?definition
    }
""",  # requires the complete ontology+dataset rdf
    "query_10": """
    SELECT ?character ?trope WHERE {
            BIND(uri(% s) AS ?character)
            % s sam:hasTrope ?trope
    }
"""
    % (
        character_suggested["suggested_query10"],
        character_suggested["suggested_query10"],
    ),
    "query_11": """
    SELECT ?character ?trope WHERE {
            BIND(uri(% s) AS ?character)
            % s sam:hasTrope ?trope .
            ?trope rdf:type sam:PeriodicTableTrope
    }
"""
    % (
        character_suggested["suggested_query11"],
        character_suggested["suggested_query11"],
    ),
    "query_12": """
    SELECT ?character ?narratorName ?descriptor WHERE {
            BIND(uri(% s) AS ?character)
            OPTIONAL{% s sam:narratorName ?narratorName .}
            OPTIONAL{% s sam:descriptor ?descriptor}
    }
"""
    % (
        character_suggested["suggested_query12"],
        character_suggested["suggested_query12"],
        character_suggested["suggested_query12"],
    ),
}

scene_suggested = {
    "query_1": "datasam:Belfagor_Arcidiavolo_Machiavelli_scene1",
    "query_2": "datasam:Belfagor_Arcidiavolo_Machiavelli_scene2",
    "query_3": "",  # not in dataset
    "query_5": "datasam:Novella_V_Giornata_II_Decameron_Boccaccio_Scene6",
    "query_6": "datasam:Novella_V_Giornata_II_Decameron_Boccaccio_Scene6",
    "query_7": "datasam:Novella_del_Grasso_Legnaiuolo_anonimo_Scene13",
    "query_8": "",  # not in dataset
    "query_9": "",  # not in dataset
}

scene_queries = {
    "query_1": """
        SELECT ?scene ?participants WHERE {
            BIND(uri(% s) AS ?scene)
            % s wdp:P710 ?participants
        }
    """
    % (scene_suggested["query_1"], scene_suggested["query_1"]),
    "query_2": """
        SELECT ?scene ?setting WHERE {
            BIND(uri(% s) AS ?scene) 
            OPTIONAL{% s sam:hasSetting ?setting}
        }
    """
    % (scene_suggested["query_2"], scene_suggested["query_2"]),
    "query_3": "",
    "query_4": """
        SELECT ?definition WHERE {
            sam:Scene rdfs:label ?definition .
        }
    """,  # requires the complete ontology+dataset rdf
    "query_5": """
        SELECT ?scene ?scene_excerpt ?scene_source WHERE {
            BIND(uri(% s) AS ?scene)
            % s sam:referenceMaterial ?scene_excerpt .
            OPTIONAL{?scene_excerpt sam:referenceMaterialSource ?scene_source} .
            OPTIONAL{?scene_excerpt sam:excerpt_text ?scene_text}
        } 
    """
    % (
        scene_suggested["query_5"],
        scene_suggested["query_5"],
    ),  # add ?scene_text to variables to obtain the full scene text
    "query_6": """
        SELECT ?scene ?change WHERE {
            BIND(uri(% s) AS ?scene) 
            OPTIONAL{% s sam:hasChange ?change}
        }
    """
    % (scene_suggested["query_6"], scene_suggested["query_6"]),
    "query_7": """
        SELECT ?scene ?trope WHERE {
            BIND(uri(% s) AS ?scene) 
            OPTIONAL{% s sam:hasTrope ?trope}
        }
    """
    % (scene_suggested["query_7"], scene_suggested["query_7"]),
    "query_8": "",
    "query_9": "",
}

trope_suggested = {
    "suggested_query1": "",
    "suggested_query2": "datasam:trope_KnightInShiningArmor",
}

trope_queries = {
    "query_1": """
    SELECT ?definition WHERE{
        sam:Trope rdfs:label ?definition .
    }
    """,
    "query_2": """
    SELECT ?trope ?trope_source WHERE{
        BIND(uri(% s) AS ?trope)
        % s sam:tropeURI ?trope_source
    }
"""% (trope_suggested['suggested_query2'], trope_suggested['suggested_query2']),
}
