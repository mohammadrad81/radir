def smart_intersect(sets: list[set]) -> set:
    print("sets: ", sets)
    if len(sets) == 1:
        return sets[0]
    sets = sorted(sets, key=lambda x: len(x)) # sort sets for query optimization
    result = sets[0].intersection(sets[1])
    for i in range(2, len(sets)):
        result.intersection_update(sets[i])
    print("intersected sets: ", result)
    return result

