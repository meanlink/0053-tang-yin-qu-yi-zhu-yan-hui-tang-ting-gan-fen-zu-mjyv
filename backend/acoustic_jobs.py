from statistics import median
from fastapi import HTTPException
from psycopg.types.json import Jsonb
from complete_link import build
from seat_similarity import signatures

def run_job(cx,kind,payload):
    if kind!="layout-acoustics":
        raise ValueError(kind)
    cx.execute("SELECT pg_advisory_xact_lock(53019)")
    hall=payload["hall"]
    rows=cx.execute('''
      SELECT s.code,s.section,s.lane,l.* FROM seats s JOIN listening_slips l ON s.code=l.seat
      WHERE s.hall=%s ORDER BY s.code
    ''',(hall,)).fetchall()
    data=signatures(rows)
    if len(data)<2:
        raise HTTPException(409,"同一会堂至少两座席完成说段和唱段试听")
    groups,trail=build(data,payload["threshold"])
    cx.execute("DELETE FROM hearing_groups WHERE hall=%s",(hall,))
    for group,diameter in groups:
        medians={key:median(data[seat][key] for seat in group) for key in ("echo","clarity","level")}
        panels=2 if medians["echo"]>=850 else int(medians["echo"]>=550)
        cx.execute("INSERT INTO hearing_groups VALUES(%s,%s,%s,%s,%s,%s,%s)",
                   ('/'.join(group),hall,list(group),diameter,panels,Jsonb(medians),Jsonb(trail)))
    return {"hall":hall,"eligible":len(data),"groups":[list(group) for group,_ in groups],"merges":trail}
