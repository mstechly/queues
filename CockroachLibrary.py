def getPermutation(L1, L2):

    if sorted(L1) != sorted(L2):
        raise ValueError("L2 must be permutation of L1 (%s, %s)" % (L1,L2))

    permutation = map(dict((v, i) for i, v in enumerate(L1)).get, L2)
    assert [L1[p] for p in permutation] == L2
    return permutation

def numberOfSwaps(permutation):
    # decompose the permutation into disjoint cycles
    nswaps = 0
    seen = set()
    for i in xrange(len(permutation)):
        if i not in seen:
           j = i # begin new cycle that starts with `i`
           while permutation[j] != i:
               j = permutation[j]
               seen.add(j)
               nswaps += 1

    return nswaps