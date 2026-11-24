from statistics import median

def signatures(rows):
    accum={}
    for row in rows:
        accum.setdefault(row["code"],[]).append(row)
    return {
        seat:{"section":samples[0]["section"],"lane":samples[0]["lane"],"clarity":median(r["clarity"] for r in samples),
              "echo":median(r["echo_ms"] for r in samples),"level":median(r["level_db"] for r in samples)}
        for seat,samples in accum.items() if {r["passage"] for r in samples}=={"spoken","sung"}
    }

def perceptual_distance(a,b):
    return max(abs(a["clarity"]-b["clarity"])/18,
               abs(a["echo"]-b["echo"])/200,
               abs(a["level"]-b["level"])/8)
