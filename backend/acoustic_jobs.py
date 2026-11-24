from statistics import median
from fastapi import HTTPException
from psycopg.types.json import Jsonb
from complete_link import build
from hearing_runs import revision
from seat_similarity import signatures

def run_job(cx,kind,payload,job_id=None):
    if kind!="layout-acoustics":
        raise ValueError(kind)
    # Listening corrections and sign-off take the same lock, so the slips read
    # below are one consistent snapshot.
    cx.execute("SELECT pg_advisory_xact_lock(53019)")
    hall=payload["hall"]
    # The result is attributed to the revision the operator asked to recompute,
    # not to whatever revision happens to be live at finish time. If a late
    # correction arrived while this job queued or ran, the result therefore stays
    # short of the live revision: it is kept for reference, but it can neither
    # become the current grouping nor overwrite a newer job's grouping, and it
    # cannot unlock sign-off.
    expected=payload.get("revision",0)
    rows=cx.execute('''
      SELECT s.code,s.section,s.lane,l.* FROM seats s JOIN listening_slips l ON s.code=l.seat
      WHERE s.hall=%s ORDER BY s.code
    ''',(hall,)).fetchall()
    data=signatures(rows)
    if len(data)<2:
        raise HTTPException(409,"同一会堂至少两座席完成说段和唱段试听")
    groups,trail=build(data,payload["threshold"])
    run=cx.execute('''
      INSERT INTO hearing_runs(job_id,hall,revision,threshold)
      VALUES(%s,%s,%s,%s) RETURNING id
    ''',(job_id,hall,expected,payload["threshold"])).fetchone()["id"]
    for group,diameter in groups:
        medians={key:median(data[seat][key] for seat in group) for key in ("echo","clarity","level")}
        panels=2 if medians["echo"]>=850 else int(medians["echo"]>=550)
        cx.execute('''
          INSERT INTO hearing_groups(run_id,key,hall,members,max_distance,recommended_panels,medians,trail)
          VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        ''',(run,'/'.join(group),hall,list(group),diameter,panels,Jsonb(medians),Jsonb(trail)))
    current=expected==revision(cx,hall)
    return {"run":run,"hall":hall,"revision":expected,"current":current,"eligible":len(data),
            "groups":[list(group) for group,_ in groups],"merges":trail,
            **({} if current else {"message":"计算期间试听有补录，本次结果仅供查阅，请按最新试听重算"})}
