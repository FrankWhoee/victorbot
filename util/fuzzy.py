import math

import jellyfish

def search(query, possibilities):
    best_possibility = possibilities[0]
    best_distance = 0
    for p in possibilities:
        distance = jellyfish.jaro_winkler_similarity(query.lower(), p.lower())
        if distance > best_distance:
            best_possibility = p
            best_distance = distance
    return best_possibility