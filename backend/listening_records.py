from typing import Literal
from fastapi import HTTPException
from pydantic import BaseModel,Field
from hearing_runs import bump,revision

class Listen(BaseModel):
    seat:str
    passage:Literal["spoken","sung"]
    clarity:int=Field(ge=0,le=100)
    echo_ms:int=Field(ge=0,le=3000)
    level_db:int=Field(ge=0,le=120)
    media_ref:str=Field(min_length=5,max_length=80)

def upsert(cx,data):
    cx.execute("SELECT pg_advisory_xact_lock(53019)")
    seat=cx.execute("SELECT hall FROM seats WHERE code=%s",(data.seat,)).fetchone()
    if not seat:
        raise HTTPException(404,"座席不存在")
    hall=seat["hall"]
    # Late corrections are always accepted, including for a seat that a signed
    # residency uses: that blueprint keeps its frozen seats and panel count.
    changed=cx.execute('''
       INSERT INTO listening_slips VALUES(%(seat)s,%(passage)s,%(clarity)s,%(echo_ms)s,%(level_db)s,%(media_ref)s)
       ON CONFLICT(seat,passage) DO UPDATE SET clarity=excluded.clarity,echo_ms=excluded.echo_ms,
       level_db=excluded.level_db,media_ref=excluded.media_ref
       WHERE (listening_slips.clarity,listening_slips.echo_ms,listening_slips.level_db,listening_slips.media_ref)
             IS DISTINCT FROM (excluded.clarity,excluded.echo_ms,excluded.level_db,excluded.media_ref)
       RETURNING seat
    ''',data.model_dump()).fetchone()
    if not changed:
        return {"seat":data.seat,"passage":data.passage,"revision":revision(cx,hall),
                "message":"试听数值没有变化，无需重算"}
    # Older groups stay stored for reference, but a corrected revision means
    # nothing currently covers the hall, so sign-off stays blocked until the
    # whole hall is recalculated.
    return {"seat":data.seat,"passage":data.passage,"revision":bump(cx,hall),
            "message":"已补录试听，需重算该会堂整套分组后才能签核"}
