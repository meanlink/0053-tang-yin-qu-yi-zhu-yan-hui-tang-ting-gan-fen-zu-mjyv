from itertools import combinations
from seat_similarity import perceptual_distance

def proximity(members,features):
    block=[features[seat] for seat in members]
    lanes=sorted(r["lane"] for r in block)
    return (len({r["section"] for r in block})==1 and len(lanes)==lanes[-1]-lanes[0]+1)

def build(features,limit):
    clusters=sorted((code,) for code in features)
    evidence=[]
    diameters={}
    while True:
        moves=[]
        for a,b in combinations(clusters,2):
            pair=tuple(sorted(a+b))
            if not proximity(pair,features):
                continue
            diameter=max(perceptual_distance(features[s],features[t]) for s,t in combinations(pair,2))
            if diameter<=limit:
                moves.append((diameter,a,b,pair))
        if not moves:
            break
        value,a,b,pair=min(moves)
        evidence.append({"left":list(a),"right":list(b),"diameter":round(value,4)})
        diameters[pair]=value
        clusters=sorted([x for x in clusters if x not in (a,b)]+[pair])
    return [(cluster,round(diameters.get(cluster,0),4)) for cluster in clusters],evidence
