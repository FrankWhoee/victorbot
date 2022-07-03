import math

import jellyfish

def search(query: str, possibilities: list) -> str:
    best_possibility = possibilities[0]
    best_distance = 0
    for p in possibilities:
        distance = jellyfish.jaro_winkler_similarity(query.lower(), p.lower())
        if distance > best_distance:
            best_possibility = p
            best_distance = distance
    return best_possibility

def map_search(queries: list, possibilities: list) -> str:
    # get the best match for each query and store it in a dict
    best_matches = {}
    for query in queries:
        best_matches[query] = search(query, possibilities)
    return best_matches